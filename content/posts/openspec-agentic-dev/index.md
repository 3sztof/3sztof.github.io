---
title: "The spec is the bottleneck, not the AI"
date: 2026-07-22
description: "After building a non-trivial serverless product almost entirely with AI-assisted coding, the clearest lesson is: the AI is fast. The specification is the constraint."
tags: ["openspec", "agentic-development", "ai", "software-design", "productivity"]
categories: ["Posts"]
draft: false
---

There is a recurring claim in the AI-assisted development space that the hard part is getting the model to write good code. In my experience building [Collide](/posts/virtual-coffee-the-story/) - a non-trivial serverless product that is, as of writing, 66 shipped OpenSpec specs, hundreds of pull requests (spec-only and implementation both), and roughly 75k lines of Python and TypeScript - that claim gets the problem backwards. The model writes good code. The constraint is knowing precisely what you want it to write.

## What OpenSpec is

[OpenSpec](https://openspec.dev) is a structured change management workflow for human-in-the-loop AI development. The core idea is that every change to a codebase begins as a written specification before a single line of code is touched. Each change lives in a directory:

```
openspec/
  specs/         # Base capability specs (living documents)
  changes/
    <slug>/
      .openspec.yaml   # status, phase, branch
      proposal.md      # problem statement + proposed solution
      design.md        # technical design (added at implementing phase)
      tasks.md         # implementation checklist
```

The lifecycle is `draft → proposed → designing → implementing → done`. You write the proposal. You own the design. The AI handles implementation.

What I appreciate is how *opinionated* it is. OpenSpec isn't a blank methodology you have to assemble yourself - it ships with a CLI that scaffolds and validates the whole structure, and a set of pre-built agent skills that teach your coding agent the workflow directly. You run `openspec` to set it up, and the agent already knows how to propose, design, and implement within the convention. That opinionated, batteries-included nature is exactly what makes it stick: there's a right way to do things, it's enforced by tooling rather than willpower, and you don't spend the first week bikeshedding your own process.

## What I actually observed

The bottleneck in every single feature was the proposal phase, not the implementation phase. When I handed the agent a well-written `proposal.md` plus a `design.md` with clear data model decisions, edge cases enumerated, and API contract defined - implementation was fast and mostly correct. When I handed it an underspecified proposal ("add a weekly digest email"), I got something that worked but missed three requirements I hadn't written down, which meant rework.

The pattern is consistent: ambiguity in the spec propagates directly into the code. The AI doesn't ask clarifying questions - it makes assumptions, usually reasonable ones, but often not the ones you would have made if you'd thought it through. The diff between "what you got" and "what you wanted" is almost always traceable to a gap in the written specification.

This is uncomfortable for developers who are used to holding requirements loosely in their heads and adjusting as they code. That workflow does not transfer to agentic development. You have to externalize the specification completely.

## The side effect nobody mentions: triage

My project has a constant stream of ideas - user feature requests, my own brainstorming, things that seem obvious at 11pm and less obvious in the morning. What I didn't expect is how useful OpenSpec became as a triage mechanism rather than just a documentation mechanism.

Writing a proposal forces you to think through an idea in the context of the full project - its vision, its tenets, its existing UX. A surprising number of ideas that felt like "let's do ittttt!" when they arrived dissolved on contact with a blank `proposal.md`. Not because they were technically hard, but because writing them down made it obvious they were gimmicks, or that they'd break something that was already working well, or that they solved a problem only I had and not the actual users. The spec backlog isn't just a roadmap - it's a graveyard of ideas I'm glad I didn't build, sorted by the moment I realized why.

This keeps the project focused on what actually matters. Feature drift is real, and it's insidious precisely because every individual feature sounds reasonable. The spec phase is where you catch drift before it becomes code.

Triage runs the other direction too. Collide is past ~1300 commits now, and while a large share of those were the agent implementing specs, plenty were the smaller things that don't warrant a full proposal - fixes, tweaks, refactors, config. Those aren't lost to the spec system, though: during triage I trace that raw commit history back into the *base* specs and the global steering docs, folding in whatever behaviour actually shipped. It's a cheap, mechanical habit with an outsized payoff - it keeps the living specs honest about what the system really does, keeps the LLM-facing docs clear enough that the agent isn't working from a stale mental model, and quietly reinforces the overall vision instead of letting the codebase and the specs drift apart. The specs describe intent; the commits are ground truth; triage is where you reconcile the two.

## "But writing specs takes time"

It used to. With AI assistance, the friction is low - you describe the problem, the agent helps draft the proposal and design doc, you review and correct it. The writing itself takes minutes rather than hours for most changes.

The more honest framing is that it's like test-driven development: the upfront cost is real, but it pays back as the project scales. (And yes, TDD is one of those things that conferences talked about for a decade and developers mostly practiced in theory rather than production - the irony of writing this as someone who actually does something TDD-adjacent with specs is not lost on me.) Once a project has 20+ specs in various states, the spec system is what makes the scope governable - both for your own brain and for the model's context window. Without it, every session starts with "okay so where were we" and ends with "I think I introduced a regression somewhere."

This is exactly why it scaled to Collide's size. With 66 shipped specs, the thing that keeps it tractable is that each change is *granular* - one proposal, one bounded scope, one well-defined slice of the system. The agent never has to hold the whole 75k-line project in its head; it holds one spec, its immediate dependencies, and the tenets. That granularity is doing double duty: it keeps the model's context window from overflowing into confusion, and it keeps *me* from greenlighting a change that quietly violates a design principle, because the proposal makes the blast radius explicit before anything is built. Big projects don't break because the AI can't write the code - they break because someone loses track of how the pieces fit. ([I know the pieces fit](https://genius.com/Tool-schism-lyrics) - I'd just rather not watch them fall away.) Small, well-scoped, written-down changes are the antidote.

The only time I skip a spec is for things I can verify and reverse in under ten minutes - a copy change, a config tweak, a one-line fix to something clearly broken. Anything that touches the data model, the API contract, or user-visible behavior gets a proposal first.

## What the AI is actually good at

Given a complete spec, the implementation quality is high. The model follows existing patterns reliably when you give it good agent instructions - I keep about 20 instruction files in `.opencode/instructions/` covering things like DynamoDB single-table access patterns, SES + ICS email generation, Lambda Powertools conventions, Cognito auth flows, testing strategy with moto. Each file is a compact reference: "here is how this project does X, follow this exactly." Without them, the agent invents its own conventions. With them, the tenth Lambda function looks like the first.

The model also doesn't get bored or cut corners. It doesn't decide the ninth similar endpoint is "basically the same" and ship something slightly inconsistent. That kind of consistency is genuinely hard for a human working alone on a personal project, and the agent delivers it essentially for free once the patterns are documented.

Where it struggles: cross-cutting changes that touch the spec's stated scope boundary, anything involving external service behavior that isn't documented somewhere it can read, and any situation where the "right" answer requires product intuition rather than engineering judgment. Those remain human decisions.

## Staying the architect

The boundary that makes the whole thing work: I own all design decisions. The AI owns all implementation decisions within the agreed design. The line is stated explicitly in my global steering file - "you are the hands; the human is the architect" - and it's there because it's easy to drift from. That whole steering file is worth its own writeup, which I've done separately: [the system prompt that keeps my AI coding agent honest](/til/agents-md-that-keeps-agents-honest/). The short version: it's built on the failure modes Andrej Karpathy laid out in his [viral AI-coding rant](https://x.com/karpathy/status/2015883857489522876) - the insight that AI's coding failures are mostly human failure modes wearing different clothes.

This is the same boundary that distinguishes a good tech lead from a hands-off manager. What's new is that it now matters at the granularity of individual feature changes rather than at the project level.

## Practical notes

The OpenSpec CLI is worth using even if you don't follow the full methodology. The habit of writing `proposal.md` before starting any non-trivial change - ten minutes of structured thinking about what you're actually trying to build - noticeably improves what you get back. And the backlog of `draft` and `proposed` specs is an honest representation of your roadmap: not a pile of vague intent, but a set of actual decisions waiting to be made.

- [OpenSpec on GitHub](https://github.com/Fission-AI/OpenSpec)

