from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


load_dotenv()

model = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.3
)

for chunk in model.stream("Write a short story about a robot learning to love."):
    print(chunk.content, end="", flush=True)
    
print("\n" + "-" *50)    


chain = (ChatPromptTemplate.from_messages(
    [
        ("human", "tell me a joke about {topic}"),
    ]
) | model | StrOutputParser())


for chunk in chain.stream({"topic": "chickens"}):
    print(chunk, end="", flush=True)




