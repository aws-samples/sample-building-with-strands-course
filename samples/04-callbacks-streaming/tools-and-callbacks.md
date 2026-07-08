# Tools and Callbacks

Agents need tools from multiple sources. Strands supports three categories: custom tools (@tool decorator), community tools (strands-agents-tools), and MCP servers for connecting to external systems. All coexist in the same agent's tool list.

## MCP (Model Context Protocol)

MCP is an open standard that gives agents a consistent way to discover and interact with external capabilities — GitHub, AWS, databases, browser tools — through a standard protocol.

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

# Remote MCP server (Streamable HTTP)
aws_knowledge = MCPClient(
    lambda: streamablehttp_client("https://knowledge-mcp.global.api.aws"),
    prefix="knowledge"
)

# Local MCP server (stdio)
aws_pricing = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-pricing-mcp-server@latest"],
        env={"AWS_REGION": "us-east-1"}
    )),
    prefix="pricing"
)

agent = Agent(tools=[aws_knowledge, aws_pricing], system_prompt="You are an AWS architect.")
agent("What AWS services should I use for a serverless FastAPI backend?")

```

📂 [mcp_http.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/03-mcp-tools/mcp_http.py) — Find all code on GitHub

## Tool Filtering

Too many tools → worse tool selection, hallucinated tool names, wasted context. Filter tools to only what your agent needs:

```python
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent

# Filter to only documentation tools
filtered_mcp = MCPClient(
    lambda: streamablehttp_client("https://aws-mcp.us-east-1.api.aws/mcp"),
    tool_filters={
        "allowed": ["aws___search_documentation", "aws___read_documentation"]
    },
)

agent = Agent(
    tools=[filtered_mcp],
    system_prompt="You are an AWS documentation assistant.",
)

```

📂 [tool_filtering.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/03-mcp-tools/tool_filtering.py) — Find all code on GitHub

# Callbacks & Streaming

Callbacks control how agent output surfaces to users. The default handler streams text to stdout, but you can replace it with custom handlers for UIs, APIs, or silent execution. For async servers, use `stream_async()`.

## Custom Callback Handler

A callback handler is a function that accepts `**kwargs`. It fires for every agent event (text chunks, tool calls, complete messages):

```python
from strands import Agent
from strands_tools import calculator

def buffered_handler(**kwargs):
    # Only show complete messages, not individual streaming chunks
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        content = kwargs["message"].get("content", [])
        for block in content:
            if "text" in block:
                print(block["text"])

agent = Agent(tools=[calculator], callback_handler=buffered_handler)
agent("What is 2 to the power of 16, minus 1?")

```

## Silent Mode

Set `callback_handler=None` to suppress all output. The agent runs and returns a result you can use programmatically:

```python
agent = Agent(tools=[calculator], callback_handler=None)
result = agent("What is 42 * 42?")
print(f"Captured result: {result}")

```

This is essential for sub-agents in multi-agent systems that run behind the scenes.

## Async Streaming (FastAPI)

For async servers, use `agent.stream_async()` — an async generator that yields events:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands_tools import calculator

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/stream")
async def stream_response(request: PromptRequest):
    async def generate():
        agent = Agent(tools=[calculator], callback_handler=None)
        async for event in agent.stream_async(request.prompt):
            if "data" in event:
                yield event["data"]

    return StreamingResponse(generate(), media_type="text/plain")

```

📂 [fastapi_streaming.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/04-callbacks-streaming/fastapi_streaming.py) — Find all code on GitHub

## Resources

- 📖 [MCP Tools Docs](https://strandsagents.com/docs/user-guide/concepts/tools/mcp-tools/)
- 📖 [Tools Overview](https://strandsagents.com/docs/user-guide/concepts/tools/)
- 📖 [Callbacks](https://strandsagents.com/docs/user-guide/concepts/streaming/callback-handlers/)

