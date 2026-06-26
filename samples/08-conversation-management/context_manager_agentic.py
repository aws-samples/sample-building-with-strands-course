"""
Context Manager: Agentic Mode

For agents where the model is better positioned to decide what stays in context.
The model gets tools to summarize, truncate, or pin messages. It trades tokens
for judgment.

Use "agentic" when your agent needs to protect specific context across long
conversations — for example, a coding agent that must remember architectural
decisions made earlier even as the conversation grows.

Start with "auto" by default. Use "agentic" when you need the model to make
contextual decisions about what's important to retain.
"""

from strands import Agent
from strands_tools import file_read, file_write, editor, shell, http_request

# The model gets context management tools and decides what to keep,
# summarize, or drop based on relevance to the current task.
agent = Agent(
    tools=[file_read, file_write, editor, shell, http_request],
    context_manager="agentic",
    system_prompt="""You are a senior software architect assistant.
You help with long-running design discussions where early decisions
inform later choices. Protect architectural context across the conversation.""",
)

# Long conversation where early context matters
agent("Let's design a payment processing system. Start with the high-level architecture.")
