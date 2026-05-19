import urllib.request
import urllib.parse
import json
from strands import Agent, tool
from strands.hooks import (
    HookProvider, HookRegistry,
    BeforeInvocationEvent, BeforeToolCallEvent,
)


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using the wttr.in API.

    Args:
        city: Name of the city to get weather for
    """
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "strands-agent"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    current = data["current_condition"][0]
    return (
        f"{city}: {current['temp_F']}°F, "
        f"{current['weatherDesc'][0]['value']}, "
        f"humidity {current['humidity']}%, "
        f"wind {current['windspeedMiles']} mph"
    )


class LimitToolCounts(HookProvider):
    def __init__(self, max_calls: int = 3):
        self.max_calls = max_calls
        self.counts: dict[str, int] = {}

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.reset)
        registry.add_callback(BeforeToolCallEvent, self.check)

    def reset(self, event: BeforeInvocationEvent) -> None:
        self.counts = {}

    def check(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use["name"]
        self.counts[name] = self.counts.get(name, 0) + 1
        if self.counts[name] > self.max_calls:
            event.cancel_tool = (
                f"'{name}' hit the {self.max_calls}-call limit. "
                "Do NOT call this tool again."
            )


agent = Agent(
    tools=[get_weather],
    hooks=[LimitToolCounts(max_calls=3)],
)

print("Weather Agent with rate limiter (type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break
    if not user_input:
        continue
    print()
    agent(user_input)
