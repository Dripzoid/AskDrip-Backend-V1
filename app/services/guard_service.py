import numpy as np

from app.core.embedding_cache import (
    cache
)

from app.services.embedding_service import (
    generate_embedding
)


# ====================================
# DOMAIN THRESHOLD
# ====================================

FASHION_THRESHOLD = 0.50


# ====================================
# FASHION DOMAIN GUARD
# ====================================

def validate_fashion_prompt(
    prompt: str
) -> bool:

    try:

        query_embedding = (
            generate_embedding(
                prompt
            )
        )

        route_data = (
            cache.kb_vectors["/chat"]
        )

        scores = (
            route_data["matrix"]
            @ query_embedding
        )

        max_score = float(
            np.max(scores)
        )

        print(
            f"\nDOMAIN SCORE: "
            f"{max_score:.4f}"
        )

        print(
            f"PROMPT: {prompt}"
        )

        return (
            max_score
            >= FASHION_THRESHOLD
        )

    except Exception as e:

        print(
            "DOMAIN GUARD ERROR:",
            str(e)
        )

        return False