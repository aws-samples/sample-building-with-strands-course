# AWS Account and Credentials Setup

This guide walks you through creating an AWS account and configuring credentials so you can run the course samples.

## 1. Create an AWS Account

If you don't already have one, create a free AWS account:

https://aws.amazon.com/resources/create-account/?p=ft&z=subnav&loc=4

The free tier gives you access to Amazon Bedrock foundation models including Amazon Nova and Meta Llama. Claude models may require a one-time use-case form (submitted automatically on first use).

## 2. Install the AWS CLI

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Verify
aws --version
```

## 3. Configure Credentials

```bash
aws configure
```

You'll be prompted for:
- **Access Key ID**: From your IAM user or the IAM Identity Center portal
- **Secret Access Key**: Paired with the above
- **Default region**: `us-east-1` recommended (broadest model availability)
- **Output format**: `json`

Alternatively, set environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## 4. Verify Access

```bash
aws sts get-caller-identity
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?contains(modelId, 'nova')].[modelId]" --output text
```

If both commands return results, you're ready to go.

## 5. Claude Model Access

Claude models on Bedrock may require a one-time use-case acknowledgment form. This is submitted automatically the first time you invoke a Claude model. It's not the same as the old "enable model access" flow - you don't need to manually enable anything in the console. If your first Claude call fails with an access error, wait a couple minutes and retry.

## Next Steps

Return to the [main README](./README.md) and start running samples.
