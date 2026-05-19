from strands import Agent
from strands.session.s3_session_manager import S3SessionManager

session_manager = S3SessionManager(
    session_id="user-456",
    bucket="agent-sessions-bucket-mtw",
    prefix="production/",
    region_name="us-east-1",
)

agent = Agent(session_manager=session_manager)
agent("Hello from production!")
