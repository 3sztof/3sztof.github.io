# Future Blog Post Topics

> Note: the previous contents of this file were all **already written and published** -
> they're linked under "Shipped" below so the backlog reflects reality. New candidate
> topics live under "Ideas". Keep this file as the single backlog; move an item to
> "Shipped" when its post goes live.

## Ideas

These are drawn from tools and work that already show up across the site but don't have
their own post yet. Each has a one-line angle so it's clear what the post *argues*, not
just what it's *about*.

### TILs (short, scrappy)

- **The baseline shell stack: zoxide, starship, bat, fzf, yazi, tldr** — the [Atuin TIL](/til/atuin/)
  promised "I should probably write a short TIL about each of them." Either one TIL per tool, or a
  single "my terminal baseline" roundup tied to the [bootstrap script](https://gist.github.com/3sztof/0d3f5c30510fcb8be23273bbbe1413ba).
  Angle: these are the seven tools I install before I feel at home on a new box.

- **Tailscale SSH + ACLs as code** — a follow-up to the [Tailscale TIL](/til/tailscale/) that goes one
  level deeper: the actual ACL JSON for "laptop reaches robots, robots can't reach each other, AWS box
  is admin-only," plus Tailscale SSH replacing scattered `authorized_keys`. Angle: your access policy
  should be a version-controlled file, not tribal knowledge.

- **Tailscale exit nodes + subnet routers for the home lab** — the practical "reach the dumb LAN gadget
  that can't run Tailscale" and "route traffic through home" patterns, with the robot/OpenClaw setup as
  the worked example.

- **cmux follow-up: did it actually retire Ghostty + Zellij?** — the verdict post the [cmux TIL](/til/cmux/)
  explicitly promises, once the native session restore has earned enough trust. Angle: honest after-N-weeks
  report, including what `cmux hooks setup` agent-session resume does and doesn't recover.

### Posts (longer, opinionated)

- **pi as a sports car, part 2 / my pi setup** — the [sports-car post](/posts/pi-coding-agent-sports-car/)
  argued the philosophy; a follow-up could show the actual minimal config, extensions, skills, and the
  "config over code" discipline. Angle: what a deliberately minimal agentic setup looks like in practice.

- **Persistent agent memory, beyond the LLM wiki** — a sequel to [llm-wiki-persistent-agent-memory](/posts/llm-wiki-persistent-agent-memory/):
  daily logs + long-term memory + scratchpad as a working system, and what actually survives across
  sessions vs. what you thought would. Angle: memory is a product surface, not a feature you bolt on.

- **MCP in anger: what a dozen MCP servers across four agents taught me** — you run MCP servers across
  opencode, codex, claude, and kiro. Angle: where MCP earns its keep vs. where a plain CLI is simpler,
  and the porting tax of keeping four agents in sync.

- **The post-thumbnail skill: generating uniform OG images from logos** — the repo's own `post-thumbnail`
  skill now fetches official SVGs (SVGL / Simple Icons / brand sites), falls back to Lucide icons, recolors
  white-fill logos, and fits any aspect ratio into a consistent safe box. Angle: a small, boring automation
  that made 25+ thumbnails look like a set - and how to upscale/trace logos when only a low-res raster exists.

- **Running an LLM on a Graviton box: the OpenClaw home-lab stack** — tie together OpenClaw on Graviton EC2,
  reached over Tailscale, with persistent memory. Angle: a self-contained always-on agent that extends itself
  and "dreams" - what the full home-lab-plus-cloud topology actually looks like end to end.

- **Code review with sub-agents: parallel Standards + Spec reviews** — the `code-review` skill runs two
  review passes (does it follow repo standards? does it match the originating spec?) in parallel sub-agents
  and reports side by side. Angle: review is two different questions, and splitting them beats one muddled pass.

## To refine / revisit

- **`async-python-concurrency` voice pass** — the post is complete but reads as a formal conference recap
  ("Special Thanks to EuroPython", key-points bullets, an AWS `pulse.aws` survey link) rather than the
  punchy first-person voice of posts like [python-monads](/posts/python-monads/). Not urgent, but worth a
  punchier intro/outro and a personal angle when there's an appetite to revisit it.

## Shipped (was the old backlog)

- DIY TRMNL build → [posts/trmnl-diy-build](/posts/trmnl-diy-build/)
- Virtual Coffee, the story → [posts/virtual-coffee-the-story](/posts/virtual-coffee-the-story/)
- OpenSpec + agentic development (Collide) → [posts/openspec-agentic-dev](/posts/openspec-agentic-dev/)
- AWS SES + ICS calendar invites in Python Lambdas → [posts/aws-ses-ics-python-lambda](/posts/aws-ses-ics-python-lambda/)
- Pulumi Python vs AWS CDK → [posts/pulumi-vs-cdk-python](/posts/pulumi-vs-cdk-python/)
- `uv` for multi-package Python monorepos → [til/uv-python-monorepo](/til/uv-python-monorepo/)
