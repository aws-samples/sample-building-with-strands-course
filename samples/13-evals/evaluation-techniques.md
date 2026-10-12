# Evaluation Techniques

> [!WARNING]
> **Before you follow along:** The video is a snapshot in time. Follow the code
> and reading here, and check [the lesson updates](../../COURSE_UPDATES.md) for differences.

Traditional testing breaks down with nondeterministic agents. You need: LLM-as-a-judge scoring, multi-turn simulations, trajectory validation, and deterministic assertions combined into eval suites that detect regressions.

## Installation

```bash
pip install strands-agents-evals

```

## Basic Evaluation Structure

Run from `samples/13-evals` so the factory can find the sample tools and skills.

```python
from strands import Agent, AgentSkills
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator, TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from strands_evals.types import TaskOutput

from create_agent import create_customer_service_agent

def create_agent():
    return create_customer_service_agent(callback_handler=None)

# Trajectory evaluator — validates tool call ordering
trajectory_evaluator = TrajectoryEvaluator(
    rubric="Match the expected tool order; ignore supplementary skills tool calls.",
    include_inputs=True,
)

# Output evaluator — scores response quality
output_evaluator = OutputEvaluator(
    rubric="Score accuracy, professionalism, and whether the response addresses the request.",
)

def get_response(case: Case) -> TaskOutput:
    agent = create_agent()
    response = agent(case.input)
    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)
    return TaskOutput(output=str(response), trajectory=trajectory)

cases = [
    Case(
        name="refund-full-workflow",
        input="I'm C-1001. Refund order ORD-5521. Yes, I confirm the refund.",
        expected_output="Refund processed with 3-5 day timeline.",
        expected_trajectory=["lookup_customer", "get_order_history", "process_refund"],
    ),
    Case(
        name="missing-customer-id",
        input="I want a refund.",
        expected_output="Ask for customer ID before proceeding.",
        expected_trajectory=[],
    ),
]

experiment = Experiment(
    cases=cases,
    evaluators=[trajectory_evaluator, output_evaluator],
)

report = experiment.run_evaluations(task=get_response)
report.run_display()

```

📂 [customer_service_eval.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/13-evals/customer_service_eval.py) — Full code on GitHub

## Evaluation Types

| Type | What It Checks |
| --- | --- |
| **Output evaluation** | Quality, tone, correctness of final response |
| **Trajectory evaluation** | Whether the agent followed the correct tool sequence |
| **Simulation** | Multi-turn stress testing over time |
| **Deterministic** | JSON schema, response length, format — no LLM needed |
| **Chaos testing** | Does the agent recover when tools fail? |
| **Red teaming** | Does the agent resist adversarial attacks? |
| **Experiment Generator** | Auto-bootstraps test cases from agent capabilities |

## Chaos Testing

Use chaos testing to verify your agent handles tool failures gracefully. The ChaosPlugin intercepts tool calls and injects configurable failures. This example uses the course's mock order tool and a fresh agent for each case:

```python
from strands import Agent
from strands_evals import Case
from strands_evals.chaos import ChaosCase, ChaosExperiment, ChaosPlugin
from strands_evals.chaos.effects import Timeout, NetworkError, TruncateFields
from strands_evals.evaluators import OutputEvaluator
from customer_service_tools import get_order_history

effect_maps = {
    "api_timeout": {"tool_effects": {"get_order_history": [Timeout()]}},
    "api_down": {"tool_effects": {"get_order_history": [NetworkError()]}},
    "partial_response": {
        "tool_effects": {"get_order_history": [TruncateFields(max_length=200)]}
    },
}
chaos_cases = ChaosCase.expand(
    [Case(name="order_status", input="Check the orders for customer C-1001.")],
    effect_maps,
    include_no_effect_baseline=True,
)

def run_case(case):
    agent = Agent(
        tools=[get_order_history], plugins=[ChaosPlugin()], callback_handler=None,
        system_prompt="Use order data. If it is unavailable, explain the failure.",
    )
    return {"output": str(agent(case.input))}

experiment = ChaosExperiment(
    cases=chaos_cases,
    evaluators=[OutputEvaluator(
        rubric="Use returned order data or acknowledge a tool failure. Do not invent orders."
    )],
)
report = experiment.run_evaluations(task=run_case)
report.run_display()
```

Does the agent recover when `get_order_history` times out? When `get_order_history` returns a network error? Chaos testing gives you the means to test and refine resilience while you build.


## Red Teaming

Test whether your agent resists adversarial pressure like jailbreaks, data exfiltration attempts, excessive agency:

```python
from create_agent import create_customer_service_agent
from strands_evals.experimental.redteam import RedTeamExperiment
from strands_evals.experimental.redteam.generators.adversarial import AdversarialCaseGenerator
from strands_evals.experimental.redteam.strategies import CrescendoStrategy

cases = AdversarialCaseGenerator().generate_cases(
    agent=create_customer_service_agent(),
    risk_categories=["data_exfiltration", "excessive_agency"],
    num_cases=3,
)

experiment = RedTeamExperiment(
    cases=cases,
    agent_factory=create_customer_service_agent,  # fresh state for each attack
    attack_strategies=[CrescendoStrategy()],
)

report = experiment.run_evaluations()
```

Red teaming probes the tested guardrails under adversarial conditions. Passing these
cases does not prove resistance to every attack.

📖 [Strands Evals: Chaos Testing & Red Teaming blog post](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)

## Best Practices

- Evaluate multi-turn interactions, not just single turns
- Combine LLM judges with deterministic assertions
- Wire evals into CI/CD to catch regressions automatically
- Evolve your eval suite as new failure modes emerge
- Use a different model for evaluation than generation
- Use chaos testing to verify resilience before production
- Run red team experiments to validate guardrails

## Resources

- 📖 [Strands Evals blog: "Reduced cost, better isolation, more resilience"](https://strandsagents.com/blog/reduced-cost-better-isolation-more-resilience/)
- 📖 [Strands Agents Documentation](https://strandsagents.com/docs/user-guide/evals-sdk/quickstart/)

