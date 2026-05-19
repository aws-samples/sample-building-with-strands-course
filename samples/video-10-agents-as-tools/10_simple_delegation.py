from strands import Agent
from strands_tools import http_request

researcher = Agent(
    name="research_specialist",
    system_prompt="You are a research specialist. Find factual information and cite sources.",
    tools=[http_request],
)

writer = Agent(
    system_prompt="You are a technical writer. Use the researcher to gather facts, then write a clear summary.",
    tools=[researcher],
)

writer("Write a summary of the latest Strands Agents SDK features.")
