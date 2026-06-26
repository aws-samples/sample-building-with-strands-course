"""
Agent Workflows: Structured Multi-Agent Coordination

Workflows provide explicit control over task execution order, dependencies, and
information flow. Each agent performs a specialized function in a defined sequence,
with outputs flowing automatically to the next step.

Two approaches:
  1. Manual sequential workflow — you control the pipeline in Python
  2. Built-in workflow tool — handles task creation, dependency resolution,
     parallel execution, and state management automatically
"""

from strands import Agent
from strands_tools import workflow


# =============================================================================
# APPROACH 1: Manual Sequential Workflow
#
# Simple and explicit. Each agent's output becomes the next agent's input.
# You control the flow in Python — no magic.
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
    """Run a sequential research → analysis → report pipeline."""

    # Step 1: Research
    research_results = researcher(f"Research the latest developments in {topic}")

    # Step 2: Analysis (receives research output)
    analysis = analyst(f"Analyze these research findings: {research_results}")

    # Step 3: Report writing (receives analysis output)
    final_report = writer(f"Create a brief report based on this analysis: {analysis}")

    return str(final_report)


# =============================================================================
# APPROACH 2: Built-in Workflow Tool
#
# The workflow tool handles dependency resolution, parallel execution,
# and state management. Define tasks with dependencies and let it run.
# =============================================================================

orchestrator = Agent(tools=[workflow])


def tool_based_workflow():
    """Use the built-in workflow tool for structured multi-step processing."""

    # Create a workflow with tasks and dependencies
    orchestrator.tool.workflow(
        action="create",
        workflow_id="content_pipeline",
        tasks=[
            {
                "task_id": "research",
                "description": "Research the current state of AI agent deployment patterns",
                "system_prompt": "You are a research specialist. Find key facts and cite sources.",
                "priority": 5,
            },
            {
                "task_id": "competitive_analysis",
                "description": "Analyze how different agent frameworks compare",
                "system_prompt": "You compare technologies objectively with pros and cons.",
                "priority": 5,
            },
            {
                "task_id": "synthesis",
                "description": "Synthesize research and competitive analysis into recommendations",
                "dependencies": ["research", "competitive_analysis"],
                "system_prompt": "You synthesize multiple inputs into clear recommendations.",
                "priority": 3,
            },
            {
                "task_id": "report",
                "description": "Write a final report with executive summary and details",
                "dependencies": ["synthesis"],
                "system_prompt": "You write clear, actionable technical reports.",
                "priority": 1,
            },
        ],
    )

    # Execute — research and competitive_analysis run in parallel,
    # synthesis waits for both, report waits for synthesis
    orchestrator.tool.workflow(action="start", workflow_id="content_pipeline")

    # Check status
    status = orchestrator.tool.workflow(action="status", workflow_id="content_pipeline")
    return status


# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENTIAL WORKFLOW: Research → Analysis → Report")
    print("=" * 60 + "\n")

    result = sequential_workflow("AI agent deployment in production")
    print(f"\n{'=' * 60}")
    print("Final report generated.")
