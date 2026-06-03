import requests
import numpy as np

from app.core.embedding_cache import cache

BASE_URL = "https://api.dripzoid.com/api/vectors"


def load_product_vectors():

    response = requests.get(
        f"{BASE_URL}/products",
        timeout=120
    )

    response.raise_for_status()

    payload = response.json()

    products = payload.get(
        "vectors",
        []
    )

    product_ids = []
    embeddings = []
    product_map = {}

    for item in products:

        product_id = (
            item["product_id"]
        )

        product_ids.append(
            product_id
        )

        embeddings.append(
            item["embedding"]
        )

        product_map[
            product_id
        ] = item["product"]

    cache.product_ids = (
        product_ids
    )

    cache.product_matrix = np.array(
        embeddings,
        dtype=np.float32
    )

    cache.products = (
        product_map
    )

    print(
        f"Loaded {len(products)} products"
    )

    print(
        f"Cached {len(cache.products)} products"
    )