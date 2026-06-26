# Steering

Steering intercepts the agent loop to inject guidance at decision points. Think of it as programmable guardrails - you define handlers that observe tool calls and agent responses, then either allow them, modify them, or block them entirely.

There are two flavors: deterministic handlers that apply rules with code (fast, predictable), and LLM-based handlers that evaluate behavior using a separate model call (flexible, but adds latency).

## Files

- **customer_service_steering.py** - The main agent file that wires up both steering handlers as plugins.
- **customer_service_tools.py** - Mock tools for the customer service domain (lookup_customer, get_order_history, process_refund, etc.).
- **steering_handlers.py** - Contains both handlers:
  - `RefundWorkflowHandler`: Enforces lookup_customer → get_order_history → process_refund ordering, and validates refund amounts match the order.
  - `ToneGuardrailHandler`: LLM-based handler that evaluates agent responses against communication guidelines.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
python customer_service_steering.py
```

Try requesting a refund and watch the steering enforce the correct tool order. Try being rude to see the tone guardrail in action.

## Key Concepts

- **Deterministic steering**: Code-based rules that guarantee specific behaviors. Example: "always look up the customer before processing a refund." No LLM call needed - fast and predictable.
- **LLM-based steering**: Use a model to evaluate complex, subjective criteria like tone, safety, or policy compliance. More flexible but adds cost and latency.
- **Composability**: Handlers compose - stack as many as you need on a single agent. They run as plugins with hooks on the agent lifecycle.
- **Workflow enforcement**: Steering can enforce tool ordering (A must happen before B), validate inputs/outputs, and block operations that violate business rules.

## Further Reading

- [Strands Agents: Hooks](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/)
- [Strands Agents: Interventions](https://strandsagents.com/docs/user-guide/concepts/agents/interventions/)
- [Hands-on Workshop: Module 3 (Skills + Steering)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/03-skills-steering)
