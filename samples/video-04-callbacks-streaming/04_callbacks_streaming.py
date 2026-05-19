"""
Callbacks & Streaming

Every agent we've built so far streams text to the terminal as the model
generates it. That's the default callback handler — a function that gets
called for every event the agent produces. You can replace it with your own.

See also:
  - 04_async_streaming.py — async iterator pattern (stream_async)
  - 04_fastapi_streaming.py — real FastAPI streaming endpoint
"""

import json
from strands import Agent
from strands_tools import calculator


# =============================================================================
# 1. Default behavior — streaming just works
# =============================================================================
# No callback_handler specified = PrintingCallbackHandler.
# Text streams to stdout as it's generated. Tool calls show inline.

print("=" * 60)
print("DEFAULT STREAMING")
print("=" * 60)

agent = Agent(tools=[calculator])
agent("What is 1024 * 768?")


# =============================================================================
# 2. Custom callback handler — buffered messages
# =============================================================================
# A callback handler is a function that accepts **kwargs. The SDK calls it
# for every event. The keys you care about:
#   - "data": a text chunk from the model
#   - "current_tool_use": dict with "name" when a tool is being called
#   - "message": a complete message object when one is finished
#   - "result": the final AgentResult when the loop finishes
#
# This one buffers text and only shows complete messages — useful for chat
# interfaces where you want polished, complete responses instead of raw
# streaming fragments.

print("\n\n" + "=" * 60)
print("CUSTOM CALLBACK — buffered messages")
print("=" * 60)


def message_buffer_handler(**kwargs):
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        print(json.dumps(kwargs["message"], indent=2, default=str))


agent = Agent(
    tools=[calculator],
    callback_handler=message_buffer_handler,
)

agent("What is 2 to the power of 16, minus 1?")


# =============================================================================
# 3. Silent mode — callback_handler=None
# =============================================================================
# Nothing prints. You get the result back programmatically.
# This matters in multi-agent systems where sub-agents run silently
# while the orchestrator streams to the user.

print("\n\n" + "=" * 60)
print("SILENT MODE")
print("=" * 60)

agent = Agent(
    tools=[calculator],
    callback_handler=None,
)

result = agent("What is 42 * 42?")
print(f"Captured result: {result}")
