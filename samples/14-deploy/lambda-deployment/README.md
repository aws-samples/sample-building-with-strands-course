# Lambda Deployment

Deploy the customer service agent to AWS Lambda using SAM (Serverless Application Model). This is a free-tier friendly option that gets your agent running behind an API Gateway endpoint.


## Prerequisites

- AWS credentials configured (see [SETUP.md](../../../SETUP.md))
- AWS SAM CLI installed:

```bash
# macOS
brew install aws-sam-cli

# Linux / pip
pip install aws-sam-cli
```

## Files

- **lambda_handler.py** - FastAPI app wrapped with Mangum for Lambda. Same agent code as the local/AgentCore versions.
- **requirements.txt** - Python dependencies packaged into the Lambda.
- **template.yaml** - SAM template defining the Lambda function, API Gateway, and IAM permissions.

## Deploy

```bash
# Build the Lambda package
sam build

# Deploy (first time, interactive prompts)
sam deploy --guided
```

SAM will ask you for:
- Stack name (e.g., `customer-service-agent`)
- Region (e.g., `us-east-1`)
- Confirm changes before deploy: Yes
- Allow SAM CLI IAM role creation: Yes

Once deployed, SAM outputs the API Gateway URL.

## Test

```bash
# Replace with your actual API URL from the deploy output
API_URL="https://abc123.execute-api.us-east-1.amazonaws.com/Prod"

# Health check
curl $API_URL/health

# Invoke the agent
curl -X POST $API_URL/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hi, I am customer C-1001. Can you check my recent orders?"}'
```

## Clean Up

```bash
sam delete --stack-name customer-service-agent
```

## Adding Session Persistence

The basic deployment above is stateless. Each invocation starts fresh. To add persistence:

1. Create a DynamoDB table for sessions
2. Use `DynamoDBSessionManager` from Strands (or write a custom one)
3. Pass a session ID in the request payload and use it to load/save state

This is what AgentCore handles automatically. On Lambda, you wire it yourself.

## Limitations

- 15-minute execution limit (long multi-turn conversations may time out)
- Cold starts add latency on first invocation
- No built-in session isolation between concurrent users
- You manage auth, memory, and observability separately
