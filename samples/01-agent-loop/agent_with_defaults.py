from strands import Agent
from strands.models import BedrockModel
from strands.vended_tools import file_editor, shell
from strands.vended_tools.web_fetch import web_fetch

agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    ),
    # Vended tools for file ops, shell, and web fetching
    tools=[file_editor, shell, web_fetch],
    # Auto context management: offloads large tool results, compresses old
    # messages into summaries, and fires proactive compression at 85% usage.
    context_manager="auto",
)

# Give it a research task
agent("Research the current state of AI agent deployment patterns in production, including common architectures, challenges teams face, and best practices. Write a summary to report.md")
