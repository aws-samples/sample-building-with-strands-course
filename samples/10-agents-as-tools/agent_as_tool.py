"""
Multi-Agent Systems: Agents as Tools

Up to now, every agent we've built has been solo. One agent, one system prompt,
one set of tools. That works until your agent needs to be good at too many things.

The alternative: specialize. Build focused agents that each do one thing well,
then compose them. That's multi-agent.

There are three patterns for this:
  1. Agents as Tools — one orchestrator calls specialists like functions (this video)
  2. Graph — explicit workflow with guaranteed execution order (next video)
  3. Swarm — agents hand off to each other dynamically (after that)

Each solves different problems. We start here because agents as tools is the
simplest, and for a lot of use cases it's the only one you need.
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import http_request


# =============================================================================
# Method 1: Pass the agent directly in the tools list.
# =============================================================================

# researcher = Agent(
#     name="researcher",
#     system_prompt="You are a research specialist. Find factual information and cite sources.",
#     tools=[http_request],
# )

# writer = Agent(
#     name="writer",
#     system_prompt="You are a technical writer. Use the researcher to gather facts, then write a clear summary.",
#     tools=[researcher],
# )

# writer("Research the fastapi/fastapi GitHub repo using the GitHub API at https://api.github.com/repos/fastapi/fastapi and write a 3-sentence summary of the project.")


# =============================================================================
# Method 2: @tool decorator 
# =============================================================================
orchestrator_model = BedrockModel(model_id="us.anthropic.claude-opus-4-6-v1")
specialist_model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")

@tool
def research_assistant(query: str, depth: str = "normal") -> str:
    """Research a topic and return sourced findings.

    Args:
        query: The research question
        depth: How thorough — "quick", "normal", or "deep"
    """
    try:
        research_agent = Agent(
            model=specialist_model,
            system_prompt=f"You are a research specialist. Research depth: {depth}.",
            tools=[http_request],
            callback_handler=None,
        )
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Research failed: {str(e)}"


# callback_handler=None suppresses streaming output. The writer's result is
# captured in `result` so you can use it programmatically. You decide which
# agent streams to the user and which runs silently.
writer = Agent(
    model=orchestrator_model,
    system_prompt="You are a technical writer. Use the research assistant to gather facts.",
    tools=[research_assistant],
)

result = writer("What are the latest Strands Agents SDK features? Check the Github API")
print(result)
