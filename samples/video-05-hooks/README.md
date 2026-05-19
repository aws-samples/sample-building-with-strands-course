# Video 5: Hooks

Hooks are middleware for the agent lifecycle — they let you inject deterministic code at key decision points (before/after tool calls, before/after the agent loop). This video shows two practical patterns: human-in-the-loop approval and rate limiting.

## Files

- **approval_interrupt.py** — Human-in-the-loop approval before file deletion. Uses `event.interrupt()` to pause execution and ask the user for confirmation.
- **rate_limiter.py** — Prevents any tool from being called more than 3 times per request. Demonstrates how hooks can enforce safety guardrails.

## Running

```bash
python approval_interrupt.py
python rate_limiter.py
```

## Notes

- The approval example will prompt you in the terminal — try both approving and denying to see the different paths.
- Rate limiting is per-request, not global. Each new agent invocation resets the counter.
