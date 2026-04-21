---
title: "Atuin is a shell history game changer"
date: 2026-03-30
description: "Replaced my default shell history with Atuin - SQLite-backed, searchable, syncable across machines. Should have done this years ago."
tags: ["shell", "cli", "tools", "productivity", "atuin"]
categories: ["TIL"]
draft: false
---

[Atuin](https://github.com/atuinsh/atuin) replaces your shell's default history (`Ctrl+R` and all) with a SQLite database that stores full command context - exit code, working directory, hostname, session, duration. The fuzzy search UI alone is worth it, but the optional encrypted sync across machines is what makes it genuinely indispensable once you work across more than one box.

![Atuin interactive search in action](demo.gif "Atuin's fuzzy search UI - filter through your entire shell history with full context")

It wires into zsh, bash, fish, and xonsh with a single `eval` line. Takes about 30 seconds to set up.

I've been putting together a [quick shell setup script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba) that installs atuin alongside the other tools I now consider baseline for a comfortable terminal environment: **zoxide** (smart `cd` with frecency ranking), **starship** (cross-shell prompt), **bat** (syntax-highlighted `cat`), **fzf** (fuzzy finder), **tmux**, **yazi** (terminal file manager), and **tldr** via tealdeer. I should probably write a short TIL about each of them.

- [atuinsh/atuin on GitHub](https://github.com/atuinsh/atuin)
- [My shell setup bootstrap script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba)
