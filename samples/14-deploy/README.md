# Deploying to Production

This section covers two deployment options:

- **Option A: Amazon Bedrock AgentCore** - The managed option. Handles compute isolation, authentication, memory, and observability automatically. Requires an AWS account with AgentCore access (paid tier).
- **Option B: AWS Lambda** - The free-tier friendly option. Simpler to set up but you manage session isolation, authentication, and memory yourself.

Both deploy the same agent code. The harness you built with Strands (tools, hooks, skills, steering, context management) works identically in either environment.

---

## Option A: AgentCore (Managed)

Amazon Bedrock AgentCore is a collection of components for building, deploying, and operating AI agents in production. It includes Runtime (isolated microVM hosting), Memory (persistent conversation and long-term retrieval), Observability (automatic tracing), and more.

AgentCore Runtime runs agents inside isolated microVMs so they can maintain state across requests. AgentCore Memory provides persistent conversation storage and semantic retrieval. Observability and tracing are automatic.

The deployed agent itself is only part of the production architecture. Runtime handles authentication (IAM/OAuth) automatically, but in a real system you still need surrounding infrastructure like API gateways, rate limiting, retries, security controls, monitoring, and error handling.

## Files

- **main.py** - The production entry point. Wires up the customer service agent with AgentCore Runtime, AgentCore Memory for persistent sessions, and all the plugins (skills, steering, conversation management).
- **pyproject.toml** - Project dependencies: `strands-agents`, `bedrock-agentcore[memory]`, and OpenTelemetry instrumentation.
- **customer_service_tools.py** - Mock tools (lookup_customer, get_order_history, process_refund).
- **steering_handlers.py** - Refund workflow enforcement and tone guardrails.
- **skills/** - Skill definitions loaded on demand by the agent.
- **customerserviceagent/** - The AgentCore CLI project with CDK infrastructure, configuration, and app code for deployment.

## Setup

### Prerequisites

- AWS credentials configured
- Node.js 20+ (for CDK)
- Python 3.10+ with `uv`
- AgentCore CLI installed

### Local Development

```bash
cd customerserviceagent
agentcore dev
```

## Deploying

```bash
# Create the AgentCore project
agentcore create

# Add memory with semantic and preference strategies
agentcore add memory --name CustomerServiceMemory --strategies SEMANTIC,USER_PREFERENCE

# Deploy to AWS
agentcore deploy
```

## Invoking the Deployed Agent

Once deployed, invoke with a session ID to maintain conversation state across requests:

```bash
SESSION_ID="your-session-id-here"

agentcore invoke --session-id "$SESSION_ID" \
  '{"prompt": "I need help returning my order", "actor_id": "morgan"}'

agentcore invoke --session-id "$SESSION_ID" \
  '{"prompt": "C-1001", "actor_id": "morgan"}'

agentcore invoke --session-id "$SESSION_ID" \
  '{"prompt": "wireless headphones", "actor_id": "morgan"}'

agentcore invoke --session-id "$SESSION_ID" \
  '{"prompt": "yes", "actor_id": "morgan"}'
```

## Key Concepts

- **Build the harness, run the harness**: Strands is how you build the harness (loop, tools, hooks, memory, guardrails). AgentCore Runtime is how you run it in production (managed compute, identity, observability).
- **AgentCore Runtime**: Hosts your agent code in isolated microVMs. Handles authentication, scaling, and request routing.
- **AgentCore Memory**: Persistent storage with configurable retrieval strategies (semantic search, user preferences). The agent remembers across sessions.
- **Session persistence**: Use `--session-id` to maintain conversation state across requests. The agent picks up where it left off.
- **Automatic observability**: Tracing and metrics are collected automatically through AgentCore - no instrumentation code needed.
- **CodeZip deployment**: Package your Python agent as a zip and deploy directly. No Docker required.
- **Environment variables**: Memory IDs and other resource references are injected automatically via environment variables at runtime.

---

## Option B: AWS Lambda (Free Tier)

If you don't have AgentCore access, you can deploy the same agent to AWS Lambda. This is simple to set up and works on the free tier, but there are trade-offs.

**What Lambda doesn't give you (that AgentCore does):**
- No automatic session isolation (you manage session IDs yourself via the request payload)
- No managed memory service (use DynamoDB or S3 for session persistence)
- 15-minute execution limit (long running agents may time out)

### Lambda Deployment

1. Install the Lambda adapter:

```bash
pip install strands-agents mangum
```

2. Create a `lambda_handler.py`:

```python
from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel
from strands import Agent
from strands.vended_plugins.skills.agent_skills import AgentSkills
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

app = FastAPI()

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise."""

skills_plugin = AgentSkills(skills=["./skills"])

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    plugins=[skills_plugin, RefundWorkflowHandler(), tone_handler],
    system_prompt=SYSTEM_PROMPT,
    conversation_manager="auto",
    callback_handler=None,
)


class Request(BaseModel):
    prompt: str


@app.post("/invoke")
def invoke(request: Request):
    result = agent(request.prompt)
    return {"response": str(result)}


# Lambda entry point
handler = Mangum(app)
```

3. Package and deploy with SAM or the AWS CLI:

```bash
# Using SAM (simplest)
sam init --runtime python3.12 --app-template hello-world
# Replace the handler with your agent code
sam build && sam deploy --guided
```

### Lambda vs AgentCore

Lambda is a straightforward way to get your agent running in the cloud, but it doesn't manage session isolation or authentication the way AgentCore does. With Lambda, you're responsible for wiring up API Gateway for auth, managing session state yourself (via DynamoDB or S3), and adding your own observability. AgentCore handles all of that automatically with isolated microVMs, built-in identity, and automatic tracing.

If you're on the free tier or just want to get something deployed quickly, Lambda works. If you need production-grade session isolation, memory, and observability without the plumbing, AgentCore is the path.

## Further Reading

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Strands Agents: Deploy to Lambda](https://strandsagents.com/docs/user-guide/deploy/deploy_to_aws_lambda/)
- [Hands-on Workshop: Module 7 (Deploy)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/07-deploy)
