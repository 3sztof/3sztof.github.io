---
title: "I take it back: OpenClaw wants a boring always-on box"
date: 2026-10-06
description: "A follow-up to my AgentCore TIL. Serverless OpenClaw loses most of what makes it interesting. I moved mine to a single Graviton EC2 instance, and now it extends itself, keeps long-term memory, and dreams."
tags: ["openclaw", "aws", "bedrock", "ec2", "graviton", "pulumi", "ai", "agents"]
categories: ["Posts"]
draft: false
---

[OpenClaw](https://github.com/openclaw/openclaw) is a personal AI agent you self-host - it lives on a machine of your own, talks to you over Telegram, Slack, or SSH, and can run commands, keep long-term memory, and extend itself over time. Back in March I wrote a [TIL about hosting OpenClaw on Bedrock AgentCore](/til/openclaw-on-bedrock-agentcore/) and said I'd try the serverless and non-serverless approaches and form a real opinion. I have one now: for the way I use it, serverless OpenClaw throws away most of the reasons to run OpenClaw at all.

## What serverless takes away

The AgentCore sample is good engineering. A Router Lambda takes the Telegram or Slack webhook, works out who you are, and starts a per-user Firecracker microVM with a workspace synced to S3. You pay nothing while nobody is talking to it.

That last property is the problem. The OpenClaw features I ended up caring about all assume a process that keeps running when I'm not talking to it:

- **Heartbeat and cron.** The agent wakes up on a schedule, checks on things, and runs jobs it set up for itself. A session that only exists while a message is in flight has nothing to wake up.
- **Dreaming.** OpenClaw consolidates memory in a scheduled background sweep (more on this below). That sweep is a cron job too.
- **A machine it can change.** When the agent installs a package, writes a systemd timer, or pulls a Docker image, I want that to still be there tomorrow. A rebuilt microVM with a synced workspace folder is not the same thing as a box the agent lives on.

Strip those away and you have a capable chatbot with a filesystem. That's useful, but it's not why people are excited about OpenClaw.

## What I run instead

One `t4g.medium` Graviton instance in `eu-central-1`, provisioned with about 20 resources of Pulumi Python (I [compared Pulumi and CDK](/posts/pulumi-vs-cdk-python/) in an earlier post):

```text
Phone (Telegram / OpenClaw app / SSH)
  └── Tailscale (WireGuard, zero public ports)
       └── EC2 t4g.medium (Graviton, Ubuntu 24.04 ARM64)
            ├── OpenClaw gateway (loopback only)
            │    ├── Amazon Bedrock via IAM instance profile
            │    ├── Exa web search, Telegram, GitHub MCP
            │    └── Skill Workshop
            ├── OpenCode, preconfigured for Bedrock
            ├── Docker
            └── 30 GB encrypted gp3 EBS, delete_on_termination: false
```

The security group has no ingress rules. Everything goes through Tailscale, with SSM Session Manager as the emergency hatch. Bedrock access comes from the instance profile, so there's no model API key to leak or rotate. The EBS volume outlives the instance, which means the agent's memory and everything it installed survived several instance replacements and an AZ move.

It costs about $35-45 a month: roughly $24 for the instance, $2.40 for the volume, $2 for Secrets Manager, plus Bedrock usage. Tailscale sits on its personal tier, which is free. `make stop` brings the compute cost to zero when I'm away.

## It extends itself

OpenClaw's exec tool runs in full mode, with a seeded allowlist so routine commands like `git`, `gh`, `aws` and `python3` don't prompt every time. The Skill Workshop - OpenClaw's self-improvement loop for authoring and refining its own skills - runs autonomously. After any long turn, a background reviewer proposes a new skill or patches an existing one, and with auto-approval it lands straight in `~/.openclaw/workspace/skills/`. I can also send `/learn` after a useful conversation, or just ask for a skill, and it writes the `SKILL.md` itself. The directory is watched, so the next session picks it up without a restart.

In practice this means I extend the agent from my phone. "Switch web search to Tavily", "set up a nightly backup of your config", "add the Linear MCP server to OpenCode" all turn into the agent editing its own config, writing a timer, or restarting its own service. There are deliberate limits: it has no IAM permissions, so it can't widen its own role. When it needs more AWS access, it drafts the Pulumi change and I apply it.

## It remembers, and it dreams

OpenClaw keeps memory in tiers. During work the agent writes observations into daily notes. A small curated core (`MEMORY.md`, `USER.md`) is loaded at the start of every session. The only process that moves things from the daily notes into that core is [dreaming](https://docs.openclaw.ai/concepts/dreaming).

Dreaming runs as a nightly sweep in three phases. Light sorts and stages recent material. REM reflects on recurring themes. Deep scores the candidates by how often and in how many different contexts they were actually recalled, and only the ones that pass every threshold get merged into `MEMORY.md`. Duplicate notes merge, stale facts get superseded, and every change is logged with its source to a Dream Diary in `DREAMS.md` that I can read. Memory gets promoted because it kept being useful, not because the agent wrote it down confidently once.

This is the part I didn't expect to like so much. After a few weeks the agent knows my projects, my AWS setup and my preferences without me repeating them, and I can audit exactly how it learned each thing. It only works because the box is up at 3am when the sweep runs, and because the volume it writes to is still there in the morning.

## Some things that bit me

The README has a longer list. The ones most likely to save you an evening:

- `eu.*` Bedrock inference profile IDs silently stall streaming responses ([openclaw#55642](https://github.com/openclaw/openclaw/issues/55642), closed as won't fix). Non-streaming calls work, which makes it confusing. Use `global.*` profiles.
- Bedrock model discovery fills the UI model list but not the inference registry. You still need explicit `models.providers` entries.
- Without `plugins.allow`, plugins load in restricted mode and fail silently at inference time.
- `t4g.medium` in `eu-central-1a` kept hitting capacity errors. `eu-central-1b` has been fine.
- Playwright MCP defaults to Chrome, which has no Linux ARM64 build. Pass `--browser=chromium`.

## Don't copy mine

The repo's README opens with "Should you run it? Probably not. Or at least not this way." I mean that. My setup encodes my choices: EU region, Graviton, Tailscale only, Bedrock only, Telegram as the main channel, one user. None of those are the right answer in general. They're just mine, and my agent has spent two months growing skills and memory around them.

That's the actual lesson. What makes OpenClaw interesting is that it adapts to one person. You don't get that from adopting someone else's opinionated deployment, whether it's an AWS sample, a Lightsail quick start, or my Pulumi repo. Start with the simplest box you're comfortable with, use it for real work, and let it grow into what you need. Your setup should end up looking different from mine.

My Pulumi infrastructure repo is private for now. I might open it up once the rough edges are filed down, and if I do it'll show up on [my GitHub](https://github.com/3sztof).
