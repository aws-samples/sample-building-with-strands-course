"""
Agent Workflows: Structured Multi-Agent Coordination

Workflows provide explicit control over task execution order, dependencies, and
information flow. Each agent performs a specialized function in a defined sequence,
with outputs flowing automatically to the next step.

For more complex coordination with parallel execution and dependency resolution,
see basic_graph.py which uses GraphBuilder.
"""

from strands import Agent


# =============================================================================
# Manual Sequential Workflow
#
# Simple and explicit. Each agent's output becomes the next agent's input.
# You control the flow in Python, no magic.
# =============================================================================

researcher = Agent(
    system_prompt="You are a research specialist. Find key information and cite sources.",
    callback_handler=None,
)

analyst = Agent(
    system_prompt="You analyze research data and extract actionable insights.",
    callback_handler=None,
)

writer = Agent(
    system_prompt="You create polished, concise reports based on analysis.",
)


def sequential_workflow(topic: str) -> str:
    """Run a sequential research -> analysis -> report pipeline."""

    # Step 1: Research
    research_results = researcher(f"Research the latest developments in {topic}")

    # Step 2: Analysis (receives research output)
    analysis = analyst(f"Analyze these research findings: {research_results}")

    # Step 3: Report writing (receives analysis output)
    final_report = writer(f"Create a brief report based on this analysis: {analysis}")

    return str(final_report)


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENTIAL WORKFLOW: Research -> Analysis -> Report")
    print("=" * 60 + "\n")

    result = sequential_workflow("AI agent deployment in production")
    print(f"\n{'=' * 60}")
    print("Final report generated.")
