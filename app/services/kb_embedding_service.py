import requests
import numpy as np

from app.core.embedding_cache import cache

BASE_URL = "https://api.dripzoid.com/api/vectors"


def load_kb_vectors():

    response = requests.get(
        f"{BASE_URL}/kb",
        timeout=120
    )

    response.raise_for_status()

    payload = response.json()

    vectors = payload.get("vectors", [])

    grouped = {
        "/chat": [],
        "/recommendation": [],
        "/color": [],
        "/outfit": []
    }

    for item in vectors:
        grouped[item["route"]].append(item)

    kb_cache = {}

    for route, records in grouped.items():

        texts = [
            record["fact_text"]
            for record in records
        ]

        embeddings = [
            record["embedding"]
            for record in records
        ]

        kb_cache[route] = {
        "records": records,
        "texts": texts,
        "matrix": np.array(
        embeddings,
        dtype=np.float32
    )
}

    cache.kb_vectors = kb_cache

    print(
        f"Loaded {len(vectors)} KB vectors"
    )