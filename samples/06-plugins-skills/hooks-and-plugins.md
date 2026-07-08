# Hooks and Plugins

Hooks inject deterministic logic into the agent lifecycle. They're middleware for agents like approval gates, rate limits, validation, and audit logging.

## Hook Architecture

- Subclass `HookProvider` to define hooks
- Register callbacks for lifecycle events in `register_hooks()`
- Multiple hooks can listen to the same event (stackable)
- `event.interrupt()` pauses the loop for human input
- `event.cancel_tool()` blocks tool execution with a message

## Example: Human Approval for Deletions

```python
from strands import Agent, tool
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry

class DeleteApprovalHook(HookProvider):
    """Intercepts delete operations for human approval."""

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.check_delete)

    def check_delete(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] != "delete_file":
            return

        approval = event.interrupt(
            "delete-approval",
            reason={"path": event.tool_use["input"]["path"]}
        )

        if approval.lower() != "y":
            event.cancel_tool = "User denied file deletion"

agent = Agent(
    tools=[list_files, read_file, write_file, delete_file],
    hooks=[DeleteApprovalHook()],
)

```

📂 [approval_interrupt.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/05-hooks/approval_interrupt.py) — Find all code on GitHub

## Example: Rate Limiting Tool Calls

```python
from strands.hooks import BeforeInvocationEvent, BeforeToolCallEvent, HookProvider, HookRegistry

class LimitToolCounts(HookProvider):
    def __init__(self, max_calls: int = 3):
        self.max_calls = max_calls
        self.counts: dict[str, int] = {}

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.reset)
        registry.add_callback(BeforeToolCallEvent, self.check)

    def reset(self, event: BeforeInvocationEvent) -> None:
        self.counts = {}

    def check(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use["name"]
        self.counts[name] = self.counts.get(name, 0) + 1
        if self.counts[name] > self.max_calls:
            event.cancel_tool = (
                f"'{name}' hit the {self.max_calls}-call limit. "
                "Do NOT call this tool again."
            )

agent = Agent(tools=[get_weather], hooks=[LimitToolCounts(max_calls=3)])

```

📂 [rate_limiter.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/05-hooks/rate_limiter.py) — Find all code on GitHub

# Plugins

**Plugins** are the extension mechanism in Strands. They let you package hooks, tools, and custom logic into reusable components that snap into any agent. Skills are one type of plugin that provides on-demand workflow instructions.

## Skills

As agents grow, system prompts bloat with irrelevant instructions. Skills solve this through **progressive disclosure** which is a technique where the agent only sees skill names at startup and loads full instructions on demand.

Each skill is a markdown file in a subfolder containing guidance for a specific task. The agent loads skill instructions only when it needs them. This is one example of context engineering.

```python
from strands import Agent, AgentSkills, tool

# Tools for customer service operations
@tool
def lookup_customer(customer_id: str) -> str:
    """Look up a customer by their ID."""
    # ... database/API call ...

@tool
def get_order_history(customer_id: str) -> str:
    """Get order history for a customer."""
    # ...

@tool
def process_refund(order_id: str, amount: float) -> str:
    """Process a refund for an order."""
    # ...

# Skills plugin discovers and registers all skills in the directory
skills_plugin = AgentSkills(skills=["./skills"])

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[skills_plugin],
    system_prompt="""You are a customer service agent. When a customer needs help,
    activate the appropriate skill for step-by-step guidance."""
)

```

📂 [customer_service.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/06-plugins-skills/customer_service.py) — Find all code on GitHub

## Plugins: The Broader Pattern

Plugins modify or extend agent behavior by packaging multiple primitives together. Skills is one built-in plugin; you can build plugins for memory, orchestration, observability, governance, or custom workflows.

## Goal Loop

Alongside opinionated defaults and out of the box components, Strands has a plugin called goal loop. You would use this when your agent's response needs to meet a quality bar before returning, and GoalLoop handles the retry loop. It validates the response after each invocation, feeds feedback back as a user message on failure, and re-invokes the agent. This continues until validation passes, a max attempt count is reached, or a timeout elapses.

## How It Works

1. The agent processes the prompt and produces a response.
2. GoalLoop extracts the last assistant message and runs the validator.
3. If the validator passes, the loop terminates with a "satisfied" result.
4. If the validator fails and budget remains, GoalLoop injects feedback as a new user message and re-invokes the agent.
5. If the attempt limit or timeout is exhausted, the loop terminates without retrying.

```python
from strands import Agent
from strands.vended_plugins.goal import GoalLoop

concise = GoalLoop(
    goal="At most 3 sentences, accessible to a 10-year-old, "
         "no jargon.",
    max_attempts=3,
)

agent = Agent(plugins=[concise])
result = agent("Explain how rainbows form.")

print(concise.last_result(agent))
# Typical output:
# GoalResult(passed=True, stop_reason='satisfied', attempts=[...])

```

## Resources

- 📖 [Hooks Docs](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/)
- 📖 [Plugins Docs](https://strandsagents.com/docs/user-guide/concepts/plugins/)
- 📖 [Skills Docs](https://strandsagents.com/docs/user-guide/concepts/plugins/skills/)
- 📖 [Goal Loop Docs](https://strandsagents.com/docs/user-guide/concepts/plugins/goal-loop/)

