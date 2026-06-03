from time import time

from fastapi import APIRouter

from app.utils.response import (
    success_response,
    error_response
)

from app.core.embedding_cache import cache

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)



@router.get("")
def health_check():

    start_time = time()

    try:

        return success_response(
            message="Health check successful",
            route="/api/v1/health/",
            start_time=start_time,
            data={
                "status": "healthy",
                "service": "AskDrip",
                "version": "1.0.0",

                # Product cache
                "product_vectors": {
                    "loaded": len(cache.products) > 0,
                    "count": len(cache.products)
                },

                # Knowledge base cache
                "knowledge_bases": {
                    "loaded": len(cache.kb_vectors) > 0,
                    "routes": list(cache.kb_vectors.keys()),
                    "count": len(cache.kb_vectors)
                }
            }
        )

    except Exception as e:

        return error_response(
            message=str(e),
            route="/api/v1/health/"
        )