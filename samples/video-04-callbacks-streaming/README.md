# Video 4: Callbacks & Streaming

This video explains how streaming works in Strands and the different ways to control and consume streamed output. You'll see callback handlers for customizing console output, async iterators for programmatic access, and a FastAPI example for streaming over HTTP.

## Files

- **callbacks_streaming.py** — Custom callback handlers that control what gets printed during agent execution (e.g., suppressing tool output, formatting text).
- **async_streaming.py** — Async iterator pattern for consuming agent events programmatically instead of printing to console.
- **fastapi_streaming.py** — Streams agent responses over HTTP using FastAPI and Server-Sent Events.

## Running

```bash
python callbacks_streaming.py
python async_streaming.py

# For the FastAPI example:
pip install fastapi uvicorn
python fastapi_streaming.py
```

Then hit `http://localhost:8000` to test the streaming endpoint.

## Notes

- The FastAPI example starts a local server — you can test it with `curl` or a browser.
- Callbacks are great for CLI tools; async iterators are better for integrating into larger applications.
