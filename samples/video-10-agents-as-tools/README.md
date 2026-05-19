# Video 10: Agents as Tools

The simplest multi-agent pattern: one agent calls another as a tool. This video shows two approaches — passing an agent directly, and wrapping one in a `@tool` function for more control over how it's invoked.

## Files

- **simple_delegation.py** — A researcher agent is passed directly as a tool to a writer agent. The writer delegates research tasks automatically.
- **as_tool.py** — Wraps an agent in a `@tool` decorated function, giving you control over the prompt, context, and how results are returned.

## Running

```bash
python simple_delegation.py
python as_tool.py
```

## Notes

- Each sub-agent has its own context window, model, and tools — they're fully independent.
- The `@tool` wrapper approach gives you more control: you can shape the input, pick a different model for the sub-agent, or post-process its output.
- This pattern works well when you have clearly separable tasks (research vs writing, analysis vs formatting).
