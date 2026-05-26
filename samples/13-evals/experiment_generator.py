"""
Automated experiment generation — bootstrap test cases from tool descriptions.
Demonstrates: ExperimentGenerator for creating evaluation suites automatically.
"""

import asyncio
from strands_evals.generators import ExperimentGenerator
from strands_evals.evaluators import TrajectoryEvaluator


# Define what your agent can do
tool_context = """
Available tools:
- lookup_customer(customer_id: str) -> str: Look up customer information by ID
- get_order_history(customer_id: str) -> str: Get order history for a customer
- process_refund(order_id: str, amount: float) -> str: Process a refund for an order

The agent is a customer service assistant for an online electronics store.
It helps customers with order inquiries, refunds, and account questions.
"""


async def generate_experiment():
    generator = ExperimentGenerator[str, str](str, str)

    experiment = await generator.from_context_async(
        context=tool_context,
        num_cases=5,
        evaluator=TrajectoryEvaluator,
        task_description="Customer service agent handling order and refund requests",
        num_topics=3,
    )

    # Save generated experiment for review
    experiment.to_file("generated_customer_service_eval")
    print("Generated experiment saved!")
    print(f"Cases generated: {len(experiment.cases)}")

    for case in experiment.cases:
        print(f"  - {case.name}: {case.input[:60]}...")

    return experiment


if __name__ == "__main__":
    asyncio.run(generate_experiment())
