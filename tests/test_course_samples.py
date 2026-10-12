"""Offline regressions for the runnable course examples.

The scripted model drives the real SDK loop. It does not call a hosted model.
"""
import importlib.util
import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from strands import Agent
from strands.models import Model
from strands.session import SnapshotSessionManager
from strands.storage import LocalFileStorage
from strands.multiagent import GraphBuilder, Swarm
from strands_evals import Case, Experiment
from strands_evals.types import EvaluationData

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


class ScriptedModel(Model):
    def __init__(self, *responses):
        self.responses = iter(responses)

    def get_config(self):
        return {"model_id": "course-offline-test"}

    def update_config(self, **kwargs):
        pass

    async def structured_output(self, *args, **kwargs):
        raise NotImplementedError
        yield

    async def stream(self, *args, **kwargs):
        response = next(self.responses)
        yield {"messageStart": {"role": "assistant"}}
        for block in response:
            if "toolUse" in block:
                call = block["toolUse"]
                yield {"contentBlockStart": {"start": {"toolUse": {
                    "name": call["name"], "toolUseId": call["toolUseId"],
                }}}}
                yield {"contentBlockDelta": {"delta": {"toolUse": {
                    "input": json.dumps(call["input"]),
                }}}}
            else:
                yield {"contentBlockStart": {"start": {}}}
                yield {"contentBlockDelta": {"delta": {"text": block["text"]}}}
            yield {"contentBlockStop": {}}
        reason = "tool_use" if any("toolUse" in b for b in response) else "end_turn"
        yield {"messageStop": {"stopReason": reason}}


