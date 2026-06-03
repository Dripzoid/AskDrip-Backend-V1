import requests

BASE_URL = (
    "https://api.dripzoid.com/api"
)


def generate_embedding(
    text: str
):

    response = requests.post(
        f"{BASE_URL}/embed",
        json={
            "text": text
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()[
        "embedding"
    ]
