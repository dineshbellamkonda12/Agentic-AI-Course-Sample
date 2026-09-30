from langchain_core.tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")


def timezone_for_city(city: str) -> ZoneInfo:
    """Resolve a city name or IANA key (e.g. london, Europe/London) to a ZoneInfo."""
    raw = city.strip()
    try:
        return ZoneInfo(raw)
    except ZoneInfoNotFoundError:
        pass

    needle = raw.lower().replace(" ", "_")
    matches = [
        tz for tz in available_timezones()
        if tz.rsplit("/", 1)[-1].lower() == needle
    ]
    if not matches:
        raise ZoneInfoNotFoundError(
            f"No time zone found for city {city!r}. Try an IANA name like 'Europe/London'."
        )
    matches.sort(key=len)
    return ZoneInfo(matches[0])


@tool
def current_time(city: str) -> str:
    "Get the current time in a given city"
    timezone = timezone_for_city(city)
    time = datetime.now(timezone)
    return time.strftime("%H:%M:%S")
    

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b



print("Name", current_time.name)
print("Description", current_time.description)
print("args", current_time.args)




