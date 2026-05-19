# Strands Agents SDK Course

Code samples for the Strands Agents SDK video course. Each folder in `samples/` corresponds to a video and contains runnable examples.

## Prerequisites

- Python 3.10+
- An AWS account (free tier works) OR API keys for your preferred model provider

## Setup

```bash
# Clone the repo
git clone https://github.com/morganwillisaws/strands-course.git
cd strands-course

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install strands-agents strands-agents-tools
```

## Model Provider Setup

Strands is model-provider agnostic. Pick one (or more) of the following:

### Amazon Bedrock (default)

Bedrock is the default provider. You need an AWS account with Bedrock model access enabled.

1. Create an AWS account at https://aws.amazon.com/free
2. Enable model access in the Bedrock console (Claude models recommended)
3. Configure credentials locally:
```bash
aws configure
```
Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-west-2
```

### Anthropic (direct API)

```bash
pip install "strands-agents[anthropic]"
export ANTHROPIC_API_KEY=your_key
```

### OpenAI

```bash
pip install "strands-agents[openai]"
export OPENAI_API_KEY=your_key
```

### Ollama (local models, no API key needed)

```bash
pip install "strands-agents[ollama]"
brew install ollama        # macOS
ollama serve               # start the server
ollama pull llama3.1       # pull a model
```

## Course Structure

| Folder | Video | Topic |
|--------|-------|-------|
| `video-01-agent-loop` | 1 | Agent harnesses and the agent loop |
| `video-02-model-providers` | 2 | Swapping model providers |
| `video-03-mcp-tools` | 3 | MCP servers and the tools ecosystem |
| `video-04-callbacks-streaming` | 4 | Callbacks and streaming |
| `video-05-hooks` | 5 | Lifecycle hooks |
| `video-06-plugins-skills` | 6 | Plugins and skills |
| `video-07-steering` | 7 | Steering handlers |
| `video-08-conversation-management` | 8 | Conversation management |
| `video-09-session-managers` | 9 | Session persistence |
| `video-10-agents-as-tools` | 10 | Agents as tools |
| `video-11-graphs` | 11 | Graph workflows |
| `video-12-swarms` | 12 | Agent swarms |
| `video-13-evals` | 13 | Evaluating agents |

## Running Examples

Each video folder is self-contained. Run examples from within the folder:

```bash
cd samples/video-01-agent-loop
python3 simple_agent.py
```

For videos 6+ that use the customer service example, run from the video folder so the `./skills` directory is found:

```bash
cd samples/video-07-steering
python3 customer_service_steering.py
```

## Additional Dependencies

Some videos require extra packages:

```bash
# Video 4 (FastAPI streaming)
pip install fastapi uvicorn

# Video 13 (Evaluations)
pip install strands-agents-evals
```

## Links

- [Strands Agents Documentation](https://strandsagents.com)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Agent Skills Specification](https://agentskills.io)
