from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import base64
load_dotenv()

client = OpenAI()

HERE = Path(__file__).parent

def save(result, filename):
    path = HERE / filename
    path.write_bytes(base64.b64decode(result.data[0].b64_json))


writer = ChatPromptTemplate.from_messages([
    ("system", "you write a short visual image prompt in short"),
    ("human", "generate an image of a {subject} with a {style} style"),
]) | ChatOpenAI(model="gpt-4o-mini", temperature=0.3) | StrOutputParser()


image_prompt = writer.invoke({"subject": "a cat wearing a spacesuit on the moon", "style": "cyberpunk"})

print("Our image prompt is: ", image_prompt)

save(
    client.images.generate(
        model="gpt-image-1-mini",
        prompt=image_prompt,
        size="1024x1024",
        quality="low",
    ),
    "scifi-cat.png",
)

