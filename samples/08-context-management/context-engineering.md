# Context Engineering

Context engineering is the discipline of deciding **what information enters the model's context window, when, and in what form**. Unlike prompt engineering (which focuses on instructions), context engineering ensures the model has the right data at the right time without overflowing the window or wasting tokens.

Context engineering breaks down into four categories:

| Category | What It Does | Strands Primitive |
| --- | --- | --- |
| **Select** | Choose what enters context, inject relevant info, filter out noise | ContextInjector plugin |
| **Compress** | Shrink what's already in context, summarize history, truncate results | ContextManager strategies (truncate, summarize, drop) |
| **Isolate** | Separate concerns, give sub-agents their own context windows | Multi-agent patterns, `context_manager="agentic"` |
| **Externalize** | Move large data out of context, store externally, keep compact reference | ContextManager stash + retrieval tool |

## The One-Line Default: context_manager="auto"

For most use cases, start here:

```python
from strands import Agent

agent = Agent(context_manager="auto")

```

This single parameter enables:

- **Offloading** large tool results to a stash, replaced with truncated previews
- **Summarization** of old messages into structured summaries (not dropped)
- **Proactive compression** firing at 85% context usage to stay ahead of overflow

In benchmarks on real code investigation tasks: **costs dropped 55% while accuracy went from 68% to 98%**. Half the tokens, better results.

For agents that need to protect specific context across long conversations, use `context_manager="agentic"` and the model gets tools to summarize, truncate, or pin messages itself.

📖 [Context Management docs](https://strandsagents.com/docs/user-guide/concepts/context-management/)

## Context Injector

The ContextInjector plugin folds ephemeral text into the model input before each call. The text is **never written to conversation history,** it augments one call only. Use it for context the agent should always have but that doesn't belong in stored history: current time, environment facts, retrieval lookups.

```python
from datetime import datetime, timezone
from strands import Agent
from strands.vended_plugins.context_injector import ContextInjector

agent = Agent(
    plugins=[
        ContextInjector(
            lambda context: f"<now>{datetime.now(timezone.utc).isoformat()}</now>"
        ),
    ],
)

```

Control **when** injection fires:

- `trigger="userTurn"` (default) - only on fresh user messages
- `trigger="everyTurn"` - before every model call including mid-task tool-result turns
- Custom predicate - `trigger=lambda context: context.state.get("recall_enabled") is True`

📖 [Context Injector docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-injector/)

## ContextManager and Offload Strategies

The `ContextManager` is the engine behind `context_manager="auto"`. When you need custom control over how context is managed, you can build your own strategy pipeline using `Offload` strategies.

> **Note:** The `ContextManager` and `Offload` APIs are currently available under `strands.experimental.context_manager`. They are fully functional and will move to the main namespace in an upcoming release.

There are three types of Offload strategies:

| Strategy | What stays in context |
| --- | --- |
| `Offload.truncate(...)` | A head/tail preview of the original |
| `Offload.summarize(...)` | An LLM-generated summary of the original |
| `Offload.drop(...)` | Nothing (original goes to stash only) |

Each strategy takes a **target** that controls what content it operates on:

```python
Offload.summarize("*")                   # everything: all message types
Offload.truncate("tool_results")         # only successful tool results
Offload.drop("tool_result_errors")       # only errored tool results
Offload.summarize("assistant_text")      # only assistant text blocks
Offload.truncate(["bash", "read_file"])  # only results from specific tools
Offload.truncate(["!read_file"])         # everything except read_file
```

And `.when(...)` sets the conditions:

- `threshold=N` - fire on individual blocks exceeding N tokens (per-block mode)
- `utilization=0.85` - fire when context window is 85% full (per-message mode)
- `preserve_recent=N` - skip the N most recent matching messages

### Truncate Strategy (Drop Oldest)

The simplest approach. Remove old messages when context gets full:

```python
from strands import Agent
from strands.experimental.context_manager import ContextManager, Offload

agent = Agent(
    tools=[...],
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.truncate("*").when(utilization=0.9, preserve_recent=10),
        ],
    ),
)

```

📂 [sliding_window.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-context-management/sliding_window.py) - Find all code on GitHub

### Summarize Strategy

Instead of dropping old messages, compress them into summaries. Preserves more information but summaries are lossy:

```python
from strands.experimental.context_manager import ContextManager, Offload

agent = Agent(
    tools=[...],
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.summarize("*").when(utilization=0.85, preserve_recent=10),
        ],
    ),
)

```

📂 [summarizing.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-context-management/summarizing.py) - Find all code on GitHub

### Custom Summarizer (Cheaper Model)

Summarizing history doesn't require your most capable model. Pass a cheaper one via the config dict:

```python
from strands.models import BedrockModel
from strands.experimental.context_manager import ContextManager, Offload

summarizer_model = BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0")

agent = Agent(
    tools=[...],
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.summarize(
                "*",
                {
                    "model": summarizer_model,
                    "system_prompt": "Summarize the customer service conversation...",
                },
            ).when(utilization=0.85, preserve_recent=8),
        ],
        stash=False,
    ),
)

```

`stash=False` disables the retrieval tool when you're doing pure summarization and don't need the agent pulling back offloaded content.

📂 [custom_summarizer.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-context-management/custom_summarizer.py) - Find all code on GitHub

## Strategy Comparison

| Strategy | Tradeoff |
| --- | --- |
| `context_manager="auto"` | Best default. Offloading + summarization + proactive compression |
| `context_manager="agentic"` | Model self-manages context. Trades tokens for judgment |
| `Offload.truncate(...)` | Simple, predictable. Loses old info entirely |
| `Offload.summarize(...)` | Preserves more info. Lossy compression, costs an LLM call |
| `Offload.drop(...)` | Most aggressive. Content goes to stash only |
| Context injection | Ephemeral per-call data. Never persisted to history |

## Resources

- 📖 [Context Management docs](https://strandsagents.com/docs/user-guide/concepts/context-management/)
- 📖 [Context Injector docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-injector/)
- 📖 [Context Offloader docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-offloader/)
