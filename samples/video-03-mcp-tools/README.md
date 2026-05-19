# Video 3: MCP Tools

This video covers MCP (Model Context Protocol) — the standard for connecting agents to external tool servers. You'll see how to connect to remote HTTP servers, local stdio servers, control tool execution order, and use pre-built community tools.

## Files

- **mcp_http.py** — Connects to the AWS Knowledge MCP server (remote HTTP) and AWS Pricing MCP server (local stdio). Shows how agents discover and use tools from MCP servers.
- **tool_executor.py** — Demonstrates sequential vs concurrent tool execution for controlling how multiple tool calls are handled.
- **community_tools.py** — Uses pre-built tools from the `strands-agents-tools` package instead of writing your own.

## Running

```bash
python mcp_http.py
python tool_executor.py
python community_tools.py
```

## Notes

- For `community_tools.py`, install the tools package first: `pip install strands-agents-tools`
- The MCP HTTP example requires network access to reach the remote server.
- Local stdio MCP servers are spawned as subprocesses — check that any required servers are installed.
