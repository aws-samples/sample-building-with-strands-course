# Context Management

As conversations grow, they can overflow the model's context window. Context management controls what happens when messages accumulate. You can truncate old messages, summarize them, or use a cheaper model for the summarization to save costs.

The SDK ships two high-level presets (`"auto"` and `"agentic"`) that work out of the box, plus a `ContextManager` class with composable `Offload` strategies for when you need custom control.

## Files

- **context_manager_auto.py** - The recommended default. One parameter (`context_manager="auto"`) gives you offloading, summarization, and proactive compression with no configuration. In benchmarks, this cut costs by 55% while improving accuracy.
- **context_manager_agentic.py** - For agents that need to decide what context to keep. The model gets tools to summarize, truncate, or pin messages. Use this when your agent needs to protect specific context across long conversations.
- **sliding_window.py** - Uses `ContextManager` with `Offload.truncate` strategies. Truncates large tool results and drops the oldest messages when context fills up. Simplest custom approach.
- **summarizing.py** - Uses `ContextManager` with `Offload.summarize` strategies. Summarizes old messages instead of dropping them. Preserves key information while reducing token count.
- **custom_summarizer.py** - Uses a cheaper model (Haiku) for the summarization strategy to reduce costs. Demonstrates passing a custom model and system prompt to the summarize strategy.
- **customer_service_tools.py** - Mock tools shared across examples.
- **steering_handlers.py** - Steering handlers shared across examples.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
# Recommended: auto mode (one-liner, best defaults)
python context_manager_auto.py

# Agentic mode (model decides what to keep)
python context_manager_agentic.py

# Custom strategies (for understanding what auto does under the hood)
python sliding_window.py
python summarizing.py
python custom_summarizer.py
```

Have a long conversation and watch how each strategy handles the growing history differently.

## Key Concepts

- **`context_manager="auto"`**: The recommended default. Offloads large tool results, compresses old messages into summaries, and fires proactive compression at 85% usage. One line, no configuration.
- **`context_manager="agentic"`**: The model gets context management tools and decides what to retain, summarize, or drop. Use when the agent needs judgment about what's important to keep across long conversations.
- **`ContextManager`**: The engine behind the presets. Build custom strategy pipelines with `Offload.truncate`, `Offload.summarize`, and `Offload.drop` for fine-grained control.
- **Offload strategies**: Three flavors: `truncate` (keep a preview), `summarize` (keep an LLM summary), `drop` (remove entirely). Each targets specific content and fires under configurable conditions.
- **Context window limits**: Every model has a maximum context size. Without management, long conversations will fail.
- **Proactive compression**: Strategies fire at configurable utilization thresholds rather than waiting for overflow.
- **Cost optimization**: Use a cheaper model for summarization. The summary doesn't need your most capable model.

## Further Reading

- [Strands Agents: Context Management](https://strandsagents.com/docs/user-guide/concepts/context-management/)
- [Hands-on Workshop: Build Your First Agent](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
