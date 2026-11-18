---
title: "Phonnect: how a guitar amp app pushed me into writing a tray app"
date: 2026-11-18T12:00:00
description: "The Spark app only runs on phones, and Windows Subsystem for Android can't do Bluetooth. So I mirrored my phone with adb and scrcpy, and then automated the whole thing into Phonnect: a small open-source tray app that puts your Android phone on your desktop the moment it connects."
tags: ["phonnect", "android", "scrcpy", "adb", "python", "side-project", "guitar"]
categories: ["Posts"]
draft: false
---

I practise guitar through a [Positive Grid Spark](https://www.positivegrid.com/) amp. The amp is great, but a lot of the fun lives in the **Spark app**: tones, presets, and backing tracks that the phone streams to the amp over Bluetooth. The app is **mobile only**. There's no Windows or macOS version. So when I practise at my desk, with a big monitor, a keyboard and a mouse in front of me, I'm still poking at a phone propped against the amp.

This post is about how that small annoyance turned into a side project: **[Phonnect](https://github.com/3sztof/phonnect)**, a small open-source (MIT) tray app for Windows, macOS and Linux that opens your Android phone's screen on your computer as soon as the phone connects.

## Attempt 1: Windows Subsystem for Android

The obvious idea was to run the Android app on Windows itself. [Windows Subsystem for Android](https://learn.microsoft.com/en-us/windows/android/wsa/) (WSA) ran Android apps on Windows 11 in a lightweight VM, and side-loading an APK into it takes one `adb install`.

It didn't work out, because **WSA has no Bluetooth**. The VM can't see the PC's Bluetooth adapter, and an amp app that can't reach the amp is just a nice preset browser. Microsoft also retired WSA in March 2025, so it was a dead end either way.

## Attempt 2: keep the app on the phone, bring the screen to the PC

If the app can't move to the PC, the screen can. The phone already has working Bluetooth and a working app, so all I need is to **see and control the phone from the desktop**. Two well-known open-source tools do exactly that:

- **[adb](https://developer.android.com/tools/adb)** (Android Debug Bridge) is Android's own command-line tool for talking to a device over USB or Wi-Fi. It ships with the Android SDK platform tools, and everything else in this post builds on it.
- **[scrcpy](https://github.com/Genymobile/scrcpy)**, by Genymobile and Romain Vimont, uses adb to mirror an Android phone's screen into a desktop window with very low latency, and sends your mouse and keyboard back to the phone. It's free, needs no app on the phone, and has no account or cloud.

This worked straight away. Plug the phone in, run `scrcpy`, and the Spark app appears in a window on my monitor, still sending audio to the amp over the phone's Bluetooth. I can change tones with the mouse without putting the guitar down.

But both are command-line tools, and it showed:

- Every session starts with opening a terminal and typing a command.
- Wireless use means pairing codes, IP addresses, and a debugging port that changes after every reboot or network change.
- On Windows a console window hangs around next to the mirror.
- The scrcpy flags I care about (audio, keyboard, rotation) are easy to forget.

That's the kind of friction you either live with or automate.

## From a script to an app

The first version was a Windows-only PowerShell + VBS script that started scrcpy when the phone appeared. It's still on the [`legacy-windows`](https://github.com/3sztof/phonnect/tree/legacy-windows) branch. It grew into a cross-platform Python app called *scrcpy-autolaunch*, which I renamed **Phonnect** ("phone" + "connect") in v0.3.

Phonnect doesn't replace scrcpy or adb. It sits in the tray (menu bar on macOS), notices when a phone connects, and opens the mirror window. In other words, it makes those two tools automatic, especially over Wi-Fi.

## What it does (v0.4.1)

### Automatic mirroring

- **Plug the phone in and the mirror opens.** Close the window and it stays closed until you plug the phone in again.
- Optionally, the same happens when the phone connects over **Wi-Fi**.
- **One tray entry per phone.** Clicking a phone means "show me this phone": Phonnect connects over Wi-Fi if needed and opens the window.

### Wi-Fi made easy

- **Pair by scanning a QR code** shown on the PC (Android 11+), or type the pairing code. `phonnect pair --qr` shows the QR code in a terminal.
- It **remembers every phone**, and learns its IP address even while it's on USB.
- When Android changes the debugging port, Phonnect **finds the phone again**. It tries mDNS first, then the last address that worked, then an optional scan of the phone's IP address. You can turn the scan off on office networks.

### Leaves the phone as it found it

- Every phone setting it changes (rotation, content size) is **saved first and restored** when the window closes or the app quits.
- **Audio stays on the phone by default.** This one is for me: the Spark app's backing tracks have to keep going to the Bluetooth amp while the screen is mirrored. If you want, sound can play on the PC instead, or on both.

### Extras on the mirror window

- A **sidebar** attached to the window: Back, Home, Recent apps, notifications, quick settings, volume, power, screenshot, an adb shell, and a slider to fit more on the screen. It works on Windows. The macOS version arrived in 0.4 and still needs testing on a real Mac.
- **Desktop mode:** the phone's desktop (taskbar, big-screen apps) in a second, PC-sized window, as if the phone were plugged into a monitor.
- **Force landscape**, **hide the phone's keyboard** while you type on the PC, and **configurable mouse buttons**. By default, right-click goes to the app instead of acting as Back.

### Install, update, forget about it

- A **one-line install** (see below). The installer shows exactly what it will install, where, and how to remove it. It asks before installing [uv](https://docs.astral.sh/uv/), and again before installing scrcpy and adb with your package manager. Uninstalling works the same way.
- **One-click updates** from the tray menu. It checks GitHub once a day and sends nothing else.
- It **starts at login**, only one copy runs, there's no console window, and it runs under your normal user account with **no admin rights**.

## How it compares

There are plenty of good tools around scrcpy already. Most of them give you a window to open and click around in. Phonnect takes a different approach: the phone simply appears when it connects, over USB or Wi-Fi, and Phonnect cleans up after itself.

| Tool | What it is | How Phonnect differs |
| --- | --- | --- |
| [scrcpy](https://github.com/Genymobile/scrcpy) | The mirroring engine itself | Phonnect is a layer on top: automatic start, tray menu, Wi-Fi pairing and reconnecting, phone settings restored afterwards |
| [autoadb](https://github.com/rom1v/autoadb) | A small command-line tool by scrcpy's author that runs a command whenever a device connects | Same "react to the connection" idea. Phonnect adds Wi-Fi, a UI, settings restore and per-phone memory |
| [QtScrcpy](https://github.com/barry-ran/QtScrcpy) | A Qt desktop GUI with multi-device and group control. The releases bundle adb | Phonnect is tray-first and automatic, and uses the scrcpy and adb from your package manager instead of bundling them |
| [Escrcpy](https://github.com/viarotel-org/escrcpy) | A feature-rich Electron GUI for scrcpy, with multi-device control and LAN discovery | A window you open and drive, vs. a lightweight background app that reacts to the phone |
| [guiscrcpy](https://github.com/srevinsaju/guiscrcpy) | A Python GUI for scrcpy (GPL-3.0), now archived | Phonnect is MIT-licensed, maintained, and focused on "it just opens" rather than a control panel |
| [Vysor](https://www.vysor.io/) | A commercial app for Android and iOS; wireless and high-quality mirroring need the paid Pro tier | Phonnect is free and open source, and builds on scrcpy's low latency |
| Microsoft Phone Link | Built into Windows; streaming phone apps to the PC works only on some phone brands | Phonnect works with any Android phone that has USB debugging, on Windows, macOS and Linux |
| Samsung DeX / AirDroid Cast | Tied to one vendor or one service | No account, no cloud, no vendor lock-in. Phonnect's desktop mode uses Android's own desktop |

## Trust and engineering

A tool that holds a debugging connection to your phone should be boring and transparent, so I put some effort into that:

- **MIT license, and no GPL dependencies** by choice.
- **No telemetry.** The only network use is the optional daily update check against GitHub's API and the optional Wi-Fi port scan.
- **No bundled binaries.** scrcpy and adb come from your OS package manager, which keeps them up to date.
- **Supply chain:**
  - Commits are GPG-signed.
  - Releases are built by GitHub Actions with build provenance, so you can check them with `gh attestation verify`.
  - CI tokens are read-only, actions are pinned by commit, and Dependabot keeps dependencies current.
  - Commits are scanned for leaked secrets with [gitleaks](https://github.com/gitleaks/gitleaks), and the findings of a recent security review have been addressed.
- **Code and process:**
  - Python, packaged with uv.
  - [Ruff](https://docs.astral.sh/ruff/) and pre-commit hooks.
  - Unit tests on Windows, macOS and Linux in CI, using fake adb and scrcpy processes.
  - Behaviour and design decisions are written down as specs with [OpenSpec](https://openspec.dev) and linked to GitHub issues. That made it much easier to build with AI agents without them slowly drifting from what I actually wanted.

## Status: what's tested and what isn't

- **Tested:** Windows 11 with a Pixel 9 Pro (GrapheneOS, Android 17). This is my daily setup.
- **macOS and Linux: experimental.** Unit tests pass in CI, but nobody has tried them with a real phone yet. The Mac fixes in 0.4 (a freeze when closing a window, sidebar docking, icon colour) haven't been confirmed on a real Mac.
- **QR pairing is new.** The window works, but nobody has scanned the code with a real phone yet.
- **Known limitation:** on my phone, starting apps from the desktop-mode taskbar does nothing, probably because of the GrapheneOS launcher. The desktop itself works.
- **Next on the backlog:** turning the phone's screen off while mirroring, always-on-top, recording, remembering the window size, favourite apps, and the battery level in the menu.

If you're on a Mac or Linux, you'd be doing me a real favour by trying it and [opening an issue](https://github.com/3sztof/phonnect/issues) with what you find.

## Try it

First, turn on USB debugging on the phone: in *Settings → About phone*, tap *Build number* 7 times, then turn on *USB debugging* in *Developer options*. If you haven't done this before, the repo has a [step-by-step phone setup guide](https://github.com/3sztof/phonnect/blob/main/docs/phone-setup.md). It also explains how to turn it all off again.

macOS / Linux:

```sh
curl -fsSL https://github.com/3sztof/phonnect/releases/latest/download/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://github.com/3sztof/phonnect/releases/latest/download/install.ps1 | iex
```

Plug the phone in, tap **Always allow from this computer**, and the mirror window opens.

It started as a way to change amp tones without picking up my phone, but nothing in it is specific to the Spark app. If you have an Android app you wish ran on your desktop, give it a try.

## Links

- [Phonnect on GitHub](https://github.com/3sztof/phonnect) and its [docs](https://github.com/3sztof/phonnect/tree/main/docs)
- [scrcpy](https://github.com/Genymobile/scrcpy): screen mirroring and control for Android
- [adb (Android Debug Bridge)](https://developer.android.com/tools/adb): Android's command-line device tool
- [autoadb](https://github.com/rom1v/autoadb): run a command when a device connects
- [Windows Subsystem for Android (archived docs)](https://learn.microsoft.com/en-us/windows/android/wsa/)
- [Positive Grid Spark](https://www.positivegrid.com/)
- [uv](https://docs.astral.sh/uv/), [OpenSpec](https://openspec.dev), [gitleaks](https://github.com/gitleaks/gitleaks)
