"""
Context Manager: Auto Mode

The simplest way to get production-grade context management.
One line gives you:
  - Large tool results offloaded to external storage with truncated previews
  - Old messages compressed into structured summaries (not dropped)
  - Proactive compression at 85% context usage to stay ahead of overflow

In benchmarks on real code investigation tasks, this cut costs by 55%
while accuracy went from 68% to 98%. Half the tokens, better results.
"""

from strands import Agent
from strands_tools import file_read, file_write, editor, shell, http_request

# That's it. One parameter replaces manual configuration of thresholds,
# summary ratios, compression timing, and offloader setup.
agent = Agent(
    tools=[file_read, file_write, editor, shell, http_request],
    context_manager="auto",
    system_prompt="You are a helpful coding assistant.",
)

# Give it a task that generates a lot of context
agent(
    "Research the top 5 Python web frameworks by GitHub stars. "
    "For each one, summarize the key features and latest version. "
    "Write the results to frameworks.md"
)
