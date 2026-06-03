import re
from re import sub
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from app.services.ai_service import (
    generate_ai_response
)

from app.services.product_service import (
    retrieve_products
)

MIN_SCORE = 0.35
DEFAULT_LIMIT = 2

PRODUCT_KEYWORDS = [
    "oversized tshirt",
    "tshirt",
    "shirt",
    "hoodie",
    "sweatshirt",
    "jacket",
    "jeans",
    "cargo",
    "trouser",
    "kurti",
    "kurta",
    "saree",
    "dress",
    "top",
    "palazzo",
    "blouse",
]

KEYWORD_MAP = {

    # Tshirts
    "tshirt": "oversized tshirt",
    "t-shirt": "oversized tshirt",
    "tshirts": "oversized tshirt",
    "t-shirts": "oversized tshirt",
    "tee": "oversized tshirt",
    "tees": "oversized tshirt",
    "graphic tee": "oversized tshirt",
    "graphic tshirt": "oversized tshirt",
    "oversized tee": "oversized tshirt",
    "oversized t-shirt": "oversized tshirt",

    # Shirts
    "shirt": "shirt",
    "shirts": "shirt",
    "casual shirt": "shirt",
    "formal shirt": "shirt",
    "linen shirt": "shirt",
    "cotton shirt": "shirt",
    "flannel shirt": "shirt",

    # Hoodies
    "hoodie": "hoodie",
    "hoodies": "hoodie",
    "zip hoodie": "hoodie",
    "pullover": "hoodie",

    # Sweatshirts
    "sweatshirt": "sweatshirt",
    "sweatshirts": "sweatshirt",
    "sweat tshirt": "sweatshirt",

    # Jackets
    "jacket": "jacket",
    "jackets": "jacket",
    "bomber jacket": "jacket",
    "denim jacket": "jacket",
    "windcheater": "jacket",
    "blazer": "jacket",
    "coat": "jacket",
    "overcoat": "jacket",

    # Jeans
    "jeans": "jeans",
    "baggy jeans": "jeans",
    "skinny jeans": "jeans",
    "wide leg jeans": "jeans",
    "slim fit jeans": "jeans",
    "denim": "jeans",

    # Cargo
    "cargo": "cargo",
    "cargos": "cargo",
    "cargo pant": "cargo",
    "cargo pants": "cargo",
    "baggy cargo": "cargo",

    # Trousers
    "trouser": "trouser",
    "trousers": "trouser",
    "pant": "trouser",
    "pants": "trouser",
    "chinos": "trouser",
    "joggers": "trouser",
    "track pant": "trouser",
    "track pants": "trouser",

    # Shorts
    "short": "shorts",
    "shorts": "shorts",
    "cargo shorts": "shorts",
    "denim shorts": "shorts",

    # Kurti
    "kurti": "kurti",
    "kurthi": "kurti",
    "kurtis": "kurti",
    "kurthi set": "kurti",

    # Kurta
    "kurta": "kurta",
    "kurtas": "kurta",
    "kurta set": "kurta",
    "kurta pajama": "kurta",
    "kurta pyjama": "kurta",

    # Saree
    "saree": "saree",
    "sarees": "saree",
    "silk saree": "saree",
    "cotton saree": "saree",
    "designer saree": "saree",
    "banarasi saree": "saree",
    "kanjivaram saree": "saree",

    # Dresses
    "dress": "dress",
    "dresses": "dress",
    "maxi dress": "dress",
    "midi dress": "dress",
    "mini dress": "dress",
    "party dress": "dress",
    "long frock": "dress",
    "long frocks": "dress",
    "frock": "dress",

    # Gowns
    "gown": "gown",
    "evening gown": "gown",

    # Tops
    "top": "top",
    "tops": "top",
    "crop top": "top",
    "tank top": "top",

    # Bottoms
    "leggings": "leggings",
    "palazzo": "palazzo",
    "palazzos": "palazzo",

    # Others
    "co-ord set": "co-ord set",
    "coord set": "co-ord set",
    "blouse": "blouse",
    "tunic": "tunic",

    # Activewear
    "activewear": "activewear",
    "gym wear": "activewear",
    "sportswear": "sportswear",
    "training wear": "sportswear",
    "running shorts": "sportswear",
    "yoga pants": "sportswear",

    # Footwear
    "sneaker": "sneakers",
    "sneakers": "sneakers",
    "shoe": "shoes",
    "shoes": "shoes"
}

PRODUCT_KEYWORDS = sorted(
    KEYWORD_MAP.keys(),
    key=len,
    reverse=True
)

def filter_products(
    products
):
    """
    Remove weak semantic matches.
    """

    return [
        product
        for product in products
        if product.get(
            "semanticScore",
            0
        ) >= MIN_SCORE
    ]




