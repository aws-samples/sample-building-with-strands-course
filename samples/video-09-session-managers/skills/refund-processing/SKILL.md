---
name: refund-processing
description: Step-by-step process for handling customer refund requests, including order verification, return window checks, and refund issuance.
---

# Refund Processing

Follow these steps when a customer requests a refund:

1. **Look up the customer** using `lookup_customer` to verify their identity and account status.

2. **Get the order details** using `get_order_history` to find the specific order they want refunded.

3. **Check the return window.** Orders are eligible for a refund within 30 days of delivery. Use the delivered_date from the order data to determine eligibility — do not ask the customer for this information. If the order was delivered more than 30 days ago, inform the customer that the return window has closed and offer alternatives like store credit.

4. **Confirm the refund** with the customer. Briefly state the order ID, item, and refund amount, then ask for a yes/no to proceed. Keep it short.

5. **Process the refund** using `process_refund` with the order ID and confirmed amount.

6. **Set expectations.** Let the customer know refunds typically take 3-5 business days to appear on their statement.

## Important Notes
- Never process a refund without confirming the details with the customer first.
- If the order total exceeds $500, inform the customer that a supervisor review is required and the refund will be processed within 24 hours.
- Always be empathetic. The customer is coming to you with a problem they want solved.
