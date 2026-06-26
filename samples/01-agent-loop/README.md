# The Agent Loop

The agent loop is the core orchestration cycle that every agent harness runs. On each request the cycle is:

```
Input & Context → Reasoning (LLM) → Tool Selection → Tool Execution → Response
```

The model reasons about what to do, optionally selects a tool, executes it, feeds the result back, and repeats until it has enough information to produce a final response. You write the tools; Strands runs the loop. Everything else in the SDK - hooks, memory, steering, deployment - wraps around this loop.

## Files

- **simple_agent.py** - The simplest possible agent: three lines of code to get a working conversational agent.
- **agent_with_tools.py** - Adds tools and a system prompt. Demonstrates `agent.messages` for inspecting conversation history and `result.metrics` for token usage and latency.
- **agent_with_defaults.py** - A fully loaded agent using Strands' opinionated defaults: built-in tools (`file_read`, `file_write`, `editor`, `shell`, `http_request`, `use_agent`), proactive context compression via `SummarizingConversationManager`, and the `ContextOffloader` plugin for handling large tool results.

## Running

```bash
python simple_agent.py
python agent_with_tools.py
python agent_with_defaults.py
```

## Key Concepts

- **Agent harness**: The system that lets an agent run - the loop, the tools, the hooks, the memory, the guardrails, and the infrastructure underneath. Strands is the SDK for building this harness with end-to-end control.
- **Three-line agent**: `Agent()` with no arguments gives you a conversational agent using Bedrock defaults.
- **Tools are decorated functions**: `@tool` plus a clear docstring is all the model needs. The docstring is the model's instruction manual - write it for the model, not just humans.
- **System prompt**: Sets behavior and guardrails in natural language. Shapes the agent's personality across all interactions.
- **The loop is inspectable**: `agent.messages` shows every step (user turns, assistant text, tool calls, tool results). `result.metrics` exposes cycle count and token usage - your first signal for cost and latency.
- **Defaults**: Strands ships preconfigured defaults (tools, compression, offloading) so you can start capable and customize from there.

## Prerequisites

- AWS credentials configured (Strands uses Bedrock by default)
- `agent_with_defaults.py` requires `strands-agents-tools`: `pip install strands-agents-tools`

## Further Reading

- [Strands Agents: Agent Loop](https://strandsagents.com/docs/user-guide/concepts/agents/agent-loop/)
- [Strands Agents: Custom Tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/)
- [Hands-on Workshop: Build Your First Agent](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