def load_sample(monkeypatch, path):
    path = SAMPLES / path
    monkeypatch.syspath_prepend(str(path.parent))
    for name in ("steering_handlers", "customer_service_tools", "create_agent"):
        monkeypatch.delitem(sys.modules, name, raising=False)
    spec = importlib.util.spec_from_file_location("course_sample", path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "course_sample", module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setenv("AWS_EC2_METADATA_DISABLED", "true")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    import socket

    def no_network(*args, **kwargs):
        raise AssertionError("Offline regression attempted network access")

    monkeypatch.setattr(socket.socket, "connect", no_network)


def test_original_delete_approvals(monkeypatch, tmp_path):
    first, second = tmp_path / "first.txt", tmp_path / "second.txt"
    first.write_text("first"); second.write_text("second")
    model = ScriptedModel([
        {"toolUse": {"name": "delete_file", "toolUseId": "one", "input": {"path": str(first)}}},
        {"toolUse": {"name": "delete_file", "toolUseId": "two", "input": {"path": str(second)}}},
    ], [{"text": "Done"}])
    replies = iter(["Delete both files", "y", "n", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(replies))
    monkeypatch.setattr("strands.Agent", lambda **kwargs: Agent(model=model, **kwargs))
    runpy.run_path(str(SAMPLES / "05-hooks/approval_interrupt.py"), run_name="__main__")
    assert not first.exists()
    assert second.read_text() == "second"


@pytest.mark.parametrize("words,score,passed", [(3, 0, False), (15, 1, True), (101, 0.5, False)])
def test_custom_evaluator_contract(monkeypatch, words, score, passed):
    module = load_sample(monkeypatch, "13-evals/custom_evaluator.py")
    evaluator = module.ResponseLengthEvaluator(min_words=10, max_words=100)
    outputs = evaluator.evaluate(EvaluationData(input="Explain", actual_output="word " * words))
    assert len(outputs) == 1
    assert evaluator.aggregator(outputs)[:2] == (score, passed)
    experiment = Experiment(cases=[Case(name="offline", input="Explain")], evaluators=[evaluator])
    report = experiment.run_evaluations(lambda case: {"output": "word " * words})
    assert report.scores[0] == score


def test_eval_factory_creates_fresh_plugins(monkeypatch):
    module = load_sample(monkeypatch, "13-evals/create_agent.py")
    monkeypatch.setattr(module, "Agent", lambda **kwargs: kwargs)
    first, second = module.create_customer_service_agent(), module.create_customer_service_agent()
    assert all(a is not b for a, b in zip(first["plugins"], second["plugins"]))
    assert Path(module.SKILLS_DIR).parent.name == "13-evals"


def test_lambda_requests_start_fresh(monkeypatch):
    module = load_sample(monkeypatch, "14-deploy/lambda-deployment/lambda_handler.py")
    configs, agents = [], []

    def factory(**kwargs):
        configs.append(kwargs)
        # Keep real tools, skills and deterministic steering. Only the hosted tone
        # judge is excluded from this offline request-isolation test.
        kwargs["plugins"] = kwargs["plugins"][:-1]
        agent = Agent(model=ScriptedModel([{"text": "Done"}]), **kwargs)
        agents.append(agent)
        return agent

    monkeypatch.setattr(module, "Agent", factory)
    from fastapi.testclient import TestClient
    with TestClient(module.app) as client:
        for prompt in ["Customer one", "Customer two"]:
            response = client.post("/invoke", json={"prompt": prompt})
            assert response.status_code == 200
            assert response.json()["response"].strip() == "Done"
    assert len(agents) == 2
    assert "Customer one" not in str(agents[1].messages)
    assert all(a is not b for a, b in zip(configs[0]["plugins"], configs[1]["plugins"]))


def test_agentcore_rejects_actor_or_session_switch(monkeypatch):
    module = load_sample(monkeypatch, "14-deploy/main.py")
    monkeypatch.setattr(module, "MEMORY_ID", "")
    monkeypatch.setattr(module, "Agent", lambda **kwargs: SimpleNamespace(config=kwargs))
    first = module.create_customer_service_agent("actor-a", "session-a")
    assert module.create_customer_service_agent("actor-a", "session-a") is first
    with pytest.raises(ValueError, match="different runtime session"):
        module.create_customer_service_agent("actor-b", "session-a")
    with pytest.raises(ValueError, match="different runtime session"):
        module.create_customer_service_agent("actor-a", "session-b")


def test_snapshot_restores_conversation(tmp_path):
    def build():
        return Agent(model=ScriptedModel([{"text": "Remembered"}]), callback_handler=None,
                     session_manager=SnapshotSessionManager(
                         "test-session", storage=LocalFileStorage(str(tmp_path))))
    first = build()
    first("My order is ORD-5521")
    assert build().messages == first.messages


@pytest.mark.parametrize("pattern", ["graph", "swarm"])
def test_snapshot_supports_multiagent(tmp_path, pattern):
    def build():
        agent = Agent(name="worker", agent_id="worker", callback_handler=None,
                      model=ScriptedModel([{"text": "Completed"}]))
        session = SnapshotSessionManager("multi", storage=LocalFileStorage(str(tmp_path)))
        if pattern == "swarm":
            return Swarm([agent], session_manager=session, max_iterations=1)
        builder = GraphBuilder()
        builder.add_node(agent, "worker")
        builder.set_entry_point("worker")
        builder.set_session_manager(session)
        return builder.build()
    assert build()("Test persistence").status.value == "completed"
    restored = build()
    assert restored("Continue").status.value == "completed"


def test_refund_workflow_runs_through_real_tool_hooks(monkeypatch):
    module = load_sample(monkeypatch, "07-steering/steering_handlers.py")
    import customer_service_tools as tools
    model = ScriptedModel(
        [{"toolUse": {"toolUseId": "lookup", "name": "lookup_customer",
                      "input": {"customer_id": "C-1001"}}}],
        [{"toolUse": {"toolUseId": "history", "name": "get_order_history",
                      "input": {"customer_id": "C-1001"}}}],
        [{"toolUse": {"toolUseId": "refund", "name": "process_refund",
                      "input": {"order_id": "ORD-5521", "amount": 79.99}}}],
        [{"text": "Refund complete"}],
    )
    agent = Agent(model=model, callback_handler=None,
                  tools=[tools.lookup_customer, tools.get_order_history, tools.process_refund],
                  plugins=[module.RefundWorkflowHandler()])
    agent("Refund the headphones")
    results = [block["toolResult"] for message in agent.messages
               for block in message["content"] if "toolResult" in block]
    assert [r["status"] for r in results] == ["success"] * 3
    assert "Refund of $79.99 processed" in results[-1]["content"][0]["text"]
