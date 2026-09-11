---
name: order-tracking
description: Help customers check the status of their orders, understand delivery timelines, and escalate delayed shipments.
---

# Order Tracking

Follow these steps when a customer asks about an order's status:

1. **Look up the customer** using `lookup_customer` to verify their identity.

2. **Get the order history** using `get_order_history` to find the relevant order.

3. **Check the shipment status** and share the current state with the customer:
   - **Processing** — Order received, not yet shipped. Expected to ship within 1-2 business days.
   - **Shipped** — In transit. Provide the tracking number and estimated delivery date.
   - **Delivered** — Confirm the delivery date and address.
   - **Delayed** — Acknowledge the delay, apologize, and follow the escalation steps below.

4. **If the order is delayed** (more than 3 days past the estimated delivery date):
   - Apologize for the inconvenience.
   - Offer the customer a choice: continue waiting with a $10 credit, or cancel for a full refund.
   - If they choose to wait, apply the credit and note it on the account.

## Important Notes
- Always provide the tracking number when available.
- If the customer says the order shows as delivered but they haven't received it, escalate to the shipping team and let the customer know they'll hear back within 24 hours.
