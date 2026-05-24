import json
from strands import Agent, tool
from strands_tools import file_read, editor, shell


@tool
def check_health_route(project_dir: str) -> str:
    """Check whether a FastAPI project already contains a /health route.

    Args:
        project_dir: Path to the project directory to inspect.
    """
    import os

    app_file = os.path.join(project_dir, "main.py")
    if not os.path.exists(app_file):
        return f"No main.py found in {project_dir}"

    with open(app_file, "r") as f:
        content = f.read()

    if "/health" in content or '"/health"' in content:
        return "A /health route already exists in main.py"
    else:
        return "No /health route found in main.py. One should be added."


SYSTEM_PROMPT = """You are a coding assistant. Inspect the project before making
changes. Make the smallest safe change possible."""

agent = Agent(
    tools=[file_read, editor, shell, check_health_route],
    system_prompt=SYSTEM_PROMPT,
)

result = agent("Inspect the FastAPI project in ./sample_project, "
               "add a /health endpoint if it doesn't already exist, "
               "and run the tests.")

# ============================================================
# Uncomment to inspect conversation history
# ============================================================
print("\n" + "=" * 60)
print("CONVERSATION HISTORY:")
print("=" * 60)
print(json.dumps(agent.messages, indent=2, default=str))

# ============================================================
# Uncomment to inspect metrics
# ============================================================
# print("\n" + "=" * 60)
# print("METRICS:")
# print("=" * 60)
# print(json.dumps(result.metrics.get_summary(), indent=2))
