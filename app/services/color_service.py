from app.services.rag_service import (
    retrieve_context
)
from app.services.assistant_service import (
    generate_assistant_response
)

from app.services.guard_service import (
    validate_fashion_prompt
)

from app.services.greeting_service import (
    is_greeting,
    get_greeting_response
)


def generate_color_match_response(
    prompt: str
):

    # ====================================
    # GREETING HANDLER
    # ====================================

    if is_greeting(prompt):
        return {
            "response":
                get_greeting_response(),
            "products": []
        }

    # ====================================
    # DOMAIN GUARD
    # ====================================

    if not validate_fashion_prompt(
        prompt
    ):
        return {
            "response":
                (
                    "I focus mainly on fashion, "
                    "streetwear, styling, and "
                    "Dripzoid products."
                ),
            "products": []
        }

    # ====================================
    # RETRIEVE RELEVANT COLOR RULES
    # ====================================

    retrieved_context = (
        retrieve_context(
            query=prompt,
            route="/color"
        )
    )

    # ====================================
    # COLOR MATCH PROMPT
    # ====================================

    enhanced_prompt = f"""
Color Knowledge:
{retrieved_context}

Question:
{prompt}

List the colors that pair well with the requested color.

Example:
Black -> White, Grey, Beige

Answer:
""".strip()

    # ====================================
    # ASSISTANT ORCHESTRATION
    # ====================================

    return generate_assistant_response(
        user_prompt=prompt,
        enhanced_prompt=enhanced_prompt
    )