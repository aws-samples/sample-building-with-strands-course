# Conversation Management

As conversations grow, they can overflow the model's context window. Conversation managers control what happens when messages accumulate — you can drop old messages, summarize them, or use a cheaper model for the summarization to save costs.

Proactive compression triggers summarization before you hit the limit, so the agent never fails due to context overflow.

## Files

- **sliding_window.py** — Keeps the N most recent messages and drops the oldest. Simplest approach — fast but loses context.
- **summarizing.py** — Summarizes old messages instead of dropping them. Preserves key information while reducing token count. Includes proactive compression.
- **custom_summarizer.py** — Uses a cheaper model (Haiku) for the summarization step to reduce costs. Also includes proactive compression and `ContextOffloader`.
- **customer_service_tools.py** — Mock tools shared across examples.
- **steering_handlers.py** — Steering handlers shared across examples.
- **skills/** — Skill definitions for the customer service agent.

## Running

```bash
python sliding_window.py
python summarizing.py
python custom_summarizer.py
```

Have a long conversation and watch how each strategy handles the growing history differently.

## Key Concepts

- **Context window limits**: Every model has a maximum context size. Without management, long conversations will fail.
- **Sliding window**: Drop the oldest N messages. Fast and simple, but you lose information permanently. Best when old context doesn't matter.
- **Summarization**: Compress old messages into a summary. Preserves key facts while reducing token count. Better when earlier context still matters.
- **Proactive compression**: Trigger summarization at a configurable threshold (e.g., 90% of context used) rather than waiting for overflow.
- **Cost optimization**: Use a cheaper model for summarization — the summary doesn't need your most capable model.
- **Context offloading**: The `ContextOffloader` plugin externalizes large tool results to storage, keeping only a preview in context.

## Further Reading

- [Hands-on Workshop: Build Your First Agent](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