def extract_product_keywords(text: str):
    text = text.lower()

    found = []
    occupied = []

    for keyword in PRODUCT_KEYWORDS:

        match = re.search(
            rf"\b{re.escape(keyword)}\b",
            text
        )

        if not match:
            continue

        start, end = match.span()

        overlap = any(
            start >= s and end <= e
            for s, e in occupied
        )

        if overlap:
            continue

        occupied.append(
            (start, end)
        )

        found.append(
            KEYWORD_MAP[keyword]
        )

    return list(
        dict.fromkeys(found)
    )

def search_products_from_keywords(
    keywords,
    limit: int = 10
):
    """
    Concurrent semantic search.

    - Deduplicates keywords
    - Searches in parallel
    - Keeps highest score per product
    """

    if not keywords:
        return []

    products_map = {}

    with ThreadPoolExecutor(
        max_workers=min(
            len(keywords),
            8
        )
    ) as executor:

        future_map = {
            executor.submit(
                retrieve_products,
                query=keyword,
                limit=limit
            ): keyword
            for keyword in keywords
        }

        for future in as_completed(
            future_map
        ):

            keyword = future_map[future]

            try:

                print(
                    f"\nSEARCHED: {keyword}"
                )

                products = filter_products(
                    future.result()
                )

                products = sorted(
                    products,
                    key=lambda p: p.get(
                        "semanticScore",
                        0
                    ),
                    reverse=True
                )[:DEFAULT_LIMIT]

                for product in products:

                    product_key = (
                        get_product_key(
                            product
                        )
                    )

                    if not product_key:
                        continue

                    existing = (
                        products_map.get(
                            product_key
                        )
                    )

                    if (
                        existing is None
                        or product.get(
                            "semanticScore",
                            0
                        ) > existing.get(
                            "semanticScore",
                            0
                        )
                    ):
                        products_map[
                            product_key
                        ] = product

            except Exception as e:

                print(
                    f"SEARCH ERROR [{keyword}]:",
                    e
                )

    final_products = sorted(
        products_map.values(),
        key=lambda p: p.get(
            "semanticScore",
            0
        ),
        reverse=True
    )

    print("\nGLOBAL RANKING")

    for p in final_products:
        print(
            p["name"],
            p["semanticScore"]
        )

    return final_products

def get_product_key(
    product
):
    """
    Deduplicate product variants.

    Example:

    trendy-baggy-cargo-jeans-61
    trendy-baggy-cargo-jeans-59
    trendy-baggy-cargo-jeans-60

    becomes:

    trendy-baggy-cargo-jeans
    """

    slug = product.get(
        "slug",
        ""
    )

    if slug:

        return sub(
            r"-\d+$",
            "",
            slug
        )

    return product.get(
        "id"
    )


def generate_assistant_response(
    user_prompt: str,
    enhanced_prompt: str | None = None,
    limit: int = 15
):
    """
    Main AskDrip orchestration layer.

    Flow:

    user prompt
        ↓
    AI response
        ↓
    semantic search(user)
        ↓
    semantic search(user + ai)
        ↓
    filter
        ↓
    deduplicate
        ↓
    merge
    """

    # =========================
    # PROMPT FOR AI
    # =========================

    prompt_for_ai = (
        enhanced_prompt
        if enhanced_prompt
        else user_prompt
    )

    # =========================
    # AI RESPONSE
    # =========================

    ai_response = (
        generate_ai_response(
            prompt_for_ai
        )
    )
    ai_response = ai_response.lstrip(": ").strip()

    # =========================
    # KEYWORDS
    # =========================

    user_keywords = (
        extract_product_keywords(
            user_prompt
        )
    )

    ai_keywords = (
        extract_product_keywords(
            ai_response
        )
    )

    all_keywords = list(
        dict.fromkeys(
            user_keywords +
            ai_keywords
        )
    )

    print(
        "\nUSER KEYWORDS:",
        user_keywords
    )

    print(
        "\nAI KEYWORDS:",
        ai_keywords
    )

    print(
        "\nALL KEYWORDS:",
        all_keywords
    )

    # =========================
    # PRODUCT SEARCH
    # =========================

    products = (
        search_products_from_keywords(
            all_keywords,
            limit=10
        )
    )

    products = products[:8]

    # =========================
    # DEBUG
    # =========================

    print("\nUSER PROMPT:")
    print(user_prompt)

    print("\nAI RESPONSE:")
    print(ai_response)



    print("\nFINAL PRODUCTS:")
    for p in products:
        print(
            p["name"],
            p.get("semanticScore")
        )

    # =========================
    # RESPONSE
    # =========================

    return {
        "response":
            ai_response,

        "products":
            products
    }