"""
Coding assistant enhanced with the AWS MCP server.
Connects to the managed AWS MCP server via streamable HTTP
to give the agent access to AWS capabilities.
"""

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import file_read, editor, shell

# Connect to the AWS MCP server (streamable HTTP)
aws_mcp = MCPClient(
    lambda: streamablehttp_client("https://aws-mcp.us-east-1.api.aws/mcp")
)

SYSTEM_PROMPT = """You are a coding assistant with AWS expertise.
Use the AWS MCP tools to look up documentation, architecture patterns,
and service details when answering questions about building on AWS.
Be concise and actionable in your recommendations."""

agent = Agent(
    tools=[aws_mcp, file_read, editor, shell],
    system_prompt=SYSTEM_PROMPT,
)

agent("I need to build a serverless FastAPI backend with authentication "
      "and file uploads. What AWS services should I use and how should "
      "I architect this?")
