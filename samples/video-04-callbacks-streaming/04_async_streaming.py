"""
Async Streaming with stream_async

Same events as the callback handler, but as an async generator.
This is what you'd use in FastAPI, aiohttp, or any async server
where you need to stream responses to clients.
"""

import asyncio
from strands import Agent
from strands_tools import calculator

# callback_handler=None so the default handler doesn't also print
agent = Agent(
    tools=[calculator],
    callback_handler=None,
)


async def main():
    last_tool_printed = None
    async for event in agent.stream_async("What is 256 + 256?"):
        if "data" in event:
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event and event["current_tool_use"].get("name"):
            tool_name = event["current_tool_use"]["name"]
            if tool_name != last_tool_printed:
                last_tool_printed = tool_name
                print(f"\n🔧 [{tool_name}]", end=" ", flush=True)
        elif "result" in event:
            print("\n✅ Stream complete")


asyncio.run(main())
