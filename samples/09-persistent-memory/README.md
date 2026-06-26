# Persistent Memory

Agents are stateless by default. Every time your program exits, the conversation is gone. Persistent memory lets your agent remember across restarts, so it can pick up where it left off without asking the user to repeat information.

In Strands, persistent memory is implemented through **session managers**. A session manager handles saving and restoring conversation history to a storage backend. You give it a session ID, and it takes care of the rest.

## Files

- **file_session_manager.py** - Saves sessions to the local filesystem. Run it twice to see it restore the previous conversation.
- **s3_session_manager.py** - Saves sessions to Amazon S3. Useful for production deployments or sharing state across machines.
- **customer_service_tools.py** - Mock tools shared across examples.
- **steering_handlers.py** - Steering handlers shared across examples.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
# Run once, have a conversation, then exit
python file_session_manager.py

# Run again - it picks up where you left off
python file_session_manager.py

# S3 version (requires AWS credentials and an S3 bucket)
python s3_session_manager.py
```

## Key Concepts

- **Session managers**: The mechanism Strands uses to persist memory. They save/restore messages to a storage backend (filesystem, S3, DynamoDB, or custom).
- **Session ID**: Determines which conversation to restore. Same ID = same conversation history.
- **File sessions**: Store conversations as JSON files on disk. Great for development and single-machine deployments.
- **S3 sessions**: Store conversations in S3. Works across machines, supports team environments, and integrates with existing AWS infrastructure.
- **Conversation vs session**: Conversation managers control *what* stays in context (compression). Session managers control *where* it's persisted (storage). They work together.
- **Automatic restoration**: When you create an agent with a session manager and an existing session ID, the previous messages are automatically loaded.

## Prerequisites

- File sessions require write access to the `sessions/` directory
- S3 sessions require AWS credentials with read/write access to the target bucket

## Further Reading

- [Strands Agents: Session Management](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/)
- [Hands-on Workshop: Module 4 (Session Managers)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/04-session-managers)
