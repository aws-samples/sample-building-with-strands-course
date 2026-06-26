# Building Agent Harnesses with Strands Agents

This repo contains runnable code samples designed to be cloned and run in your own AWS account. Each folder in `samples/` covers a core concept of building AI agent harnesses - from the basic agent loop through multi-agent systems, evaluations, and production deployment.

## What is Strands?

[Strands](https://strandsagents.com) is an open-source agent harness toolkit from AWS. It's available in both Python and TypeScript. It includes:

- **Strands Agents** - The agent framework. Build the loop, connect tools, add hooks, manage context, compose multi-agent systems. This is what the course focuses on.
- **Strands Evals** - Evaluate agent quality with LLM-as-a-judge, trajectory validation, chaos testing, and red teaming.
- **Strands Shell** - Sandboxed execution environments for agents that need filesystem and network access.
- **Strands MCP Server** - Expose your Strands agents as [MCP tool servers](https://strandsagents.com/docs/user-guide/quickstart/python/#strands-mcp-server-optional) so other agents and tools can call them.

This course explores the agent framework in depth and touches on evaluations. There's a lot more to explore in the [full documentation](https://strandsagents.com/docs/user-guide/quickstart/python/).

## Prerequisites

- Python 3.10+
- An AWS account (free tier works for most samples) - [create one here](https://aws.amazon.com/resources/create-account/?p=ft&z=subnav&loc=4)
- AWS credentials configured - see [SETUP.md](./SETUP.md) for step-by-step instructions

## Quick Start

```bash
git clone https://github.com/morganwillisaws/strands-course.git
cd strands-course

python3 -m venv .venv
source .venv/bin/activate

pip install strands-agents strands-agents-tools
```

Then pick any sample and run it:

```bash
cd samples/01-agent-loop
python simple_agent.py
```

## Alternative Model Providers

Strands is model-agnostic. You can use it without AWS if you prefer another provider:

| Provider | Install | Auth |
|----------|---------|------|
| Anthropic | `pip install "strands-agents[anthropic]"` | `ANTHROPIC_API_KEY` |
| OpenAI | `pip install "strands-agents[openai]"` | `OPENAI_API_KEY` |
| Ollama (local) | `pip install "strands-agents[ollama]"` | None - runs on your machine |

See `samples/02-model-providers/` for examples of each.

## Course Structure

| Folder | Topic |
|--------|-------|
| `01-agent-loop` | Agent harnesses and the agent loop |
| `02-model-providers` | Swapping model providers |
| `03-mcp-tools` | Tools, MCP servers, and tool filtering |
| `04-callbacks-streaming` | Callbacks, streaming, and FastAPI |
| `05-hooks` | Lifecycle hooks and safety guardrails |
| `06-plugins-skills` | Plugins and on-demand skills |
| `07-steering` | Steering handlers and workflow enforcement |
| `08-conversation-management` | Context management and compression |
| `09-persistent-memory` | Session managers for persistent memory |
| `10-agents-as-tools` | Multi-agent: agents as tools |
| `11-graphs` | Graphs and structured workflows |
| `12-swarms` | Agent swarms and shared context |
| `13-evals` | Evaluating agents |
| `14-deploy` | Deploying to production (AgentCore + Lambda) |

## Running Examples

Each folder is self-contained. For folders that use the customer service example (06+), run from inside the folder so `./skills` is found:

```bash
cd samples/07-steering
python customer_service_steering.py
```

## Additional Dependencies

Some samples need extra packages:

```bash
# FastAPI streaming (04)
pip install fastapi uvicorn

# Evaluations (13)
pip install strands-agents-evals

# Deployment - AgentCore (14)
pip install bedrock-agentcore
```

## Troubleshooting

### Getting throttled on Bedrock?

Claude models on the free tier have low rate limits. If you're hitting `ThrottlingException`, switch to a different model:

```python
from strands import Agent
from strands.models.bedrock import BedrockModel

agent = Agent(model=BedrockModel(model_id="amazon.nova-pro-v1:0"))
```

Other options: `amazon.nova-lite-v1:0`, `amazon.nova-micro-v1:0`, `meta.llama3-1-70b-instruct-v1:0`

The samples default to Claude Sonnet for best quality. See `02-model-providers/` for how to swap.

### Claude access error on first call?

Claude models require a one-time use-case acknowledgment. It's submitted automatically on first invocation. If you get an access error, wait a couple minutes and retry.

### ModuleNotFoundError: strands?

Make sure you activated the virtual environment:

```bash
source .venv/bin/activate
pip install strands-agents strands-agents-tools
```

### AWS credentials not found?

See [SETUP.md](./SETUP.md) for full credential configuration instructions.

## What's Next

This course covers the core agent framework. Here are areas to explore once you're comfortable building harnesses:

### Guardrails and Safety

Amazon Bedrock Guardrails let you add content filtering, topic blocking, and PII detection to your agent without writing custom hooks. You configure policies in the Bedrock console and attach them to your model calls.

- [Bedrock Guardrails with Strands](https://github.com/aws-samples/sample-amazon-bedrock-for-beginners) - Setup guides and integration samples

### RAG and Knowledge Bases

Amazon Bedrock Knowledge Bases give your agent access to your own documents through retrieval-augmented generation. The agent queries the knowledge base as a tool and gets grounded answers from your data.

- [Knowledge Bases with Strands](https://github.com/aws-samples/sample-amazon-bedrock-for-beginners) - How to create a knowledge base and connect it to a Strands agent

### AgentCore Samples

More examples of deploying and operating agents with Amazon Bedrock AgentCore:

- [Strands Agents Samples](https://github.com/strands-agents/samples) - Official samples including AgentCore deployments, multi-agent patterns, and production architectures

### Strands Ecosystem

- [Strands Shell](https://github.com/strands-agents/shell) - Sandboxed execution for agents
- [Strands Evals](https://github.com/strands-agents/evals) - Chaos testing, red teaming, and evaluation suites
- [Community Packages](https://strandsagents.com/docs/community/community-packages/) - Tools and integrations built by the community

## Links

- [Strands Agents Homepage](https://strandsagents.com)
- [Strands Agents Documentation](https://strandsagents.com/docs/user-guide/quickstart/python/)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Strands Evals](https://github.com/strands-agents/evals)
- [Strands Shell](https://github.com/strands-agents/shell)
- [Hands-on Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US)
- [Create an AWS Account](https://aws.amazon.com/resources/create-account/?p=ft&z=subnav&loc=4)
