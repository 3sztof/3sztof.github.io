---
title: "Speaker and Program Committee Member: PyCon Wrocław 2026"
date: 2026-11-18
draft: false
description: "Co-presenting 'Would you accept this PEP?' - an interactive talk on Python language design - at PyCon Wrocław 2026, while also serving on the Program Committee."
tags: ["Python", "PEP", "Language Design", "Public Speaking", "Conference", "PyCon", "Wrocław"]
---

## Presentation

- **Topic**: Would you accept this PEP?
- **Language**: English
- **Format**: Interactive two-speaker talk, 30 minutes
- **Co-presenter**: [Mateusz Zaremba](https://www.linkedin.com/in/mateusz-zaremba/), Senior Architect at Ørsted

For the third year in a row, Mateusz and I are returning to PyCon Wrocław together. This time with a talk that is less about writing Python and more about understanding why Python looks the way it does.

The premise: Python did not become Python by accepting every good-looking idea. Some proposals sounded absurd but addressed real problems. Others looked like obvious improvements until compatibility, semantics, tooling, or one deeply inconvenient edge case entered the room. The language is shaped by thousands of small decisions made in public, and most of them are still readable today if you know where to look.

## The format

The audience becomes the language review team for 30 minutes.

After a quick warmup, we present three real Python Enhancement Proposals - without immediately revealing their outcomes. For each one, one of us makes the strongest case for the change. The audience votes: accept, reject, or send it back. Then the other speaker gets one more slide of rebuttal before we show what actually happened.

The proposals on the agenda:

**PEP 336 - Make None Callable** (opening warmup, already decided). What if calling `None` was a silent no-op instead of a `TypeError`? The idea was to simplify callback dispatch tables. Guido's response has become something of a classic.

**PEP 3126 - Remove Implicit String Concatenation**. Adjacent string literals in Python silently merge: `"foo" "bar"` becomes `"foobar"`. That is not a bug - it is intentional C heritage. But a missing comma in a list of strings produces the same result with no warning. The PEP tried to ban the feature entirely during the Python 3 cleanup window. The community said no. Then Guido made the exact same mistake six years later and briefly reopened the question.

**PEP 802 - Display Syntax for the Empty Set**. Every built-in collection has an empty literal: `[]`, `()`, `{}`. Except sets. `{}` is a dict. So you write `set()`, which is a name lookup that breaks if someone shadows it. PEP 802 proposed `{/}` to fill the gap. The discussion thread ran to 246 posts before a participant asked for it to be closed on the grounds that it had become repetitive.

**PEP 823 - None-Aware Access Operators**. The newest proposal, still unresolved as we prepare the talk. `a?.b` and `a?[key]` would short-circuit to `None` when the receiver is `None`, avoiding the repetitive `if x is not None` chains that show up whenever you work with optional data. Python has debated this family of operators since 2015 across four separate PEPs. This one is the narrowest attempt yet, with Guido as sponsor, and the Steering Council has an open issue on it.

## What the talk is really about

The proposals are the vehicle. The actual subject is how language design works in practice.

A PEP is not a petition. Comment counts do not decide anything. The Steering Council has final authority and may delegate to a PEP-Delegate for specific domains. Public discussion is evidence, not a ballot. A good case on both sides is what makes a decision defensible - and what makes a later reversal expensive.

We want the audience to feel that tension directly. Voting before seeing the outcome, then hearing the rebuttal, is a different experience from reading about governance in a document. If a few people change their vote along the way, the talk has done its job.

## Program Committee

This year I also served on the PyCon Wrocław Program Committee, helping the organizers review talk submissions and shape the conference program. It is a different kind of work from presenting - reading proposals, thinking about what a room full of Python developers actually wants to leave knowing, trying to build a schedule that is both technically strong and varied.

If you are thinking about submitting to a Python conference and have not done it before: the feedback process is genuinely useful, and the bar is not "are you an expert" but "do you have something interesting to say."

## Event

- **Dates**: November 20-21, 2026
- **Location**: Concordia Design Wrocław, Wyspa Słodowa 7, Wrocław, Poland
- **Website**: [pyconwroclaw.com](https://www.pyconwroclaw.com/)

## Related

- [Speaker: PyCon Wrocław 2025](/speaking/2025-pycon-wroclaw/) - Async Python: Concurrency Without the Headaches
- [Speaker: PyCon Wrocław 2024](/speaking/2024-pycon-wroclaw/) - Our first PyCon Wrocław talk
