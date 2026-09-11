"""
Context Strategy: Summarize

Instead of dropping old messages, compress them into LLM-generated summaries.
Preserves more information than truncation but introduces compression risk
since summaries are lossy.

This uses the new ContextManager with an Offload.summarize strategy that
replaces old messages with summaries when utilization hits the threshold.
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
    # Summarize strategy: truncate large tool results immediately, then
    # summarize the oldest messages when context hits 85% full.
    # preserve_recent=10 keeps the last 10 messages untouched.
    context_manager=ContextManager(
        strategies=[
            Offload.truncate("tool_results").when(threshold=2500),
            Offload.summarize("*").when(utilization=0.85, preserve_recent=10),
        ],
    ),
)

print("Customer Service Agent with Summarization (type 'quit' to exit)")
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
