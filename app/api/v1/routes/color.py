import traceback

from time import time

from fastapi import APIRouter

from app.schemas.common import (
    PromptRequest
)

from app.services.color_service import (
    generate_color_match_response
)

from app.services.message_service import (
    save_message
)

from app.utils.response import (
    success_response,
    error_response
)

router = APIRouter(
    prefix="/color-match",
    tags=["Color Match"]
)


@router.post("")
async def color_match(
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
        # GENERATE COLOR RESPONSE
        # =========================

        result = (
            generate_color_match_response(
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
            message="Color match generated successfully",
            route="/api/v1/color-match/",
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

        print("\n===== COLOR MATCH ERROR =====")
        print(repr(e))
        traceback.print_exc()

        return error_response(
            message=repr(e),
            route="/api/v1/color-match/"
        )