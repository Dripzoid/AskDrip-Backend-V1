from app.services.guard_service import (
    validate_fashion_prompt
)

from app.services.greeting_service import (
    is_greeting,
    get_greeting_response
)

from app.services.assistant_service import (
    generate_assistant_response
)

from app.services.rag_service import (
    retrieve_context
)

def generate_recommendation_response(
    prompt: str
):

    # ====================================
    # GREETING HANDLER
    # ====================================

    if is_greeting(
        prompt
    ):
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
    # RETRIEVE RELEVANT FASHION KNOWLEDGE
    # ====================================

    retrieved_context = (
        retrieve_context(
            query=prompt,
            route="/recommendation"
        )
    )
    print(retrieved_context)

    # ====================================
    # RECOMMENDATION PROMPT
    # ====================================

    enhanced_prompt = f"""
Fashion Knowledge:
{retrieved_context}

User Question:
{prompt}

Answer using only the fashion knowledge.

Answer:
""".strip()

    # ====================================
    # ASSISTANT ORCHESTRATION
    # ====================================

    return generate_assistant_response(
        user_prompt=prompt,
        enhanced_prompt=enhanced_prompt
    )