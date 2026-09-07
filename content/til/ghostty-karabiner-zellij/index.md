---
title: "Ghostty + Karabiner + Zellij: making three opinionated tools share a keyboard"
date: 2026-07-14
description: "Getting Ghostty, Karabiner-Elements, and Zellij to coexist without stepping on each other's keybindings took more work than expected. Here's my config and why it is the way it is - share yours."
tags: ["ghostty", "karabiner", "zellij", "shell", "cli", "tools", "keyboard", "macos"]
categories: ["TIL"]
draft: false
---

**Please do not do what I did.** I mean it. What follows is a post about spending a non-trivial number of evenings remapping modifier keys on a computer that shipped with a perfectly functional keyboard, because I decided that Apple's opinions about where `Ctrl` should live were personally offensive to me. A normal person adapts to their tools. I apparently negotiate with them at the kernel level.

The only excuse I have is years of GNU/Linux muscle memory so deeply embedded that my fingers genuinely cannot accept that `Home` scrolls without moving the cursor, that `Ctrl+S` doesn't save, or that `Alt+F4` doesn't close anything. macOS is a great operating system that I have spent considerable effort making feel like it isn't. This is that story.

If your `Cmd` key feels fine where it is: close this tab, go touch grass, you're winning at life. If you've ever opened Karabiner at 11pm to fix "just one more binding" - pull up a chair.

