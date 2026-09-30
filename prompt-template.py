from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "you have {years} of experience in {field}"),
    ("human", "I want to learn about {topic}")
]
)

result = prompt.invoke(
    {
        "years": 5,
        "field": "software engineering",
        "topic": "machine learning"
    })

print(model.invoke(result))


