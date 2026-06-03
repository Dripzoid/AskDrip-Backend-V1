from app.services.embedding_service import (
    generate_embedding
)

embedding = generate_embedding(
    "black oversized streetwear outfit"
)

print(
    len(embedding)
)