from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="You are a python trainer and answer only python related questions."),

    HumanMessage(content="tell me about python programming language"),
]

response = llm.invoke(messages)

print(response.content)

print(response.usage_metadata)

print(response.usage_metadata.get("model_name"))

messages.append(HumanMessage(content="what are next steps to learn python programming language"))

print("---- Next Step ---")
print(llm.invoke(messages).content)

print(llm.invoke(messages).usage_metadata)

messages.append(HumanMessage(content="tell me about what are next steps to learn java, no python here"))

print("---- Next Step java ---")

print(llm.invoke(messages).content)

print(llm.invoke(messages).usage_metadata)