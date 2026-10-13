---
title: "LLM Wiki: a compounding knowledge base for your AI coding sessions"
date: 2026-08-19
description: "Instead of re-explaining your project to the AI on every session, teach it once and let every agent remember. The LLM Wiki pattern as a shared long-term memory that plugs into all of your coding agents."
tags: ["ai", "tools", "productivity", "opencode", "pi", "obsidian", "knowledge-management", "agentic-development"]
categories: ["Posts"]
draft: false
---

One of the more persistent frustrations with AI-assisted coding is the blank slate problem. Every new session starts from zero. You re-explain the project structure, the conventions, the decisions made three months ago and why, the names of the services, the reason the auth layer works the way it does. It's tedious, it burns context window space, and the explanations are never as good as they would be if you'd written them down properly.

That frustration gets worse, not better, once you run **more than one coding agent**. I bounce between pi, opencode, and a couple of others depending on the task. Each one starting from zero means re-explaining the same project three different ways, and worse: a hard-won insight I taught one agent on Monday is invisible to the agent I open on Tuesday. The knowledge is trapped per-agent, per-session. What I actually want is one shared, long-term memory that every agent reads from and writes to - so a learning saved anywhere is available everywhere.

The LLM Wiki pattern is a solution to this. The core idea comes from [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): maintain a directory of Markdown files that the AI agent is responsible for keeping up to date, and inject those files as context at the start of every session. Over time the wiki becomes a dense, accurate representation of everything the agent needs to know. Session logs are ephemeral; wiki pages accumulate. The twist I care about most now is that nothing in that pattern is tied to a single agent - the same vault can back all of them.

## What it actually is

A directory of Markdown files. That's the whole thing. The wiki lives in an Obsidian vault, organized into `wiki/projects/`, `wiki/concepts/`, `wiki/people/`, and `wiki/playbooks/`. The agent creates new pages, cross-references existing ones, and updates facts when things change. You review and occasionally correct.

The format I've converged on: every project gets a set of pages covering overview, architecture, infrastructure, development workflow, and anything else that matters. Not "what does a human user need to know" - "what does the agent need to know to work on this project?" That's a different and more useful document. It covers the DynamoDB single-table access patterns, the IaC module structure, the branch naming conventions, the reason certain design decisions were made. Things you'd otherwise explain from scratch every second session.

A page is just Markdown with a bit of frontmatter. Here's the shape of a project architecture page (illustrative - names changed):

```markdown
---
aliases: ["Collide Architecture"]
tags: [project/collide, architecture]
updated: 2026-08-14
---
# Collide - Architecture

## Data model
Single DynamoDB table `collide-main`. Access patterns:
- User by id: PK=`USER#<id>`, SK=`PROFILE`
- Matches for a user: PK=`USER#<id>`, SK begins_with `MATCH#`
- **Why single-table:** read patterns are all key-based; no ad-hoc queries
  justify the cost/complexity of a second store. See [[decisions/why-single-table]].

## Services
- `payment-intent` Lambda - idempotent via `IDEMP#<key>` items, 24h TTL
- `notification-fanout` Lambda - SNS -> per-channel SQS

## Gotchas
- The Pulumi layer build must run before `pulumi up` or the Lambdas get a stale
  layer ARN. `cld build-layers` wraps it.
```

That is the entire interface. No database, no proprietary format - a human can open it in Obsidian, an agent can read it as context, and `qmd` can index it. The `[[decisions/why-single-table]]` style cross-links turn the vault into a navigable graph of "what" plus "why."

(That `[[wikilink]]` is for Obsidian's own graph view; the agent-facing convention is plain `[Title](relative/path.md)` links, which render everywhere and don't depend on Obsidian. Pick one and be consistent - mixing them is the main footgun.)

## The session flow

Three lifecycle points do the work, and every agent I use exposes hooks for all three:

**At session start**, a hook injects relevant wiki pages into the system prompt - always-on concept pages (shell environment, tool setup) plus the project-specific pages matched by the current working directory. The injected bundle is deliberately small and is anchored by two per-project files: a `hot.md` cache (the handful of facts you need every single time) and an `active-context.md` (what's in flight right now, including an open task list). A few kilobytes of factual context that replaces ten minutes of re-explanation.

**At session end**, a hook captures the session transcript to a dated session log under `memory/<project>/sessions/`, then auto-commits the wiki (behind a cooldown so you don't get a commit per turn). Nothing is "compiled" yet - this is just a cheap, raw capture.

**Consolidation** is the step that turns raw logs into durable knowledge, and it runs as a *separate background pass* rather than inline, so it never slows down your actual session. A background `wiki-ops` worker - the same agent, minus the interactive hooks - reads the recent session logs, extracts the facts worth keeping, and folds them into the canonical project pages, regenerating `active-context.md` as it goes. What triggers it varies by client: some run it on session end, some on a size/time threshold (enough unconsolidated logs have piled up), some on a schedule. The important part is that it's gated - it doesn't fire after every turn, and it runs out of band. Session logs are ephemeral; wiki pages accumulate.

Mechanically, that looks roughly like this (an opencode `wiki-flush` writing a session log):

```markdown
<!-- wiki/memory/collide/sessions/2026-08-14.md -->
## Session 2026-08-14

### What happened
- Added idempotency keys to the payment-intent Lambda
### Decisions
- Store keys in the existing single-table design (PK=`IDEMP#<key>`), 24h TTL
  - Rejected a separate table: not worth the extra IaC + cost for a short-lived guard
