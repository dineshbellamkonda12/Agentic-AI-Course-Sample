from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def word_count(text: str) -> int:
    """Count the number of words in a text"""
    return len(text.split())


model_with_tools = model.bind_tools([multiply, word_count])

result = model_with_tools.invoke(
    "What is 2 * 3? How many words are in the following sentence: 'The quick brown fox jumps over the lazy dog?'"
)

print("content:", result.content)
print("tool_calls:", result.tool_calls)


if result.tool_calls:
    tool_call = result.tool_calls[0]
    print("--------------------------------")
    print("tool call names:", tool_call["name"])
    print("tool call args:", tool_call["args"])
    print("--------------------------------")
    
    tools = {"multiply": multiply, "word_count": word_count}

    selected_tool = tools[tool_call["name"]]

    tool_result = selected_tool.invoke(tool_call["args"])

    print("tool result:", tool_result)
else:
    print("no tool calls")

