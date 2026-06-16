# Graphs

Graphs define explicit execution order between agents using nodes and edges. Unlike agents-as-tools (where the orchestrator decides flow dynamically), graphs give you deterministic control — including parallel fan-out, conditional branching, and feedback loops.

Use graphs when you know the execution order ahead of time and want it guaranteed.

## Files

- **basic_graph.py** — A research pipeline: research → analysis + summarization (parallel fan-out) → report writing. Demonstrates nodes, edges, and parallel execution.

## Running

```bash
python basic_graph.py
```

## Key Concepts

- **Nodes**: Each node is an agent (or any callable). Nodes execute when all their incoming edges are satisfied.
- **Edges**: Define dependencies between nodes. An edge from A to B means B waits for A to complete before starting.
- **Parallel fan-out**: Nodes without dependencies on each other run concurrently. In the example, analysis and summarization happen simultaneously.
- **Deterministic flow**: Unlike agents-as-tools where the model decides the order, graphs guarantee the sequence you defined.
- **Data flow**: Each node receives the output of its predecessor nodes as input.
- **When to use graphs**: Pipelines with known structure, fan-out/fan-in patterns, workflows that need guaranteed execution order, and feedback loops.

## Comparison

| Pattern | Flow Control | Best For |
|---------|-------------|----------|
| Agents as Tools | Orchestrator decides | Separable domains, synthesis |
| Graphs | Defined by edges | Known pipelines, parallelism |
| Swarms | Agents decide | Unknown sequences, exploration |
