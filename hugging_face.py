import os

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

endpoint = HuggingFaceEndpoint(
	repo_id="meta-llama/Llama-3.1-8B-Instruct",
	task="text-generation",
	max_new_tokens=200,
	temperature=0.3,
)


model = ChatHuggingFace(llm=endpoint)

model_response = model.invoke("What is the capital of France?")

print(model_response.content)


