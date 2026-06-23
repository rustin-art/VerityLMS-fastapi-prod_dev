from dotenv import load_dotenv
import requests
import os


load_dotenv()
print("<!---- API Key loaded for client----!>")


API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}",
    "Content-Type": "application/json"
}


def generate_response(
    prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.7
):

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]