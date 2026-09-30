from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7
)

StroutputParser = StrOutputParser()

json_output_parser = JsonOutputParser()

reponse = llm.invoke("capital of France")


text_output = StroutputParser.invoke(reponse)

print(text_output)

chatprompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You have {years} years of experience in {field}.
        Return a JSON object with exactly these keys:
        - \"title\": a short title
        - \"topics\": a list of advanced topics
        - \"conclusion\": a short conclusion

        {format_instructions}
        """
    ),
    ("human", "I want to learn about {topic}")
])

result = chatprompt.invoke(
    {
        "years": 5,
        "field": "software engineering",
        "topic": "machine learning",
        "format_instructions": json_output_parser.get_format_instructions()
    })

json_output = (llm | json_output_parser).invoke(result)




print(type(json_output))

print(json_output)




