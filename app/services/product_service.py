from app.services.embedding_service import (
    generate_embedding
)

from app.services.semantic_search_service import (
    search_products
)


def retrieve_products(
    query: str,
    limit: int = 10
):

    query_embedding = (
        generate_embedding(
            query
        )
    )

    return search_products(
        query_embedding=query_embedding,
        top_k=limit,
        min_score=0.35
    )
    
def build_product_context(
    products
):

    if not products:
        return ""

    lines = []

    seen = set()

    for product in products:

        name = product.get(
            "name",
            ""
        )

        if name in seen:
            continue

        seen.add(name)

        lines.append(
            f"""
Name: {name}
Price: ₹{product.get('actualPrice') or product.get('price')}
Category: {product.get('category', {}).get('category', '')}
Subcategory: {product.get('subcategory')}
Colors: {", ".join(product.get('colors', [])) if isinstance(product.get('colors'), list) else product.get('colors', '')}
Semantic Score: {product.get('semanticScore', 0):.4f}
"""
        )

    return "\n".join(lines)