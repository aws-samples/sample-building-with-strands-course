"""
Demonstrates tool filtering — listing all tools from an MCP server
and then filtering down to only the ones you need.
"""

import logging
logging.getLogger("mcp").setLevel(logging.CRITICAL)

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient

# Connect to the AWS MCP server
aws_mcp = MCPClient(
    lambda: streamablehttp_client("https://aws-mcp.us-east-1.api.aws/mcp")
)

with aws_mcp:
    # List all available tools from the server
    print("=" * 60)
    print("ALL TOOLS FROM AWS MCP SERVER:")
    print("=" * 60)
    for tool in aws_mcp.list_tools_sync():
        desc = (tool.mcp_tool.description or '')[:80]
        print(f"  - {tool.tool_name}: {desc}")

    print(f"\nTotal tools: {len(aws_mcp.list_tools_sync())}")

    # Now filter to only the tools we need
    print("\n" + "=" * 60)
    print("FILTERED TOOLS (allowed list):")
    print("=" * 60)

# Create a new client with filtering (outside the with block)
filtered_mcp = MCPClient(
    lambda: streamablehttp_client("https://aws-mcp.us-east-1.api.aws/mcp"),
    tool_filters={
        "allowed": ["aws___search_documentation", "aws___read_documentation"]
    },
)

agent = Agent(
    tools=[filtered_mcp],
    system_prompt="You are an AWS documentation assistant. Only use documentation tools.",
)

print("Agent created with filtered tool set.")
print(f"Available tools: {agent.tool_names}")
