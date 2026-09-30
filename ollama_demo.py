from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(model="mistral:latest")


message = model.invoke("What is the capital of France?")

print(message.content)

print("\n" + "-" *50)


chain = (ChatPromptTemplate.from_messages(
    [   
        ("system", "tell me strictly only jokes, but not about any others"),
        ("human", "tell me a serious thing about {topic}"),
    ]
) | model | StrOutputParser())


for chunk in chain.stream({"topic": "chickens"}):
    print(chunk, end="", flush=True)