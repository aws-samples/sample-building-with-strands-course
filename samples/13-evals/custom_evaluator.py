"""
Custom Evaluator

Extend the Evaluator base class for pure Python checks — no LLM judge needed.
Useful for deterministic things like response length, JSON schema validation,
or keyword presence.
"""

from strands import Agent
from strands_evals import Case, Experiment
from strands_evals.evaluators import Evaluator
from strands_evals.types.evaluation import EvaluationData, EvaluationOutput


class LengthEvaluator(Evaluator):
    """Evaluates if response length is within acceptable range."""

    def __init__(self, min_len: int, max_len: int):
        super().__init__()
        self.min_len = min_len
        self.max_len = max_len

    def evaluate(self, data: EvaluationData) -> list[EvaluationOutput]:
        length = len(str(data.actual_output))
        in_range = self.min_len <= length <= self.max_len
        return [
            EvaluationOutput(
                score=1.0 if in_range else 0.0,
                test_pass=in_range,
                reason=f"Length {length}, expected [{self.min_len}, {self.max_len}]",
            )
        ]

    async def evaluate_async(self, data):
        return self.evaluate(data)


def get_response(case: Case) -> str:
    agent = Agent(callback_handler=None)
    return str(agent(case.input))


cases = [
    Case(name="concise", input="What is 2 + 2?", expected_output="4"),
    Case(
        name="detailed",
        input="Explain how the internet works.",
        expected_output="A detailed explanation",
    ),
]

experiment = Experiment(
    cases=cases,
    evaluators=[LengthEvaluator(min_len=10, max_len=5000)],
)
reports = experiment.run_evaluations(get_response)
reports[0].run_display()
