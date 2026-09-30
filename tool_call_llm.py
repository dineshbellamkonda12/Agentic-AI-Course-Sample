import requests
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from langchain_core.tools import tool

from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class CurrencyConversion(BaseModel):
    amount: float = Field(description="The amount to convert")
    from_currency: str = Field(description="The currency to convert from")
    to_currency: str = Field(description="The currency to convert to")

@tool("currency_conversion", args_schema=CurrencyConversion)
def currency_conversion(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert an amount from one currency to another using live exchange rates."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency == to_currency:
        return amount

    url = "https://api.frankfurter.app/latest"
    response = requests.get(
        url,
        params={"amount": amount, "from": from_currency, "to": to_currency},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data["rates"][to_currency]

model_with_tools = model.bind_tools([currency_conversion])

response = model_with_tools.invoke("Convert 100 USD to EUR")

print("content:", response.content)
print("tool_calls:", response.tool_calls)

if response.tool_calls:
    tool_call = response.tool_calls[0]
    result = currency_conversion.invoke(tool_call["args"])
    print("tool result:", result)
