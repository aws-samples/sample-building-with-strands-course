# Hooks

Hooks add deterministic control to a probabilistic loop. They inject code at lifecycle events — before/after tool calls and before/after the agent loop — without changing the agent's logic. Unlike tools (which the model decides to use), hooks fire automatically every time, regardless of what the model reasons.

A runaway loop could call the same tool dozens of times. A model might attempt a destructive operation without asking. Hooks solve this by enforcing rules that don't depend on the model "deciding" to behave.

## Files

- **approval_interrupt.py** — Human-in-the-loop approval before file deletion. Uses `event.interrupt()` to pause execution and ask the user for confirmation.
- **rate_limiter.py** — Prevents any tool from being called more than 3 times per request. Demonstrates how hooks can enforce safety boundaries.

## Running

```bash
python approval_interrupt.py
python rate_limiter.py
```

## Key Concepts

- **Deterministic vs probabilistic**: Prompting asks the model to behave. Hooks guarantee it. Limits run every time, not when the model feels like it.
- **Lifecycle events**: Hooks register callbacks on `BeforeInvocationEvent`, `BeforeToolCallEvent`, `AfterToolCallEvent`, and other lifecycle points.
- **Cancel mechanism**: `event.cancel_tool` skips a tool call and feeds a message back to the model explaining why — so it learns and stops retrying.
- **Interrupts**: `event.interrupt()` pauses agent execution and returns control to the caller — useful for approval workflows.
- **Per-request state**: Rate limits and counters reset per invocation (`BeforeInvocationEvent`), not for the agent's lifetime.
- **Composability**: Multiple hooks can fire for the same event. They're stored as a list per event type, so you can layer behaviors.
- **Separation of concerns**: Hooks don't touch tools or prompts — they're a separate, reusable layer.

## When to Use Hooks

- Rate limit tool usage to prevent runaway loops
- Require human approval before destructive operations
- Log every tool call for audit trails
- Validate tool inputs/outputs against business rules
- Enforce access control on sensitive tools

## Further Reading

- [Strands Agents: Hooks](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/)
- [Hands-on Workshop: Module 2 (Hooks)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/02-hooks)
