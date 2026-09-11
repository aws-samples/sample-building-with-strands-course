"""
Context Strategy: Truncate (Drop Oldest)

The simplest approach to context management: when the context window fills up,
remove the oldest messages. Fast, predictable, and where most agents start.

This uses the new ContextManager with an Offload.truncate strategy that removes
old messages when utilization hits the threshold, keeping the most recent ones.
"""

from strands import Agent, AgentSkills
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

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[
        skills_plugin,
        RefundWorkflowHandler(),
        tone_handler,
    ],
    system_prompt=SYSTEM_PROMPT,
    # Truncate strategy: when context hits 90% full, remove the oldest messages
    # while preserving the 10 most recent. Large tool results (>2500 tokens)
    # are truncated to a preview immediately.
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.truncate("*").when(utilization=0.9, preserve_recent=10),
        ],
    ),
)

print("Customer Service Agent with Truncate Strategy (type 'quit' to exit)")
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
