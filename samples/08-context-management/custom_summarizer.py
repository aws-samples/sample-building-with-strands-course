"""
Context Strategy: Summarize with a Cheaper Model

Summarizing history doesn't require your most capable model. You can pass a
cheaper one via the SummarizeConfig to reduce costs. The main agent keeps using
whatever model you configured; only the summarization LLM call uses the cheaper one.
"""

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from strands.experimental.context_manager import ContextManager, Offload
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

# Use a cheaper model for the summarization calls
summarizer_model = BedrockModel(
    model_id="us.anthropic.claude-haiku-4-20250514-v1:0",
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[
        skills_plugin,
        RefundWorkflowHandler(),
        tone_handler,
    ],
    system_prompt=SYSTEM_PROMPT,
    # Custom summarization: use a cheaper model with a domain-specific prompt.
    # The main agent still uses the default model for reasoning.
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.summarize(
                "*",
                {
                    "model": summarizer_model,
                    "system_prompt": (
                        "Summarize the following customer service conversation. "
                        "Focus on: customer identity (name, ID, account status), "
                        "the issue or request, actions already taken, and any "
                        "unresolved problems or pending next steps."
                    ),
                },
            ).when(utilization=0.85, preserve_recent=8),
        ],
        stash=False,
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
