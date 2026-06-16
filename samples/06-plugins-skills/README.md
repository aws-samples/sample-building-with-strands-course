# Plugins and Skills

Plugins and skills are two composition patterns that help manage agent complexity as your system grows.

**Plugins** bundle tools, hooks, and initialization logic into reusable packages. Instead of manually wiring up multiple related components, you install a plugin and it handles the setup.

**Skills** provide progressive disclosure for instructions. Rather than stuffing every possible instruction into the system prompt upfront (which wastes context and confuses the model), skills are loaded on demand when the agent encounters a relevant request.

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

## Key Concepts

- **Prompt bloat**: Loading all instructions into the system prompt wastes tokens, dilutes attention, and increases cost. Skills solve this.
- **On-demand loading**: The agent discovers available skills and loads only the one it needs for the current request.
- **Skill format**: Each skill is a markdown file (`SKILL.md`) in its own directory. The agent reads the directory listing to discover skills, then loads the relevant one.
- **Plugin interface**: Plugins implement lifecycle hooks and tool registration in a single class — install once, get the full behavior.

## Further Reading

- [Hands-on Workshop: Module 3 (Skills + Steering)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/03-skills-steering)
