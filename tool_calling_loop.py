from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def word_count(text: str) -> int:
    """Count the number of words in a text"""
    return len(text.split())

@tool
def current_time_all_countries(location: str) -> str:
    """Get the current local time for a country, city, or state."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import requests

    location = location.strip()
    if not location:
        return "Please provide a country, city, or state name."

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results or not results[0].get("timezone"):
        return f"I couldn't find a timezone for {location!r}."

    result = results[0]
    timezone_name = result["timezone"]
    local_time = datetime.now(ZoneInfo(timezone_name))
    place = ", ".join(
        part for part in (result.get("name"), result.get("country")) if part
    )
    return f"The current time in {place or location} is {local_time:%Y-%m-%d %H:%M:%S} ({timezone_name})."


tools = [multiply, word_count, current_time_all_countries]

tool_names = [tool.name for tool in tools]

model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

messages = [
    SystemMessage(content=f"You are a helpful assistant. You have access to the following tools: {', '.join(tool_names)}."),
    HumanMessage(content="Hello! Can you help me with some tasks? I need to multiply 7 and 8, count the words in 'Hello world from LangChain!', and find out the current time in Tokyo.")
]

while True:
    response = model.invoke(messages)
    print(f"Assistant: {response.content}")
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_func = next((tool for tool in tools if tool.name == tool_name), None)
            if tool_func:
                try:
                    result = tool_func.invoke(tool_call["args"])
                except Exception as e:
                    result = f"Tool '{tool_name}' raised an error: {e}"
            else:
                result = f"Tool '{tool_name}' not found."
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
        continue

    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append(HumanMessage(content=user_input))
    



