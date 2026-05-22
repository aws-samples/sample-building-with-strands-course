# Video 9: Session Managers

Session managers persist conversation history and agent state across application restarts. This video shows two options: local filesystem (great for development) and Amazon S3 (great for production or team environments).

## Files

- **file_session_simple.py** — Saves sessions to the local filesystem. Run it twice to see it restore the previous conversation.
- **s3_session.py** — Saves sessions to Amazon S3. Useful for production deployments or sharing state across machines.
- **customer_service_tools.py** — Mock tools shared across examples.
- **steering_handlers.py** — Steering handlers shared across examples.
- **skills/** — Skill definitions for the customer service agent.

## Running

```bash
# Run once, have a conversation, then exit
python file_session_simple.py

# Run again — it picks up where you left off
python file_session_simple.py

# S3 version (requires AWS credentials and an S3 bucket)
python s3_session.py
```

## Notes

- File sessions are stored in the `sessions/` directory by default.
- For S3, make sure your AWS credentials have read/write access to the target bucket.
- Session IDs determine which conversation to restore — same ID = same conversation.
