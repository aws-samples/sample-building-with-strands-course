# Persistent Memory

> [!WARNING]
> **Before you follow along:** The video is a snapshot in time. Follow the code
> and reading here, and check [the lesson updates](../../COURSE_UPDATES.md) for differences.

Agents are stateless by default. Every time your program exits, the conversation is gone. Persistent memory lets your agent remember across restarts, so it can pick up where it left off without asking the user to repeat information.

In Strands, persistent memory is implemented through **session managers**. A session manager handles saving and restoring conversation history to a storage backend. You give it a session ID, and it takes care of the rest.

## Which Session Manager Should I Use?

| Session Manager | Use When |
|---|---|
| **SnapshotSessionManager** | An optional way to save and restore the session state together. |
| **FileSessionManager** | Existing sessions using the record-based format, or Graph/Swarm multi-agent persistence. |
| **S3SessionManager** | Same as FileSessionManager but backed by S3 instead of local disk. |
| **AgentCore Memory** | Production deployments where you need intelligent long-term recall alongside session persistence. See `14-deploy/`. |

`SnapshotSessionManager` uses the unified `Storage` backend (`LocalFileStorage`, `S3Storage`, `InMemoryStorage`), so you swap the backend without changing your session logic. The `FileSessionManager` and `S3SessionManager` examples still work; you do not need to switch.

## Files

- **snapshot_session_manager.py** - An optional approach. Uses `SnapshotSessionManager` with `LocalFileStorage`. Run it twice to see it restore the previous conversation.
- **file_session_manager.py** - Record-based persistence to the local filesystem. Still supported for existing sessions and multi-agent use.
- **s3_session_manager.py** - Record-based persistence to Amazon S3. Useful for production deployments or sharing state across machines.
- **customer_service_tools.py** - Mock tools shared across examples.
- **steering_handlers.py** - Steering handlers shared across examples.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
# Follow the examples from the video
python file_session_manager.py
python s3_session_manager.py

# Optional: snapshot-based persistence
python snapshot_session_manager.py

# Run again - it picks up where you left off
python snapshot_session_manager.py
```

> [!TIP]
> The `FileSessionManager` and `S3SessionManager` examples shown in the video are
> still valid. `SnapshotSessionManager` is an optional alternative for saving and
> restoring a conversation. You do not need to switch to follow this lesson.
>
> See the [session management docs](https://strandsagents.com/docs/user-guide/sdk/agents/session-management/) for setup and examples.

> [!TIP]
> Memory stores let an agent use saved information, such as customer preferences,
> in future conversations. `MemoryManager` connects the agent to those stores so it
> can retrieve that information. You can add this alongside your session manager;
> it does not replace the examples in this lesson.
>
> See the [memory docs](https://strandsagents.com/docs/user-guide/sdk/memory/overview/) for an introduction, or
> [configure how your agent reads and writes memories](https://strandsagents.com/docs/user-guide/sdk/memory/managing-memory/).

## Key Concepts

- **Session managers**: The mechanism Strands uses to persist memory. They save/restore agent state to a storage backend.
- **Session ID**: Determines which conversation to restore. Same ID = same conversation history.
- **Snapshot vs record-based**: `SnapshotSessionManager` saves the serialized session state as one atomic blob. `FileSessionManager`/`S3SessionManager` save individual message records. Snapshots are simpler and support checkpoints.
- **Storage backends**: `SnapshotSessionManager` uses the unified Storage interface: `LocalFileStorage` (dev), `S3Storage` (production), `InMemoryStorage` (testing).
- **Saved versions**: If you want to restore an earlier version of a session, you can configure snapshots. See the session management docs for details.
- **Context vs session**: Context managers control *what* stays in context (compression, offloading). Session managers control *where* it's persisted (storage). They work together.
- **Session vs memory**: Session managers persist the conversation for a single session. For durable knowledge across sessions (preferences, facts, decisions), look at `MemoryManager` and memory stores.

## Prerequisites

- File/snapshot sessions require write access to the `sessions/` directory
- S3 sessions require AWS credentials with read/write access to the target bucket

## Further Reading

- [Strands Agents: Session Management](https://strandsagents.com/docs/user-guide/sdk/agents/session-management/)
- [Strands Agents: Memory](https://strandsagents.com/docs/user-guide/sdk/memory/overview/)
- [Hands-on Workshop: Module 4 (Session Managers)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/04-session-managers)
