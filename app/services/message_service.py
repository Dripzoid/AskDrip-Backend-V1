from app.services.dripzoid_service import (
    DripzoidService
)


async def save_message(
    *,
    user_id: str,
    conversation_id: str,
    role: str,
    content: str,
    model: str | None = None,
    token_count: int | None = None
):
    return await (
        DripzoidService
        .save_message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model,
            token_count=token_count
        )
    )