from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import HelpfulnessEvaluator, GoalSuccessRateEvaluator
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry import StrandsEvalsTelemetry

from create_agent import create_customer_service_agent

# Setup telemetry for trace-based evaluation
telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
memory_exporter = telemetry.in_memory_exporter


def task_function(case: Case) -> dict:
    """Run a multi-turn simulated conversation with the full customer service agent."""

    # Create simulator to drive the conversation
    simulator = ActorSimulator.from_case_for_user_simulator(
        case=case,
        max_turns=8,
    )

    # Create the full customer service agent (tools, steering, skills)
    agent = create_customer_service_agent(
        trace_attributes={
            "gen_ai.conversation.id": case.session_id,
            "session.id": case.session_id,
        },
        callback_handler=None,
    )

    # Run multi-turn conversation
    user_message = case.input

    while simulator.has_next():
        agent_response = agent(user_message)
        user_result = simulator.act(str(agent_response))
        user_message = str(user_result.structured_output.message)

    # Map traces to session for evaluation
    all_spans = memory_exporter.get_finished_spans()
    mapper = StrandsInMemorySessionMapper()
    session = mapper.map_to_session(all_spans, session_id=case.session_id)

    return {"output": str(agent_response), "trajectory": session}


# Define test cases with goals the simulator will try to achieve
test_cases = [
    Case[str, str](
        name="refund-request",
        input="Hi, I need to return a laptop I bought. My customer ID is C-1001.",
        metadata={"task_description": "Customer gets refund processed for their order"},
    ),
    Case[str, str](
        name="order-tracking",
        input="Can you check on my orders? My customer ID is C-1002.",
        metadata={"task_description": "Customer receives order status information"},
    ),
    Case[str, str](
        name="account-issue",
        input="My account seems to be having issues. Customer ID C-1001.",
        metadata={"task_description": "Customer gets account troubleshooting help"},
    ),
]

# Evaluate with multiple evaluators
evaluators = [
    HelpfulnessEvaluator(),
    GoalSuccessRateEvaluator(),
]

experiment = Experiment[str, str](cases=test_cases, evaluators=evaluators)
reports = experiment.run_evaluations(task_function)

print("=== Multi-Turn Simulation Results ===")
for report in reports:
    report.run_display()
