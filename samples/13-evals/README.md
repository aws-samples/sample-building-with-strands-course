# Evaluations

Traditional software testing breaks down with AI agents because of nondeterminism. The same input can produce different outputs across runs, and failures are often subtle - responses that are low quality, unsafe, incomplete, or off-policy rather than outright wrong. Evaluations give you systematic ways to measure agent quality and catch regressions.

## Files

- **basic_eval.py** - Simple output evaluation using LLM-as-a-judge with a custom rubric.
- **trajectory_eval.py** - Validates that the agent called tools in the correct order (not just that the output looks right).
- **custom_evaluator.py** - Pure Python evaluator with no LLM needed - good for deterministic checks like "did the response contain a tracking number?"
- **experiment_generator.py** - Automatically bootstraps candidate evaluation cases from tool descriptions. Useful for discovering missing coverage areas.
- **simulator_eval.py** - Multi-turn simulated conversations using `ActorSimulator`. Drives the full customer service agent through realistic interactions and evaluates with `HelpfulnessEvaluator` and `GoalSuccessRateEvaluator`.
- **customer_service_eval.py** - End-to-end evaluation of the customer service agent across multiple scenarios.
- **create_agent.py** - Factory function for creating the customer service agent (shared by eval scripts).
- **customer_service_tools.py** - Mock tools shared with the customer service agent.
- **steering_handlers.py** - Steering handlers shared with the customer service agent.
- **skills/** - Skill definitions for the customer service agent.

## Running

```bash
pip install strands-agents-evals

python basic_eval.py
python trajectory_eval.py
python custom_evaluator.py
python experiment_generator.py
python simulator_eval.py
python customer_service_eval.py
```

## Key Concepts

- **LLM-as-a-judge**: Use a model to evaluate another model's output against a rubric. Flexible but non-deterministic - run evals multiple times to check consistency.
- **Trajectory evaluation**: Validates the agent followed the correct workflow, not just that the final answer looks right. Example: did it look up the customer before processing the refund?
- **Custom evaluators**: Pure Python checks with no LLM needed. Fast, free, and deterministic. Use for anything you can verify with code.
- **Experiment generation**: Automatically bootstrap test cases from tool descriptions to discover missing coverage areas. Not a replacement for hand-crafted evals, but useful for getting started.
- **Multi-turn simulation**: Most agents look great on turn one. Failures surface after longer interactions when context accumulates and the model drifts. `ActorSimulator` drives multi-turn conversations to catch these.
- **CI/CD integration**: Wire evals into your pipeline so deployments fail automatically if reliability scores drop below acceptable thresholds.
- **Evolving suites**: Production users expose edge cases you didn't anticipate. Your eval suite should grow continuously as new failure modes are discovered.

## Further Reading

- [Strands Evals: Getting Started](https://strandsagents.com/docs/user-guide/evals-sdk/quickstart/)
- [Strands Evals: Evaluators](https://strandsagents.com/docs/user-guide/evals-sdk/evaluators/)
- [Strands Evals: Chaos Testing](https://strandsagents.com/docs/user-guide/evals-sdk/chaos_testing/)
- [Hands-on Workshop: Module 6 (Evals)](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US/06-evals)
