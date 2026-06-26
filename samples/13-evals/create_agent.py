"""
Creates the customer service agent with tools, skills, and steering.
Shared between the interactive script and evaluation suites.
"""

import sys
import os

# Add the steering folder to path so we can import the tools and handlers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "07-steering"))

from strands import Agent, AgentSkills
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

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

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "07-steering", "skills")


def create_customer_service_agent(**kwargs):
    """Create the full customer service agent with tools, skills, and steering."""
    skills_plugin = AgentSkills(skills=[SKILLS_DIR])

    defaults = dict(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[
            skills_plugin,
            RefundWorkflowHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
        conversation_manager="auto",
    )
    defaults.update(kwargs)

    return Agent(**defaults)
