from strands import Agent
from strands.multiagent import GraphBuilder
from strands_tools import http_request

researcher = Agent(
    name="researcher",
    system_prompt="You are a research specialist. Gather comprehensive information from the web.",
    tools=[http_request],
)

analyst = Agent(
    name="analyst",
    system_prompt="You are a data analyst. Identify patterns, trends, and key insights from the research provided.",
)

summarizer = Agent(
    name="summarizer",
    system_prompt="You are a summarizer. Condense raw research into concise key points and takeaways.",
)

report_writer = Agent(
    name="report_writer",
    system_prompt="You synthesize analysis and summaries into a clear, well-structured final report.",
)

builder = GraphBuilder()
builder.add_node(researcher, "research")
builder.add_node(analyst, "analysis")
builder.add_node(summarizer, "summarize")
builder.add_node(report_writer, "report")

builder.add_edge("research", "analysis")
builder.add_edge("research", "summarize")
builder.add_edge("analysis", "report")
builder.add_edge("summarize", "report")

builder.set_execution_timeout(600)

graph = builder.build()

result = graph("Research the impact of AI on healthcare")

print(f"Status: {result.status}")
print(f"Execution order: {[n.node_id for n in result.execution_order]}")
