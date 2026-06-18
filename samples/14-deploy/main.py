import json
import logging
import os
from strands import Agent
from strands.vended_plugins.skills.agent_skills import AgentSkills
from strands.agent.conversation_manager import SlidingWindowConversationManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

logger = logging.getLogger(__name__)

# ============================================================
# AgentCore App
# ============================================================
app = BedrockAgentCoreApp()


# ============================================================
# Configuration
# ============================================================
MEMORY_ID = os.environ.get("BEDROCK_AGENTCORE_MEMORY_ID", "")
REGION = "us-east-1"

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

skills_plugin = AgentSkills(skills=["./skills"])

_agent = None

# ============================================================
# Build the Agent
# ============================================================
def create_customer_service_agent(actor_id: str, session_id: str | None = None):
    """Create the customer service agent with AgentCore Memory."""

    global _agent
    
    if _agent is None:

        session_manager = None
        if MEMORY_ID:
            agentcore_memory_config = AgentCoreMemoryConfig(
                memory_id=MEMORY_ID,
                session_id=session_id,
                actor_id=actor_id,
                retrieval_config={
                    "/users/{actorId}/facts": RetrievalConfig(),
                    "/users/{actorId}/preferences": RetrievalConfig(),
                },
            )

            session_manager = AgentCoreMemorySessionManager(
                agentcore_memory_config=agentcore_memory_config,
                region_name=REGION,
            )

        _agent = Agent(
            tools=[lookup_customer, get_order_history, process_refund],
            plugins=[
                skills_plugin,
                RefundWorkflowHandler(),
                tone_handler,
            ],
            system_prompt=SYSTEM_PROMPT,
            conversation_manager=SlidingWindowConversationManager(window_size=20),
            session_manager=session_manager,
        )

    return _agent


@app.entrypoint
def invoke(payload, context):
    """Handle incoming requests from AgentCore Runtime."""
    raw_prompt = payload.get("prompt")

    # Get session_id from runtime context (passed via --session-id flag)
    session_id = context.session_id

    # Try to parse structured fields from the prompt
    try:
        parsed = json.loads(raw_prompt)
        prompt = parsed.get("prompt")
        actor_id = parsed.get("actor_id")
    except (TypeError, json.JSONDecodeError):
        prompt = raw_prompt
        actor_id = payload.get("actor_id")

    if not prompt:
        raise ValueError("Missing required field: prompt")
    if not actor_id:
        raise ValueError("Missing required field: actor_id")
    if not session_id:
        raise ValueError("Missing required field: session_id (pass via --session-id)")

    logger.info(f"invoke: actor_id={actor_id}, session_id={session_id}, prompt={prompt[:50]}")

    agent = create_customer_service_agent(actor_id=actor_id, session_id=session_id)
    response = agent(prompt)

    return {"response": str(response)}


# ============================================================
# Run the Agent
# ============================================================
if __name__ == "__main__":
    app.run()
