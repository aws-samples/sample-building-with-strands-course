# Persistent Memory

Agents are stateless by default. Every time your program exits, the conversation is gone. Persistent memory lets your agent remember across restarts, so it can pick up where it left off without asking the user to repeat information.

In Strands, persistent memory is implemented through **session managers**. A session manager handles saving and restoring conversation history to a storage backend. You give it a session ID, and it takes care of the rest.

## Which Session Manager Should I Use?

| Session Manager | Use When |
|---|---|
| **SnapshotSessionManager** | New single-agent sessions. Recommended default. Saves the whole agent as one atomic blob. Supports immutable checkpoints. |
| **FileSessionManager** | Existing sessions using the record-based format, or Graph/Swarm multi-agent persistence. |
| **S3SessionManager** | Same as FileSessionManager but backed by S3 instead of local disk. |
| **AgentCore Memory** | Production deployments where you need intelligent long-term recall alongside session persistence. See `14-deploy/`. |

`SnapshotSessionManager` uses the unified `Storage` backend (`LocalFileStorage`, `S3Storage`, `InMemoryStorage`), so you swap the backend without changing your session logic. The older managers (`FileSessionManager`, `S3SessionManager`) still work and are needed for multi-agent orchestration.

## Files

- **snapshot_session_manager.py** - The recommended approach for new sessions. Uses `SnapshotSessionManager` with `LocalFileStorage`. Run it twice to see it restore the previous conversation.
- **file_session_manager.py** - Record-based persistence to the local filesystem. Still supported for existing sessions and multi-agent use.
- **s3_session_manager.py** - Record-based persistence to Amazon S3. Useful for production deployments or sharing state across machines.
- **customer_service_tools.py** - Mock tools shared across examples.
- **steering_handlers.py** - Steering handlers shared across examples.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
# Recommended: snapshot-based persistence
python snapshot_session_manager.py

# Run again - it picks up where you left off
python snapshot_session_manager.py

# Record-based alternatives (still supported)
python file_session_manager.py
python s3_session_manager.py
```

## Key Concepts

- **Session managers**: The mechanism Strands uses to persist memory. They save/restore agent state to a storage backend.
- **Session ID**: Determines which conversation to restore. Same ID = same conversation history.
- **Snapshot vs record-based**: `SnapshotSessionManager` saves the full agent state as one atomic blob. `FileSessionManager`/`S3SessionManager` save individual message records. Snapshots are simpler and support checkpoints.
- **Storage backends**: `SnapshotSessionManager` uses the unified Storage interface: `LocalFileStorage` (dev), `S3Storage` (production), `InMemoryStorage` (testing).
- **Immutable snapshots**: `SnapshotSessionManager` supports checkpointing via `snapshot_trigger`. Restore to any prior point, not just the latest.
- **Context vs session**: Context managers control *what* stays in context (compression, offloading). Session managers control *where* it's persisted (storage). They work together.
- **Session vs memory**: Session managers persist the conversation for a single session. For durable knowledge across sessions (preferences, facts, decisions), look at `MemoryManager` and memory stores.

## Prerequisites

- File/snapshot sessions require write access to the `sessions/` directory
- S3 sessions require AWS credentials with read/write access to the target bucket

## Further Reading

- [Strands Agents: Session Management](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/)
- [Strands Agents: Memory](https://strandsagents.com/docs/user-guide/concepts/memory/overview/)
- [Hands-on Workshop: Module 4 (Session Managers)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/04-session-managers)
