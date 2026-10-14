---
title: "Tired of driving a tank? Try pi"
date: 2026-10-07
description: "My coding agents turned into tanks: dozens of MCP servers, sub-agent crews, gigabytes of state. pi is the opposite - an engine, four wheels, and whatever you bolt on yourself."
tags: ["ai", "agentic-development", "pi", "opencode", "tools", "productivity"]
categories: ["Posts"]
draft: false
---

Are you tired of your overbloated, vendor-opinionated agentic IDE or TUI? Try [pi](https://pi.dev).

I started using pi today, and within a few hours every other agent on my machine started to look like a tank. A tank can roll over any obstacle, but it burns a lot of fuel, it's slow to turn, and nobody drives one for fun. pi is a sports car: an engine, four wheels, and a steering wheel that responds. It isn't for everyone. If you like the car to drive itself, stick with the tank. If you want to feel the road, read on.

## How my agents became tanks

To be fair to the tanks, I built most of the armour myself. Every time an agent could do something new, I added it. Here's what a scan of my laptop turned up:

| Agent | MCP servers configured | Extras | On disk |
|---|---|---|---|
| opencode | 35 (20 enabled) | 9 plugins, a 10-agent sub-agent crew, 24 skills | 61 MB |
| kiro-cli + Kiro IDE | 22 | 80 agent configs, 39 skills, a "crew" runtime | 3.8 GB |
| codex | 18 | 7 sub-agents, 15 skills | 174 MB |
| claude | 18 | 29 skills, marketplace plugins | 42 MB |

opencode is my daily driver, with 142 launches in my shell history. Its sub-agent plugin alone ships ten named agents with Greek-myth names, and I have both cloud memory and a local wiki plugin on top. Kiro's 3.8 GB is mostly a 2.9 GB multi-agent runtime plus 441 MB of saved sessions. The same handful of AWS, Slack, GitLab and calendar MCP servers is copied into four different config formats.

Every one of those MCP servers adds its tool schemas to the prompt of every request, whether the task needs them or not. Every skill adds its description. Every opinionated system prompt adds the vendor's idea of how I should work. The agent gets heavier, slower to start, and harder to predict, and I lose track of what it's actually doing.

![A 1943 technical manual animation of M4 Sherman tank variants](tank.gif "Me, adding one more MCP server. Source: U.S. War Department, TM 9-2800 (1943), public domain, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:M4A1_to_M4A3_tank_animation.gif)")

## What pi ships with

pi calls itself "a minimal, extensible agent harness that you can make your own". Out of the box the model gets four tools: `read`, `bash`, `edit` and `write`. The system prompt is short enough to [read in a minute](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts). There is no plan mode, no sub-agents and no permission prompts before every tool call. The [homepage](https://pi.dev) says it plainly: "Pi ships with powerful defaults but skips features like sub-agents and plan mode."

That's the engine and the four wheels. Everything else comes as extensions (TypeScript modules with access to tools, commands, events and the TUI), skills, prompt templates and themes, bundled into packages you install from npm or git. pi can also edit itself: ask it to build an extension, run `/reload`, and keep going.

A few things I noticed in the first hours:

- **I can see the whole car.** Every tool in the prompt is one I chose. When something misbehaves, there are only a few places to look.
- **It's quick.** Short prompt, few tools, so less input per request and less for the model to second-guess.
- **Sessions are trees.** `/tree` jumps back to any earlier point and branches from there, all in one file.
- **Models are interchangeable.** 15+ providers, and adding my own was about 100 lines of TypeScript.

## It's not for everyone

A sports car has no roll cage by default. pi's [security docs](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md) say it directly: pi "does not ask for approval before every tool call", and it runs with your user's permissions. If you don't add guardrails or run it in a container, an `rm -rf` is one bad completion away.

The same goes for features. If you want sub-agents or memory, you pick a package or build one. That's a cost. You need to know what you want, read what you install, and accept that the setup is yours to maintain. If you'd rather hand the wheel to a vendor and let it decide, the tanks are good at that.

![A simulated car powersliding through a corner](powerslide.gif "Drifting is a skill issue, in the good sense. Source: Swulong, CC BY-SA 4.0, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Simulation_of_powerslide.gif)")

## Are you actually driving?

This is the part that surprised me most. With the heavy agents I often feel like a passenger. I type a request, a crew of sub-agents plans, delegates and reports back, and tokens burn while tasks churn. The work gets done, but I'm not really steering.

With pi I steer. `Enter` sends a steering message mid-run, `Alt+Enter` queues a follow-up, and the agent does what it's told with tools I understand. It's more engaging, and the results are easier to review because there's less machinery between my intent and the diff.

## How I made pi mine

None of this means I run pi bare. I spent the afternoon fitting parts, and the difference from the tanks is that I chose every one and can explain why it's there.

**Skills ported from my other agents.** pi reads the same `SKILL.md` format, so I pointed it at existing folders instead of rewriting anything: 14 skills from codex (code review, bug diagnosis, commit conventions, research, the [LLM Wiki](/posts/llm-wiki-persistent-agent-memory/) skill and more) and 2 from claude (PowerPoint and Obsidian CLI). My global `AGENTS.md`, the [one that keeps agents honest](/til/agents-md-that-keeps-agents-honest/), came over unchanged.

**Two hand-written extensions:**

- `safety-guard.ts` (90 lines), ported from my codex hook. It blocks recursive force deletes in any spelling, git hook bypasses, `git push` and full environment dumps. I later found that sub-agents and side-conversation sessions don't load extensions by default, so I wired the guard into those explicitly and tested it.
- `local-provider.ts` (115 lines), a custom provider that discovers models live from a local OpenAI-compatible endpoint.

**Packages, picked one at a time:**

- `pi-mcp-adapter` replaces the built-in MCP support with a single proxy tool that connects servers lazily. My pi config has 3 MCP servers. The others are listed in a notes file and get added when a task needs them.
- `pi-subagents`, loaded dynamically, so only a tiny "enable" tool sits in the prompt until I actually want to delegate.
- `pi-web-access` for web search and fetching, `pi-memory` for long-term memory and a scratchpad, `pi-lens` for LSP and ast-grep code intelligence.
- Small quality-of-life ones: a todo list, structured questions, a powerline footer, side conversations with `/btw`, and `cc-safety-net` as a second guard.

**Parts I took back off.** Two packages I installed duplicated things I already had, so they're disabled. The AWS skills sit behind a single router skill instead of 16 prompt entries. Those changes cut the tool definitions from 67 KiB to 42 KiB and the skill listing from 29 KiB to 10 KiB per request. That's the kind of tuning I never did on the tanks, because I couldn't see where the weight was.

The whole config is tracked in my dotfiles, so a new machine gets the same car.

## Should you switch?

If you're happy with your agent, probably not. If you've noticed that you configure it more than you drive it, give pi an afternoon. Install it with `curl -fsSL https://pi.dev/install.sh | sh`, start with the four default tools, and add parts only when you miss them. You'll end up with fewer parts than you expect.

- [pi.dev](https://pi.dev) - homepage and docs
- [earendil-works/pi](https://github.com/earendil-works/pi) - source
- [pi packages](https://pi.dev/packages) - extensions, skills and themes from the community

<sub>Thumbnail: pi logo from [pi.dev](https://pi.dev).</sub>
