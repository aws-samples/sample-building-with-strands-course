import re

from strands.vended_plugins.steering import (
    SteeringHandler, LLMSteeringHandler,
    Proceed, Guide, ToolSteeringAction,
    LedgerProvider,
)


class RefundWorkflowHandler(SteeringHandler):
    """Deterministic handler: enforce refund workflow ordering.

    Rules:
    1. Must look up the customer before processing a refund
    2. Must check order history before processing a refund
    """

    name = "refund-workflow"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "process_refund":
            return Proceed(reason="Not a refund operation")

        print("[STEERING] 🔍 process_refund attempted — checking workflow...")

        ledger = self.steering_context.data.get("ledger", {})
        tool_calls = ledger.get("tool_calls", [])
        print(f"[STEERING] 📋 Ledger has {len(tool_calls)} tool calls: {[c.get('tool_name', '?') + ':' + c.get('status', '?') for c in tool_calls]}")

        # Must look up customer first
        customer_verified = any(
            c["tool_name"] == "lookup_customer" and c["status"] == "success"
            for c in tool_calls
        )
        if not customer_verified:
            print("[STEERING] ⚠️  Blocked: must look up customer first")
            return Guide(
                reason="You must look up the customer with lookup_customer "
                "before processing a refund."
            )

        # Must check order history
        order_checked = any(
            c["tool_name"] == "get_order_history" and c["status"] == "success"
            for c in tool_calls
        )
        if not order_checked:
            print("[STEERING] ⚠️  Blocked: must check order history first")
            return Guide(
                reason="You must check the order history with get_order_history "
                "before processing a refund."
            )

        # Validate refund amount matches the order
        refund_order_id = tool_use.get("input", {}).get("order_id", "")
        refund_amount = tool_use.get("input", {}).get("amount", 0)

        # Find the order history result in the ledger
        order_result = None
        for c in tool_calls:
            if c["tool_name"] == "get_order_history" and c["status"] == "success":
                order_result = c.get("result", [{}])[0].get("text", "")
                break

        if order_result and refund_order_id:
            # Check that the order ID exists in the order history
            if refund_order_id not in order_result:
                print(f"[STEERING] ⚠️  Blocked: order {refund_order_id} not found in customer's order history")
                return Guide(
                    reason=f"Order {refund_order_id} does not appear in this customer's order history. "
                    "Verify the order ID is correct."
                )

            # Check that the refund amount matches the order amount
            pattern = rf"{re.escape(refund_order_id)}.*?\$(\d+\.\d{{2}})"
            match = re.search(pattern, order_result)
            if match:
                actual_amount = float(match.group(1))
                if refund_amount != actual_amount:
                    print(f"[STEERING] ⚠️  Blocked: refund amount ${refund_amount:.2f} doesn't match order amount ${actual_amount:.2f}")
                    return Guide(
                        reason=f"Refund amount ${refund_amount:.2f} does not match the order amount "
                        f"of ${actual_amount:.2f} for {refund_order_id}. Use the correct amount."
                    )

        print("[STEERING] ✅ Refund workflow validated — proceeding")
        return Proceed(reason="Refund workflow validated")


class ToneGuardrailHandler(LLMSteeringHandler):
    name = "tone-guardrail"

    def __init__(self):
        super().__init__(
            system_prompt="""You are evaluating a customer service agent's responses.
Ensure the agent follows these communication guidelines:

- Don't overpromise or guarantee specific timelines beyond what the system confirms
- Don't blame the customer, other departments, or third parties
- Acknowledge the customer's frustration before jumping to solutions
- Don't offer discounts, credits, or compensation beyond what's in the workflow instructions
- Keep responses concise and actionable — no walls of text
- Never share internal system details, error codes, or technical jargon with the customer
- If the agent can't help, it should clearly explain why and offer an alternative

If the agent violates any of these, provide specific guidance on what to fix."""
        )

    async def steer_after_model(self, **kwargs):
        print("[TONE] 🔍 Evaluating agent response...")
        result = await super().steer_after_model(**kwargs)
        action_type = type(result).__name__
        print(f"[TONE] {'✅ Approved' if action_type == 'Proceed' else '⚠️  Guided: ' + getattr(result, 'reason', '')}")
        return result


tone_handler = ToneGuardrailHandler()
