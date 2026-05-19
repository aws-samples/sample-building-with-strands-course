from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SummarizingConversationManager

# Use a cheaper model for summarization
summarizer = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-haiku-4-20250514-v1:0",
    )
)

agent = Agent(
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.4,
        preserve_recent_messages=8,
        summarization_agent=summarizer,
    )
)

agent("Start a deep discussion about microservices architecture...")
