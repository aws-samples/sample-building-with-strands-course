from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.vended_plugins.context_offloader import ContextOffloader, FileStorage
from strands_tools import file_read, file_write, editor, shell, http_request, use_agent

agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    ),
    # Built-in tools for file ops, shell, web, and subagent delegation
    tools=[file_read, file_write, editor, shell, http_request, use_agent],
    # Proactive compression — summarizes context before hitting the limit
    conversation_manager=SummarizingConversationManager(
        proactive_compression={"compression_threshold": 0.9},
    ),
    # Offloads large tool results externally, keeps a preview in context
    plugins=[
        ContextOffloader(
            storage=FileStorage("./offloaded"),
            max_result_tokens=8_000,
            preview_tokens=2_000,
        ),
    ],
)

# Give it a research task
agent("Research the current state of AI agent deployment patterns in production, including common architectures, challenges teams face, and best practices. Write a summary to report.md")
