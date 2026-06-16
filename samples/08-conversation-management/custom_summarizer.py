from strands import Agent, AgentSkills
from strands.models import BedrockModel
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.vended_plugins.context_offloader import ContextOffloader, FileStorage
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests. When a customer needs help, activate the appropriate
skill for step-by-step guidance.

Important guidelines:
- Always ask for the customer ID first if you don't have it.
- Use the data returned by tools to answer questions. Do not ask the customer for
  information that is already available in the tool results.
- Never show internal IDs, system formats, or example data to the customer.
- Be warm but efficient. Customers want their problem solved, not a long conversation."""

skills_plugin = AgentSkills(skills=["./skills"])

# Use a cheaper model for summarization with a custom prompt
# that focuses on what matters for customer service conversations
SUMMARIZATION_PROMPT = """Summarize the following customer service conversation.
Focus on:
- Customer identity (name, ID, account status)
- The issue or request they came in with
- Actions already taken (tools called, information retrieved)
- Any unresolved problems or pending next steps
"""

summarizer = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-haiku-4-20250514-v1:0",
    ),
    system_prompt=SUMMARIZATION_PROMPT,
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[
        skills_plugin,
        RefundWorkflowHandler(),
        tone_handler,
        ContextOffloader(
            storage=FileStorage("./offloaded"),
            max_result_tokens=8_000,
            preview_tokens=2_000,
        ),
    ],
    system_prompt=SYSTEM_PROMPT,
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.4,
        preserve_recent_messages=8,
        summarization_agent=summarizer,
        proactive_compression={
            "compression_threshold": 0.9,
        },
    ),
)

print("Customer Service Agent with Custom Summarizer (type 'quit' to exit)")
print("-" * 60)

while True:
    user_input = input("\nCustomer: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break
    if not user_input:
        continue
    print()
    agent(user_input)
    print(f"\n[DEBUG] Messages in context: {len(agent.messages)}")
