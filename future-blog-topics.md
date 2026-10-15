# Future Blog Post Topics

My running backlog. Each idea has a one-line angle - what the post argues, not just what it's about.
When something ships, move it to "Shipped from this backlog".

## Ideas

### TILs (short, scrappy)

- **Tailscale SSH + ACLs as code** - a follow-up to the [Tailscale TIL](/til/tailscale/): the actual ACL
  JSON for "laptop reaches robots, robots can't reach each other, AWS box is admin-only", plus Tailscale SSH
  replacing scattered `authorized_keys`. Angle: access policy should be a version-controlled file, not tribal knowledge.

- **Tailscale exit nodes + subnet routers for the home lab** - reaching the LAN gadget that can't run
  Tailscale, and routing traffic through home, with the robot/OpenClaw setup as the worked example.

- **cmux follow-up: did it actually retire Ghostty + Zellij?** - the verdict the [cmux TIL](/til/cmux/)
  promises, once session restore has earned my trust. Angle: an honest after-N-weeks report, including what
  `cmux hooks setup` agent-session resume does and doesn't recover.

### Posts (longer, opinionated)

- **pi after a month** - the [sports-car post](/posts/pi-coding-agent-sports-car/) covered the first day and
  the [published setup](https://gist.github.com/3sztof/c94b9b1176085e79fcfa06100b9a1374). Angle: what stayed
  installed, what I ripped out, and whether I still open the tanks at all.

- **Agent memory, compared** - the [LLM wiki](/posts/llm-wiki-persistent-agent-memory/), OpenClaw's
  daily-notes-plus-dreaming tiers (from the [Graviton post](/posts/openclaw-on-graviton-ec2/)), and `pi-memory`,
  side by side. Angle: what actually survives across sessions vs. what I expected to survive.

- **MCP vs. a plain CLI** - after trimming MCP down to a handful of servers in pi. Angle: where MCP earns its
  keep, and where a CLI plus a skill file does the same job with less prompt weight.

- **The post-thumbnail skill** - this repo's `post-thumbnail` skill fetches official SVGs (SVGL / Simple Icons /
  brand sites), falls back to Lucide icons, recolours white logos, and fits any aspect ratio into the same safe box.
  Angle: a small, boring automation that made every thumbnail on the site look like a set - plus what to do when
  only a low-res raster logo exists.

- **OpenClaw, a few months in** - a follow-up to the [Graviton post](/posts/openclaw-on-graviton-ec2/).
  Angle: what the agent built for itself, what dreaming actually kept, and what I had to clean up after it.

- **Code review as two questions** - my code-review agent skill runs two passes in parallel sub-agents: does the
  change follow the repo's standards, and does it match the spec it came from? Angle: review is two different
  questions, and splitting them beats one muddled pass.

## To revisit

- **`async-python-concurrency` voice pass** - it reads as a conference recap rather than first person.
  Worth a punchier intro/outro and a personal angle at some point.

## Shipped from this backlog

- DIY TRMNL build - [posts/trmnl-diy-build](/posts/trmnl-diy-build/)
- Virtual Coffee, the story - [posts/virtual-coffee-the-story](/posts/virtual-coffee-the-story/)
- The baseline shell stack - [posts/shell-baseline](/posts/shell-baseline/)
