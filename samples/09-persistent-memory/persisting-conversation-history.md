# Persisting Conversation History

> [!WARNING]
> **Before you follow along:** The video is a snapshot in time. Follow the code
> and reading here, and check [the lesson updates](../../COURSE_UPDATES.md) for differences.

Session managers persist conversation history and agent state across runs. Without them, everything resets when the process stops. They're implemented as hook providers, so persistence is just another harness behavior layered through hooks.

## File Session Manager (Record-Based)

Run these examples from `samples/09-persistent-memory`.

The record-based approach persists each message individually. Still supported for existing sessions and available for existing record-based Graph/Swarm sessions.

```python
from strands import Agent
from customer_service_tools import lookup_customer, get_order_history, process_refund

SYSTEM_PROMPT = "Help customers with their orders using the available tools."
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

agent = Agent(session_manager=session_manager)

```

📂 [s3_session_manager.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/09-persistent-memory/s3_session_manager.py) - Find all code on GitHub

## Snapshot Session Manager

> [!TIP]
> The `FileSessionManager` and `S3SessionManager` examples shown in the video are
> still valid. `SnapshotSessionManager` is an optional alternative for saving and
> restoring a conversation. You do not need to switch to follow this lesson.
>
> See the [session management docs](https://strandsagents.com/docs/user-guide/sdk/agents/session-management/) for setup and examples.

`SnapshotSessionManager` saves the session state together, instead of saving each
message as a separate record.

```python
from strands import Agent
from customer_service_tools import lookup_customer, get_order_history, process_refund

SYSTEM_PROMPT = "Help customers with their orders using the available tools."
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

## When to Use Which

| Manager | Best For |
|---|---|
| `SnapshotSessionManager` | Save and restore a single agent, Graph/Swarm, or Bidi session. |
| `FileSessionManager` | Existing record-based sessions; retains their storage format. |
| `S3SessionManager` | Same as File but with S3 for cross-machine access. |

## Session vs Memory

> [!TIP]
> Memory stores let an agent use saved information, such as customer preferences,
> in future conversations. `MemoryManager` connects the agent to those stores so it
> can retrieve that information. You can add this alongside your session manager;
> it does not replace the examples in this lesson.
>
> See the [memory docs](https://strandsagents.com/docs/user-guide/sdk/memory/overview/) for an introduction, or
> [configure how your agent reads and writes memories](https://strandsagents.com/docs/user-guide/sdk/memory/managing-memory/).

Session managers handle **conversation persistence** within a single session. For durable knowledge that persists **across sessions** (user preferences, facts, decisions), Strands has a separate `MemoryManager` with memory stores. Session management and memory serve different purposes:

- **Session** = persist the conversation so the agent can resume where it left off
- **Memory** = durable knowledge across sessions, without replaying past conversations

See the [Memory docs](https://strandsagents.com/docs/user-guide/sdk/memory/overview/) for more.

## Community Session Managers

The Strands community has built additional session manager backends for distributed and production workloads:

| Package | Backend | Link |
| --- | --- | --- |
| **AgentCore Memory** | Amazon Bedrock AgentCore, intelligent retrieval + long-term memory | [Docs](https://strandsagents.com/docs/integrations/session-managers/agentcore-memory/) |
| **Valkey/Redis** | Valkey (Redis-compatible), fast distributed session storage | [GitHub](https://github.com/jeromevdl/strands-valkey-session-manager) |

Community session managers implement the same SessionManager interface. Swap them in without changing your agent code.

There's also a community guide on [building a DynamoDB session manager](https://community.aws/content/2z0jB7JYkoiKeuZvD4mX8rnsjHA/context-management-in-strandssdk-with-dynamodb) if you need a serverless persistence layer.

## Resources

- 📖 [Session Management Docs](https://strandsagents.com/docs/user-guide/sdk/agents/session-management/)
- 📖 [Memory Docs](https://strandsagents.com/docs/user-guide/sdk/memory/overview/)
- 📖 [Community Packages Catalog](https://strandsagents.com/integrations/)
