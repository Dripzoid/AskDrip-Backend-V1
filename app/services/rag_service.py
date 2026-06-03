from app.services.embedding_service import (
    generate_embedding
)

from app.services.semantic_search_service import (
    search_kb
)


def retrieve_context(
    query: str,
    route: str,
    top_k: int = 3
):

    try:

        query_embedding = (
            generate_embedding(
                query
            )
        )

        results = search_kb(
            route=route,
            query_embedding=query_embedding,
            top_k=top_k
        )

        return "\n".join(
    item["text"]
    for item in results
)

    except Exception as e:

        print(
            "SEMANTIC RAG ERROR:",
            str(e)
        )

        return ""