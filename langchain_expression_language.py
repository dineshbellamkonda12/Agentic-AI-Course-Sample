from dotenv import load_dotenv

from langchain_openai import ChatOpenAI 

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "you have {years} of experience in {field}"),
    ("human", "tell me about {topic} in very concise manner")
])

model = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7
)   


parser = StrOutputParser()

chain = prompt | model | parser

chain_result = chain.invoke(
    {
        "years": 5,
        "field": "software engineering",
        "topic": "machine learning"
    })

print(chain_result)

print("-------------------")

translate = (ChatPromptTemplate.from_messages([
    ("system", "You are a translator that translates English to Hindi"),
    ("human", "{text}")
]) | model | parser)

full = chain | translate

full_result = full.invoke(
    {
        "years": 5,
        "field": "software engineering",
        "topic": "machine learning",
        "text": "I want to learn about machine learning"
    })

print(full_result)