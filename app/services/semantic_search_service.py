import numpy as np

from app.core.embedding_cache import (
    cache
)


def search_kb(
    route: str,
    query_embedding,
    top_k: int = 5
):
    route_data = cache.kb_vectors[route]

    scores = (
        route_data["matrix"]
        @ query_embedding
    )

    indices = (
        np.argsort(scores)[::-1][:top_k]
    )

    return [
        {
            "score": float(scores[i]),
            "text": route_data["texts"][i]
        }
        for i in indices
    ]



def search_products(
    query_embedding,
    top_k: int = 10,
    min_score: float = 0.35
):

    scores = (
        cache.product_matrix
        @ query_embedding
    )

    indices = np.argsort(
        scores
    )[::-1]

    results = []

    for i in indices:

        score = float(scores[i])

        if score < min_score:
            break

        product_id = (
            cache.product_ids[i]
        )

        product = (
            cache.products[
                product_id
            ]
        )

        product = {
            **product,
            "semanticScore": score,
            "semanticDistance":
                1.0 - score
        }

        results.append(
            product
        )

        if len(results) >= top_k:
            break

    return results
    