### Follow-ups
- Backfill is not needed; keys only matter going forward
```

A later consolidation pass reads that, decides the idempotency decision is durable, and promotes it into the project's architecture page - so the *next* session (in any agent) starts already knowing it, without the session log sticking around forever.

## How quickly does it become useful?

Almost immediately - and that surprised me. Within the first few sessions, I noticed I could reference concepts loosely ("the matching algorithm", "the notification flow", "the Pulumi layer build") and the agent would already know what I meant. No pointing to files, no pasting context, no "as we discussed previously." It just knew.

The UX boost compounds over time. After a few months across several projects, the wiki covers full architecture of multiple codebases, infrastructure details, DynamoDB schema decisions and the reasoning behind them, development workflow conventions, and a running log of design choices. When I start a new session on a project I haven't touched in weeks, the agent picks up with the same context it would have had if I'd been working on it every day.

## What it doesn't solve

Per-session shell history and pane state - that's what [Atuin](/til/atuin/) and [Zellij](/til/zellij/) handle. The wiki knows what was decided; it doesn't know what commands were run. Also: genuinely novel work still requires the same back-and-forth as any new problem. The wiki is a shared memory for things that have been established; it doesn't substitute for the actual thinking on new ground.

## The search layer

The wiki is indexed by [qmd](https://github.com/tobi/qmd), a local hybrid search engine running BM25 + vector + reranking on the Markdown files, exposed as an MCP server in opencode. In practice I mostly rely on the injected context, but semantic search across the full wiki is useful for cross-cutting queries and for the consolidation agent.

## One vault, many agents

This is the part that changed how I think about the whole thing. The vault is just Obsidian-compatible Markdown indexed by qmd - there is nothing agent-specific about it. So the same vault can plug into every agent I use, and each one gets a thin integration that does two jobs: inject relevant pages at session start, and flush a session log at the end. The heavy lifting (consolidation, search) happens once, against the shared files, regardless of which agent produced them.

Concretely, my pi setup runs two memory layers side by side, and the split between them is the useful part. pi ships its own [pi-memory](https://github.com/jayzeng/pi-memory) plugin, which **auto-captures** working memory - daily logs, running context, the scratchpad - without being asked. The LLM Wiki integration points at the shared vault and is deliberately **write-explicit**: it only writes when I call `wiki-flush` or `wiki-consolidate`. They are separate stores, both read at session start, with different jobs:

- **pi-memory = the scratch brain.** High-churn, auto-captured, pi-local. Great for "what was I doing yesterday."
- **the wiki = the curated long-term brain.** Low-churn, deliberate, *shared across every agent*. The things worth keeping forever.

Keeping them separate avoids the obvious failure mode - a shared long-term store getting polluted with every half-finished thought - while still letting pi benefit from its native memory. A fact I decide is durable gets promoted into the wiki, and from there it's visible to opencode, Codex, Claude Code, and Kiro too. The agents disagree on a lot - prompts, tools, defaults - but they agree on where the durable knowledge lives.

Wiring an agent up is intentionally thin. For opencode it's a plugin registration plus pointing the integration at your vault - roughly:

```jsonc
// opencode.json
{
  "plugin": ["llm-wiki"],          // injects context on start, flushes on idle
  "mcp": {
    "qmd": {                        // semantic search over the vault
      "command": ["qmd", "mcp", "--root", "${LLM_WIKI_ROOT}"]
    }
  }
}
```

```bash
# the one piece of shared state every agent needs: where the vault lives
export LLM_WIKI_ROOT="$HOME/Documents/llm-wiki"
```

Every other agent gets its own thin shim against the same `LLM_WIKI_ROOT` and the same `qmd` index. That's the whole trick: one environment variable and one search index, and suddenly every agent is reading and writing the same brain.

The payoff is that "long-term memory" stops being a feature of one tool and becomes a **shared substrate** across my whole workflow. The learnings that are genuinely useful across contexts - how a given codebase is wired, why a design decision was made, the gotcha that cost me an afternoon once - get written once and are reachable from whichever agent I happen to open. That is a strictly better place to keep knowledge than inside any single agent's private memory.

## Building it yourself, and credit where it's due

The LLM Wiki pattern isn't tied to any specific tool, and that's the whole point. The same idea - AI-maintained Markdown files injected as session context - can be realised with opencode's built-in long-term memory plugins, Amazon Q Developer's "My Context" feature (which indexes your local workspace and conversations), or several other pre-built solutions. If you want something off the shelf, those are worth exploring first.

The shared-vault, qmd-indexed, multi-agent version I run is built on a core implemented by [Aubrey Oosthuizen](https://auronmatrix.github.io/). He wrote the hard part - the wiki engine and the consolidation logic; I added the integrations that plug it into opencode and pi, and polished a few edges. The core itself is a proprietary internal project, so I won't go into its internals here - but, crucially, **the principles are open**: an Obsidian-compatible vault, hybrid search over Markdown, a session-start inject and a session-end flush, and a background consolidation pass. None of that depends on his implementation. If you build those four pieces against your own vault, you have the same thing.

If you want something fully adjusted to your own needs - your own vault structure, your own session log format, your own consolidation logic - building it from scratch is a genuine learning experience and the result is exactly what you need rather than what someone else decided you need. The Karpathy gist is a good starting point; the rest is Markdown files and a bit of plumbing.

- [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) - the original pattern
- [qmd](https://github.com/tobi/qmd) - the local hybrid search engine
- [Aubrey Oosthuizen](https://auronmatrix.github.io/) - author of the LLM Wiki core my shared-vault setup is built on
