---
title: "Speaker: Warsaw Python Pizza 2026"
date: 2026-04-23
description: "Presenting 'Beat the Pareto Principle: Let AI Handle the How, So You Can Focus on the Why' at Warsaw Python Pizza."
tags: ["Python", "AI", "LLM", "MCP", "Public Speaking", "Conference", "Warsaw", "Python Pizza"]
---

## Presentation

- **Topic**: Beat the Pareto Principle: Let AI Handle the How, So You Can Focus on the Why
- **Language**: English
- **Date**: May 9, 2026
- **Format**: 10-minute talk

*This is an upcoming talk - the event takes place on May 9, 2026.*

We don't go to conferences to hear someone read documentation aloud. We go to be inspired - to see the *why* behind the *how*. Yet most tech speakers fall into the Pareto trap: spending over 80% of their prep time on low-value work - tweaking slide layouts, writing Wikipedia-style definitions, chasing research rabbit holes, and formatting code snippets - only to deliver a talk that lacks pulse and impact.

This talk is about breaking that pattern. By wiring LLMs into the preparation workflow via an MCP pipeline, we let AI handle the *how* - research, formatting, and structure - and reclaim the time and energy to focus on the *why*: the story, the opinion, the lived experience that only the speaker can provide.

The talk is self-demonstrating: the deck itself was built using exactly the loop it describes. The abstract and session details provided the *why*; the AI handled layout, research, Slidev syntax, and styling. A Playwright MCP closed the feedback cycle - screenshots, DOM inspection, fix, repeat - without ever leaving the agent.

### The Pareto Tax

Most tech speakers spend 80% of their preparation time on work that an LLM can do in minutes. The remaining 20% - the message, the arc, the moment that makes an audience lean in - gets whatever energy is left. The result is technically correct content delivered without pulse. The fix is not to work harder; it is to stop doing the wrong 80%.

### The AI Loop

The core workflow is a six-step cycle with the speaker at the center:

1. **Generate** - prompt the LLM with the talk's abstract, constraints, and story intent
2. **Validate** - use Playwright MCP to screenshot and inspect the output
3. **Refine** - feed the visual and structural feedback back into the agent
4. **Learn** - understand what the model produced and why
5. **Practice** - rehearse with the actual output, in your own words
6. **Stay on message** - cut anything that doesn't serve the *why*

This loop works with any code-friendly slide format. The talk used [Slidev](https://sli.dev) - Markdown and Vue components in a Git repository, fully writable by an LLM. The same pattern applies to Reveal.js or Marp. The browser MCP is what transforms a one-shot generation into a real iterative feedback cycle.

The starter templates used for this talk (with skills and MCP pre-configured) are available on GitHub:
- [github.com/3sztof/slidev-starter-opencode](https://github.com/3sztof/slidev-starter-opencode)
- [github.com/3sztof/slidev-starter-kiro](https://github.com/3sztof/slidev-starter-kiro)

### The Documentation Trap

The talk doesn't just sell the pipeline - it warns about the dependency it creates. If AI writes your code or content, three uncomfortable moments will eventually arrive: a colleague asks you to explain a design decision in a PR review, a bug surfaces at 2 a.m., or a customer needs a live unscripted walkthrough. In all three cases, "the AI wrote it" is not an answer.

> "Delegation without understanding is not oversight. It is abdication."

The practical response is four habits: review every AI output like a junior developer's PR, prompt the model to explain its choices, prototype something yourself first - even badly - to build mental ownership, and always be able to tell the story in your own words before any talk, review, or demo.

### Flipping the Ratio

The goal is to invert the Pareto distribution. Before: 80% formatting, research, and layout; 20% the message. After: 20% steering the AI and reviewing its output; 80% the message, the story, the *why*. The audience showed up for the speaker. The point of the pipeline is to give that speaker time to actually prepare.

## Event

- **Date**: May 9, 2026
- **Location**: PJAIT building A, Auditorium, Koszykowa 86, Warsaw, Poland
- **Website**: https://warsaw.python.pizza/
- **Live Stream**: Available on the day of the event

## More

Python Pizza is an annual micro-conference originating in Naples in 2017. It has since visited Hamburg, Berlin, Cuba, Czechia, and a number of other cities, always organized entirely by volunteers and centered on one constraint: every talk is exactly 10 minutes. That constraint strips away filler and forces speakers to get to the point fast - which makes it exactly the right venue for a talk about eliminating low-value preparation work.

Warsaw is the latest city to host the event. The 2026 edition is held at PJAIT (Polish-Japanese Academy of Information Technology), brought together by Piotr Grędowski, Dorota Ostrowska, Natalia Traczewska, and the Data Science Club PJATK.

## Resources

- [Warsaw Python Pizza](https://warsaw.python.pizza/)
- [Python Pizza](https://python.pizza/)
- [Slidev](https://sli.dev)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [slidev-starter-opencode](https://github.com/3sztof/slidev-starter-opencode)
- [slidev-starter-kiro](https://github.com/3sztof/slidev-starter-kiro)
