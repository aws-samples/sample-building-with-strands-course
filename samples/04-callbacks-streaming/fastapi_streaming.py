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
