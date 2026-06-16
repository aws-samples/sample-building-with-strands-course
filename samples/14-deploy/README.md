# Deploying to Production with AgentCore

Amazon Bedrock AgentCore is a collection of components for building, deploying, and operating AI agents in production. It includes Runtime (isolated microVM hosting), Memory (persistent conversation and long-term retrieval), Observability (automatic tracing), and more.

AgentCore Runtime runs agents inside isolated microVMs so they can maintain state across requests. AgentCore Memory provides persistent conversation storage and semantic retrieval. Observability and tracing are automatic — no manual wiring needed.

The deployed agent itself is only part of the production architecture. Runtime handles authentication (IAM/OAuth) automatically, but in a real system you still need surrounding infrastructure like API gateways, rate limiting, retries, security controls, monitoring, and error handling.

## Files

- **main.py** — The production entry point. Wires up the customer service agent with AgentCore Runtime, AgentCore Memory for persistent sessions, and all the plugins (skills, steering, conversation management).
- **pyproject.toml** — Project dependencies: `strands-agents`, `bedrock-agentcore[memory]`, and OpenTelemetry instrumentation.
- **customer_service_tools.py** — Mock tools (lookup_customer, get_order_history, process_refund).
- **steering_handlers.py** — Refund workflow enforcement and tone guardrails.
- **skills/** — Skill definitions loaded on demand by the agent.
- **customerserviceagent/** — The AgentCore CLI project with CDK infrastructure, configuration, and app code for deployment.

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
- **Automatic observability**: Tracing and metrics are collected automatically through AgentCore — no instrumentation code needed.
- **CodeZip deployment**: Package your Python agent as a zip and deploy directly. No Docker required.
- **Environment variables**: Memory IDs and other resource references are injected automatically via environment variables at runtime.

## Further Reading

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Hands-on Workshop: Module 7 (Deploy)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/07-deploy)
