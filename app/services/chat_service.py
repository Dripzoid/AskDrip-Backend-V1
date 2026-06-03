from app.services.rag_service import (
    retrieve_context
)

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


def generate_chat_response(
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
                    "streetwear, styling, outfits, "
                    "and Dripzoid products."
                ),

            "products": []
        }

    # ====================================
    # RETRIEVE RELEVANT FASHION CONTEXT
    # ====================================

    retrieved_context = (
        retrieve_context(
            query=prompt,
            route="/chat"
        )
    )

    # ====================================
    # CHAT PROMPT
    # ====================================

    enhanced_prompt = f"""
You are AskDrip, a fashion assistant.

Relevant Fashion Knowledge:
{retrieved_context}

User Question:
{prompt}

Answer the user's question using the relevant fashion knowledge above.

Guidelines:

- Focus on fashion, styling, outfits, colors, trends, and clothing advice.
- Use the fashion knowledge when relevant.
- Keep responses concise and conversational.
- Do not invent fashion facts that are not supported by the knowledge.
- Answer in 2-4 sentences.

Answer:
""".strip()

    # ====================================
    # ASSISTANT ORCHESTRATION
    # ====================================

    return generate_assistant_response(
        user_prompt=prompt,
        enhanced_prompt=enhanced_prompt
    )