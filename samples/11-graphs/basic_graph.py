from strands import Agent
from strands.multiagent import GraphBuilder
from strands_tools import http_request

researcher = Agent(
    name="researcher",
    system_prompt="You are a research specialist. Make one or two http requests max to gather key facts, then return your findings as bullet points. Do not follow links or do additional searches.",
    tools=[http_request],
)

analyst = Agent(
    name="analyst",
    system_prompt="You are a data analyst. Identify the top 3 patterns and their implications from the research provided. Keep your response under 150 words.",
)

summarizer = Agent(
    name="summarizer",
    system_prompt="You are a summarizer. Condense the research into 4-5 bullet points. Keep it under 100 words.",
)

report_writer = Agent(
    name="report_writer",
    system_prompt="You synthesize analysis and summaries into a clear, well-structured final report. Keep it under 250 words.",
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
