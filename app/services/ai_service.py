import requests
import traceback

from app.services.guard_service import (
    validate_fashion_prompt
)

from app.services.greeting_service import (
    is_greeting,
    get_greeting_response
)


LLAMA_SERVER_URL = (
    "http://140.245.255.87:8080/completion"
)


def generate_ai_response(
    prompt: str
) -> str:

    original_prompt = (
        prompt.strip()
    )

    print(
        f"INPUT PROMPT => [{original_prompt}]"
    )

    # =========================
    # GREETING HANDLER
    # =========================

    if is_greeting(
        original_prompt
    ):

        print(
            "GREETING DETECTED"
        )

        return (
            get_greeting_response()
        )

    # =========================
    # DOMAIN GUARD
    # =========================

    if not validate_fashion_prompt(
        original_prompt
    ):

        print(
            "DOMAIN GUARD TRIGGERED"
        )

        return (
            "I specialize in fashion, "
            "streetwear, styling, outfits, "
            "and Dripzoid products. "
            "Try asking me for outfit "
            "recommendations or fashion advice."
        )

    # =========================
    # CHAT TEMPLATE
    # =========================

    final_prompt = f"""
<|im_start|>user
{original_prompt}
<|im_end|>

<|im_start|>assistant
""".strip()

    print(
        "\nFINAL PROMPT:\n"
    )

    print(
        final_prompt
    )

    payload = {
    "prompt": final_prompt,
    "n_predict": 64,
    "temperature": 0.1,
    "top_p": 0.9,
    "repeat_penalty": 1.15,
    "stop": ["<|im_end|>"]
    }

    try:

        response = requests.post(
            LLAMA_SERVER_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        print(
            "RAW RESPONSE:",
            response.text
        )

        data = (
            response.json()
        )

        generated_text = (
            data.get(
                "content",
                ""
            )
            .replace(
                "<|im_start|>",
                ""
            )
            .replace(
                "<|im_end|>",
                ""
            )
            .replace(
                "assistant",
                ""
            )
            .strip()
        )

        # =========================
        # CLEANUP
        # =========================

        generated_text = (
            generated_text
            .replace(
                "Question:",
                ""
            )
            .replace(
                "Answer:",
                ""
            )
            .replace(
                "Response:",
                ""
            )
            .strip()
        )

        # =========================
        # FALLBACK
        # =========================

        if not generated_text:

            print(
                "EMPTY RESPONSE"
            )

            return (
                "Sorry, I couldn't generate "
                "a fashion recommendation."
            )

        return (
            generated_text
        )

    except Exception as e:



        print("LLAMA ERROR")
        traceback.print_exc()

        return (
            "Sorry, AskDrip AI is currently "
            "unavailable. Please try again."
        )
