"""
AWS Lambda deployment for the customer service agent.

Uses Mangum to wrap a FastAPI app as a Lambda handler.
The agent code is identical to what runs locally or on AgentCore.
"""

import os
import sys

from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel

from strands import Agent
from strands.vended_plugins.skills.agent_skills import AgentSkills
from strands.agent.conversation_manager import SummarizingConversationManager
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

app = FastAPI()

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests. When a customer needs help, activate the appropriate
skill for step-by-step guidance.

Important guidelines:
- Always ask for the customer ID first if you don't have it.
- Use the data returned by tools to answer questions. Do not ask the customer for
  information that is already available in the tool results.
- Never show internal IDs, system formats, or example data to the customer.
- Be warm but efficient. Customers want their problem solved, not a long conversation."""

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")

skills_plugin = AgentSkills(skills=[SKILLS_DIR])

# Note: once strands-agents supports context_manager="auto" on PyPI,
# replace the SummarizingConversationManager with just: conversation_manager="auto"
agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[skills_plugin, RefundWorkflowHandler(), tone_handler],
    system_prompt=SYSTEM_PROMPT,
    conversation_manager=SummarizingConversationManager(
        proactive_compression={"compression_threshold": 0.85},
    ),
    callback_handler=None,
)


class InvokeRequest(BaseModel):
    prompt: str


class InvokeResponse(BaseModel):
    response: str


@app.post("/invoke", response_model=InvokeResponse)
def invoke(request: InvokeRequest):
    result = agent(request.prompt)
    return InvokeResponse(response=str(result))


@app.get("/health")
def health():
    return {"status": "ok"}


# Lambda entry point
handler = Mangum(app)
