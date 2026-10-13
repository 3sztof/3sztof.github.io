---
title: "cmux might retire my overengineered Ghostty + Zellij setup"
date: 2026-10-13
description: "A native macOS terminal built on libghostty with vertical tabs, notification rings for AI agents, and - the part that sold me - session restore that resumes shells and agent sessions after a reboot, which is what I always wanted Zellij to do."
tags: ["cmux", "ghostty", "zellij", "terminal", "macos", "ai", "agents", "tools", "productivity"]
categories: ["TIL"]
draft: false
---

Another one from my friend Sebastien, who has a good track record of handing me tools I end up depending on - his [blog](https://sebastien.tech/) is worth a follow. This time it is [cmux](https://cmux.com/).

I have written before about my terminal stack: [Zellij replacing tmux](/til/zellij/), and the [evening-eating saga of making Ghostty, Karabiner, and Zellij share a keyboard](/til/ghostty-karabiner-zellij/). That setup works, but I will be honest about what it is - **overengineered**. Three opinionated tools negotiating over the same keybindings, a multiplexer layered on top of a terminal emulator, modifier keys remapped at the kernel level. cmux looks like it collapses most of that into one native app, and the migration cost is suspiciously low.

## What cmux actually is

cmux is a **native macOS terminal app** (Swift + AppKit, not Electron) built on [libghostty](https://github.com/ghostty-org/ghostty) - the same rendering engine Ghostty itself uses, consumed as a library the way an app embeds WebKit for web views. So you get Ghostty's GPU-accelerated rendering, but inside an app that ships multiplexing as first-class GUI features instead of leaving it to tmux or Zellij.

The headline features:

- **Vertical and horizontal tabs** in a sidebar that shows each workspace's git branch, linked PR status, working directory, listening ports, and latest notification - plus split panes, horizontal and vertical.
- **Notification rings** - when a coding agent needs your attention, its pane gets a blue ring and its tab lights up. These fire off standard terminal escape sequences (OSC 9/99/777) or a `cmux notify` CLI you wire into agent hooks.
- **A built-in, scriptable browser** you can split next to your terminal, with an automation API ported from [agent-browser](https://github.com/vercel-labs/agent-browser).
- **Programmable** through a CLI and a Unix socket: create workspaces, split panes, send keystrokes, drive the browser.
- **No config files or prefix keys** required for the multiplexing - it is GUI-native, so no `Ctrl+b` dance.

The author's own [motivation](https://github.com/manaflow-ai/cmux) is running many Claude Code and Codex sessions in parallel and losing track of which one needs input. That is a very AI-era problem, and it maps directly onto the "few named tabs" discipline I [already try to keep in Zellij](/til/zellij/#my-workflow-few-tabs-named).

## Why trying it is nearly free

The reason this isn't a disruptive switch: **cmux reads my existing `~/.config/ghostty/config`**. Themes, fonts, colors, cursor, even terminal keybindings and leader sequences carry over directly. The look and feel I already tuned comes along for free, which removes the usual "re-tune everything" tax that normally keeps me on a setup long after I have outgrown it.

Install is a one-liner:

```bash
brew tap manaflow-ai/cmux
brew install --cask cmux
```

## The part that sold me: resuming shells and agent sessions

This is the feature I care about most, and it is exactly why I started digging into Zellij in the first place - I want my work to survive a reboot, a crash, or an accidental quit. cmux treats the [workspace layout as durable state](https://cmux.com/blog/session-restore) rather than something tied to one app process. On relaunch it brings back the window/workspace/pane tree, working directories, terminal scrollback (best effort), and even the in-app browser's URL and history.

The part Zellij can't touch: cmux can **resume agent sessions**. Install its hooks (`cmux hooks setup`) and it records a native session ID for Claude Code, Codex, OpenCode, Pi, Gemini CLI, Amp, Cursor CLI, and a dozen others. After a relaunch it rebuilds the layout and relaunches each agent with *that agent's own resume command and the saved session ID* - so you continue the same conversation, not a blank prompt. That is as close to "hibernate my whole agentic workflow" as I have seen.

It is honest about the boundary: cmux restores what it owns and what tools expose through their own resume APIs; it does **not** checkpoint arbitrary live process memory. Plain shells, vim, and unsupported tools reopen as normal terminals rather than replaying stale prompts or secrets - a deliberate, sane default.

This is where Zellij has always felt half-done to me. [Zellij's session serialization](/til/zellij/#session-serialization-the-real-hook) saves the layout and re-runs commands in command panes behind a "Press Enter to run" prompt - but it cannot resume an agent's actual session, and the per-pane shell history that built up is gone (that is your shell's job, which is why I lean on [Atuin](/til/atuin/)). cmux's model - layout as durable state plus real agent-session resume - is what I wanted Zellij's resurrection to be.

And if I do need live detach/reattach across a quit or crash, cmux has `cmux local-zellij` and `cmux local-tmux` for exactly that. So I can even run Zellij *under* cmux during the transition and peel it away once I trust the native restore - the opposite of the usual all-or-nothing terminal migration.

## Where I actually stand

I have not fully switched yet - this is a "trying it, and it has real potential" post, not a verdict. The honest caveats:

- **macOS only.** My home lab and robots are Linux, so cmux is a workstation tool, not a universal one. Zellij still rides along on remote boxes over SSH.
- **It is young and moving fast**, with nightly builds and a Founder's Edition - par for the course for a tool at this stage.
- The real test is whether the native session restore earns enough trust that I stop reaching for `cmux local-zellij`. If it does, my three-tool stack becomes one app, and I get to delete a non-trivial amount of config I have been quietly embarrassed by.

If that happens, I will write the follow-up admitting the Ghostty + Karabiner + Zellij saga was a detour. For now: thanks again to Sebastien - this is a genuinely clever take on what a terminal should be in the agent era.

- [cmux.com](https://cmux.com/)
- [cmux session restore (the feature that sold me)](https://cmux.com/blog/session-restore)
- [manaflow-ai/cmux on GitHub](https://github.com/manaflow-ai/cmux)
- [The Zen of cmux](https://cmux.com/blog/zen-of-cmux)
- [My Zellij TIL](/til/zellij/) and [the Ghostty + Karabiner + Zellij config saga](/til/ghostty-karabiner-zellij/)
- Thanks to [Sebastien's blog](https://sebastien.tech/) for the recommendation
