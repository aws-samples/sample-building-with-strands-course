# Video 11: Graphs

Graphs define explicit execution order between agents using nodes and edges. Unlike agents-as-tools (where the orchestrator decides when to delegate), graphs give you deterministic control over the flow — including parallel fan-out, conditional branching, and feedback loops.

## Files

- **basic_graph.py** — A research pipeline: research → analysis + summarization (parallel fan-out) → report writing. Demonstrates nodes, edges, and parallel execution.

## Running

```bash
python basic_graph.py
```

## Notes

- Graphs are best when you know the execution order ahead of time and want it to be deterministic.
- Parallel nodes run concurrently — useful for independent tasks like analysis and summarization.
- Compare this to agents-as-tools (Video 10) where the orchestrator decides the flow dynamically.
