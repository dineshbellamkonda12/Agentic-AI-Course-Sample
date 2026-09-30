from openai import OpenAI

from dotenv import load_dotenv

client = OpenAI()

load_dotenv()

response = client.responses.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "what is AI in short"
        }
    ]
)

print(response.output_text)