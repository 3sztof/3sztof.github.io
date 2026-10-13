---
title: "k9s makes kubectl feel like punch cards"
date: 2026-10-05
description: "A long-overdue shout-out to k9s - the terminal UI that turns kubectl get/logs/exec/describe/context-juggling into a single keystroke-driven dashboard."
tags: ["kubernetes", "cli", "tools", "productivity", "k9s", "devops"]
categories: ["TIL"]
draft: false
---

I actually learned about [k9s](https://k9scli.io/) years ago, but it never got the shout-out it deserves. It's a terminal UI that sits on top of your existing kubeconfig, watches the cluster in real time, and lets you navigate, observe, and manage resources interactively - no raw `kubectl` incantations required. If you still live in `kubectl get pods -w` in one pane, `kubectl logs -f` in another, and `kubectl exec -it` in a third, this collapses all of it into one keystroke-driven window.

<script src="https://asciinema.org/a/305944.js" id="asciicast-305944" async="true"></script>

You drive everything from a `:` command bar - `:pods` (or `:po`), `:deploy`, `:svc`, `:ns`, `:nodes`, even `:xray po` for a dependency graph and `:pulses` for a cluster dashboard. Views live-update as the API server changes. On any resource, single keys do the obvious thing: `l` streams logs, `s` shells into a container, `d` describes, `v` views the YAML, `e` edits it in `$EDITOR`, `ctrl-d` deletes (with a confirm). `/` filters with regex, `ctrl-a` lists every resource alias, and `?` shows the full mnemonic cheatsheet. Switching clusters is just `:ctx`. The muscle memory arrives within an afternoon.

The part that keeps me honest: context and namespace juggling. Instead of `kubectl config use-context` roulette - and the occasional heart-stopping moment of running a delete against the wrong cluster - the active context and namespace are always on screen, and switching is two keystrokes. For read-only poking around a production cluster, there's even a `--readonly` flag that disables every mutating command.

It's written in Go, Apache-2.0 licensed, and maintained by [Fernand Galiana](https://github.com/derailed) (`derailed`) under Imhotep Software - sitting at roughly 34k GitHub stars as of this writing, which tells you I'm late to the party, not early. Install is a one-liner on every platform:

```bash
# macOS / Linux (official Homebrew tap)
brew install derailed/k9s/k9s

# Windows
scoop install k9s   # or: choco install k9s

# Arch
pacman -S k9s
```

Or grab a [standalone binary](https://github.com/derailed/k9s/releases). Then just run `k9s`. Quit with `:q` or `Ctrl-C`.

- [k9scli.io](https://k9scli.io/) - official site and docs
- [derailed/k9s on GitHub](https://github.com/derailed/k9s)
- [K9s Tour (asciinema)](https://asciinema.org/a/305944) - the demo embedded above
