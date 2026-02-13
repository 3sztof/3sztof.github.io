---
title: "Supercharging Opencode with AWS Bedrock, Oh-My-Opencode, and Custom Skills"
date: 2026-02-13
description: "A practical guide to configuring Opencode CLI with AWS Bedrock models, oh-my-opencode for multi-agent orchestration, plugins, and custom skills for faster agentic development"
tags: ["opencode", "aws-bedrock", "claude", "ai", "agentic-development", "oh-my-opencode", "mcp", "productivity"]
categories: ["Tools", "AI", "Development"]
---

After a few months of experimenting with AI coding assistants, I've settled on a setup that significantly accelerates my development workflow. This post walks through configuring [Opencode](https://opencode.ai/) with AWS Bedrock, the oh-my-opencode plugin for multi-agent orchestration, and various plugins and skills that make the whole system more powerful.

## Why This Setup?

A few reasons I landed on this particular combination:

1. **Model flexibility**: Opencode works with any LLM provider - Anthropic direct, AWS Bedrock, OpenAI, local models via Ollama. No vendor lock-in.
2. **Cost management**: AWS Bedrock with cross-region inference gives access to Claude Opus 4.5, Sonnet 4.5, and Haiku 4.5 with AWS billing - useful if you're already in the AWS ecosystem.
3. **Multi-agent orchestration**: Oh-my-opencode adds specialized sub-agents that can work in parallel on different aspects of a task.
4. **Extensibility**: MCP servers, plugins, and skills let you customize the experience for your specific workflows.

## The Architecture

The setup consists of several layers:

| Layer | Purpose |
|-------|---------|
| **Opencode CLI** | Core agentic coding interface (TUI or CLI) |
| **oh-my-opencode** | Multi-agent orchestration plugin |
| **AWS Bedrock** | LLM provider with Claude models |
| **MCP Servers** | External tool integrations |
| **Plugins** | System-level extensions |
| **Skills** | Reusable knowledge modules |

## Prerequisites

Before starting, you'll need:

- [Node.js](https://nodejs.org/) v18 or later
- An AWS account with Bedrock access enabled
- AWS CLI configured with credentials (`aws configure`)
- Basic comfort with the terminal

## Step 1: Install Opencode

```bash
# Install globally via npm
npm install -g @opencode-ai/cli

# Or use npx to run directly
npx opencode
```

Verify the installation:

```bash
opencode --version
```

## Step 2: Configure AWS Bedrock

Opencode supports AWS Bedrock out of the box. The model format is `amazon-bedrock/<model-id>`.

For cross-region inference (recommended for better availability), use the `global.` prefix:

```
amazon-bedrock/global.anthropic.claude-opus-4-5-20251101-v1:0
amazon-bedrock/global.anthropic.claude-sonnet-4-5-20250929-v1:0
amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0
```

Make sure your AWS credentials are configured:

```bash
# Check your current identity
aws sts get-caller-identity

# If not configured, run:
aws configure
```

You'll need appropriate IAM permissions for Bedrock. At minimum:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

## Step 3: Install Oh-My-Opencode

[Oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) is the plugin that transforms Opencode into a multi-agent system. It adds specialized agents that can work in parallel on different aspects of your tasks.

```bash
# Add to your opencode config
# In ~/.config/opencode/opencode.json, add to the plugin array:
```

Edit `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "oh-my-opencode@latest"
  ]
}
```

### Configure Agent Models

Create `~/.config/opencode/oh-my-opencode.json` to specify which models each agent uses:

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "amazon-bedrock/global.anthropic.claude-opus-4-5-20251101-v1:0"
    },
    "oracle": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    "librarian": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    "explore": {
      "model": "amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0"
    }
  },
  "categories": {
    "visual-engineering": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    "ultrabrain": {
      "model": "amazon-bedrock/global.anthropic.claude-opus-4-5-20251101-v1:0"
    },
    "quick": {
      "model": "amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0"
    }
  }
}
```

### The Agent Hierarchy

Oh-my-opencode provides several specialized agents:

| Agent | Role | Recommended Model |
|-------|------|-------------------|
| **Sisyphus** | Main orchestrator, handles complex multi-step tasks | Opus (expensive but capable) |
| **Oracle** | High-quality consultation for architecture decisions | Sonnet |
| **Librarian** | Research external docs, examples, best practices | Sonnet |
| **Explore** | Fast codebase exploration, pattern discovery | Haiku (cheap, fast) |
| **Hephaestus** | Implementation-focused agent | Opus or Sonnet |

The key insight is **model tiering**: use expensive models (Opus) for complex reasoning, mid-tier (Sonnet) for most tasks, and cheap models (Haiku) for exploration and simple operations.

## Step 4: Add Useful Plugins

Plugins extend Opencode's capabilities at the system level. Here are some I find useful:

```json
{
  "plugin": [
    "oh-my-opencode@latest",
    "@mathew-cf/opencode-terminal-notifier",
    "envsitter-guard@latest",
    "@tarquinen/opencode-smart-title",
    "opencode-wakatime"
  ]
}
```

| Plugin | Purpose |
|--------|---------|
| **terminal-notifier** | Desktop notifications when tasks complete |
| **envsitter-guard** | Prevents accidental exposure of .env secrets |
| **smart-title** | Auto-generates meaningful session titles |
| **wakatime** | Tracks coding time for productivity metrics |

## Step 5: Configure MCP Servers

MCP (Model Context Protocol) servers give Opencode access to external tools and data sources. Add them to your `opencode.json`:

```json
{
  "mcp": {
    "awslabs.aws-documentation-mcp-server": {
      "type": "local",
      "command": ["uvx", "awslabs.aws-documentation-mcp-server@latest"],
      "environment": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "enabled": true,
      "timeout": 120000
    },
    "awslabs.cdk-mcp-server": {
      "type": "local",
      "command": ["uvx", "awslabs.cdk-mcp-server@latest"],
      "enabled": true
    },
    "smart-connections": {
      "type": "local",
      "command": ["node", "/path/to/smart-connections-mcp/dist/index.js"],
      "environment": {
        "SMART_VAULT_PATH": "/path/to/obsidian/vault"
      },
      "enabled": true
    }
  }
}
```

Some MCP servers I use regularly:

| Server | Purpose |
|--------|---------|
| **aws-documentation** | Query AWS docs directly |
| **cdk-mcp-server** | CDK construct information |
| **smart-connections** | Semantic search over Obsidian notes |
| **excel** | Read/write Excel files |

## Step 6: Install Skills

Skills are reusable knowledge modules that agents can load on-demand. They're markdown files that give agents specialized knowledge about specific topics.

```bash
# Skills are stored in ~/.config/opencode/skills/
# Each skill is a directory with a SKILL.md file

