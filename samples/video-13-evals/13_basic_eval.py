"""
Basic Agent Evaluation with OutputEvaluator

The simplest evaluation: define test cases, write a rubric, and let an
LLM judge score the agent's responses.
"""

from strands import Agent
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator


def get_response(case: Case) -> str:
    agent = Agent(callback_handler=None)
    return str(agent(case.input))


cases = [
    Case(
        name="capital",
        input="What is the capital of France?",
        expected_output="Paris",
    ),
    Case(
        name="math",
        input="What is 15% of 200?",
        expected_output="30",
    ),
    Case(
        name="explain",
        input="Explain recursion in one sentence.",
        expected_output="A function that calls itself to solve smaller subproblems.",
    ),
]

evaluator = OutputEvaluator(
    rubric="""
    Score 1.0 if the response is accurate and complete.
    Score 0.5 if partially correct or missing key details.
    Score 0.0 if incorrect or irrelevant.
    """,
)

experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(get_response)
reports[0].run_display()
