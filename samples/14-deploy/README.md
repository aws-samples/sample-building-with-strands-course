# Deploying to Production

> [!WARNING]
> **Before you follow along:** The video is a snapshot in time. Follow the code
> and reading here, and check [the lesson updates](../../COURSE_UPDATES.md) for differences.

This section covers two deployment options:

- **Option A: Amazon Bedrock AgentCore** - The managed option. Handles compute isolation, authentication, memory, and observability automatically. Requires an AWS account with AgentCore access (paid tier).
- **Option B: AWS Lambda** - The free-tier friendly option. Simpler to set up but you manage session isolation, authentication, and memory yourself.

Both use the same tools, skills, and steering. Their request and session lifecycles differ, as described below.

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
- **CourseDemo/** - Created by the commands below; it is not included in the repository.

## Setup

### Prerequisites

- AWS credentials configured
- Node.js 20+ (for CDK)
- Python 3.10+ with `uv`
- AgentCore CLI installed

### Create and Deploy the Project

Run from `samples/14-deploy`:

```bash
# From samples/14-deploy, install the CLI and create a Python Strands project.
npm install -g @aws/agentcore
agentcore create --name CourseAgent --project-name CourseDemo \
  --framework Strands --model-provider Bedrock --language Python --memory none

# Replace the generated starter with this lesson's agent and dependencies.
cp main.py customer_service_tools.py steering_handlers.py pyproject.toml \
  CourseDemo/app/CourseAgent/
cp -R skills/. CourseDemo/app/CourseAgent/skills/
cd CourseDemo

agentcore add memory --name CustomerServiceMemory --strategies SEMANTIC,USER_PREFERENCE
agentcore deploy

# Reuse this ID for this actor's conversation; generate a new ID for another user.
SESSION_ID="$(python3 -c 'import uuid; print(uuid.uuid4())')"
agentcore invoke --session-id "$SESSION_ID" \
  '{"prompt": "I need help returning my order", "actor_id": "customer-demo"}'
```

For local testing after scaffolding, use `agentcore dev` from `CourseDemo`.
The complete `main.py` accepts both a direct JSON payload and the JSON string carried
inside the CLI's prompt field. Keep one actor per runtime session. Its cached agent
rejects a different actor/session pair, while the Lambda example starts fresh on
every request. This demo's `actor_id` is caller-supplied; bind it to authenticated
identity in an application.

The CLI memory command creates local configuration before deployment. Verify the
runtime has `BEDROCK_AGENTCORE_MEMORY_ID` after deployment; without it the sample
keeps process-local conversation history only.

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

Use the complete FastAPI/Mangum sample and SAM template in `lambda-deployment/`:

```bash
cd lambda-deployment
pip install -r requirements.txt
sam build
sam deploy --guided
```

Each HTTP request creates a new agent and new plugins. Requests do not share
conversation history. For persistence, use a session-specific `SnapshotSessionManager`
with durable storage and bind session IDs to authenticated users.

### Lambda vs AgentCore

Lambda is a straightforward way to get your agent running in the cloud, but it doesn't manage session isolation or authentication the way AgentCore does. With Lambda, you're responsible for wiring up API Gateway for auth, managing session state yourself (via DynamoDB or S3), and adding your own observability. AgentCore handles all of that automatically with isolated microVMs, built-in identity, and automatic tracing.

If you're on the free tier or just want to get something deployed quickly, Lambda works. If you need production-grade session isolation, memory, and observability without the plumbing, AgentCore is the path.

## Further Reading

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [Strands Agents: Deploy to Lambda](https://strandsagents.com/docs/user-guide/sdk/deploy/deploy_to_aws_lambda/)
- [Hands-on Workshop: Module 7 (Deploy)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/07-deploy)
