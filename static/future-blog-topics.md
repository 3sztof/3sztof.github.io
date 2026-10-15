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

- **A Valheim dedicated server as cost-optimised IaC** - my [aws-cdk-valheim-server](https://github.com/3sztof/aws-cdk-valheim-server)
  wraps the community [lloesche/valheim-server-docker](https://github.com/lloesche/valheim-server-docker) image (which runs
  IronGate's official Valheim dedicated server) on EC2 via AWS CDK: S3 backups, a CloudWatch idle-alarm -> Lambda
  auto-stop, a public API Gateway + Python Lambda REST API to start/stop/status, and optional Discord lifecycle hooks.
  Angle: a game server you only pay for while someone's playing - and crediting the OSS it stands on. Public repo, ready to write.

- **ToneBot: plain English to a guitar amp preset** - [tonebot](https://github.com/3sztof/tonebot) takes a tone described
  in words and emits a ready-to-push preset for the Positive Grid Spark 2. Angle: an LLM as a translation layer from
  natural language to domain hardware, tied to the [Angine de Poitrine](/music/angine-de-poitrine/) music thread.
  **Caveat: the project is currently abandoned - needs real work on my end before this is honest to publish.**

- **Bridging an observability gap with an OpenTelemetry connector** - a small OTel connector I built to get
  telemetry out of a tool that didn't export it cleanly. Angle: when a product has a blind spot, a thin OTel
  bridge beats waiting for first-party support - what the connector maps, and the gotchas of shimming OTel onto
  something that wasn't designed for it. **Gate: must open-source the connector first, and clear employer review
  before anything is written - keep it tool-agnostic and leak nothing internal (same bar as the pi gist).**

## To revisit

- **`async-python-concurrency` voice pass** - it reads as a conference recap rather than first person.
  Worth a punchier intro/outro and a personal angle at some point.

## Shipped from this backlog

- DIY TRMNL build - [posts/trmnl-diy-build](/posts/trmnl-diy-build/)
- Virtual Coffee, the story - [posts/virtual-coffee-the-story](/posts/virtual-coffee-the-story/)
- The baseline shell stack - [posts/shell-baseline](/posts/shell-baseline/)
