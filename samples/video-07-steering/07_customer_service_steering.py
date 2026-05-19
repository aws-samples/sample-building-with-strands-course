from strands import Agent, AgentSkills
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
        skills_plugin,              # On-demand workflow instructions
        RefundWorkflowHandler(),    # Deterministic: enforce refund steps
        tone_handler,               # LLM-based: enforce communication quality
    ],
    system_prompt=SYSTEM_PROMPT,
)

print("Customer Service Agent with Steering (type 'quit' to exit)")
print("-" * 55)

while True:
    user_input = input("\nCustomer: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break
    if not user_input:
        continue
    print()
    agent(user_input)
