from time import time

from fastapi import APIRouter

from app.schemas.common import (
    PromptRequest
)

from app.services.outfit_service import (
    generate_outfit_response
)

from app.services.message_service import (
    save_message
)

from app.utils.response import (
    success_response,
    error_response
)

router = APIRouter(
    prefix="/outfit",
    tags=["Outfit"]
)


@router.post("")
async def outfit(
    data: PromptRequest
):
    # START RESPONSE TIMER

    start_time = time()

    try:

        # =========================
        # SAVE USER MESSAGE
        # =========================

        await save_message(
            user_id=data.userId,
            conversation_id=data.conversationId,
            role="user",
            content=data.prompt
        )

        # =========================
        # GENERATE OUTFIT RESPONSE
        # =========================

        result = (
            generate_outfit_response(
                data.prompt
            )
        )

        # =========================
        # SAVE ASSISTANT MESSAGE
        # =========================

        await save_message(
            user_id=data.userId,
            conversation_id=data.conversationId,
            role="assistant",
            content=result["response"]
        )

        # =========================
        # SUCCESS RESPONSE
        # =========================

        return success_response(
            message="Outfit generated successfully",
            route="/api/v1/outfit/",
            start_time=start_time,
            data={
                "conversationId":
                    data.conversationId,

                "prompt":
                    data.prompt,

                "response":
                    result["response"],

                "products":
                    result["products"]
            }
        )

    except Exception as e:

        print(
            "OUTFIT ERROR:",
            str(e)
        )

        return error_response(
            message=str(e),
            route="/api/v1/outfit/"
        )