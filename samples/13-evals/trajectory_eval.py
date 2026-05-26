"""
Trajectory evaluation — validates the agent followed the correct workflow.
Demonstrates: TrajectoryEvaluator, tools_use_extractor, expected tool sequences.
"""

from strands import Agent, tool
from strands_evals import Case, Experiment
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor


@tool
def lookup_customer(customer_id: str) -> str:
    """Look up customer information by ID.

    Args:
        customer_id: The customer's unique identifier.
    """
    return f"Customer {customer_id}: Sarah Johnson, email: sarah@example.com, status: active"


@tool
def get_order_history(customer_id: str) -> str:
    """Get order history for a customer.

    Args:
        customer_id: The customer's unique identifier.
    """
    return f"Orders for {customer_id}: ORD-001 ($89.99, delivered), ORD-002 ($149.99, shipped)"


@tool
def process_refund(order_id: str, amount: float) -> str:
    """Process a refund for an order.

    Args:
        order_id: The order to refund.
        amount: The refund amount in dollars.
    """
    return f"Refund of ${amount:.2f} processed for {order_id}. Confirmation: REF-12345"


def get_response_with_tools(case: Case) -> dict:
    """Run agent and capture tool trajectory."""
    agent = Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        system_prompt="""You are a customer service agent. When processing refunds, you MUST:
1. First look up the customer
2. Then check their order history
3. Only then process the refund
Always follow this exact order.""",
        callback_handler=None,
    )

    response = agent(case.input)

    # Extract the tool call trajectory
    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)

    return {"output": str(response), "trajectory": trajectory}


# Define cases with expected tool sequences
test_cases = [
    Case[str, str](
        name="refund-workflow",
        input="Customer C-1001 wants a refund for order ORD-001 ($89.99).",
        expected_trajectory=["lookup_customer", "get_order_history", "process_refund"],
        metadata={"category": "workflow_compliance"},
    ),
    Case[str, str](
        name="info-lookup-only",
        input="Can you look up customer C-1001 and tell me their order history?",
        expected_trajectory=["lookup_customer", "get_order_history"],
        metadata={"category": "workflow_compliance"},
    ),
]

# Create trajectory evaluator
evaluator = TrajectoryEvaluator(
    rubric="""
    Evaluate whether the agent followed the expected tool sequence:
    - Use in_order_match: the expected tools should appear in order,
      but extra tools in between are acceptable.
    - Score 1.0 if the expected sequence is followed correctly.
    - Score 0.5 if tools are called but in wrong order.
    - Score 0.0 if expected tools are missing entirely.
    """,
    include_inputs=True,
)

# Give evaluator context about available tools
sample_agent = Agent(tools=[lookup_customer, get_order_history, process_refund])
tool_descriptions = tools_use_extractor.extract_tools_description(sample_agent, is_short=True)
evaluator.update_trajectory_description(tool_descriptions)

# Run experiment
experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
reports = experiment.run_evaluations(get_response_with_tools)

print("=== Trajectory Evaluation Results ===")
reports[0].run_display()
