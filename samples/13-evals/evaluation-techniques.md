# Evaluation Techniques

Traditional testing breaks down with nondeterministic agents. You need: LLM-as-a-judge scoring, multi-turn simulations, trajectory validation, and deterministic assertions combined into eval suites that detect regressions.

## Installation

```bash
pip install strands-agents-evals

```

## Basic Evaluation Structure

```python
from strands import Agent, AgentSkills
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator, TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from strands_evals.types import TaskOutput

def create_agent():
    return Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[AgentSkills(skills=["./skills"]), RefundWorkflowHandler()],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )

# Trajectory evaluator — validates tool call ordering
trajectory_evaluator = TrajectoryEvaluator(
    rubric="Score 1.0 if workflow sequence matches expected trajectory...",
    include_inputs=True,
)

# Output evaluator — scores response quality
output_evaluator = OutputEvaluator(
    rubric="Score 1.0 if professional, empathetic, addresses the concern...",
)

def get_response(case: Case) -> TaskOutput:
    agent = create_agent()
    response = agent(case.input)
    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)
    return TaskOutput(output=str(response), trajectory=trajectory)

cases = [
    Case(
        name="refund-full-workflow",
        input="I'm customer C-1001. Refund my headphones order ORD-5521 please.",
        expected_output="Refund processed with 3-5 day timeline.",
        expected_trajectory=["lookup_customer", "get_order_history", "process_refund"],
    ),
    Case(
        name="missing-customer-id",
        input="I want a refund.",
        expected_output="Ask for customer ID before proceeding.",
        expected_trajectory=["lookup_customer"],
    ),
]

experiment = Experiment(
    cases=cases,
    evaluators=[trajectory_evaluator, output_evaluator],
)

report = experiment.run_evaluations(task=get_response)

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

Use chaos testing to verify your agent handles tool failures gracefully. The ChaosPlugin intercepts tool calls and injects configurable failures. The following example evaluates a pokemon game agent. This is a snippet showing just the chaos testing piece, and you can find the full source code for the agent on GitHub:

```python
from strands import Agent
from strands_evals.chaos import ChaosCase, ChaosExperiment, ChaosPlugin
from strands_evals.chaos.effects import Timeout, NetworkError, TruncateFields
from strands_evals.evaluators.deterministic import Contains

chaos = ChaosPlugin()
agent = Agent(
    tools=[get_pokemon, get_move],
    context_manager="auto",
    plugins=[chaos],
)

# Define failure scenarios
effect_maps = {
    "api_timeout": {"tool_effects": {"get_move": [Timeout()]}},
    "api_down": {"tool_effects": {"get_pokemon": [NetworkError()]}},
    "partial_response": {"tool_effects": {"get_pokemon": [TruncateFields(max_length=200)]}},
}

# Expand cases across all failure modes (+ a no-failure baseline)
chaos_cases = ChaosCase.expand(
    [Case(name="earthquake_ice_beam", input="Which Pokemon learns both Earthquake and Ice Beam with the highest Attack?")],
    effect_maps,
    include_no_effect_baseline=True,
)

experiment = ChaosExperiment(
    cases=chaos_cases,
    evaluators=[Contains(value="rampardos", case_sensitive=False, name="correct_answer")],
)

report = experiment.run_evaluations(task=lambda case: {"output": str(agent(case.input))})

```

Does the agent recover when `get_move` times out? When `get_pokemon` returns a network error? Chaos testing gives you the means to test and refine resilience while you build.

📂 [pokemon_team_advisor](https://github.com/strands-agents/samples/tree/main/python/05-technical-use-cases/pokemon-team-advisor) — Find the full code on GitHub

## Red Teaming

Test whether your agent resists adversarial pressure like jailbreaks, data exfiltration attempts, excessive agency:

```python
from strands_evals.experimental.redteam import RedTeamExperiment
from strands_evals.experimental.redteam.generators.adversarial import AdversarialCaseGenerator
from strands_evals.experimental.redteam.strategies import CrescendoStrategy

cases = AdversarialCaseGenerator().generate_cases(
    agent=agent,
    risk_categories=["data_exfiltration", "excessive_agency"],
    num_cases=3,
)

experiment = RedTeamExperiment(
    cases=cases,
    agent=agent,
    strategies=[CrescendoStrategy()],
)

report = experiment.run()

```

Red teaming validates that your guardrails hold under adversarial conditions, not just happy-path inputs.

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

