"""
FastAPI Streaming Endpoint

A real streaming AI endpoint in ~20 lines. Run with:
    uvicorn fastapi_streaming:app --reload

Test with:
    curl -X POST http://localhost:8000/stream \
        -H "Content-Type: application/json" \
        -d '{"prompt": "What is 1024 * 768?"}'
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent, tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression and return the result.

    Args:
        expression: A math expression like '1024 * 768' or '2 ** 16 - 1'
    """
    # NOTE: eval() is used here for simplicity in this demo.
    # Do not use eval() with untrusted input in production.
    return str(eval(expression))


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