[Ghostty](https://ghostty.org/), [Karabiner-Elements](https://karabiner-elements.pqrs.org/), and [Zellij](https://zellij.dev/) are each opinionated about keyboard input. Running all three together means their opinions conflict in non-obvious ways. Here's the full map of what I did and why.

## The bottom layer: macOS Polish Pro layout

The Polish character input (`ą`, `ę`, `ó`, `ś`, `ł`, `ź`, `ż`, `ć`, `ń`) is handled by the **Polish Pro** macOS keyboard input source, not by Karabiner. Polish Pro maps these to `Option + <letter>` - so `Option+a` → `ą`, `Option+e` → `ę`, and so on. This matches the standard GNU/Linux and Windows Polish layout that I've used for my entire career, and it works well.

The consequence: `Option+<letter>` is fully consumed by Polish character input. Any application that expects `Alt+<letter>` as a keybinding - including Zellij's defaults - will receive a Polish character instead. This is why several Zellij defaults had to move.

## The Karabiner layer: Windows/Linux muscle memory

Karabiner handles everything else. My config is not exotic - it's the accumulated muscle memory of years on GNU/Linux and Windows, translated into macOS rules:

**Ctrl → Cmd remaps (outside terminals):** `Ctrl+C/V/X/Z/Y/A/S/F/W/N` map to their `Cmd+` equivalents in non-terminal apps. This is the standard "make macOS feel like Windows" config that many Polish developers run. I shouldn't need to context-switch between `Ctrl+S` in VS Code on Windows and `Cmd+S` on macOS.

**Home/End keys behave like Linux:** `Home` → `Cmd+Left` (start of line), `End` → `Cmd+Right` (end of line), with `Ctrl+Home`/`Ctrl+End` for start/end of file. macOS's default `Home`/`End` behavior - scrolling without moving the cursor - is wrong.

**`Cmd+arrow` ↔ `Option+arrow` swap:** macOS uses `Cmd+arrow` for beginning/end of line and `Option+arrow` for word-by-word movement. GNU/Linux and Windows use `Ctrl+arrow` for words and `Home`/`End` for lines. Swapping `Cmd` and `Option` on arrows brings macOS closer to what my hands expect. This swap is also what causes the Ghostty/Zellij conflicts described below.

**`Alt+F4` → `Cmd+Q`:** Close application. I still reach for `Alt+F4` after twenty years.

**`Cmd+Option+arrow` → `Ctrl+arrow`:** Switch macOS virtual desktops. Default is `Ctrl+arrow`, which conflicts with terminal use. Moved to `Cmd+Option+arrow` which nothing else wants.

All of this is synced via [chezmoi](https://www.chezmoi.io/) and applies identically to my built-in MacBook keyboard, my home external keyboard, and my office external keyboard. Switching machines is frictionless.

My own Karabiner config isn't public, but you don't need it - the Ctrl→Cmd and PC-style Home/End behaviour is the well-known [PC-Style Shortcuts](https://ke-complex-modifications.pqrs.org/#pc_shortcuts) ruleset from the official Karabiner gallery, which you can import in one click. It's a great starting point to layer your own tweaks on top of.

## The Ghostty layer

Ghostty intercepts some combinations before the running application sees them:

- `Cmd+t` → new tab
- `Cmd+w` → close tab
- `Cmd+<number>` → switch tab

The `Cmd+arrow` ↔ `Option+arrow` swap from Karabiner means a logical `Cmd+Right` (end of line in text) arrives at Ghostty as a physical `Option+Right`. In a terminal, `Option+Right` emits the escape sequence `ESC f` (the standard sequence for "move word forward"), which Zellij interprets as `Alt+f` — its toggle for floating panes. This was causing floating panes to open every time I moved to the end of a line.

My resolution for Ghostty: nothing in its config. Accept that `Cmd+t` opens a new Ghostty tab rather than reaching Zellij's tab mode, and remap Zellij instead.

## The Zellij layer

With all of the above in mind, the Zellij config changes:

```kdl
keybinds {
    normal {
        // Ctrl+p conflicts with opencode - move pane mode
        bind "Alt r" { SwitchToMode "Pane"; }
        // Ctrl+t grabbed by Ghostty new tab - move tab mode
        bind "Alt t" { SwitchToMode "Tab"; }
        // Alt+arrows for pane focus (Alt+letter unusable due to Polish Pro)
        bind "Alt Left"  { MoveFocus "Left"; }
        bind "Alt Right" { MoveFocus "Right"; }
        bind "Alt Up"    { MoveFocus "Up"; }
        bind "Alt Down"  { MoveFocus "Down"; }
        unbind "Ctrl p"
        unbind "Ctrl t"
    }
    shared_except "locked" {
        // Shift+arrow for pane focus
        bind "Shift Left"  { MoveFocus "Left"; }
        bind "Shift Right" { MoveFocus "Right"; }
        bind "Shift Up"    { MoveFocus "Up"; }
        bind "Shift Down"  { MoveFocus "Down"; }
        // Shift+Alt+arrow for tab cycling
        bind "Shift Alt Left"  { GoToPreviousTab; }
        bind "Shift Alt Right" { GoToNextTab; }
        // Karabiner's Cmd→Option swap makes these fire on physical Cmd+h/j/k/l
        unbind "Alt h"
        unbind "Alt j"
        unbind "Alt k"
        unbind "Alt l"
        // Cmd+Right sends ESC f → Zellij reads as Alt+f → floating pane toggle
        unbind "Alt f"
    }
}
```

## What I'm curious about

I arrived at this through trial and error, not a principled process. Honestly, I'm not sure I'd have had the patience to untangle it all a few years ago - a fair chunk of the credit goes to LLM-powered coding agents, which turn out to be genuinely good at spotting the kind of cross-config inconsistencies and silent keybinding conflicts that I'd otherwise only find by accident, one maddening floating pane at a time.

The bits I'd most like to improve:

- Whether there's a cleaner way to audit keybinding conflicts across a layered stack before they cause problems - I found all of these by accident
- Whether other people running Ghostty + Zellij have a less convoluted arrangement
- Whether anyone has found a way to have Polish Pro's `Option+letter` and `Alt+letter` terminal bindings coexist without choosing one or the other

If you have a meaningfully different setup - or a simpler one that covers the same ground - I'd genuinely like to see it. [My GitHub](https://github.com/3sztof) or [LinkedIn](https://www.linkedin.com/in/3sztof/) both work.

- [Ghostty documentation](https://ghostty.org/docs)
- [Karabiner-Elements documentation](https://karabiner-elements.pqrs.org/docs/)
- [Karabiner "PC-Style Shortcuts" (official gallery)](https://ke-complex-modifications.pqrs.org/#pc_shortcuts) - the public ruleset my Ctrl→Cmd and Home/End remaps are based on
- [rux616/karabiner-windows-mode](https://github.com/rux616/karabiner-windows-mode) - a more comprehensive Windows-style ruleset if you want to go further
- [Zellij keybindings documentation](https://zellij.dev/documentation/keybindings)
- [Zellij TIL on this blog](/til/zellij/)
