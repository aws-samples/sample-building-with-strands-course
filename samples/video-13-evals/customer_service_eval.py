"""
Customer Service Steering Evaluation

Evaluates the customer service agent with steering handlers:
- Refund workflow enforcement (lookup_customer → get_order_history → process_refund)
- Tone and professionalism of responses
- Correct tool usage for different customer scenarios
"""

from strands import Agent, AgentSkills
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator, TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from strands_evals.types import TaskOutput

from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, ToneGuardrailHandler

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests. When a customer needs help, activate the appropriate
skill for step-by-step guidance.

Important guidelines:
- Always ask for the customer ID first if you don't have it.
- Use the data returned by tools to answer questions. Do not ask the customer for
  information that is already available in the tool results.
- Never show internal IDs, system formats, or example data to the customer.
- Be warm but efficient. Customers want their problem solved, not a long conversation.
- When a customer explicitly confirms they want a refund processed, proceed without
  asking for additional confirmation."""

def create_agent():
    """Create a fresh customer service agent for each test case."""
    return Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[
            AgentSkills(skills=["./skills"]),
            RefundWorkflowHandler(),
            ToneGuardrailHandler(),
        ],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )


# --- Trajectory evaluator: checks tool call ordering ---

trajectory_evaluator = TrajectoryEvaluator(
    rubric="""
    Evaluate the agent's tool usage sequence for customer service workflows.

    For refund requests, the correct workflow is:
    1. lookup_customer must be called first to verify the customer
    2. get_order_history must be called to find the relevant order
    3. process_refund is called last with the correct order and amount

    For order status or account inquiries:
    1. lookup_customer must be called first
    2. get_order_history is called if order info is needed

    If the expected trajectory is empty (no tools expected), score 1.0 if no tools
    were called — the agent correctly asked for more information instead of guessing.

    IMPORTANT: The agent has a skills plugin that provides workflow guidance. Calls to
    the `skills` tool (to load skill documents like refund-processing or order-tracking)
    are acceptable and should NOT be penalized. Ignore `skills` tool calls when comparing
    against the expected trajectory — they are supplementary context lookups, not workflow steps.

    Score 1.0 if the core workflow sequence matches the expected trajectory (ignoring skills calls).
    Score 0.5 if core tools are used but in wrong order or critical parameters are wrong.
    Score 0.0 if critical expected steps are missing or completely wrong tools are used.
    """,
    include_inputs=True,
)

# --- Output evaluator: checks response quality and tone ---

output_evaluator = OutputEvaluator(
    rubric="""
    Evaluate the customer service agent's response quality:

    Score 1.0 if ALL of the following are true:
    - Response is professional and empathetic
    - Response directly addresses the customer's concern
    - No internal IDs, system jargon, or technical details are exposed
    - Response is concise and actionable
    - Does not overpromise or guarantee timelines beyond what tools confirm

    Score 0.5 if the response is mostly good but:
    - Slightly too verbose or includes unnecessary filler
    - Minor tone issues (too formal, too casual)
    - Partially addresses the concern

    Score 0.0 if:
    - Response is rude, dismissive, or blames the customer
    - Exposes internal system details
    - Completely fails to address the customer's issue
    - Makes up information not returned by tools
    """,
)


def get_response(case: Case) -> TaskOutput:
    """Run the agent and capture both output and tool trajectory."""
    agent = create_agent()
    response = agent(case.input)

    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(
        agent.messages
    )
    trajectory_evaluator.update_trajectory_description(
        tools_use_extractor.extract_tools_description(agent)
    )

    return TaskOutput(output=str(response), trajectory=trajectory)


# --- Test cases ---

cases = [
    # Refund workflow: should follow lookup → orders → refund
    Case(
        name="refund-full-workflow",
        input="Hi, I'm customer C-1001. I'd like a refund for my wireless headphones order ORD-5521. Yes, I confirm — please process the refund now.",
        expected_output="Refund processed for the wireless headphones order, with 3-5 business day timeline.",
        expected_trajectory=["lookup_customer", "get_order_history", "process_refund"],
    ),
    # Order status inquiry: should lookup customer then check orders
    Case(
        name="order-status-check",
        input="I'm customer C-1001. Where is my USB-C Hub order?",
        expected_output="The USB-C Hub is shipped with an estimated delivery date and tracking info.",
        expected_trajectory=["lookup_customer", "get_order_history"],
    ),
    # Delayed order: should show empathy and provide tracking info
    Case(
        name="delayed-order-frustration",
        input="This is customer C-1002. My keyboard order is delayed and I'm really frustrated!",
        expected_output="Acknowledge frustration, provide order status and tracking details for the delayed keyboard.",
        expected_trajectory=["lookup_customer", "get_order_history"],
    ),
    # Customer lookup only: basic account inquiry
    Case(
        name="account-info",
        input="Can you look up my account? I'm C-1001.",
        expected_output="Provide the customer's account information without exposing internal IDs.",
        expected_trajectory=["lookup_customer"],
    ),
    # No customer ID provided: agent should ask for it
    Case(
        name="missing-customer-id",
        input="I want to return something I bought last week.",
        expected_output="Agent asks for the customer ID before proceeding.",
        expected_trajectory=[],
    ),
]


if __name__ == "__main__":
    experiment = Experiment(
        cases=cases,
        evaluators=[trajectory_evaluator, output_evaluator],
    )
    reports = experiment.run_evaluations(get_response)
    reports[0].run_display()
