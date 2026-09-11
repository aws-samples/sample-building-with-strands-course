# Persisting Conversation History

Session managers persist conversation history and agent state across runs. Without them, everything resets when the process stops. They're implemented as hook providers, so persistence is just another harness behavior layered through hooks.

## Snapshot Session Manager (Recommended)

The recommended approach for new single-agent sessions. Saves the entire agent state as one atomic blob instead of individual message records. Supports immutable checkpoints for restoring to any prior point.

```python
from strands import Agent
from strands.session import SnapshotSessionManager
from strands.storage import LocalFileStorage

session_manager = SnapshotSessionManager(
    session_id="customer-session-001",
    storage=LocalFileStorage("./sessions"),
)

agent = Agent(
    tools=[lookup_customer, get_order_history, process_refund],
    system_prompt=SYSTEM_PROMPT,
    context_manager="auto",
    session_manager=session_manager,
)

```

Persistence happens automatically: the agent state is saved after each invocation by default. Use `save_latest_on="message"` to save after every message instead.

For production, swap `LocalFileStorage` for `S3Storage`:

```python
from strands.storage import S3Storage

session_manager = SnapshotSessionManager(
    session_id="customer-session-001",
    storage=S3Storage(bucket="my-agent-sessions", prefix="production/"),
)

```

📂 [snapshot_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/snapshot_session_manager.py) - Find all code on GitHub

## File Session Manager (Record-Based)

The record-based approach persists each message individually. Still supported for existing sessions and required for Graph/Swarm multi-agent persistence.

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
    context_manager="auto",
    session_manager=session_manager,
)

```

📂 [file_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/file_session_manager.py) - Find all code on GitHub

## S3 Session Manager (Record-Based)

Same record-based approach backed by S3 instead of local disk:

```python
from strands.session.s3_session_manager import S3SessionManager

session_manager = S3SessionManager(
    session_id="customer-session-001",
    bucket="my-agent-sessions",
    prefix="customer-service/",
    region_name="us-east-1",
)

agent = Agent(..., session_manager=session_manager)

```

📂 [s3_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/s3_session_manager.py) - Find all code on GitHub

## When to Use Which

| Manager | Best For |
|---|---|
| `SnapshotSessionManager` | New single-agent sessions. Simpler, atomic saves, supports checkpoints. |
| `FileSessionManager` | Existing record-based sessions, Graph/Swarm multi-agent, bidirectional streaming. |
| `S3SessionManager` | Same as File but with S3 for cross-machine access. |

## Session vs Memory

Session managers handle **conversation persistence** within a single session. For durable knowledge that persists **across sessions** (user preferences, facts, decisions), Strands has a separate `MemoryManager` with memory stores. Session management and memory serve different purposes:

- **Session** = persist the conversation so the agent can resume where it left off
- **Memory** = durable knowledge across sessions, without replaying past conversations

See the [Memory docs](https://strandsagents.com/docs/user-guide/concepts/memory/overview/) for more.

## Community Session Managers

The Strands community has built additional session manager backends for distributed and production workloads:

| Package | Backend | Link |
| --- | --- | --- |
| **AgentCore Memory** | Amazon Bedrock AgentCore, intelligent retrieval + long-term memory | [Docs](https://strandsagents.com/docs/community/session-managers/agentcore-memory/) |
| **Valkey/Redis** | Valkey (Redis-compatible), fast distributed session storage | [GitHub](https://github.com/jeromevdl/strands-valkey-session-manager) |

Community session managers implement the same SessionManager interface. Swap them in without changing your agent code.

There's also a community guide on [building a DynamoDB session manager](https://community.aws/content/2z0jB7JYkoiKeuZvD4mX8rnsjHA/context-management-in-strandssdk-with-dynamodb) if you need a serverless persistence layer.

## Resources

- 📖 [Session Management Docs](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/)
- 📖 [Memory Docs](https://strandsagents.com/docs/user-guide/concepts/memory/overview/)
- 📖 [Community Packages Catalog](https://strandsagents.com/docs/community/community-packages/)
