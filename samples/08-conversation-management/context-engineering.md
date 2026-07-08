# Context Engineering

Context engineering is the discipline of deciding **what information enters the model's context window, when, and in what form**. Unlike prompt engineering (which focuses on instructions), context engineering ensures the model has the right data at the right time without overflowing the window or wasting tokens.

Context engineering breaks down into four categories:

| Category | What It Does | Strands Primitive |
| --- | --- | --- |
| **Select** | Choose what enters context — inject relevant info, filter out noise | ContextInjector plugin |
| **Compress** | Shrink what's already in context — summarize history, truncate results | ConversationManager (sliding window, summarization) |
| **Isolate** | Separate concerns — give sub-agents their own context windows | Multi-agent patterns, `context_manager="agentic"` |
| **Externalize** | Move large data out of context — store externally, keep compact reference | ContextOffloader plugin |

## The One-Line Default: context_manager="auto"

For most use cases, start here:

```python
from strands import Agent

agent = Agent(context_manager="auto")

```

This single parameter enables:

- **Offloading** — large tool results stored externally, replaced with truncated preview
- **Summarization** — old messages compressed into structured summaries (not dropped)
- **Proactive compression** — fires at 85% context usage to stay ahead of overflow

In benchmarks on real code investigation tasks: **costs dropped 55% while accuracy went from 68% to 98%**. Half the tokens, better results.

For agents that need to protect specific context across long conversations, use `context_manager="agentic"` and the model gets tools to summarize, truncate, or pin messages itself.

📖 [Context management blog post](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)

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

- `trigger="userTurn"` (default) — only on fresh user messages
- `trigger="everyTurn"` — before every model call including mid-task tool-result turns
- Custom predicate — `trigger=lambda context: context.state.get("recall_enabled") is True`

📖 [Context Injector docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-injector/)

## Context Offloader

Large tool results (file reads, API responses, database queries) can overwhelm the context window. The ContextOffloader intercepts results **at tool execution time** before they enter conversation and stores them externally:

```python
from strands import Agent
from strands.vended_plugins.context_offloader import ContextOffloader, FileStorage

agent = Agent(
    plugins=[
        ContextOffloader(
            storage=FileStorage("./offloaded"),
            max_result_tokens=8_000,
            preview_tokens=2_000,
        ),
    ],
)

```

What the agent sees: the first ~2,000 tokens as a preview plus a storage reference. The plugin registers a `retrieve_offloaded_content` tool so the agent can fetch the full content when needed.

Storage backends: `InMemoryStorage` (dev/testing), `FileStorage` (local), `S3Storage` (production).

📖 [Context Offloader docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-offloader/)

## Conversation Managers (Compression)

### Sliding Window

Keeps only the N most recent messages. Simple, predictable, and where most agents start:

```python
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    conversation_manager=SlidingWindowConversationManager(
        window_size=20,
        should_truncate_results=True,
        proactive_compression={
            "compression_threshold": 0.9,
        },
    ),
)

```

📂 [sliding_window.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-conversation-management/sliding_window.py) — Find all code on GitHub

### Summarizing Conversation Manager

Instead of dropping old messages, compress them into summaries. Preserves more information but introduces compression risk:

```python
from strands.agent.conversation_manager import SummarizingConversationManager

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3,
        preserve_recent_messages=10,
        proactive_compression={
            "compression_threshold": 0.9,
        },
    ),
)

```

📂 [summarizing.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-conversation-management/summarizing.py) — Find all code on GitHub

### Custom Summarizer Agent

Use a cheaper model with a domain-specific summarization prompt:

```python
from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SummarizingConversationManager

SUMMARIZATION_PROMPT = """Summarize the following customer service conversation.
Focus on:
- Customer identity (name, ID, account status)
- The issue or request they came in with
- Actions already taken (tools called, information retrieved)
- Any unresolved problems or pending next steps
"""

summarizer = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-haiku-4-20250514-v1:0"),
    system_prompt=SUMMARIZATION_PROMPT,
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.4,
        preserve_recent_messages=8,
        summarization_agent=summarizer,
        proactive_compression={"compression_threshold": 0.9},
    ),
)

```

📂 [custom_summarizer.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/08-conversation-management/custom_summarizer.py) — Find all code on GitHub

## Strategy Comparison

| Strategy | Tradeoff |
| --- | --- |
| `context_manager="auto"` | Best default. Offloading + summarization + proactive compression |
| `context_manager="agentic"` | Model self-manages context. Trades tokens for judgment |
| Sliding window | Simple, predictable. Loses old info entirely |
| Summarization | Preserves more info. Lossy compression risk |
| Context offloading | Handles big individual results. Agent can retrieve full content |
| Context injection | Ephemeral per-call data. Never persisted to history |

## Resources

- 📖 [Context Management blog: "Reduced cost, better isolation, more resilience"](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)
- 📖 [Context Injector docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-injector/)
- 📖 [Context Offloader docs](https://strandsagents.com/docs/user-guide/concepts/plugins/context-offloader/)
- 📖 [Conversation Management docs](https://strandsagents.com/docs/user-guide/concepts/agents/conversation-management/)

