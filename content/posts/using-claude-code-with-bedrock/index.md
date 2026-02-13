---
title: "Using Claude Code with Bedrock Backend"
date: 2026-02-13
draft: false
description: "A guide to setting up and using Claude Code CLI with Amazon Bedrock backend"
tags: ["claude", "anthropic", "bedrock", "aws", "cli", "generative-ai", "programming"]
---

> **⚠️ Model IDs change frequently**: The model IDs and configuration in this guide reflect the state at the time of writing. Anthropic regularly releases new Claude versions on Bedrock. Always check the [AWS Bedrock supported models documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) and [Bedrock model IDs reference](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html) for the most current model identifiers and regional availability.

Claude Code is a powerful CLI tool that allows you to interact with Claude AI models directly from your terminal. This guide will walk you through setting up Claude Code to work with Amazon Bedrock as the backend provider.

## What is Claude Code?

Claude Code is a powerful CLI tool that brings Claude's AI capabilities to your terminal. It provides an interactive coding assistant that understands your local files and can help with various software engineering tasks.

Check out this video for a quick overview of Claude Code in action:

{{< youtube AJpK3YTTKZ4 >}}

## Prerequisites

- AWS account with [Bedrock access enabled](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html)
- [Node.js (v14 or later) and npm](https://nodejs.org/en/download/) installed on your system
- AWS CLI installed and [configured with appropriate permissions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Access to Anthropic Claude models in your AWS Bedrock account (Claude Sonnet 4.5 recommended)

## Setup Steps

1. **Install Claude Code CLI**

   Install the official Claude Code CLI tool from Anthropic:

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

   You can verify the installation was successful by running:

   ```bash
   claude --version
   ```

   For detailed installation instructions, refer to the [official Claude Code documentation](https://docs.anthropic.com/claude/docs/claude-code).

2. **Configure AWS Credentials**

   Ensure your AWS credentials are properly configured with permissions for Bedrock:

   ```bash
   aws configure
   ```

   You'll need to enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (use a region where Claude models are available, like `us-east-1`)
   - Default output format (recommended: `json`)

   For IAM permissions, your user/role needs:
   - `bedrock:InvokeModel`
   - `bedrock:InvokeModelWithResponseStream`
   - `bedrock:ListFoundationModels`
   - `bedrock:ListInferenceProfiles`
   
   For detailed AWS credentials setup, see the [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

3. **Enable Claude Model Access in Bedrock**

   1. Navigate to the [AWS Bedrock console](https://console.aws.amazon.com/bedrock) in a [supported region](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) (e.g., `us-east-1`)

   2. Complete Bedrock onboarding if needed (accept terms and conditions)

   3. Go to "Model access" → "Manage model access"

   4. Find "Anthropic" and enable the Claude models you want to use:
      - **Claude Sonnet 4.5** (recommended) - `global.anthropic.claude-sonnet-4-5-20250929-v1:0`
      - **Claude Opus 4.6** (most capable) - for complex reasoning and agentic tasks
      - **Claude Haiku 4.5** (fast/cheap) - `us.anthropic.claude-haiku-4-5-20251001-v1:0`
   
   5. Click "Request model access" and "Save changes"

   6. Wait a few minutes for access to be granted (status will change from "Pending" to "Access granted")

   You can verify access using the AWS CLI:
   ```bash
   aws bedrock list-foundation-models --region us-east-1 | grep anthropic.claude
   ```

   If you encounter issues, check that your account has completed [Bedrock onboarding](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html#setting-up-manage-access) and review [service quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) in your selected region.

4. **Set Environment Variables**

   To tell Claude Code to use Bedrock as its backend, you need to set some environment variables. These are special settings that tell the software which model to use and where to find it.

   ### Quick Start (Temporary Use)

   If you just want to try Claude Code with Bedrock quickly, you can run these commands in your terminal before using Claude:

   ```bash
   # Copy and paste these lines into your terminal
   export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-5-20250929-v1:0'
   export CLAUDE_CODE_USE_BEDROCK=1
   ```

   After running these commands in your terminal window, you can immediately use Claude Code with Bedrock by running `claude` commands in that same terminal window. However, these settings will only last until you close that terminal window.

   ### For US East Region (Virginia)
   
   If you're using the US East region (which is the default for many AWS accounts):

   ```bash
   export AWS_REGION='us-east-1'
   ```

   ### Optional: Configure Haiku Model

   Claude Code uses a smaller/faster model for some operations. By default, it auto-selects the Haiku model, but you can manually specify it:

   ```bash
   export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
   ```

   ### For Permanent Configuration

   To avoid having to set these variables every time, you can make them permanent by adding them to your shell's configuration file:

   1. Open your shell configuration file in a text editor:
      - For Mac/Linux with Bash: `nano ~/.bashrc` or `nano ~/.bash_profile`
      - For Mac with Zsh: `nano ~/.zshrc`
      - For Fish shell: `nano ~/.config/fish/config.fish`

   2. Add these lines at the end of the file:
      ```bash
      # Claude Code Bedrock configuration
      export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-5-20250929-v1:0'
      export CLAUDE_CODE_USE_BEDROCK=1
      export AWS_REGION='us-east-1'  # Change this if using a different region
      # Optional: explicitly set Haiku model version
      # export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
      ```

   3. Save the file and exit the editor
      - In nano: Press `Ctrl+O` to save, then `Enter`, then `Ctrl+X` to exit

   4. Apply the changes by reloading your configuration:
      ```bash
      # For bash (choose one depending on which file you edited)
      source ~/.bashrc
      # OR
      source ~/.bash_profile
      
      # For zsh
      source ~/.zshrc
      
      # For fish
      source ~/.config/fish/config.fish
      ```

   After completing these steps, Claude Code will use Bedrock in all your terminal sessions.

## Using Claude Code with Bedrock

Claude Code has access to the directory where it's executed, allowing it to analyze your project files, understand your codebase, and assist with development tasks. It guides you through complex processes by suggesting next steps and requesting permission before running commands that modify your files or system.

Once configured with Bedrock, you can start using Claude Code with commands like:

```bash
# Run Claude in interactive mode (most useful way to use Claude Code)
claude

# Ask Claude a question
claude "How do I optimize Docker images?"

# Run Claude with context from specific files
claude --context path/to/file.py "Explain this code"

# Multiple contexts for more comprehensive analysis
claude --context file1.js --context file2.js "How do these components interact?"
```

## Benefits of Using Bedrock Backend

- Data privacy - your queries stay within your AWS environment
- Cost management through AWS billing
- Access control through IAM policies
- Lower latency (depending on region configuration)
- Integration with AWS Guardrails for content filtering

## Alternative Authentication Methods

### Using AWS SSO

If your organization uses AWS SSO, you can configure Claude Code to automatically refresh credentials:

1. Create or edit `~/.claude/settings.json`:
   ```json
   {
     "awsAuthRefresh": "aws sso login --profile myprofile",
     "env": {
       "AWS_PROFILE": "myprofile"
     }
   }
   ```

2. Claude Code will automatically detect expired credentials and run the refresh command.

### Using Bedrock API Keys (Simplified Auth)

For simpler setups without full AWS CLI configuration, you can use Bedrock API Keys:

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
export CLAUDE_CODE_USE_BEDROCK=1
```

This eliminates the need for AWS CLI configuration and is ideal for developers who only need Bedrock access.

## Enterprise Features

### AWS Guardrails Integration

You can implement content filtering via Bedrock Guardrails by adding custom headers:

```json
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

This is useful for compliance-focused organizations that need to filter or moderate AI responses.

## Troubleshooting

If you encounter issues with Claude Code using Bedrock, try these troubleshooting steps:

### Connection and Authentication Issues

1. **Verify AWS Credentials and Permissions**
   ```bash
   # Check if your credentials are properly configured
   aws sts get-caller-identity
   
   # Verify you have Bedrock access
   aws bedrock list-foundation-models --region us-east-1
   ```

2. **Confirm Model Access**
   ```bash
   # Check if Claude Sonnet 4.5 is available to your account
   aws bedrock list-foundation-models --query "modelSummaries[?contains(modelId, 'claude')]" --region us-east-1
   ```

3. **Region Configuration**
   - Ensure your `AWS_REGION` environment variable (or default region) is set to a region where Claude models are available
   - Verify model availability in your region in the [Bedrock service endpoints documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints-service.html)

### Common Error Messages

- **"AccessDeniedException"** - Check IAM permissions; your user/role needs `bedrock:InvokeModel` permission
- **"ValidationException: Model not found"** - Verify model ID and region compatibility
- **"ResourceNotFoundException"** - Ensure you've completed model access approval
- **"ThrottlingException"** or **"429 Too many tokens, please wait before trying again."** - You may have exceeded your quota or rate limit. When this happens, the Claude CLI will display a message saying "429 Too many tokens, please wait before trying again." This is because AWS Bedrock enforces rate limits on API requests to prevent abuse and ensure fair resource allocation across all users.

  **What's happening:** AWS Bedrock has token rate limits that restrict how many tokens you can process within a specific timeframe (usually per minute). When you exceed this limit, AWS returns a 429 error code (Too Many Requests), which Claude CLI then displays as a user-friendly message.
  
  **How to fix it:**
  - Wait a few minutes before trying again to allow your token quota to refresh
  - For production applications, implement exponential backoff and retry logic
  - If you consistently hit limits, request a [quota increase through the AWS Service Quotas console](https://console.aws.amazon.com/servicequotas/)
  - Check your [Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) to understand your current limits

### Environment Debugging

Run Claude Code with debug logging enabled:

```bash
DEBUG=* claude "Your prompt here"
```

For persistent issues, you can check AWS CloudTrail logs to see if your Bedrock API calls are being made and any errors they're returning:

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=InvokeModel
```

For more comprehensive troubleshooting and documentation:
- [Claude Code documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Bedrock troubleshooting guide](https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting.html)

## Meta: How This Post Was Created

This post was originally created using Claude Code CLI in interactive mode, shortly after Claude Code's initial release when there were no mature open-source alternatives. The initial content and featured image were generated entirely through AI-assisted conversation.

Since then, the post has been significantly refactored and updated to reflect the latest model versions and configuration options.

**Author's note**: I have since migrated my AI coding workflow to [OpenCode](/posts/opencode-aws-bedrock-setup/) and [AWS Kiro](https://kiro.dev/) - both excellent alternatives that emerged after Claude Code's launch. This post remains relevant for those who prefer or need to use Claude Code with Bedrock.