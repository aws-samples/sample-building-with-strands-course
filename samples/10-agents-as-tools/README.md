# Agents as Tools

The simplest multi-agent pattern: one orchestrator agent calls specialist agents as tools. The orchestrator stays in control, decides when to delegate, and synthesizes the results. This is the hub-and-spoke model.

There are two approaches — pass an agent directly in the tools list (simplest), or wrap it in a `@tool` function for full control over invocation.

## Files

- **agent_as_tool.py** — Demonstrates both approaches:
  1. **Direct pass** (commented out) — A researcher agent is passed directly in the writer's tools list. The writer delegates research tasks automatically.
  2. **@tool decorator** (active) — Wraps an agent in a `@tool` function, giving you control over the prompt, model selection, and how results are returned. Uses a stronger model (Opus) for orchestration and a lighter model (Sonnet) for the specialist.

## Running

```bash
python agent_as_tool.py
```

## Key Concepts

- **The docstring is the routing logic**: It tells the orchestrator when to delegate. The model routes based on tool descriptions — you never write an `if` statement.
- **Agent isolation**: Each sub-agent has its own context window, model, and tools. They're fully independent — one agent's context doesn't leak into another's.
- **Orchestrator control**: The orchestrator decides when to call the specialist, what to ask, and how to use the response. It's a function call, not a handoff.
- **Model heterogeneity**: Use a stronger model for the orchestrator (which needs to reason about what to delegate) and a cheaper model for specialists (which do focused work).
- **Silent sub-agents**: Use `callback_handler=None` on sub-agents to suppress their streaming output. Only the orchestrator streams to the user.
- **When to use this pattern**: Clearly separable domains, when you want one agent synthesizing everything, when you need request/response semantics between agents.

## Further Reading

- [Strands Agents: Agents as Tools](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/)
- [Strands Agents: Multi-Agent Patterns](https://strandsagents.com/docs/user-guide/concepts/multi-agent/multi-agent-patterns/)
- [Hands-on Workshop: Module 5 (Multi-Agent)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/05-multi-agent)
