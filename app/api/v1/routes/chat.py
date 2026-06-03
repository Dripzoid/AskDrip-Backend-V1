from time import time

from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest
)

from app.services.chat_service import (
    generate_chat_response
)

from app.services.message_service import (
    save_message
)

from app.utils.response import (
    success_response,
    error_response
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)




@router.post("")
async def chat(
    data: ChatRequest
):
    # =========================
    # START RESPONSE TIMER
    # =========================

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
        # GENERATE CHAT RESPONSE
        # =========================

        result = (
            generate_chat_response(
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
            message=
                "Response generated successfully",

            route=
                "/api/v1/chat/",

            start_time=
                start_time,

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
            "CHAT ERROR:",
            str(e)
        )

        return error_response(
            message=str(e),
            route="/api/v1/chat/"
        )