---
title: "Supercharging Opencode with AWS Bedrock and Oh-My-Openagent"
date: 2026-02-13
lastmod: 2026-04-03
description: "A practical guide to configuring Opencode CLI with AWS Bedrock models, oh-my-openagent for multi-agent orchestration, plugins, and skills for faster agentic development"
tags: ["opencode", "aws-bedrock", "claude", "ai", "agentic-development", "oh-my-openagent", "mcp", "productivity"]
categories: ["Tools", "AI", "Development"]
---

After a few months of experimenting with AI coding assistants, I've settled on a setup that significantly accelerates my development workflow. This post walks through configuring [Opencode](https://opencode.ai/) with AWS Bedrock, the oh-my-openagent plugin for multi-agent orchestration, and various plugins and skills that make the whole system more powerful.

> **This post is a snapshot in time.** The agentic tooling ecosystem moves extremely fast - plugin names change, model recommendations shift, new features land weekly. Treat everything here as my current best knowledge as of the `lastmod` date above, not as a permanent reference.

> **Note**: oh-my-opencode was recently renamed to [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent). If you have an existing setup, update your plugin reference from `oh-my-opencode@latest` to `oh-my-openagent@latest` in `opencode.json`. The config file (`oh-my-opencode.json`) name stays the same.

> **A word of caution**: oh-my-openagent is an advanced setup. It significantly changes how Opencode behaves - it introduces a full agent hierarchy, custom hooks, opinionated prompts, and a lot of moving parts. If you're new to Opencode, I'd strongly recommend spending some time with plain Opencode first. Get comfortable with how it works, how models are configured, how sessions behave. Understanding your tooling is the only way to avoid shooting yourself in the foot when something doesn't work as expected.

## Why This Setup?

A few reasons I landed on this particular combination:

1. **Model flexibility**: Opencode works with any LLM provider - Anthropic direct, AWS Bedrock, OpenAI, local models via Ollama. No vendor lock-in.
2. **Cost management**: AWS Bedrock with cross-region inference gives access to Claude Sonnet 4.6 and Haiku 4.5 with AWS billing - useful if you're already in the AWS ecosystem.
3. **Multi-agent orchestration**: Oh-my-openagent adds specialized sub-agents that can work in parallel on different aspects of a task.
4. **Extensibility**: MCP servers, plugins, and skills let you customize the experience for your specific workflows.

## The Architecture

The setup consists of several layers:

| Layer | Purpose |
|-------|---------|
| **Opencode CLI** | Core agentic coding interface (TUI or CLI) |
| **oh-my-openagent** | Multi-agent orchestration plugin |
| **AWS Bedrock** | LLM provider with Claude models |
| **MCP Servers** | External tool integrations |
| **Plugins** | System-level extensions |
| **Skills** | Reusable knowledge modules |

## Prerequisites

Before starting, you'll need:

- An AWS account with Bedrock access enabled
- AWS CLI configured with credentials (`aws configure`)
- Basic comfort with the terminal

## Step 1: Install Opencode

