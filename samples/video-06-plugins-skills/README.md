# Video 6: Plugins & Skills

This video introduces two composition patterns. Plugins modify agent behavior by bundling tools, hooks, and initialization logic together. Skills provide progressive disclosure — instructions are loaded on demand when the agent needs them, rather than stuffing everything into the system prompt upfront.

## Files

- **customer_service.py** — A customer service agent that uses the built-in `AgentSkills` plugin to load skills on demand.
- **skills/** — Directory containing skill definitions:
  - `refund-processing/SKILL.md` — Instructions for handling refund requests
  - `order-tracking/SKILL.md` — Instructions for tracking orders
  - `account-troubleshooting/SKILL.md` — Instructions for resolving account issues

## Running

```bash
python customer_service.py
```

Then try asking things like:
- "I want a refund for order #12345"
- "Where is my package?"
- "I can't log into my account"

## Notes

- Skills are just markdown files in a directory — the agent discovers and loads them as needed.
- Watch how the agent only loads the relevant skill for each request instead of having all instructions in context at once.
