# Video 7: Steering

Steering intercepts the agent loop to inject guidance at decision points — think of it as programmable guardrails. This video builds two handlers: one that enforces a deterministic tool-call order for refunds, and one that uses an LLM to evaluate tone. Both compose together as plugins on the same agent.

## Files

- **customer_service_steering.py** — The main agent file that wires up both steering handlers as plugins.
- **customer_service_tools.py** — Mock tools for the customer service domain (lookup_customer, get_order_history, process_refund, etc.).
- **steering_handlers.py** — Contains both handlers:
  - `RefundWorkflowHandler`: enforces lookup_customer → get_order_history → process_refund ordering, and validates refund amounts match the order.
  - `ToneGuardrailHandler`: LLM-based handler that evaluates agent responses against communication guidelines.
- **skills/** — Skill definitions for the customer service agent.

## Running

```bash
python customer_service_steering.py
```

Try requesting a refund and watch the steering enforce the correct tool order. Try being rude to see the tone guardrail in action.

## Notes

- Deterministic handlers (like RefundWorkflow) are fast and predictable — no LLM call needed.
- LLM-based handlers (like ToneGuardrail) are more flexible but add latency.
- Handlers compose — you can stack as many as you need on a single agent.
