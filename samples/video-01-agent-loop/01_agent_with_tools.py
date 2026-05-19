import json
from strands import Agent, tool
from strands_tools import http_request, current_time


@tool
def letter_counter(word: str, letter: str) -> int:
    """Count occurrences of a specific letter in a word.

    Args:
        word: The input word to search in
        letter: The specific letter to count

    Returns:
        The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())


SYSTEM_PROMPT = """You are a personal assistant. Be professional, warm, and helpful in all interactions."""

agent = Agent(tools=[http_request, current_time, letter_counter], system_prompt=SYSTEM_PROMPT)

message = """How many stars does the strands-agents repo have on GitHub, what time is it, and how many R's are in strawberry?"""
result = agent(message)


print("\nFULL CONTEXT:")
print(json.dumps(agent.messages, indent=2, default=str))


#print(json.dumps(result.metrics.get_summary(), indent=2, default=str))

#print(f"\nTotal cycles: {result.metrics.get_summary()['total_cycles']}")
#print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
#print(f"Duration: {sum(result.metrics.cycle_durations):.2f}s")
