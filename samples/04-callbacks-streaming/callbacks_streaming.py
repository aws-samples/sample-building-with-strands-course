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

print("=" * 60)
print("DEFAULT STREAMING")
print("=" * 60)

agent = Agent(tools=[calculator])
agent("What is 1024 * 768?")


# =============================================================================
# 2. Custom callback handler — buffered messages
# =============================================================================

print("\n\n" + "=" * 60)
print("CUSTOM CALLBACK — buffered output")
print("=" * 60)


def buffered_handler(**kwargs):
    # "data" events are individual text chunks as they stream in.
    # We ignore them here (no printing) so nothing appears mid-generation.

    # "message" fires when a complete message is ready.
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        # Extract just the text content from the complete message
        content = kwargs["message"].get("content", [])
        for block in content:
            if "text" in block:
                print(block["text"])


agent = Agent(
    tools=[calculator],
    callback_handler=buffered_handler,
)

agent("What is 2 to the power of 16, minus 1?")


# =============================================================================
# 3. Silent mode — callback_handler=None
# =============================================================================

print("\n\n" + "=" * 60)
print("SILENT MODE")
print("=" * 60)

agent = Agent(
    tools=[calculator],
    callback_handler=None,
)

result = agent("What is 42 * 42?")
print(f"Captured result: {result}")
