from langchain.agents import create_agent

from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

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


agent = create_agent(
    model="gpt-4o-mini",
    tools=[multiply, current_time_all_countries],
    system_prompt="You are a helpful assistant. You have access to the following tools: multiply, current_time_all_countries.",
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "Hello! Can you help me with some tasks? I need to multiply 7 and 8, and find out the current time in Tokyo."}
    ]   
})

print("Final result:", result["messages"][-1].content)