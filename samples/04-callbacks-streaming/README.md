# Callbacks and Streaming

By default, Strands streams model output token-by-token to the console. Callback handlers let you customize this behavior - suppress tool output, format text differently, or route events to a logging system. For programmatic consumption, async iterators give you structured access to every event the agent produces. For serving agents over HTTP, you can stream responses using Server-Sent Events.

## Files

- **callbacks_streaming.py** - Custom callback handlers that control what gets printed during agent execution (e.g., suppressing tool output, formatting text).
- **async_streaming.py** - Async iterator pattern for consuming agent events programmatically instead of printing to console.
- **fastapi_streaming.py** - Streams agent responses over HTTP using FastAPI and Server-Sent Events.

## Running

```bash
python callbacks_streaming.py
python async_streaming.py

# For the FastAPI example:
pip install fastapi uvicorn
uvicorn fastapi_streaming:app --reload
```

Then test the streaming endpoint:

```bash
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 1024 * 768?"}'
```

## Key Concepts

- **Callback handlers**: Intercept streaming events (text chunks, tool starts/ends, errors) and decide what to do with them. Great for CLI tools.
- **Async iterators**: Consume agent events as a structured stream - better for integrating into larger applications where you need programmatic control.
- **SSE streaming**: Server-Sent Events let web clients consume agent output incrementally over HTTP, giving users real-time feedback.
- **Suppressing output**: Use `callback_handler=None` on agents that should run silently (like sub-agents) so only the orchestrator streams to the user.

## Further Reading

- [Strands Agents: Streaming](https://strandsagents.com/docs/user-guide/concepts/streaming/)
- [Strands Agents: Async Iterators](https://strandsagents.com/docs/user-guide/concepts/streaming/async-iterators/)
- [Hands-on Workshop: Build Your First Agent](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
