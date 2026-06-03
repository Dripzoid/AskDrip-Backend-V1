import os
import httpx

DRIPZOID_API_URL = os.getenv(
    "DRIPZOID_API_URL"
)

DRIPZOID_INTERNAL_KEY = os.getenv(
    "DRIPZOID_INTERNAL_KEY"
)


class DripzoidService:

    @staticmethod
    def _headers(
        user_id: str
    ):
        return {
            "X-Internal-Key":
                DRIPZOID_INTERNAL_KEY,
            "X-User-Id":
                user_id
        }

    @staticmethod
    async def create_conversation(
        user_id: str,
        title: str = "New Chat"
    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{DRIPZOID_API_URL}/api/v1/askdrip/conversations",
                json={
                    "title": title
                },
                headers=(
                    DripzoidService
                    ._headers(
                        user_id
                    )
                )
            )

            response.raise_for_status()

            return response.json()

    @staticmethod
    async def save_message(
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
        model: str | None = None,
        token_count: int | None = None
    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{DRIPZOID_API_URL}/api/v1/askdrip/messages",
                json={
                    "conversationId":
                        conversation_id,
                    "role":
                        role,
                    "content":
                        content,
                    "model":
                        model,
                    "tokenCount":
                        token_count
                },
                headers=(
                    DripzoidService
                    ._headers(
                        user_id
                    )
                )
            )

            response.raise_for_status()

            return response.json()

    @staticmethod
    async def get_messages(
        user_id: str,
        conversation_id: str
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{DRIPZOID_API_URL}/api/v1/askdrip/conversations/{conversation_id}/messages",
                headers=(
                    DripzoidService
                    ._headers(
                        user_id
                    )
                )
            )

            response.raise_for_status()

            return response.json()