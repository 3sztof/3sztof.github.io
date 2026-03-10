---
title: "Speaker: Warsaw IT Days 2026"
date: 2026-03-20
description: "Presenting 'Monads in Python: Math Hell or Pure Perfection?' at Warsaw IT Days 2026 alongside Mateusz Zaremba."
tags: ["Python", "Monads", "Functional Programming", "Conference", "Warsaw IT Days"]
---

## Presentation

- **Topic**: Monads in Python: Math Hell or Pure Perfection?
- **Language**: Polish / English
- **Date**: March 20, 2026
- **Co-presenter**: [Mateusz Zaremba](https://www.linkedin.com/in/mateusz-zaremba/), Senior Architect at Ørsted

In a joint talk with [Mateusz Zaremba](https://www.linkedin.com/in/mateusz-zaremba/), we explored monads - one of those concepts that has a reputation for being scary and Haskell-exclusive - and showed what they actually look like when applied pragmatically in Python.

The talk started with an honest premise: we avoided monads for years, decided to finally learn them properly, and building a conference talk was our way of forcing ourselves through the material. The result was a presentation that skips the category theory and focuses on the single question that matters for working Python developers: *when does this actually help me ship better code?*

The presentation covered:
- Why monads exist in the first place (Haskell's purity problem and how IO monads solve it)
- The minimal theory you need: functors, `bind`, and the three laws
- Why Python usually doesn't need monads - and being honest about that
- Three patterns where they genuinely help: `Result` for error pipelines, `Maybe` for nested optionals, `Reader` for dependency injection
- A practical decision framework: when to reach for them, and when not to
- The `returns` library as the production-grade Python implementation

For a deeper look at the content, check out my [blog post on monads in Python](/posts/python-monads/).

## Event

- **Date**: March 20, 2026
- **Location**: PGE Narodowy, Warsaw, Poland
- **Website**: https://warszawskiedniinformatyki.pl/
- **Recording**: Available after the event

## More

Warsaw IT Days (Warszawskie Dni Informatyki) is one of Poland's largest and most established IT and Data Science conferences, bringing together over 10,000 participants annually. The 2026 edition at PGE Narodowy featured 25+ tracks and 300+ talks across all levels and technology areas.

This was the first public run of the monads talk - a topic we genuinely found hard to learn and even harder to explain clearly. Getting it in front of a large audience was the real test.

## Resources

The resource that made this whole topic finally click for us was Arjan Egges from [ArjanCodes](https://arjancodes.com) - his article [Python Functors and Monads: A Practical Guide](https://arjancodes.com/blog/python-functors-and-monads) and the companion video [What the Heck Are Monads?!](https://www.youtube.com/watch?v=Q0aVbqim5pE) cut through the usual noise and made the concepts genuinely accessible. If you want to go deeper after the talk, start there.
