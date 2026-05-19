# Video 1: The Agent Loop

This video introduces the core concept behind Strands Agents — the agent loop. You'll see how a minimal 3-line agent works, then build up to adding tools and a system prompt. We also look at how to inspect what's happening under the hood with message history and metrics.

## Files

- **simple_agent.py** — The simplest possible agent: three lines of code to get a working conversational agent.
- **agent_with_tools.py** — Adds tools and a system prompt to the agent. Demonstrates `agent.messages` for inspecting conversation history and `result.metrics` for token usage and latency.

## Running

```bash
python simple_agent.py
python agent_with_tools.py
```

## Notes

- Make sure you have AWS credentials configured (Strands uses Bedrock by default).
- Check `result.metrics` output to understand how many tokens each request uses — helpful for cost estimation.
