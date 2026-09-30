

import base64

import requests
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral:latest")

image_url = "https://github.com/user-attachments/assets/2059d1a7-914c-402c-8c2c-290fdc2997b2"
image_response = requests.get(image_url, timeout=30)
image_response.raise_for_status()
encoded_image = base64.b64encode(image_response.content).decode("utf-8")

url_image = llm.invoke([
    HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Describe the image in detail"
            },
            {
                "type": "image_url",
                "image_url": {"url": encoded_image}
            }
        ]
    )
])

print(url_image.content)

print(url_image.usage_metadata)

