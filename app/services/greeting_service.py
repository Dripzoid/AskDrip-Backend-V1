import random


GREETINGS = {
    "hi",
    "hello",
    "hey",
    "hi askdrip",
    "hello askdrip",
    "hey askdrip",
    "good morning",
    "good afternoon",
    "good evening",
    "yo",
    "sup",
    "what's up",
    "whats up",
    "hola",
    "greetings",
    "askdrip",
    "hi there",
    "hello there",
    "hey there",
    "hii",
    "helloo"
}


GREETING_RESPONSES = [
    "👋 Hey! I'm AskDrip. Need an outfit recommendation or styling tip today?",
    "🔥 Welcome to AskDrip! Tell me your style, occasion, or vibe and I'll help you build the perfect fit.",
    "😎 Hey there! Ask me about streetwear, outfits, fashion trends, or Dripzoid products.",
    "👕 Hi! Looking for outfit inspiration? AskDrip has you covered.",
    "🚀 Welcome back! Let's build your next drip-worthy outfit.",
    "✨ Hey! From casual college looks to streetwear fits, I'm here to help.",
    "🧢 What's up! Tell me what you're wearing or where you're going, and I'll suggest an outfit.",
    "👟 Hello! Need help matching colors, sneakers, cargos, or oversized tees?",
    "🔥 Yo! Ready to upgrade your style? Ask away.",
    "😎 Hey fashion enthusiast! What kind of look are you going for today?",
    "👋 Hi there! I can recommend outfits based on your style, budget, or occasion.",
    "🎯 Welcome! Let's create a clean, trendy, and confident look together.",
    "💯 Hey! Ask me anything about fashion, streetwear, or Dripzoid collections.",
    "🖤 Hello! Looking for minimalist, oversized, or urban streetwear inspiration?",
    "⚡ Hey! Whether it's a party, college, or casual outing, I'll help you dress better.",
    "👕 Hi! Share your preferred colors or style and I'll suggest a complete outfit.",
    "🌟 Welcome to AskDrip! Your personal fashion assistant is ready.",
    "🔥 Hey! Let's find the perfect combination of clothing and accessories for your vibe.",
    "😄 Hello! Need fashion advice, outfit ideas, or styling suggestions?",
    "🚀 Hey! Tell me the occasion and I'll recommend a stylish look in seconds."
]


def is_greeting(prompt: str) -> bool:

    prompt = prompt.strip().lower()

    if prompt in GREETINGS:
        return True

    if len(prompt.split()) <= 3:
        for greeting in GREETINGS:
            if greeting in prompt:
                return True

    return False


def get_greeting_response() -> str:

    return random.choice(
        GREETING_RESPONSES
    )