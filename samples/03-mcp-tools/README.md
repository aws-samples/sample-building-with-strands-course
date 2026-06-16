# Tools and MCP

Tools give agents the ability to take actions and access information beyond what's in the model's training data. Strands supports three sources of tools: custom `@tool` functions you write, built-in tools from `strands-agents-tools`, and MCP (Model Context Protocol) servers that expose capabilities over a standard interface.

MCP is particularly powerful because it lets you connect agents to externally managed tool servers — the agent discovers available tools dynamically at runtime rather than having them hardcoded.

## Files

- **mcp_http.py** — Connects to the AWS Knowledge MCP server (remote HTTP) and AWS Pricing MCP server (local stdio). Shows how agents discover and use tools from MCP servers.
- **mcp_coding_agent.py** — A coding assistant that connects to the AWS MCP server via streamable HTTP, giving the agent access to AWS documentation, architecture patterns, and service details.
- **tool_filtering.py** — Lists all tools from an MCP server and filters down to only the ones you need using `tool_filters` with an allowed list.
- **tool_executor.py** — Demonstrates sequential vs concurrent tool execution for controlling how multiple tool calls are handled.

## Running

```bash
python mcp_http.py
python mcp_coding_agent.py
python tool_filtering.py
python tool_executor.py
```

## Key Concepts

- **MCP servers**: External processes that expose tools over a standard protocol. Can run locally (stdio) or remotely (HTTP).
- **Tool discovery**: Agents learn what tools are available at runtime from the MCP server's tool list — no hardcoding needed.
- **Tool filtering**: In production, restrict which tools an agent can access using `tool_filters`. Only expose what the agent actually needs.
- **Security boundary**: Tools execute with the permissions of the host process. If you give an agent the shell tool, you've given it access to your machine. With MCP, you're giving tools someone else controls to your agent. Be thoughtful about what you connect.
- **Coexistence**: Custom tools, built-in tools, and MCP tools can all live in the same agent's tool list.

## Prerequisites

- MCP HTTP examples require network access to reach the remote AWS MCP server
- `mcp_coding_agent.py` requires `strands-agents-tools`: `pip install strands-agents-tools`
- Local stdio MCP servers are spawned as subprocesses — check that any required servers are installed

## Further Reading

- [Strands Agents: Tools](https://strandsagents.com/docs/user-guide/concepts/tools/)
- [Hands-on Workshop: Build Your First Agent](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
