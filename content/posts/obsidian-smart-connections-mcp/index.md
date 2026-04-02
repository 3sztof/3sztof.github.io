---
title: "Obsidian + AI: From Simple Plugin to Full Agent Integration"
date: 2026-02-12
lastmod: 2026-04-02
description: "Three tiers of AI-powered Obsidian: the Smart Connections plugin alone covers most users. The CLI and MCP integrations go further - but only if you actually need them."
tags: ["obsidian", "ai", "smart-connections", "mcp", "knowledge-management", "productivity", "opencode", "kiro", "claude-code"]
categories: ["Tools", "Productivity", "AI"]
---

A few colleagues recently saw my Obsidian setup and asked how I get AI agents to search my notes semantically - not just keyword matching, but actually understanding what I'm looking for.

The honest answer is: **most people only need one plugin**. The rest is optional depth for people who want AI agents to interact with their vault programmatically.

This post is structured in three tiers. Stop at whichever one covers your actual needs.

---

## Tier 1: Smart Connections plugin (most users - stop here)

**If you just want AI-powered semantic search inside Obsidian, this is all you need.**

[Smart Connections](https://github.com/brianpetro/obsidian-smart-connections) is a community plugin that generates embeddings for your notes locally using a bundled model (TaylorAI/bge-micro-v2, 384 dimensions). No API key, no external calls, no cost. Your notes stay on your machine.

### Installation

1. Obsidian Settings → Community plugins → Browse
2. Search "Smart Connections" → Install → Enable

That's it. The plugin starts embedding your notes in the background. Progress is visible in the Smart Connections panel (brain icon in the sidebar).

**A few things to know:**
- First-time embedding takes a few minutes depending on vault size
- Notes shorter than ~200 characters won't be embedded
- Embeddings live in `.smart-env/` inside your vault - small footprint, usually under 10MB

### What you get

Once embeddings are done, the Smart Connections panel shows semantically similar notes whenever you open any note. You can also chat with your vault directly from the plugin - ask questions in natural language and it retrieves relevant notes as context.

This covers the vast majority of use cases: finding related notes, surfacing connections you'd forgotten, querying your own writing. **If this is what you were looking for, you're done.**

---

## Tier 2: Obsidian CLI + agent skills (for agent users)

If you want AI agents outside Obsidian - coding assistants, terminal agents - to read and write your vault, the [Obsidian CLI](https://obsidian.md/changelog/2026-02-10-desktop-v1.12.0/) (released February 2026) is the clean way to do it.

```bash
# Read a note
obsidian read "Ideas/conference-talks.md"

# Append content
obsidian append "Ideas/conference-talks.md" "New idea from today's session"

# Create a note
obsidian create "Meeting Notes/2026-02-12.md"

# Read today's daily note
obsidian daily:read

# Set a property
obsidian property:set "note.md" status "published"
```

### Wiring it into your agent

The practical way to give an agent access to your vault is through an agent skill - a set of instructions that tells the agent how and when to use the CLI. There are ready-made skills for this on [skills.sh](https://skills.sh/kepano/obsidian-skills): one for the [Obsidian CLI](https://skills.sh/kepano/obsidian-skills/obsidian-cli), one for [Obsidian Bases](https://skills.sh/kepano/obsidian-skills/obsidian-bases), and one covering [Obsidian markdown conventions](https://skills.sh/kepano/obsidian-skills/obsidian-markdown). Install whichever covers your workflow and the agent knows how to interact with your vault without you re-explaining it every session.

This tier gives you **write access** (create, append, update notes) in addition to read, and works cleanly across any MCP-compatible agent (Opencode, Kiro, Claude Code, etc.). It doesn't require cloning repos or running local servers - just the CLI and a skill config.

---

## Tier 3: Agent-accessible semantic search (advanced users only)

> **Stop here unless you specifically need semantic search available to external AI agents via MCP.** This section is for people who have already used Tiers 1 and 2 and found them insufficient. It requires comfort with Node.js, local servers, and JSON config files. It is functional but involves more moving parts than the options above.

The payoff over the CLI tier: **semantic search**. The CLI can read and write notes by path, but it can't answer "find everything I wrote about async Python" without knowing which files to look at. An MCP server that has access to your Smart Connections embeddings can.

### State of the ecosystem (April 2026)

The honest picture first, because the landscape is fragmented and worth understanding before you invest time in any setup.

**Smart Connections has no official MCP server.** Brian Petro's project (4,700+ stars, actively developed) exposes nothing over MCP. The gap is real and unfilled on the official side.

The community options, ranked by maintenance health (state as of April 2, 2026):

| Project | Stars | Last commit | Semantic search | Notes |
|---|---|---|---|---|
| [aaronsb/obsidian-mcp-plugin](https://github.com/aaronsb/obsidian-mcp-plugin) | 271 | March 2026 | Graph traversal (not embeddings) | Best architecture; runs inside Obsidian; beta only (BRAT) |
| [jacksteamdev/obsidian-mcp-tools](https://github.com/jacksteamdev/obsidian-mcp-tools) | 698 | July 2025 | ✅ Smart Connections embeddings | Seeking maintainers since mid-2025 |
| [StevenStavrakis/obsidian-mcp](https://github.com/StevenStavrakis/obsidian-mcp) | 673 | June 2025 | ❌ Keyword only | Cleanest setup; no embeddings |
| [msdanyg/smart-connections-mcp](https://github.com/msdanyg/smart-connections-mcp) | 31 | Oct 2025 | ✅ Smart Connections embeddings | One-person side project; still the only working embedding-based option |

If you need embedding-based semantic search for agents right now, `msdanyg/smart-connections-mcp` is still the only working option despite its small footprint. It's clever in one specific way: it doesn't re-embed anything - it reads the `.smart-env/` files Smart Connections already computed. The hackiness is in the packaging, not the approach.

If you want the best-maintained option and can live without embedding-based search, `aaronsb/obsidian-mcp-plugin` is the one to watch - it runs as a proper Obsidian plugin, serves MCP over HTTP on `localhost:3001`, supports wikilink graph traversal, Dataview queries, and Obsidian Bases. It got commits in March 2026. The catch: it's beta, install via BRAT only.

The setup below uses `msdanyg/smart-connections-mcp` since it's the only embedding path. Substitute `aaronsb` if graph traversal is enough for your use case.

### What this looks like in practice

> "Search my notes for ideas related to conference talk proposals. Then find notes similar to the top results. Summarize the key themes."

The agent chains `search_notes` with `get_similar_notes` and synthesizes across your vault without you naming a single file. This is genuinely powerful - it's just that getting here requires the setup below.

### Setup

**Prerequisites:** Node.js v18+, Smart Connections plugin already running (Tier 1), an MCP-compatible client.

```bash
git clone https://github.com/msdanyg/smart-connections-mcp.git
mkdir -p ~/.local/share/mcp-servers
mv smart-connections-mcp ~/.local/share/mcp-servers/
cd ~/.local/share/mcp-servers/smart-connections-mcp
npm install
npm run build
```

### MCP tools exposed

| Tool | Description |
|------|-------------|
| `search_notes` | Semantic search using text queries |
| `get_similar_notes` | Find notes similar to a given note |
| `get_connection_graph` | Build multi-level relationship graphs |
| `get_embedding_neighbors` | Direct vector similarity queries |
| `get_note_content` | Retrieve note content with block extraction |
| `get_stats` | Knowledge base statistics |

### Client configuration

**Opencode** (`~/.config/opencode/opencode.json`):

```json
{
  "mcp": {
    "smart-connections": {
      "type": "local",
      "command": [
        "node",
        "/Users/YOUR_USERNAME/.local/share/mcp-servers/smart-connections-mcp/dist/index.js"
      ],
      "environment": {
        "SMART_VAULT_PATH": "/path/to/your/obsidian/vault"
      },
      "enabled": true,
      "timeout": 120000
    }
  }
}
```

**Kiro CLI:**

```json
{
  "mcpServers": {
    "smart-connections": {
      "command": "node",
      "args": ["/Users/YOUR_USERNAME/.local/share/mcp-servers/smart-connections-mcp/dist/index.js"],
      "env": {
        "SMART_VAULT_PATH": "/path/to/your/obsidian/vault"
      }
    }
  }
}
```

**Claude Code** (`~/.claude.json` for global, or `.mcp.json` in your project root):

```json
{
  "mcpServers": {
    "smart-connections": {
      "command": "node",
      "args": ["/Users/YOUR_USERNAME/.local/share/mcp-servers/smart-connections-mcp/dist/index.js"],
      "env": {
        "SMART_VAULT_PATH": "/path/to/your/obsidian/vault"
      }
    }
  }
}
```

Alternatively, add it from the command line:

```bash
claude mcp add smart-connections \
  -e SMART_VAULT_PATH=/path/to/your/obsidian/vault \
  -- node /Users/YOUR_USERNAME/.local/share/mcp-servers/smart-connections-mcp/dist/index.js
```

Other MCP-compatible clients follow the same pattern - command, args, environment pointing at your vault.

> **Personal note:** I keep the smart-connections MCP disabled by default in Opencode and only enable it when I have a very specific query that needs semantic vault search. Most sessions don't need it, and having it always on just adds noise to the agent's tool list.

### Troubleshooting

**Connection errors / "server not found":** Verify the path is absolute and correct, confirm `npm run build` completed without errors, ensure `SMART_VAULT_PATH` points to a vault with Smart Connections enabled, restart your MCP client after config changes.

**Empty search results:** Smart Connections may still be generating embeddings - check the plugin panel. Notes under ~200 characters aren't embedded. Try broader queries.

**Slow first query:** Expected behavior - first query loads embeddings into memory. Subsequent queries are fast.

**"Embedding dimension mismatch":** You changed Smart Connections' model. Delete `.smart-env/` from your vault, restart Obsidian, wait for re-embedding.

### Security

- The MCP server has read access to your **entire vault**. Only enable for vaults you're comfortable exposing to AI agents.
- Embeddings encode semantic content - not human-readable, but not meaningless either. Treat `.smart-env/` with care.
- Well-designed MCP clients ask before invoking tools. Don't disable those prompts.

---

## Which tier do you need?

| You want... | Use |
|---|---|
| Semantic search and connections inside Obsidian | **Tier 1** - Smart Connections plugin |
| AI agents that can read/write your vault | **Tier 2** - Obsidian CLI + skill |
| Semantic search available to external agents via MCP | **Tier 3** - Smart Connections MCP |

Most people are Tier 1. Tier 3 is worth the setup only if you've hit the ceiling of what Tier 1 and 2 offer and specifically need agent-accessible semantic search.

---

## Resources

- [Smart Connections Plugin](https://github.com/brianpetro/obsidian-smart-connections)
- [smart-connections-mcp](https://github.com/msdanyg/smart-connections-mcp) - embedding-based MCP server (small project, works)
- [aaronsb/obsidian-mcp-plugin](https://github.com/aaronsb/obsidian-mcp-plugin) - best-maintained option, graph traversal, beta
- [jacksteamdev/obsidian-mcp-tools](https://github.com/jacksteamdev/obsidian-mcp-tools) - Smart Connections embeddings via MCP, maintenance uncertain
- [StevenStavrakis/obsidian-mcp](https://github.com/StevenStavrakis/obsidian-mcp) - clean, no embeddings
- [obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api) - gold-standard REST plugin (1.9k stars)
- [Obsidian CLI release notes](https://obsidian.md/changelog/2026-02-10-desktop-v1.12.0/)
- [skills.sh Obsidian skills](https://skills.sh/kepano/obsidian-skills) - CLI, Bases, and markdown skills for agents
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Opencode](https://opencode.ai/) - [Kiro CLI](https://kiro.dev/) - [Claude Code](https://claude.ai/code)
