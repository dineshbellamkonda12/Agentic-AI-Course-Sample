import sys

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

print(model.invoke("what is the time right now in london?").content)
