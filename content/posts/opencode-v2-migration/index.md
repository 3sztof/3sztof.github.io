---
title: "OpenCode 2 broke five of my nine plugins, and I don't miss most of them"
date: 2026-11-18
description: "What changed in OpenCode 2, why it's worth the upgrade, which parts of my old plugin-heavy setup are now built in, and how I ported my own plugin to the new API."
tags: ["opencode", "ai", "agentic-development", "oh-my-openagent", "plugins", "mcp", "tools", "productivity"]
categories: ["Tools", "AI", "Development"]
---

> This is a follow-up to [Supercharging Opencode with AWS Bedrock and Oh-My-Openagent](/posts/opencode-aws-bedrock-setup/) and [LLM Wiki: a compounding knowledge base for your AI coding sessions](/posts/llm-wiki-persistent-agent-memory/). If you set things up from either of those posts, read this one first.

After upgrading to OpenCode 2.1.4, five of my nine plugins failed to load. Notifications, smart session titles and my wiki context were all gone, and the TUI didn't say why.

The fix took an evening. Most of it was deleting plugins, because OpenCode 2 now does their jobs itself. This post covers what's new and why it's worth upgrading, which parts of my old setup are now built in, what actually broke, and how I ported the one plugin I couldn't replace.

## What's new in OpenCode 2, and why it's worth the upgrade

OpenCode 2 is a big release with three intentional breaking changes: a new plugin API, a new server API, and a single global `cli.json` for terminal settings (migrated automatically from `tui.json`). Everything else is meant to stay compatible, and in practice my 470-line V1 `opencode.json` loaded unchanged. These are the changes I noticed in daily use.

**A shared background service.** Every OpenCode window now talks to one background server that owns sessions, configuration, plugins and tool execution. Config changes reload on save, so there's no restart after editing `opencode.json`. If something gets stuck, `opencode service restart` fixes it, and `opencode --standalone` gives you a private server to test against.

**Code Mode for MCP tools.** In the Bedrock post I told you to keep most MCP servers disabled, because every enabled server adds its tool schemas to every request. In V2, MCP tools are reached through Code Mode by default: the model gets one `execute` tool that runs JavaScript against a searchable catalog of tools, and only looks up the ones it needs. It can also call several tools in parallel and filter their output before any of it reaches the context. A server that should be called directly can opt out with `"codemode": false`. The main reason for my "disable everything" advice is mostly gone.

**Built-in subagents.** OpenCode now ships `build` and `plan` primary agents, plus `general` and `explore` subagents. Subagents run in child sessions with fresh context, in the foreground or in the background, and report back to the parent. You can define your own in `.opencode/agents/*.md` and control which ones an agent may launch with `subagent` permissions.

**Snapshots with `/undo` and `/redo`.** OpenCode snapshots the working directory around each model step. `/undo` rolls back the conversation *and* the files the agent changed, then puts your prompt back in the composer to edit. It needs a Git repository and isn't a replacement for commits, but it takes the fear out of "let it try".

**Small things that add up.**

