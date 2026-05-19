"""
Trajectory Evaluation

Evaluates whether the agent followed the correct sequence of tool calls.
Useful for agents where the process matters as much as the output.
"""

from strands import Agent, tool
from strands_evals import Case, Experiment
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from strands_evals.types import TaskOutput


@tool
def search_database(query: str) -> str:
    """Search the database for information.

    Args:
        query: The search query
    """
    return f"Results for: {query}"


@tool
def format_results(data: str) -> str:
    """Format search results for display.

    Args:
        data: Raw data to format
    """
    return f"Formatted: {data}"


evaluator = TrajectoryEvaluator(
    rubric="""
    The correct workflow is:
    1. search_database must be called first
    2. format_results must be called second

    Score 1.0 if the sequence is correct.
    Score 0.5 if tools are used but in wrong order.
    Score 0.0 if steps are missing.
    """,
    include_inputs=True,
)


def get_response(case: Case) -> TaskOutput:
    agent = Agent(
        tools=[search_database, format_results],
        system_prompt="Always search first, then format the results.",
        callback_handler=None,
    )
    response = agent(case.input)

    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(
        agent.messages
    )
    evaluator.update_trajectory_description(
        tools_use_extractor.extract_tools_description(agent)
    )

    return TaskOutput(output=str(response), trajectory=trajectory)


cases = [
    Case(
        name="search-and-format",
        input="Find information about Python programming",
        expected_trajectory=["search_database", "format_results"],
    ),
]

experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(get_response)
reports[0].run_display()
