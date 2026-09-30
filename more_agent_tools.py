import sys

from dotenv import load_dotenv

from langchain.agents import create_agent

from langchain_core.tools import tool

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

# Our Data --> Imagine it is our order database

ORDER_DATABASE = {
    "1001": {"item": "Laptop", "quantity": 1, "price": 1200},
    "1002": {"item": "Smartphone", "quantity": 2, "price": 800},
    "1003": {"item": "Headphones", "quantity": 3, "price": 150},
    "1004": {"item": "Monitor", "quantity": 1, "price": 300},
    "1005": {"item": "Keyboard", "quantity": 5, "price": 50},
}

#imagine we have stock database too

STOCK_DATABASE = {
    "Laptop": {"stock": 10},
    "Smartphone": {"stock": 20},
    "Headphones": {"stock": 15},
    "Monitor": {"stock": 5},
    "Keyboard": {"stock": 25},
}   

# get the order status
@tool
def get_order_status(order_id: str) -> str:
    """Get the status of an order by its ID."""
    order = ORDER_DATABASE.get(order_id)
    if order:
        return f"Order {order_id}: {order['quantity']} x {order['item']} at ${order['price']} each."
    else:
        return f"Order ID {order_id} not found."    
    
    
# get the stock status
@tool
def get_stock_status(item_name: str) -> str:
    """Get the stock status of an item by its name."""
    stock = STOCK_DATABASE.get(item_name)
    if stock:
        return f"Item {item_name} has {stock['stock']} units in stock."
    else:
        return f"Item {item_name} not found in stock database."
    

# Apply discount to an order
@tool
def apply_discount(order_id: str, discount_percentage: float) -> str:
    """Apply a discount to an order by its ID."""
    order = ORDER_DATABASE.get(order_id)
    if order:
        original_price = order['price']
        discounted_price = original_price * (1 - discount_percentage / 100)
        order['price'] = round(discounted_price, 2)  # Update the price in the database
        return f"Discount applied to Order {order_id}. New price: ${order['price']}."
    else:
        return f"Order ID {order_id} not found."

# Estimate delivery time for an order
@tool
def estimate_delivery_time(order_id: str) -> str:
    """Estimate the delivery time for an order by its ID."""
    order = ORDER_DATABASE.get(order_id)
    if order:
        # For simplicity, let's assume delivery time is 5 days for all orders
        return f"Estimated delivery time for Order {order_id} is 5 days."
    else:
        return f"Order ID {order_id} not found."
        

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_order_status, get_stock_status, apply_discount, estimate_delivery_time],
    system_prompt="You are a helpful assistant. You have access to the following tools: get_order_status, get_stock_status, apply_discount, estimate_delivery_time.",
)

def ask_agent(question: str):
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]   
    })
    return result["messages"][-1].content


print("-" * 50)

#Stream the response from the agent
result = agent.stream({
    "messages": [
        {"role": "user", "content": "tell me the status of order 1001, check the stock for Laptop, apply a 10% discount to order 1001, and estimate the delivery time for order 1001."}
    ]
}, stream_mode="messages")

print("Streaming response:")
for message, _metadata in result:
    if message.text:
        print(message.text, end="", flush=True)