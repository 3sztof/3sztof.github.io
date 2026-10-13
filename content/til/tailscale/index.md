---
title: "Tailscale turned my scattered machines into one flat network"
date: 2026-10-13
description: "A WireGuard-based mesh VPN that stitched my home lab, robots, and AWS boxes into a single private network - no port forwarding, no bastion hosts, no static IPs to remember."
tags: ["networking", "vpn", "tailscale", "homelab", "wireguard", "tools"]
categories: ["TIL"]
draft: false
---

A shout-out to my friend Sebastien for putting [Tailscale](https://tailscale.com/) in front of me - his [blog](https://sebastien.tech/) is worth a follow. I now run basically all of my networking through it: the home lab, a couple of robots, and some AWS machines (including the box that hosts [OpenClaw](/posts/openclaw-on-graviton-ec2/)). It is one of those tools that quietly deletes an entire category of problems I used to spend evenings on.

## The problem it deletes

Before Tailscale, connecting to any of these machines meant the usual zoo: port forwarding on the home router, dynamic DNS to track the residential IP that keeps changing, SSH bastions, security groups opened a little wider than I was comfortable with, and a mental map of which box lives behind which NAT. Every new device was another round of the same yak-shave.

[Tailscale](https://tailscale.com/) is a mesh VPN built on [WireGuard](https://www.wireguard.com/). You install it on each machine, authenticate with an identity provider you already use (Google, GitHub, whatever), and every device joins a single private network - a *tailnet*. Each machine gets a stable `100.x.y.z` address and a short MagicDNS name that never changes, no matter which network it is physically sitting on.

The important part: it is a **mesh**, not a hub-and-spoke VPN. Traffic goes directly peer-to-peer whenever the NAT gods allow it, with Tailscale's coordination servers only brokering the initial connection and handing out keys. When a direct path genuinely can't be punched through a hostile NAT, it falls back to encrypted DERP relays so the connection still works - just with an extra hop.

## What it looks like in practice

Install is a one-liner on most platforms:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

After that, every machine on the tailnet can reach every other machine by name:

```bash
ssh robot-01          # a robot on my LAN, over its tailnet name
ssh openclaw          # a Graviton EC2 box in AWS
```

No security group rule opening SSH to the internet, no public IP, no VPN concentrator I have to maintain. The AWS boxes keep their SSH port closed to the world entirely and are only reachable over the tailnet.

## The features that actually earn their keep

A few things graduated this from "neat" to "load-bearing" for me:

- **MagicDNS** - machines are reachable by name, not by a `100.x` address I have to look up. `ssh openclaw` just works from anywhere.
- **Tailscale SSH** - Tailscale can terminate SSH itself and gate it with your tailnet ACLs, so access is governed by identity and policy instead of scattered `authorized_keys` files.
- **ACLs as code** - the whole access policy is one JSON file. "My laptop can reach the robots; the robots cannot reach each other; the AWS box is admin-only" is a few lines, version-controlled.
- **Subnet routers** - one node can advertise a whole subnet into the tailnet, so a device that *can't* run Tailscale (a dumb LAN gadget, a printer, a robot's onboard controller) is still reachable through a nearby node that can.
- **Exit nodes** - route all traffic through a chosen machine when you want to, which is handy for the home lab and for appearing to come from a known IP.

## Where it fits my setup

The robots are the clearest win. They roam between my home Wi-Fi, a phone hotspot, and occasionally someone else's network, so their physical IP is never stable. On the tailnet they keep one name and I can SSH in or stream telemetry regardless of where they woke up that morning. The AWS machines are the second win: OpenClaw's host sits on a locked-down security group with no inbound SSH, and I reach it purely over Tailscale. The home lab ties it together as the always-on anchor of the mesh.

The honest caveats: you are trusting Tailscale's coordination plane for key distribution and device authorization (the data plane stays end-to-end encrypted via WireGuard, but the control plane is theirs). If that tradeoff bothers you, [Headscale](https://github.com/juanfont/headscale) is an open-source re-implementation of the control server you can self-host. For me the hosted version is worth it - this is one of the few pieces of infrastructure I am happy to not run myself.

- [tailscale.com](https://tailscale.com/)
- [How Tailscale works](https://tailscale.com/blog/how-tailscale-works)
- [WireGuard](https://www.wireguard.com/)
- [Headscale - self-hosted control server](https://github.com/juanfont/headscale)
- Thanks to [Sebastien's blog](https://sebastien.tech/) for the recommendation
