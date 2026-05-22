# Video 12: Swarms

Swarms let agents hand off to each other autonomously — there's no predefined execution order. Each agent decides who to pass control to next based on what it discovers. This video builds an incident debugging system where specialized agents collaborate to diagnose issues.

## Files

- **debugging_swarm.py** — An incident triage system with four agents: triage, log analyst, metrics analyst, and deployment reviewer. Agents share context and build on each other's discoveries.

## Running

```bash
python debugging_swarm.py
```

## Notes

- Swarms are powerful but need safety bounds. Watch for these settings in the code:
  - `max_handoffs` — limits how many times agents can pass control
  - `max_iterations` — caps total agent turns
  - `execution_timeout` — hard time limit
- Agents share context across handoffs, so each one builds on what previous agents found.
- Compare this to graphs (Video 11) — swarms are better when you don't know the right order upfront.
