"""
Demonstrates mixing multi-agent patterns:

Pattern 1: A Swarm used as a node inside a Graph
Pattern 2: An Agent used as a tool inside a Graph node

Graph structure:
  [investigation_swarm] → [report_writer (calls editor_agent as a tool)]
"""

from strands import Agent, tool
from strands.multiagent.swarm import Swarm
from strands.multiagent.graph import GraphBuilder


# ============================================================
# Tools for the swarm
# ============================================================
@tool
def search_logs(query: str) -> str:
    """Search application logs for relevant entries.

    Args:
        query: Search term to look for in logs.
    """
    return f"[LOG] Found entries matching '{query}': connection timeout at 14:32, pool exhausted at 14:33, retry failed at 14:34"


@tool
def check_metrics(service: str) -> str:
    """Check monitoring metrics for a service.

    Args:
        service: Name of the service to check metrics for.
    """
    return f"[METRICS] {service}: CPU 45%, Memory 78%, Connection Pool 100% (exhausted), Error Rate 25%"


# ============================================================
# PATTERN 1: Swarm as a Graph node
#
# These agents hand off to each other autonomously.
# The swarm itself becomes a single node in the graph.
# ============================================================
log_agent = Agent(
    name="log-analyst",
    system_prompt="You analyze application logs. If you find infrastructure issues, hand off to metrics-analyst. Be concise.",
    tools=[search_logs],
)

metrics_agent = Agent(
    name="metrics-analyst",
    system_prompt="You analyze system metrics and identify root causes. Summarize your findings concisely. Do not hand off.",
    tools=[check_metrics],
)

investigation_swarm = Swarm(
    nodes=[log_agent, metrics_agent],
    entry_point=log_agent,
    max_handoffs=3,
    max_iterations=5,
)


# ============================================================
# PATTERN 2: Agent as a tool inside a Graph node
#
# The report_writer is a graph node. It calls editor_agent
# as a tool to get help formatting its output.
# ============================================================
editor_agent = Agent(
    name="editor",
    system_prompt="You are a technical editor. Take raw findings and rewrite them as a clear, professional incident report with sections: Summary, Root Cause, and Recommended Actions. Be concise.",
    callback_handler=None,
)

report_writer = Agent(
    name="report-writer",
    system_prompt="You write incident reports. Use the editor tool to format your findings into a professional report.",
    tools=[editor_agent.as_tool(name="editor", description="Format raw findings into a professional incident report")],
)


# ============================================================
# Graph: Swarm node → Agent-as-tool node
# ============================================================
graph = GraphBuilder()
graph.add_node(investigation_swarm, "investigate")  # Pattern 1: swarm is a node
graph.add_node(report_writer, "write_report")       # Pattern 2: uses agent-as-tool
graph.add_edge("investigate", "write_report")
graph.set_entry_point("investigate")
workflow = graph.build()


# ============================================================
# Run
# ============================================================
print("=" * 60)
print("MIXED PATTERNS:")
print("  Node 1: Swarm (agents hand off internally)")
print("  Node 2: Agent that calls another agent as a tool")
print("=" * 60 + "\n")

result = workflow("The payment service is returning 500 errors for 25% of requests. Started 30 minutes ago.")

print("\n" + "=" * 60)
print(f"Status: {result.status}")
print(f"Execution order: {result.execution_order}")
print("=" * 60)
