import json
from strands import Agent, tool
from strands_tools import http_request, file_write


@tool
def query_product_database(query: str) -> str:
    """Query the internal product database for inventory and pricing information.

    Args:
        query: Search query for products (e.g., "wireless headphones", "USB-C hub")
    """
    products = {
        "wireless headphones": "SKU-WH100: Wireless Headphones Pro — $79.99, 142 in stock, 4.5★ rating, launched 2025-03",
        "usb-c hub": "SKU-UC200: USB-C Hub 7-in-1 — $45.00, 89 in stock, 4.2★ rating, launched 2024-11",
        "mechanical keyboard": "SKU-MK300: Mechanical Keyboard RGB — $149.99, 23 in stock, 4.8★ rating, launched 2025-01",
        "noise cancelling": "SKU-NC400: Noise Cancelling Earbuds — $129.99, 67 in stock, 4.6★ rating, launched 2025-05",
    }
    key = query.lower()
    matches = [info for product_key, info in products.items() if product_key in key]
    if matches:
        return "\n".join(matches)
    return f"No products found matching '{query}'. Available: wireless headphones, usb-c hub, mechanical keyboard, noise cancelling"


SYSTEM_PROMPT = """You are a product research analyst. You help the team understand
market positioning by comparing competitor pricing with our internal catalog.

When given a research task:
1. Use http_request to gather public market data 
2. Use query_product_database to check our internal pricing and inventory
3. Write a brief competitive analysis and save it using file_write"""

agent = Agent(
    tools=[http_request, file_write, query_product_database],
    system_prompt=SYSTEM_PROMPT,
)

result = agent("Research what wireless headphones are trending on the market and compare it against our offerings. "
               "Write a short competitive positioning summary and save it to report.md")

# ============================================================
# Uncomment to inspect conversation history
# ============================================================
print("\n" + "=" * 60)
print("CONVERSATION HISTORY:")
print("=" * 60)
print(json.dumps(agent.messages, indent=2, default=str))

