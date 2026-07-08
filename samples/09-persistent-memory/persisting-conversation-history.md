# Persisting Conversation History

Session managers persist conversation history and agent state across runs. Without them, everything resets when the process stops. They're implemented as hook providers — persistence is just another harness behavior layered through hooks.

## File Session Manager

```python
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

session_manager = FileSessionManager(
    session_id="customer-session-001",
    storage_dir="./sessions",
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    system_prompt=SYSTEM_PROMPT,
    conversation_manager="auto",
    session_manager=session_manager,
)

```

Persistence happens automatically at three points:

1. **Init** — loads existing session data
2. **Message added** — writes to storage
3. **After invocation** — syncs state

📂 [file_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/file_session_manager.py) — Find all code on GitHub

## S3 Session Manager

Swap storage backends without rewriting the app:

```python
from strands.session.s3_session_manager import S3SessionManager

session_manager = S3SessionManager(
    session_id="customer-session-001",
    bucket_name="my-agent-sessions",
    prefix="customer-service/",
    region="us-east-1",
)

agent = Agent(..., session_manager=session_manager)

```

📂 [s3_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/s3_session_manager.py) — Find all code on GitHub

## Important Distinction

Session managers handle **conversation persistence**. But in production, context comes from many sources beyond chat history like databases, RAG systems, long-term memory, external APIs. Those are separate context sources retrieved at runtime via tools.

## Community Session Managers

The Strands community has built additional session manager backends for distributed and production workloads:

| Package | Backend | Link |
| --- | --- | --- |
| **AgentCore Memory** | Amazon Bedrock AgentCore — intelligent retrieval + long-term memory | [Docs](https://strandsagents.com/docs/community/session-managers/agentcore-memory/) |
| **Valkey/Redis** | Valkey (Redis-compatible) — fast, distributed session storage | [GitHub](https://github.com/jeromevdl/strands-valkey-session-manager) |

Community session managers implement the same SessionManager interface — swap them in without changing your agent code.

There's also a community guide on [building a DynamoDB session manager](https://community.aws/content/2z0jB7JYkoiKeuZvD4mX8rnsjHA/context-management-in-strandssdk-with-dynamodb) if you need a serverless persistence layer.

## Resources

- 📖 [Session Management Docs](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/)
- 📖 [Community Packages Catalog](https://strandsagents.com/docs/community/community-packages/)

