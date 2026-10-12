from strands import Agent
from strands_evals import Case
from strands_evals.chaos import ChaosCase, ChaosExperiment, ChaosPlugin
from strands_evals.chaos.effects import Timeout, NetworkError, TruncateFields
from strands_evals.evaluators import OutputEvaluator
from customer_service_tools import get_order_history

if __name__ == "__main__":

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
