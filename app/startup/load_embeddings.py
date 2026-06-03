from app.services.kb_embedding_service import (
    load_kb_vectors
)

from app.services.product_embedding_service import (
    load_product_vectors
)


def initialize_embeddings():

    print("Loading embeddings...")

    load_kb_vectors()

    load_product_vectors()

    print("Embeddings loaded successfully")