# Video 13: Evaluations

How do you know if your agent is actually good? This video covers evaluation patterns: LLM-as-a-judge for output quality, trajectory evaluation for verifying tool usage, and pure Python evaluators for deterministic checks. We also evaluate the customer service agent end-to-end.

## Files

- **basic_eval.py** — Simple output evaluation using LLM-as-a-judge with a custom rubric.
- **trajectory_eval.py** — Validates that the agent called tools in the correct order (not just that the output looks right).
- **custom_evaluator.py** — Pure Python evaluator with no LLM needed — good for deterministic checks like "did the response contain a tracking number?"
- **customer_service_eval.py** — End-to-end evaluation of the customer service agent across multiple scenarios.
- **customer_service_tools.py** — Mock tools shared with the customer service agent.
- **steering_handlers.py** — Steering handlers shared with the customer service agent.
- **skills/** — Skill definitions for the customer service agent.

## Running

```bash
# Install the evals package first
pip install strands-agents-evals

python basic_eval.py
python trajectory_eval.py
python custom_evaluator.py
python customer_service_eval.py
```

## Notes

- LLM-as-a-judge is flexible but non-deterministic — run evals multiple times to check consistency.
- Trajectory evals catch cases where the agent gets the right answer but through the wrong process.
- Custom evaluators are fast and free — use them for anything you can check with code.
- Combine all three approaches for comprehensive coverage.
