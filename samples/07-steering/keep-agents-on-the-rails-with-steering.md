# Keep Agents on the Rails with Steering

Instructions in prompts aren't always reliably followed, especially as context grows. Steering lets you inspect and influence agent behavior at runtime, returning one of three outcomes: **Proceed**, **Guide**, or **Interrupt**.

Strands Steering hooks achieved a [100% accuracy pass rate across 600 evaluation runs](https://strandsagents.com/blog/steering-accuracy-beats-prompts-workflows/), compared to 82.5% for simple prompt-based instructions and 80.8% for graph-based workflows.

## Two Types of Steering

| Type | How It Works | Use Case |
| --- | --- | --- |
| **Deterministic** (SteeringHandler) | Python logic inspects the events ledger | Enforcing workflow ordering, validating parameters |
| **LLM-based** (LLMSteeringHandler) | A second agent judges the output | Tone/policy compliance, nuanced quality checks |

## Deterministic Steering: Enforce Refund Workflow

```python
from strands.vended_plugins.steering import (
    SteeringHandler, Proceed, Guide, ToolSteeringAction, LedgerProvider,
)

class RefundWorkflowHandler(SteeringHandler):
    name = "refund-workflow"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "process_refund":
            return Proceed(reason="Not a refund operation")

        ledger = self.steering_context.data.get("ledger", {})
        tool_calls = ledger.get("tool_calls", [])

        # Must look up customer first
        customer_verified = any(
            c["tool_name"] == "lookup_customer" and c["status"] == "success"
            for c in tool_calls
        )
        if not customer_verified:
            return Guide(reason="You must look up the customer first.")

        # Must check order history
        order_checked = any(
            c["tool_name"] == "get_order_history" and c["status"] == "success"
            for c in tool_calls
        )
        if not order_checked:
            return Guide(reason="You must check order history first.")

        return Proceed(reason="Refund workflow validated")

```

## LLM-Based Steering: Tone Guardrail

```python
from strands.vended_plugins.steering import LLMSteeringHandler

class ToneGuardrailHandler(LLMSteeringHandler):
    name = "tone-guardrail"

    def __init__(self):
        super().__init__(
            system_prompt="""Evaluate the customer service response against these policies:
            - Don't overpromise timelines
            - Acknowledge customer frustration
            - Don't offer unauthorized compensation
            - Keep responses concise
            If violated, provide specific guidance on what to fix."""
        )

```

## Composing Everything into an Agent

```python
agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[
        skills_plugin,              # On-demand workflow instructions
        RefundWorkflowHandler(),    # Deterministic: enforce refund steps
        tone_handler,               # LLM-based: enforce communication quality
    ],
    system_prompt=SYSTEM_PROMPT,
)

```

📂 [customer_service_steering.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/07-steering/customer_service_steering.py) · [steering_handlers.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/07-steering/steering_handlers.py) — Find all code on GitHub

## Resources

- 📖 [Steering Hooks](https://strandsagents.com/docs/user-guide/concepts/plugins/steering/)

