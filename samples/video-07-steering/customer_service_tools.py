from strands import tool

# --- Mock customer data ---

CUSTOMERS = {
    "C-1001": {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "555-0142",
        "account_status": "active",
    },
    "C-1002": {
        "name": "Mike Chen",
        "email": "mike.chen@email.com",
        "phone": "555-0198",
        "account_status": "locked",
    },
}

ORDERS = {
    "C-1001": [
        {
            "order_id": "ORD-5521",
            "item": "Wireless Headphones",
            "amount": 79.99,
            "status": "Delivered",
            "order_date": "2026-04-20",
            "delivered_date": "2026-04-28",
            "tracking": "TRK-998877",
        },
        {
            "order_id": "ORD-5488",
            "item": "USB-C Hub",
            "amount": 45.00,
            "status": "Shipped",
            "order_date": "2026-05-01",
            "estimated_delivery": "2026-05-06",
            "tracking": "TRK-887766",
        },
    ],
    "C-1002": [
        {
            "order_id": "ORD-5390",
            "item": "Mechanical Keyboard",
            "amount": 149.99,
            "status": "Delayed",
            "order_date": "2026-04-15",
            "estimated_delivery": "2026-04-25",
            "tracking": "TRK-776655",
        },
    ],
}


# --- Tools ---

@tool
def lookup_customer(customer_id: str) -> str:
    """Look up a customer by their ID.

    Args:
        customer_id: The customer ID
    """
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return f"No customer found with ID {customer_id}"
    return (
        f"Customer: {customer['name']}\n"
        f"Email: {customer['email']}\n"
        f"Phone: {customer['phone']}\n"
        f"Account Status: {customer['account_status']}"
    )


@tool
def get_order_history(customer_id: str) -> str:
    """Get order history for a customer.

    Args:
        customer_id: The customer ID
    """
    orders = ORDERS.get(customer_id)
    if not orders:
        return f"No orders found for customer {customer_id}"
    lines = []
    for order in orders:
        line = (
            f"Order {order['order_id']}: {order['item']} — ${order['amount']:.2f} "
            f"[{order['status']}] Ordered: {order['order_date']} "
        )
        if order.get("delivered_date"):
            line += f"Delivered: {order['delivered_date']} "
        if order.get("estimated_delivery"):
            line += f"Est. Delivery: {order['estimated_delivery']} "
        line += f"Tracking: {order['tracking']}"
        lines.append(line)
    return "\n".join(lines)


@tool
def process_refund(order_id: str, amount: float) -> str:
    """Process a refund for an order.

    Args:
        order_id: The order ID to refund
        amount: The refund amount in dollars
    """
    return f"Refund of ${amount:.2f} processed for order {order_id}. Expect 3-5 business days."