- `/btw <question>` asks a side question about the session without adding it to the conversation.
- Tabs are on by default, so several sessions stay open side by side.
- [References](https://opencode.ai/v2/docs/references/) give the agent named access to other directories or Git repositories, such as a docs repo or a shared library.
- Nested `AGENTS.md` files are discovered as the agent reads deeper into a project. Note that V2 reads only `AGENTS.md`, so a `CLAUDE.md` fallback no longer works.
- [Warming](https://opencode.ai/v2/docs/warming/) optionally sends small keep-alive requests while you pause between prompts, so provider prompt caches don't expire. It's off by default and costs a little, but on Bedrock with long contexts it can be worth testing.
- Permissions are one ordered list where the last matching rule wins, instead of rules grouped by tool. The `bash` action is now `shell` and `task` is now `subagent`.

Two defaults are worth knowing before you upgrade. **Access outside the project directory is allowed by default** (V1 asked first). If you want the old behaviour, add `{ "action": "external_directory", "resource": "*", "effect": "ask" }` to `permissions`. And **todos are off by default**. Turn them back on with `"experimental": { "todo": true }`.

## What's now built in

Here's my old plugin list, set against what OpenCode 2 ships:

| What I used | What it did | In OpenCode 2 |
| --- | --- | --- |
| `@mathew-cf/opencode-terminal-notifier` | Desktop notification when a task finishes | Built in: `attention.notifications` in `cli.json`, plus optional sounds |
| `@tarquinen/opencode-smart-title` | Meaningful session titles | Built in: a hidden `title` agent names sessions |
| `opencode-websearch-cited` | Web search with sources | Built in: a `websearch` tool with Exa, Firecrawl, Parallel, Tavily or TinyFish as the provider, and source links in answers |
| `oh-my-openagent` | Agent hierarchy, background delegation, planning | Partly: `general` and `explore` subagents, background child sessions and the `plan` agent cover the basics, but not OmO's named agents, categories or Team Mode |
| "Keep MCP servers disabled" (a habit, not a plugin) | Saving tokens | Mostly unnecessary with Code Mode |
| `envsitter-guard` | Stops the agent reading `.env` secrets | Partly: the built-in `build` agent asks before reading sensitive environment files. I still keep the plugin for its safe inspection tools |

Session titles need no config. Notifications need one setting in `~/.config/opencode/cli.json`:

```json
{
  "attention": {
    "notifications": true
  }
}
```

Web search needed no config. The first search asks you to allow it and pick a provider, and you can pin one with `"websearch": { "provider": "tavily" }` in `opencode.json`.

## What broke

Every failing plugin logged the same error:

```text
PluginModule.LoadError: Plugin must export a default definition with an id and an effect or setup function.
```

V1 plugins don't run in OpenCode 2. The new API wants a default export with an `id` and a `setup(ctx)` function, and a V1 plugin function returns an object of hooks instead. Renaming config entries isn't enough; the plugin code has to be ported. There's a second, quieter change: **a configured local plugin path must be a directory** (OpenCode loads its `index.ts`). A path to a single `.ts` file is skipped with only a warning in the log.

None of this shows up in the TUI. To find it:

```bash
opencode plugin list    # loaded plugins show an ID and version; broken ones show "-"
grep 'failed to load plugin' ~/.local/share/opencode/log/opencode.log | tail
```

This is where my nine plugins ended up:

| Plugin | Result | What I did |
| --- | --- | --- |
| `envsitter-guard` | Works | Already ships a V2 build |
| `cc-safety-net` | Works | Already ships a V2 build |
| `opencode-wakatime` | Works | Nothing |
| `opencode-mem` | Works | Nothing |
| `oh-my-openagent` | Broken, then a no-op | The cache was stuck on an old release; 5.1.48 loads but does nothing, so I removed it (see below) |
| `terminal-notifier` | Broken | Removed, replaced by built-in notifications |
| `smart-title` | Broken | Removed, replaced by the built-in title agent |
| `opencode-websearch-cited` | Broken | Removed, replaced by built-in web search |
| `llm-wiki` (my own) | Broken | Ported to the V2 API |

The plugin list in `opencode.json` is now short. V1's `plugin` key still works, but `plugins` is the V2 name:

```json
{
  "plugins": [
    "envsitter-guard@latest",
    "cc-safety-net",
    "opencode-wakatime",
    "opencode-mem"
  ]
}
```

My local llm-wiki plugin isn't in that list at all, which I'll explain in the porting section.

## The oh-my-openagent situation

oh-my-openagent was the centrepiece of the Bedrock post, so it gets its own section. The short version: **on OpenCode 2 it loads, but it does nothing.**

My installed copy was an old 4.x release from the plugin cache, which fails with the error above. `opencode plugin update oh-my-openagent@latest` pulled 5.1.48, which does load. The [OpenCode 2 support issue](https://github.com/code-yeongyu/oh-my-openagent/issues/8485) was closed by a fix that adds a V2 `setup()` entry, but that entry only logs a notice: "OpenCode 2 support is limited: the plugin loads, but its agents, tools and hooks are not active here." Full support is planned in small steps ([#9389](https://github.com/code-yeongyu/oh-my-openagent/issues/9389)), with no date.

The author's recommended path is **OmO Native**: a standalone `omo` command (npm package `omo-ai`) built on [senpi](https://github.com/code-yeongyu/senpi), a fork of the [pi](/posts/pi-coding-agent-sports-car/) coding agent with the OmO extension built in. It's a separate agent, not something that runs inside OpenCode. `omo setup` imports your OpenCode keys, providers, MCP servers, skills and OmO model choices, and never writes to OpenCode's files, so you can run both side by side. senpi's own README lists the discipline agents, Team Mode and the category router among the OmO features with no direct senpi counterpart. I haven't checked how much the OmO extension adds back.

So the choice today is:

1. **Stay on OpenCode 1** if OmO inside OpenCode is the reason you use OpenCode.
2. **Move to OmO Native** if you want OmO itself and don't mind a different harness.
3. **Use OpenCode 2 without OmO's orchestration.** The built-in subagents cover the basic "explore in the background, plan, then build" loop.

I picked the third option and removed the plugin. Given how much I [enjoyed pi](/posts/pi-coding-agent-sports-car/), it's funny that OmO's next home is a pi fork.

There's also a less technical reason I didn't wait for V2 support. OmO is no longer really an OpenCode plugin project. It's turning into a product: [omo.dev](https://omo.dev) presents it as a tool from Sisyphus Labs, with its own installer, a desktop app in beta and chat integrations on the way. The code is still public, but it's source-available under the Sustainable Use License (SUL-1.0), not open source: personal and internal business use is fine, and commercial redistribution isn't. That's the authors' call to make, and the project is still very active. It's still a little sad to watch one of the most interesting community projects around OpenCode move away from it and towards a commercial product of its own.

## Porting a plugin: llm-wiki as a worked example

My [LLM Wiki](/posts/llm-wiki-persistent-agent-memory/) plugin had no replacement, so I ported it. It's a good test case because it uses most V1 extension points: a shell environment hook, a system prompt transform, a compaction hook, an idle event listener, four custom tools, and calls that spawn background sessions.

The [V1 plugin migration guide](https://opencode.ai/v2/docs/build/plugins/migrate-v1) has a full hook mapping. These are the ones I needed:

| V1 | OpenCode 2 |
| --- | --- |
| `export const MyPlugin: Plugin = async (ctx) => ({ ... })` | `export default { id, setup(ctx) { ... } }` |
| `shell.env` | `ctx.shell.hook("create.before", ...)` |
| `experimental.chat.system.transform` | `ctx.session.hook("context", ...)`, push to `event.system` |
| `experimental.session.compacting` | `ctx.session.hook("compaction", ...)` |
| `event` (for `session.idle`) | `for await (const e of ctx.event.subscribe(...))` |
| `tool: { name: tool({ args: zod }) }` | `ctx.tool.transform(editor => editor.add({ input: jsonSchema }))` |
| `client.session.create/promptAsync/messages` | `ctx.session.create/prompt/context` |
| `ctx.directory` | `ctx.location.directory` |
| returned `dispose` | cleanup function returned from `setup` |

The skeleton looks like this:

```ts
import type { Plugin } from "@opencode/plugin"

export default {
  id: "llm-wiki",
  async setup(ctx) {
    const cwd = ctx.location.directory

    await ctx.session.hook("context", (event) => {
      event.system.push({ type: "text", text: `<wiki-context>\n${loadContext(cwd)}\n</wiki-context>` })
    })

    const controller = new AbortController()
    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (event.type === "session.idle") scheduleFlush(event.data.sessionID)
      }
    })()

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "wiki-search",
        description: "Search the LLM Wiki via qmd",
        input: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
        async execute(input, context) {
          return { content: await search((input as { query: string }).query, context.signal) }
        },
      })
    })

    return () => controller.abort()
  },
} satisfies Plugin.Plugin
```

Four things caught me out:

- **Use a type-only import.** `import type { Plugin } from "@opencode/plugin"` is erased at runtime, so a local plugin file loads without installing any dependencies. `Plugin.define()` is just an identity function, so a plain object with `satisfies` works the same.
- **Install into `plugins/<name>/index.ts` and don't register it.** OpenCode 2 auto-discovers plugin files and directories in `~/.config/opencode/plugins/` and in a project's `.opencode/plugins/`. My old installer added a `file://.../llm-wiki.ts` entry to `opencode.json`, which V2 skips because it points to a file. The new installer removes that entry.
- **Events carry less data.** `session.idle` now carries only the `sessionID`, so the plugin fetches the session to get its title and agent, and to skip child sessions and its own `wiki-ops` sessions. User messages no longer carry an agent name either, so the agent comes from the session.
- **There's no toast API.** V1 plugins could poke the TUI. OpenCode 2 plugins have no notification surface, so errors now go only to the plugin's log file.

The port is about the same size as the original. The helper functions (context loading, session logs, the git auto-commit) didn't change at all.

## Migration checklist

If you're coming from my earlier posts, this is the short version:

1. Run `opencode plugin list` and grep the log for `failed to load plugin`.
2. Run `opencode plugin update` to refresh cached packages. Some plugins already ship V2 builds.
3. Remove `terminal-notifier`, `smart-title` and `opencode-websearch-cited`, and set `"attention": { "notifications": true }` in `~/.config/opencode/cli.json`.
4. Decide about oh-my-openagent: stay on V1, move to OmO Native, or remove the no-op plugin as I did.
5. Move any local plugin to `plugins/<name>/index.ts` and port it, following the [migration guide](https://opencode.ai/v2/docs/build/plugins/migrate-v1).
6. Re-check `permissions`: external directories are now allowed by default, and `bash`/`task` are now `shell`/`subagent`.
7. If you manage dotfiles, update them too. My chezmoi repo still had the V1 plugin list and would have put it back on the next `chezmoi apply`.

## Resources

- [OpenCode: Migrate from V1](https://opencode.ai/v2/docs/migrate-v1) - config, permissions, agents and other changes
- [OpenCode: Migrate plugins from V1](https://opencode.ai/v2/docs/build/plugins/migrate-v1) - the hook mapping
- [OpenCode: Plugins](https://opencode.ai/v2/docs/plugins) - loading, discovery and plugin management
- [OpenCode: CLI settings](https://opencode.ai/v2/docs/cli/config) - `cli.json`, including notifications
- [oh-my-openagent #8485](https://github.com/code-yeongyu/oh-my-openagent/issues/8485) - OpenCode 2 support status
- [Migrating from OpenCode to OmO Native](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/migrating-from-opencode.md)
