from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="Just tell me only telugu movies"),    

    HumanMessage(content="tell me latest telugu movies"),
]

print(llm.invoke(messages).content)

print(llm.invoke(messages).usage_metadata)

print("---- Next Step ---")


messages.append(HumanMessage(content="tell me latest hindi movies with release date,no telugu movies"))

print(llm.invoke(messages).content)

print(llm.invoke(messages).usage_metadata)
