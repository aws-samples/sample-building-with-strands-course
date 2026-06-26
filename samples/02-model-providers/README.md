# Model Providers

Strands separates agent logic from model selection. You can swap the underlying model provider without changing your agent code - your tools, system prompt, and orchestration logic stay identical regardless of which provider you use.

## Files

- **model_providers.py** - A single file with multiple provider configurations. Uncomment the provider you want to use and run.

## Running

```bash
python model_providers.py
```

## Supported Providers

| Provider | Setup Required |
|----------|---------------|
| **Bedrock** (default) | AWS credentials configured |
| **Anthropic** | `ANTHROPIC_API_KEY` environment variable |
| **OpenAI** | `OPENAI_API_KEY` environment variable |
| **Ollama** | Ollama running locally (`ollama serve`) |

## Key Concepts

- **Provider abstraction**: The `Agent` class accepts a `model=` parameter that takes any provider instance. Your agent code doesn't know or care which model is behind it.
- **Local models**: Ollama lets you run models entirely on your machine - useful for development, offline use, or when you want to avoid API costs.
- **Cross-provider portability**: Build your agent once, then swap models based on cost, latency, capability, or deployment requirements.

## Further Reading

- [Strands Agents: Model Providers](https://strandsagents.com/docs/user-guide/concepts/model-providers/)
- [Amazon Bedrock Provider](https://strandsagents.com/docs/user-guide/concepts/model-providers/amazon-bedrock/)
- [Ollama Provider](https://strandsagents.com/docs/user-guide/concepts/model-providers/ollama/)
