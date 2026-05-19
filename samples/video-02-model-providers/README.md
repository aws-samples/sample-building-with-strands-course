# Video 2: Model Providers

This video shows how to swap the underlying model provider without changing your agent code. Strands supports Bedrock, Anthropic, OpenAI, and Ollama out of the box — your agent logic stays identical regardless of which one you pick.

## Files

- **model_providers.py** — A single file with multiple provider configurations. Uncomment the provider you want to use and run.

## Running

```bash
python model_providers.py
```

## Notes

- Each provider requires its own credentials/setup:
  - **Bedrock**: AWS credentials configured
  - **Anthropic**: `ANTHROPIC_API_KEY` environment variable
  - **OpenAI**: `OPENAI_API_KEY` environment variable
  - **Ollama**: Ollama running locally (`ollama serve`)
- Only one provider should be uncommented at a time.
