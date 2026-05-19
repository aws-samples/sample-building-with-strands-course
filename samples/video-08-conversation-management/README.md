# Video 8: Conversation Management

As conversations grow, they can overflow the model's context window. This video covers strategies for managing conversation history: dropping old messages (sliding window), summarizing them, or using a cheaper model for summarization to save costs.

## Files

- **sliding_window_simple.py** — Keeps the N most recent messages and drops the oldest. Simplest approach — fast but loses context.
- **summarizing_simple.py** — Summarizes old messages instead of dropping them. Preserves key information while reducing token count.
- **custom_summarizer.py** — Uses a cheaper model (Haiku) for the summarization step to reduce costs.
- **customer_service_tools.py** — Mock tools shared across examples.
- **steering_handlers.py** — Steering handlers shared across examples.
- **skills/** — Skill definitions for the customer service agent.

## Running

```bash
python sliding_window_simple.py
python summarizing_simple.py
python custom_summarizer.py
```

Have a long conversation and watch how each strategy handles the growing history differently.

## Notes

- Sliding window is best when old context doesn't matter (e.g., simple Q&A).
- Summarization is better when you need to retain facts from earlier in the conversation.
- Using a cheaper model for summarization is a good cost optimization — the summary doesn't need the most capable model.
