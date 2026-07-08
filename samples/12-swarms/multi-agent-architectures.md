# Multi-Agent Architectures

Strands provides three composable multi-agent patterns. Each solves a different coordination problem, and they can nest inside each other.

| Pattern | Structure | Use When |
| --- | --- | --- |
| **Agents as Tools** | Hub-and-spoke. Orchestrator calls specialists | Clear manager-specialist relationship, isolated context |
| **Graph** | DAG with explicit edges | You can draw the workflow on a whiteboard |
| **Swarm** | Autonomous handoffs, no predefined structure | The team needs to figure it out together |

## Agents as Tools

Wrap one agent as a tool for another. Each specialist gets its own isolated context window — great for noisy tools that would pollute the orchestrator's context.

### Pass Agent Directly

```python
from strands import Agent
from strands_tools import http_request

researcher = Agent(
    name="researcher",
    system_prompt="You are a research specialist. Find factual information.",
    tools=[http_request],
)

writer = Agent(
    name="writer",
    system_prompt="You are a technical writer. Use the researcher to gather facts.",
    tools=[researcher],  # Pass agent directly as a tool
)

writer("Research the FastAPI GitHub repo and write a 3-sentence summary.")

```

### @tool Decorator

```python
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import http_request

orchestrator_model = BedrockModel(model_id="us.anthropic.claude-opus-4-6-v1")
specialist_model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")

@tool
def research_assistant(query: str, depth: str = "normal") -> str:
    """Research a topic and return sourced findings.

    Args:
        query: The research question
        depth: How thorough — "quick", "normal", or "deep"
    """
    research_agent = Agent(
        model=specialist_model,
        system_prompt=f"You are a research specialist. Research depth: {depth}.",
        tools=[http_request],
        callback_handler=None,  # Run silently
    )
    response = research_agent(query)
    return str(response)

writer = Agent(
    model=orchestrator_model,
    system_prompt="You are a technical writer. Use the research assistant.",
    tools=[research_assistant],
)

```

📂 [agent_as_tool.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/10-agents-as-tools/agent_as_tool.py) — Find all code on GitHub

Data flow: orchestrator sends a string → specialist runs its own loop → returns a string. Context resets between calls (isolation).

## Graph

Graphs give you explicit control over execution order. Each node is a full agent; edges express dependencies. The graph resolves what runs in parallel and what waits.

```python
from strands import Agent
from strands.multiagent import GraphBuilder
from strands_tools import http_request

researcher = Agent(
    name="researcher",
    system_prompt="Gather comprehensive information from the web.",
    tools=[http_request],
)

analyst = Agent(
    name="analyst",
    system_prompt="Identify patterns, trends, and key insights from research.",
)

summarizer = Agent(
    name="summarizer",
    system_prompt="Condense raw research into concise key points.",
)

report_writer = Agent(
    name="report_writer",
    system_prompt="Synthesize analysis and summaries into a final report.",
)

builder = GraphBuilder()
builder.add_node(researcher, "research")
builder.add_node(analyst, "analysis")
builder.add_node(summarizer, "summarize")
builder.add_node(report_writer, "report")

builder.add_edge("research", "analysis")
builder.add_edge("research", "summarize")   # analyst + summarizer run in parallel
builder.add_edge("analysis", "report")
builder.add_edge("summarize", "report")      # report waits for both

builder.set_execution_timeout(600)
graph = builder.build()

result = graph("Research the impact of AI on healthcare")

```

📂 [basic_graph.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/11-graphs/basic_graph.py) — Find all code on GitHub

Data flow: entry nodes receive the original task. Downstream nodes receive the original task + labeled outputs from dependencies. Use `invocation_state` for metadata (user IDs, feature flags) not exposed to models.

Common patterns: sequential pipelines, parallel fan-out, conditional branching, and cyclic feedback loops (with `set_max_node_executions` to prevent infinite loops).

## Agent Swarms

In a swarm, agents hand off to each other autonomously with no predefined structure. The execution path emerges from what each agent discovers.

```python
from strands import Agent
from strands.multiagent import Swarm

triage = Agent(
    name="triage",
    system_prompt="Initial assessment. Hand off to the relevant specialist.",
)

log_analyst = Agent(
    name="log_analyst",
    system_prompt="Analyze application logs. Hand off if you find infra/deployment issues.",
    tools=[check_application_logs],
)

metrics_analyst = Agent(
    name="metrics_analyst",
    system_prompt="Analyze system metrics. Hand off based on findings.",
    tools=[check_metrics_dashboard],
)

deployment_reviewer = Agent(
    name="deployment_reviewer",
    system_prompt="Review recent deployments and infrastructure changes.",
    tools=[check_recent_deployments, check_infrastructure_status],
)

debugging_swarm = Swarm(
    [triage, log_analyst, metrics_analyst, deployment_reviewer],
    entry_point=triage,
    max_handoffs=10,
    max_iterations=10,
    execution_timeout=300.0,
    node_timeout=120.0,
    repetitive_handoff_detection_window=6,
    repetitive_handoff_min_unique_agents=2,
)

result = debugging_swarm(
    "Payment service returning 500 errors for 25% of requests. Started 30 min ago."
)

```

📂 [debugging_swarm.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/12-swarms/debugging_swarm.py) — Find all code on GitHub

Key differences: handoff = full transfer of control (not a function call). Agents share accumulated context. Strands injects `handoff_to_agent` tool automatically.

**Safety controls** — always configure these or swarms can ping-pong forever:

| Setting | Purpose |
| --- | --- |
| `max_handoffs` | Total handoff cap |
| `max_iterations` | Total agent execution cap |
| `execution_timeout` | Wall-clock time limit for entire swarm |
| `node_timeout` | Time limit per agent turn |
| `repetitive_handoff_detection_window` | Detect ping-pong loops |

## Composing Patterns

These patterns nest: a swarm can be a node in a graph, a graph can contain agents-as-tools, an agent-as-tool can internally run a graph. Start with the simplest pattern that fits your coordination needs and compose up.

## Resources

- 📖 [Multi-Agent Patterns Overview](https://strandsagents.com/docs/user-guide/concepts/multi-agent/multi-agent-patterns/)
- 📖 [Agents as Tools](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/)
- 📖 [Graph Workflows](https://strandsagents.com/docs/user-guide/concepts/multi-agent/graph/)
- 📖 [Swarms](https://strandsagents.com/docs/user-guide/concepts/multi-agent/swarm/)
- 📖 [Workflow (Deterministic Pipelines)](https://strandsagents.com/docs/user-guide/concepts/multi-agent/workflow/)