Follow the [official installation guide](https://opencode.ai/docs) for your platform. Verify the installation:

```bash
opencode --version
```

## Step 2: Configure AWS Bedrock

Opencode supports AWS Bedrock out of the box. The model format is `amazon-bedrock/<model-id>`.

For cross-region inference (recommended for better availability), use the `global.` prefix:

```
amazon-bedrock/global.anthropic.claude-sonnet-4-6
amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0
```

### Authentication options

There are two ways to authenticate with Bedrock - you don't need to choose upfront, Opencode handles both:

**Option A - AWS CLI profile (classic)**: If you already have `aws configure` set up, Opencode picks it up automatically. Nothing extra needed.

```bash
# Check your current identity
aws sts get-caller-identity

# If not configured:
aws configure
```

**Option B - API key via TUI (easier)**: Opencode's interactive TUI has a built-in auth flow for Bedrock that accepts an AWS access key ID and secret directly - no CLI setup required. Run `opencode auth login`, select AWS Bedrock as the provider, and enter your credentials when prompted. Useful if you're on a machine without the AWS CLI or want to use a dedicated key.

Either way, the IAM principal you use needs at minimum:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

## Step 3: Install Oh-My-Openagent

[Oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) is the plugin that transforms Opencode into a multi-agent system. It adds specialized agents that can work in parallel on different aspects of your tasks.

The quickest way to get started is the interactive installer, which walks you through provider setup and writes the config for you:

```bash
bunx oh-my-openagent install
```

Alternatively, configure it manually by editing your files directly as shown below.

Edit `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "oh-my-openagent@latest"
  ]
}
```

### Configure Agent Models

Create `~/.config/opencode/oh-my-opencode.json` to specify which models each agent uses:

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/master/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "amazon-bedrock/global.anthropic.claude-opus-4-6"
    },
    "hephaestus": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "oracle": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "librarian": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "explore": {
      "model": "amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0"
    },
    "multimodal-looker": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "prometheus": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "metis": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "momus": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "atlas": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    }
  },
  "categories": {
    "visual-engineering": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "ultrabrain": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "deep": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "artistry": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "quick": {
      "model": "amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0"
    },
    "unspecified-low": {
      "model": "amazon-bedrock/global.anthropic.claude-haiku-4-5-20251001-v1:0"
    },
    "unspecified-high": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    },
    "writing": {
      "model": "amazon-bedrock/global.anthropic.claude-sonnet-4-6"
    }
  }
}
```

### The Agent Hierarchy

Oh-my-openagent provides a full team of specialized agents:

| Agent | Role | Model tier |
|-------|------|------------|
| **Sisyphus** | Main orchestrator - delegates, plans, ships | Opus |
| **Hephaestus** | Implementation-focused builder | Sonnet |
| **Oracle** | High-quality consultation for architecture and hard debugging | Sonnet |
| **Librarian** | Research external docs, OSS examples, best practices | Sonnet |
| **Explore** | Fast codebase grep and pattern discovery | Haiku (cheap, fast) |
| **Prometheus** | Pre-task planning and interview-style scope definition | Sonnet |
| **Metis** | Pre-planning consultant - surfaces ambiguities before work starts | Sonnet |
| **Momus** | Plan reviewer - critiques work plans for gaps and clarity | Sonnet |
| **Atlas** | General-purpose background agent | Sonnet |
| **Multimodal Looker** | Image and visual analysis | Sonnet |

The model tiering is deliberate: **Opus** for Sisyphus only - it's the orchestrator that reasons about the whole task, so quality here pays the biggest dividends. **Sonnet** for most specialist agents and categories. **Haiku** for high-frequency, low-complexity operations where speed matters more than depth. Delegated categories (below) never use Opus - Sisyphus dispatches those tasks, not the other way around.

### Task Categories

Beyond named agents, oh-my-openagent supports task categories that let Sisyphus delegate work to a domain-appropriate model:

| Category | Model | When used |
|----------|-------|-----------|
| `visual-engineering` | Sonnet | Frontend, UI/UX, CSS, animations |
| `ultrabrain` | Sonnet | Hard logic, architecture decisions |
| `deep` | Sonnet | Autonomous research + end-to-end implementation |
| `artistry` | Sonnet | Creative, unconventional problem-solving |
| `quick` | Haiku | Single-file changes, typos, trivial edits |
| `unspecified-low` | Haiku | Low-effort tasks that don't fit other categories |
| `unspecified-high` | Sonnet | Higher-effort tasks that don't fit other categories |
| `writing` | Sonnet | Documentation, prose, technical writing |

## Step 4: Add Useful Plugins

Plugins extend Opencode's capabilities at the system level. Here are some I find useful:

```json
{
  "plugin": [
    "oh-my-openagent@latest",
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
    }
  }
}
```

Some MCP servers I use regularly:

| Server | Purpose |
|--------|---------|
| **aws-documentation** | Query AWS docs directly |
| **cdk-mcp-server** | CDK construct information |

### Keep most servers disabled by default

Every enabled MCP server adds tools to the agent's context at the start of each session - even if you never use them. With several servers enabled, you're burning tokens on tool descriptions before you've typed a single word.

My approach: disable everything in `opencode.json` with `"enabled": false`, and only turn on what I actually need for a given task. Opencode makes this fast - hit `Ctrl+P` to open the command palette and toggle MCP servers on the fly, or use `/` commands to enable one before starting a specific task.

```json
{
  "mcp": {
    "awslabs.cdk-mcp-server": {
      "command": ["uvx", "awslabs.cdk-mcp-server@latest"],
      "enabled": false
    }
  }
}
```

The only server I keep permanently enabled is `aws-documentation` since it's useful across almost every task. Everything else gets toggled on demand.

## Step 6: Install Skills

Skills are reusable knowledge modules - markdown files that give agents specialized knowledge about a topic. They're loaded on-demand, so they don't bloat every session.

### Where to Find Skills

The [skills.sh](https://skills.sh) ecosystem is the main source for community skills I use regularly, but it's not the only option - skills are just directories with a `SKILL.md` file, so you can share them as Git repos, Gists, or any other way you'd share a markdown file. Install from skills.sh via:

```bash
npx skills add <publisher>/<skill-name>
```

Browse the [skills.sh leaderboard](https://skills.sh) to find what's available - the ecosystem is growing fast and covers a wide range of domains.

Skills are stored in `~/.config/opencode/skills/` - each one is a directory containing a `SKILL.md` file. You can also write your own: create a directory there with a `SKILL.md` that captures whatever specialized knowledge you want the agent to have (internal tooling docs, project conventions, workflow patterns, etc.).

A practical example: I have custom skills for working with [Obsidian](https://obsidian.md) - one for Obsidian-flavored markdown syntax (wikilinks, callouts, properties, embeds), one for the Bases feature (database-like views of notes), and one for interacting with my vault over MCP. Without these, the agent would produce generic markdown that doesn't render correctly in Obsidian. With them, it writes notes that slot straight into my vault.

### Configuring Skills for an Agent

Once installed, you reference skills by name when delegating tasks. Oh-my-openagent's Sisyphus agent automatically detects available skills and loads the relevant ones based on context. You can also reference them explicitly in your prompts.

The [oh-my-openagent README](https://github.com/code-yeongyu/oh-my-openagent) maintains an up-to-date list of built-in and community skills.

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
| Haiku 4.5 | Exploration, quick/trivial tasks | $ |
| Sonnet 4.6 | Most coding tasks, research, specialist agents | $$ |
| Opus 4.6 | Main orchestration (Sisyphus) | $$$ |

My configuration puts Sisyphus on Opus 4.6 - it's the agent that reasons about the whole task, decides what to delegate, and synthesizes results, so the quality improvement is worth the cost. Everything else runs on Sonnet 4.6, with Haiku for `explore`, `quick`, and `unspecified-low` categories where speed matters more than depth.

> **Note on model choice**: oh-my-openagent will warn you at startup if Sisyphus isn't running on Claude Opus. The plugin is explicitly optimised for it - reduced orchestration quality, weaker delegation, and less reliable task completion are all called out as consequences of using a lighter model. The warning references Opus 4.5, but Opus 4.6 on Bedrock is the direct successor and works well. If you're using a non-Opus model for Sisyphus to save cost, go in with eyes open.

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
- [oh-my-openagent GitHub](https://github.com/code-yeongyu/oh-my-openagent) - Multi-agent plugin
- [AWS Bedrock Claude Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) - Model availability
- [MCP Specification](https://modelcontextprotocol.io/) - Model Context Protocol
- [skills.sh](https://skills.sh) - Community skills ecosystem

---

*This setup has become central to my daily development workflow. Curious to hear how others are configuring their agentic development environments - what models, plugins, or workflows have you found effective?*
