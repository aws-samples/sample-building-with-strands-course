from strands import Agent, AgentSkills
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.session.file_session_manager import FileSessionManager
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

session_manager = FileSessionManager(
    session_id="customer-session-001",
    storage_dir="./sessions",
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    system_prompt=SYSTEM_PROMPT,
    conversation_manager=SlidingWindowConversationManager(window_size=20),
    session_manager=session_manager,
)

print("Customer Service Agent with Persistence (type 'quit' to exit)")
print("-" * 60)
print(f"Session: {session_manager.session_id}")
print(f"Restored messages: {len(agent.messages)}")

while True:
    user_input = input("\nCustomer: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break
    if not user_input:
        continue
    print()
    agent(user_input)