# Install a skill from the ecosystem
npx skills add jackspace/claudeskillz@hugo

# Or create your own
mkdir -p ~/.config/opencode/skills/my-skill
# Add SKILL.md with your specialized knowledge
```

Skills I currently have installed:

- **hugo** - Static site generation with Hugo
- **git-commit** - Conventional commit message formatting
- **manimce-best-practices** - Manim animation library patterns
- **obsidian** - Obsidian vault interaction

## Step 7: Create an AGENTS.md

The `AGENTS.md` file in `~/.config/opencode/` provides global instructions that all agents follow. This is where you codify your engineering principles:

```markdown
# Engineering Principles

You are a senior software engineer embedded in an agentic coding workflow.

## Core Behaviors

### Assumption Surfacing (Critical)
Before implementing anything non-trivial, explicitly state your assumptions:
- Never silently fill in ambiguous requirements
- Surface uncertainty early

### Push Back When Warranted
You are not a yes-machine. When the human's approach has clear problems:
- Point out the issue directly
- Propose an alternative
- Accept their decision if they override

### Simplicity Enforcement
Prefer the boring, obvious solution. Cleverness is expensive.
```

This ensures consistent behavior across all agents and sessions.

## Practical Workflows

### Parallel Exploration

When tackling an unfamiliar codebase, fire multiple explore agents in parallel:

```
> Search for authentication patterns in this repo
> Also look for how error handling is done
> And find the database access patterns
```

The explore agent (running Haiku) quickly surfaces patterns while you focus on the main task.

### Delegating to Specialists

For complex tasks, the main agent can delegate to specialists:

```
> Implement a new REST endpoint for user preferences
```

Behind the scenes, Sisyphus might:
1. Fire `explore` to understand existing endpoint patterns
2. Consult `oracle` for architecture decisions
3. Delegate implementation to a sub-agent
4. Run verification

### Research-Heavy Tasks

For tasks requiring external knowledge:

```
> How should I implement DynamoDB single-table design for this use case?
```

The `librarian` agent queries documentation, finds examples on GitHub, and synthesizes recommendations - all without you leaving the terminal.

## Cost Considerations

With AWS Bedrock, you pay per token. Model tiering helps manage costs:

| Model | Use Case | Relative Cost |
|-------|----------|---------------|
| Haiku 4.5 | Exploration, simple tasks | $ |
| Sonnet 4.5 | Most coding tasks | $$ |
| Opus 4.5 | Complex reasoning, architecture | $$$ |

My configuration uses Haiku for `explore` and `quick` categories, Sonnet for most work, and reserves Opus for `ultrabrain` and main orchestration.

## Troubleshooting

### "Model not found" errors

Ensure you've enabled the specific Claude models in your AWS Bedrock console. Cross-region inference models require explicit enablement.

### Slow responses

Check your AWS region. Cross-region inference (`global.` prefix) routes to the nearest available region but can add latency. Consider using region-specific model IDs if latency is critical.

### Plugin installation issues

```bash
# Clear plugin cache
rm -rf ~/.config/opencode/node_modules
rm ~/.config/opencode/package-lock.json

# Reinstall
opencode
```

### MCP server timeouts

Increase the timeout in your config:

```json
{
  "mcp": {
    "server-name": {
      "timeout": 180000
    }
  }
}
```

## Resources

- [Opencode Documentation](https://opencode.ai/docs) - Official docs
- [oh-my-opencode GitHub](https://github.com/code-yeongyu/oh-my-opencode) - Multi-agent plugin
- [AWS Bedrock Claude Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) - Model availability
- [MCP Specification](https://modelcontextprotocol.io/) - Model Context Protocol

---

*This setup has become central to my daily development workflow. Curious to hear how others are configuring their agentic development environments - what models, plugins, or workflows have you found effective?*
