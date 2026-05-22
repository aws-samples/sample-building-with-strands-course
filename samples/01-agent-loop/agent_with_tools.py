import json
from strands import Agent, tool
from strands_tools import http_request, current_time


@tool
def letter_counter(word: str, letter: str) -> int:
    """Count how many times a specific letter appears in a word.

    Args:
        word: The word to search through.
        letter: The single letter to count.
    """
    return word.lower().count(letter.lower())


SYSTEM_PROMPT = """You are a personal assistant. Be professional, warm,
and helpful in all interactions."""

agent = Agent(
    tools=[http_request, current_time, letter_counter],
    system_prompt=SYSTEM_PROMPT,
)

result = agent("How many stars does the strands-agents/sdk-python repo have on GitHub, "
               "what time is it, and how many R's are in strawberry?")

# print("\n" + "=" * 60)
# print("CONVERSATION HISTORY:")
# print("=" * 60)
# print(json.dumps(agent.messages, indent=2, default=str))

# print("\n" + "=" * 60)
# print("METRICS:")
# print("=" * 60)
# print(json.dumps(result.metrics.get_summary(), indent=2))
