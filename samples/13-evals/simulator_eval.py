"""
Multi-turn simulation evaluation.
Demonstrates: ActorSimulator for generating realistic multi-turn conversations
and evaluating agent behavior over time.

Uses the same customer service agent from Videos 6-9 with tools, skills, and steering.
"""

from strands import Agent, AgentSkills
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import HelpfulnessEvaluator, GoalSuccessRateEvaluator
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry import StrandsEvalsTelemetry

# Import the customer service tools and steering from our existing code
import sys
sys.path.insert(0, "../07-steering")
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

# Setup telemetry for trace-based evaluation
telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
memory_exporter = telemetry.in_memory_exporter

skills_plugin = AgentSkills(skills=["../07-steering/skills"])


def task_function(case: Case) -> dict:
    """Run a multi-turn simulated conversation with the full customer service agent."""

    # Create simulator to drive the conversation
    simulator = ActorSimulator.from_case_for_user_simulator(
        case=case,
        max_turns=8,
    )

    # Create the full customer service agent with steering and skills
    agent = Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[
            skills_plugin,
            RefundWorkflowHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
        conversation_manager=SlidingWindowConversationManager(window_size=20),
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
        input="Hi, I bought a laptop last week and it arrived with a cracked screen. I need a refund.",
        metadata={"task_description": "Customer gets refund processed for damaged item"},
    ),
    Case[str, str](
        name="order-tracking",
        input="Where is my order? I placed it 3 days ago and haven't received any shipping updates.",
        metadata={"task_description": "Customer receives tracking information or status update"},
    ),
    Case[str, str](
        name="product-question",
        input="I'm looking at the new wireless headphones on your site. Do they work with Android?",
        metadata={"task_description": "Customer gets accurate product compatibility information"},
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
