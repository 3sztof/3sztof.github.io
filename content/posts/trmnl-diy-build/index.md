---
title: "Building a DIY TRMNL e-ink display: what worked and what didn't"
date: 2026-08-27
description: "A Seeed Studio XIAO ESP32 kit, a 3D printed case on the fridge, LaraPaper self-hosted on a Synology NAS, and a Raspberry Pi that couldn't keep up. An honest account."
tags: ["trmnl", "e-ink", "diy", "hardware", "esp32", "larapaper", "raspberry-pi"]
categories: ["Posts"]
draft: false
---

[TRMNL](https://trmnl.com/) is a small e-ink display designed as a personal dashboard - weather, calendar, tasks, whatever you want to surface at a glance. The DIY version is a kit based on the [Seeed Studio XIAO ESP32](https://www.seeedstudio.com/XIAO-ESP32C3-p-5431.html) with open-source firmware, and a choice of self-hosted backends. The official device is $139. The DIY path is cheaper and considerably more educational - and more frustrating, in roughly equal measure.

I used the [TRMNL 7.5" OG DIY Kit](https://www.seeedstudio.com/TRMNL-7-5-Inch-OG-DIY-Kit-p-6481.html) from Seeed Studio - a 7.5 inch 800×480 e-paper panel with an ESP32 microcontroller. The hardware assembly is genuinely easy: a connector, a couple of screws, and firmware flashing via USB. I 3D printed a case for it and mounted it on my fridge with magnets. It sits there displaying my daily schedule and is one of the few screens in my life that I don't feel bad glancing at.

## Backend: Terminus vs LaraPaper

The TRMNL ecosystem has two main self-hosted backends:

**[Terminus](https://github.com/usetrmnl/terminus)** - the official open-source BYOS (Bring Your Own Server). Docker-based, Ruby on Rails. The reference implementation.

**[LaraPaper](https://github.com/larapaper/larapaper)** - a PHP/Laravel alternative with a plugin ecosystem. This is what I ended up running.

I tried both. LaraPaper won - the UX was better at the time of my experiments and the plugin ecosystem made it easier to add custom dashboards without touching Rails. I hosted it on my **Synology DS920+ NAS** without issues. Docker Compose up, nginx reverse proxy, done.

## The Raspberry Pi experiment

After the NAS setup was stable, I wanted to move to a **Raspberry Pi 3B** as the host. The reasoning: the Pi is always on (the NAS spins down), it's a low-power connected node, and - more interestingly - it's on my [Tailscale](https://tailscale.com/) tailnet alongside the AWS EC2 box that runs [OpenClaw](/posts/openclaw-on-graviton-ec2/). That tailnet is the interesting part: because every node has a stable name and no open ports, OpenClaw can reach the Pi (and therefore the LaraPaper instance driving the display) directly over the private network. In practice that means I can tell an AI agent - from Telegram or my phone, through OpenClaw - "push this to the fridge," and it can trigger a LaraPaper render on the Pi without a single inbound port being open anywhere. The display becomes something an agent can write to, not just a thing I configure by hand. Zero open ports, full control, through a private tailnet. The dream.

The reality: the Pi 3B struggles to render images for the TRMNL display. LaraPaper's image generation pipeline is heavier than it looks, and the Pi 3B's hardware can't keep up reliably. It works, but there's friction - rendering timeouts, occasional blank screens, general sluggishness. I'm still trying to polish this. The Pi 4 would likely handle it fine; the 3B is at its limit. Work in progress.

## The real gripe: self-hosted ≠ full-featured, and that's not well communicated

The most frustrating part of the DIY/self-hosted experience isn't the hardware or the hosting - it's discovering that several plugins rely on TRMNL's proprietary cloud connectors that you can't replicate when self-hosting. Google Calendar is the obvious example: the TRMNL cloud acts as an OAuth intermediary. Without it, you need to build your own OAuth flow, run a cloud function to fetch calendar events, and wire it up yourself. The plugin exists in LaraPaper's ecosystem, but it won't work out of the box without the TRMNL cloud doing its part.

This isn't clearly communicated in the documentation. You find out when you set up the plugin and nothing happens. It would save new self-hosters significant time if the docs clearly labelled which plugins require cloud connectors.

## Building and maintaining it with an agent

The other half of the self-hosted story is upkeep: once the device is on the fridge, you want to tweak layouts, add widgets, and fix the odd broken plugin without it becoming a weekend job every time. This is where I leaned on AI agents, and it's where the DIY path actually got *fun* rather than fiddly. Three complementary paths bridged every gap I hit:

- **LaraPaper's MCP server - the most reliable path.** This ended up being how I do most of the work: creating and refining widgets, adjusting layouts, poking at the state of the instance. An agent talking to LaraPaper over [MCP](https://modelcontextprotocol.io/) gets structured, first-class access to the things I actually want to change, so "add a widget that shows X" is a conversation rather than a manual slog through the UI. The custom plugin I'd mentioned building earlier? It was built and iterated this way - describe the widget, let the agent scaffold it against LaraPaper, render, look at the result, refine.
- **The HTTP API** for the programmatic bits MCP didn't cover - scripted updates, pushing content, wiring the display into other automations (including the OpenClaw-over-Tailscale path above).
- **Browser automation** for the last mile: the parts of LaraPaper's dashboard that live only in the web UI. For this I tried Vercel's [agent-browser](https://github.com/vercel-labs/agent-browser) - a fast native CLI built for AI agents that exposes the page as an accessibility tree with element refs (`snapshot`, then `click @e2`, `fill @e3`), which is far more robust for an agent than pixel-hunting - paired with [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) for inspection and debugging.

Between the three, there was no part of my setup an agent couldn't reach: structured changes through MCP, scripted changes through the API, and UI-only changes through the browser. That's what closed the gap between "self-hosted TRMNL is a tinkering project" and "self-hosted TRMNL is something I can maintain by talking to it."

## What I think of TRMNL as a company

Despite the self-hosted friction, I genuinely like how TRMNL operates. The device and cloud pricing is relatively high by design - and a meaningful portion of that revenue flows back to the community. Through their [Creator Fund](https://trmnl.com/blog/creator-fund), 80% of TRMNL+ subscription revenue and 10-15% of hardware sales go directly to plugin authors and open-source contributors, paid out monthly. Plugin authors earn based on installs, playlist presence, and impressions. Open-source contributors (firmware, BYOS implementations, 3D models, localisations) each get a share. The first payout in late 2025 distributed over $15,000 to creators. It's a fair model - you're paying for a device and service that funds the community building the ecosystem you're using.

## The Kindle angle

TRMNL officially supports [retrofitting an old Kindle into a TRMNL display](https://github.com/usetrmnl/trmnl-koreader) via KOReader - this is now the recommended method as of 2026, replacing the older KUAL/WinterBreak approach. You jailbreak the Kindle, install KOReader, drop in TRMNL's plugin, point it at your BYOD license or self-hosted server. The result is a higher-resolution display than the native TRMNL hardware (Kindle Paperwhite at 1448×1072 vs the standard 800×480) running on hardware that was otherwise sitting in a drawer.

I haven't tried this yet - I love my active Kindle too much to use it as an experiment and don't have a spare. But it's on the list. If you have an old Kindle 6th gen or newer collecting dust, the KOReader method is worth a look.

## Is it worth it?

For the tinkering itself: absolutely yes. Building the device, setting up the backend, [creating widgets agentically](#building-and-maintaining-it-with-an-agent), wiring it into a Tailscale network so an AI agent can push updates to it - all of that was fun and educational. The fridge display genuinely gets used daily.

For the "I just want a dashboard that works": buy the $139 device and use the TRMNL cloud. The self-hosted path requires knowing your way around Docker, PHP, OAuth, and potentially image generation pipelines. The gap between what the cloud offering does and what you get out of the box with self-hosting is real and not well-signposted.

Recommended if you like to tinker, know both software and hardware (or want to learn), or have old hardware to repurpose. Not recommended if you want something that works in an afternoon without surprises.

- [TRMNL DIY documentation](https://docs.trmnl.com/go/diy)
- [LaraPaper on GitHub](https://github.com/larapaper/larapaper)
- [Terminus on GitHub](https://github.com/usetrmnl/terminus)
- [TRMNL Creator Fund](https://trmnl.com/blog/creator-fund)
- [Turn a Kindle into a TRMNL via KOReader](https://github.com/usetrmnl/trmnl-koreader)
- [TRMNL 7.5" OG DIY Kit on Seeed Studio](https://www.seeedstudio.com/TRMNL-7-5-Inch-OG-DIY-Kit-p-6481.html)
- [Vercel agent-browser](https://github.com/vercel-labs/agent-browser) - the browser-automation CLI I used for the LaraPaper UI
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) - inspection and debugging over MCP
