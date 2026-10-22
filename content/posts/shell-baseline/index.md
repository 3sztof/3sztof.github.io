---
title: "My modern shell setup: the CLI tools I install before I feel at home"
date: 2026-10-14
description: "zoxide, starship, bat, ripgrep, fd, fzf, yazi, and tldr - the handful of CLI upgrades I bootstrap onto every new box, with Atuin on top. Small tools, picked deliberately."
tags: ["shell", "cli", "tools", "productivity", "zoxide", "ripgrep", "fd", "fzf", "yazi"]
categories: ["Tools", "Productivity"]
draft: false
---

Every time I set up a new machine - a laptop, a cloud box, a robot - there's a short list of tools I install before the terminal feels like mine. None of them are new or clever; they're small upgrades to commands I run hundreds of times a day. Most of them live in a [bootstrap script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba) so a fresh box is five minutes from comfortable.

I checked my own [Atuin](/til/atuin/) stats before writing this, to make sure I was recommending what I actually use and not what I think I should.

## zoxide - `cd` that learns

[zoxide](https://github.com/ajeetdsouza/zoxide) replaces `cd` with a version that ranks directories by frecency (frequency + recency). After a day, `z proj` jumps straight to the project I mean and I stop typing `cd ../../../` chains. `zi` opens an interactive fuzzy picker (via fzf) when the guess is ambiguous. In my history `z` sits in the top handful of commands - above any single `git` subcommand - which is a fair proxy for how much navigation it saves.

```bash
eval "$(zoxide init zsh)"   # aliases cd if you want it to
```

![zoxide jumping between directories by a fragment of their path](demo-zoxide.gif "`z api` then `z web` - zoxide jumps to the best match")

## ripgrep - search that keeps up

[ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) is a recursive search tool that respects `.gitignore` by default and is fast enough that I never think about whether a search is worth running. I reach for it constantly. `rg TODO`, `rg -t py def`, `rg -l pattern` to list files - it has replaced `grep -r` entirely, and it's what my editor and most of my scripts shell out to under the hood.

![ripgrep searching a project for TODO and a Python pattern](demo-ripgrep.gif "`rg TODO`, then a type-filtered `rg -t py`")

## fd - `find` without the manpage

[fd](https://github.com/sharkdp/fd) is a friendlier `find`: `fd config` instead of `find . -name '*config*'`. Sensible defaults (skips `.git`, respects `.gitignore`), colored output, regex or glob. It pairs with the others - `fd -e md | fzf` to pick a markdown file, or as fzf's own file-walker.

![fd finding files by name and extension](demo-fd.gif "`fd server`, then `fd -e py`")

## bat - `cat` with syntax highlighting

[bat](https://github.com/sharkdp/bat) is `cat` with syntax highlighting, line numbers, and git-change markers in the gutter. I alias `cat=bat` on personal machines. It also makes a good pager, and it's my go-to fzf previewer once I wire it up (`--preview 'bat --color=always {}'`) - that's a config choice, not automatic, but it's the first thing I set.

![bat printing a Python file with syntax highlighting and line numbers](demo-bat.gif "`bat` on a source file - highlighting, line numbers, a file header")

## fzf - fuzzy-find anything

[fzf](https://github.com/junegunn/fzf) turns any list into an interactive filter. The shell bindings earn their keep on their own - `Ctrl-T` to drop a file into the current command, `**<Tab>` completion - but the real use is piping anything into it: `git branch | fzf`, `kubectl get pods | fzf`. It's the picker that zoxide's `zi` and plenty of my own one-liners are built on.

![fzf fuzzy-filtering a piped list of files](demo-fzf.gif "files piped into fzf, filtered by typing a few characters")

## starship - a prompt that just works

[Starship](https://starship.rs/) is a cross-shell prompt that shows what I care about without a weekend of config: git branch and dirty state, the language version for the current directory, and how long the last command took. By default it turns the prompt character red on a failed command; if you want the numeric exit code you enable the `status` module (it's off by default). Fast, identical across zsh/bash/fish, and the defaults are good enough that I barely touch `starship.toml`.

![starship prompt showing git branch and a dirty-state indicator](demo-starship.gif "the prompt picks up the branch and flips to a dirty indicator after an edit")

## yazi - a terminal file manager

[yazi](https://github.com/sxyazi/yazi) is a quick terminal file manager with vim-style keys, image and text previews (its own built-in highlighter), and async everything. I reach for it when I want to *browse* rather than `ls`/`cd` - sorting downloads, poking through an unfamiliar repo, bulk-renaming. It has fzf-style filtering and zoxide jumps built in, so it fits the rest of the set.

![yazi terminal file manager navigating a project with a live preview pane](demo-yazi.gif "yazi: navigate with hjkl, preview on the right")

## tldr - the examples you actually wanted

[tldr](https://tldr.sh/) gives you the handful of real examples instead of a 400-line man page. `tldr tar` tells me the extract incantation in two seconds. It doesn't replace `man` for depth, but it replaces the "how do I use this again?" web search almost entirely. I use the [tealdeer](https://github.com/tealdeer-rs/tealdeer) client - a fast, cached Rust implementation of tldr - so the pages are local and instant.

![tldr showing a concise tar cheatsheet](demo-tldr.gif "`tldr tar` via tealdeer - the examples, not the manual")

## And Atuin, on top of all this

The one I'd miss most isn't in the list above because it got [its own write-up](/til/atuin/): [Atuin](https://github.com/atuinsh/atuin) replaces your shell history with a SQLite database - full context per command, a fuzzy `Ctrl-R` search, and optional encrypted sync across machines. It's the piece that makes a *new* box feel like an old one, because my history comes with me. If you try one thing from this post, [read the Atuin TIL](/til/atuin/) and start there.

## The through-line

Each of these does one thing and composes with the others - zoxide and yazi lean on fzf, ripgrep and fd feed it, bat previews for it, Atuin covers the history. That's the opposite of the all-in-one shell framework: a few sharp tools I understand, installed deliberately, over one big thing that does everything opaquely. It's the same instinct behind the rest of my setup.

## The agent goes on the box too

These days a new machine isn't comfortable until the coding agent is on it too, set up the same deliberate way. I use [pi](/posts/pi-coding-agent-sports-car/) for that and [published my setup as a gist](https://gist.github.com/3sztof/c94b9b1176085e79fcfa06100b9a1374) - same principle as this post, one layer up.

One note on the [bootstrap script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba): it still installs `tmux`, but I've since moved to [Zellij](/til/zellij/) (and I'm [eyeing cmux](/til/cmux/)), so treat that line as legacy. Everything else I'd install again today without thinking.

- [My shell setup bootstrap script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba) - installs most of these in one go (ripgrep and fd come from your package manager)
- [zoxide](https://github.com/ajeetdsouza/zoxide) · [ripgrep](https://github.com/BurntSushi/ripgrep) · [fd](https://github.com/sharkdp/fd) · [bat](https://github.com/sharkdp/bat) · [fzf](https://github.com/junegunn/fzf) · [starship](https://starship.rs/) · [yazi](https://github.com/sxyazi/yazi) · [tealdeer](https://github.com/tealdeer-rs/tealdeer)
- [Atuin](/til/atuin/) - the shell-history piece, written up on its own
- [My pi setup, as a gist](https://gist.github.com/3sztof/c94b9b1176085e79fcfa06100b9a1374) - the coding agent that goes on the same box
