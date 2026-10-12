from create_agent import create_customer_service_agent
from strands_evals.experimental.redteam import RedTeamExperiment
from strands_evals.experimental.redteam.generators.adversarial import AdversarialCaseGenerator
from strands_evals.experimental.redteam.strategies import CrescendoStrategy

if __name__ == "__main__":

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
