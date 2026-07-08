# Configuring Model Providers

Model choice is an architecture decision. Different models have different strengths, costs, latency characteristics, and tool-use behavior. Strands abstracts providers behind a common interface so your agent code stays the same regardless of the underlying model.

## Configuring Providers

All providers follow the same pattern: instantiate a model class, pass it to the agent.

```python
from strands import Agent
from strands.models import BedrockModel
from strands.models.anthropic import AnthropicModel
from strands.models.ollama import OllamaModel
from strands.models.openai import OpenAIModel
import os

# Amazon Bedrock (default if no model specified)
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-opus-4-6-v1"
)

# Anthropic direct API
anthropic_model = AnthropicModel(
    client_args={"api_key": os.environ["ANTHROPIC_API_KEY"]},
    model_id="claude-sonnet-4-20250514",
    max_tokens=1024,
    params={"temperature": 0.7},
)

# OpenAI
openai_model = OpenAIModel(
    client_args={"api_key": os.environ["OPENAI_API_KEY"]},
    model_id="gpt-4o",
    params={"max_tokens": 1000, "temperature": 0.7},
)

# Local with Ollama (no cloud APIs needed)
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="gemma4:latest",
)

# Use any provider — agent code stays identical
agent = Agent(model=ollama_model)
agent("Explain the agent loop in one paragraph.")

```

📂 [model_providers.py](https://github.com/aws-samples/sample-building-with-strands-course/tree/main/samples/02-model-providers/model_providers.py) — Find all code on GitHub

## Multi-Model Architectures

In sophisticated systems, different agents use different models:

- Fast/cheap model → lightweight classification
- Strong reasoning model → orchestration
- Specialized model → code generation
- Different provider entirely → evaluation/verification (avoids same-model bias)

## Ollama Setup

```bash
brew install ollama
ollama serve
ollama pull gemma3:latest

```

## Resources

- 📖 [Model Providers Docs](https://strandsagents.com/docs/user-guide/concepts/model-providers/)
- 🚀 [Getting Started Guide](https://strandsagents.com/docs/user-guide/quickstart/python/)
- 📂 [Course Code Repository](https://github.com/aws-samples/sample-building-with-strands-course)

