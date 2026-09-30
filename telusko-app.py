import os
from dotenv import load_dotenv

import requests

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json"
}

payload = [
    {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "what is AI in short"
            }
        ]
    }
]

response = requests.post(url, headers=headers, json=payload)

print("---- Response from OpenAI API ---")
print(response.json())
print("---- ---")
print(response.status_code)
print(response.json().get("choices", [{}])[0].get("message", {}).get("content", "No content found"))