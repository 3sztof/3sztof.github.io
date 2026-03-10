---
title: "Monads in Python: What We Actually Learned"
date: 2026-03-10
description: "Mateusz and I avoided monads for years. Then we decided to learn them properly - and give a conference talk about it. Here's what the journey looked like."
tags: ["python", "monads", "functional-programming", "returns", "software-design"]
categories: ["Development", "Python"]
---

A few months ago, [Mateusz Zaremba](https://www.linkedin.com/in/mateusz-zaremba/) and I made a deal: we'd finally learn monads. Not just read a blog post about them, bookmark it, and move on - actually understand them well enough to explain them to someone else.

The method we picked was a bit extreme: commit to giving a conference talk first, then figure the rest out.

This post is the written version of what we ended up with after going through that process.

## Why We Kept Avoiding Them

The standard introduction to monads goes something like this:

> "A monad is just a monoid in the category of endofunctors."

And then you close the tab.

This happened to both of us multiple times over the years. The definition is technically correct and pedagogically useless. Every time we got close to the topic, it felt like walking into a graduate maths lecture halfway through - the notation was unfamiliar, the motivation was unclear, and the examples were all in Haskell.

The other thing that made it easy to avoid: Python didn't seem to need them. You write a function, call it, handle exceptions, check for `None`. Life goes on.

## The Forcing Function

The way we finally broke through was by committing to the talk before we felt ready. Once the CFP was submitted and accepted, there was no backing out. That external deadline did more for our learning than any number of good intentions.

This is a pattern worth knowing: if there's something you've been meaning to learn but keep deprioritising, teaching it is one of the best ways to actually do it. The preparation forces you to resolve every gap, every "I sort of understand this" handwave. You can't bluff your way through a slide.

## Why Monads Exist (The Real Answer)

The honest reason monads were invented is Haskell's purity constraint. In Haskell, all functions must be pure - no side effects, no IO, no mutation. But real programs need to read files, print output, and handle errors. Monads are the mechanism Haskell uses to represent side effects as values and sequence them in a controlled way.

Python has none of these constraints. You can call `print()` anywhere, mutate global state, raise exceptions - no special type required. So the main reason monads exist in Haskell simply doesn't apply to Python.

This was an important realisation for us. A lot of the friction in learning monads comes from trying to understand them in a Python context, where the original motivation doesn't map cleanly. Once you understand *why Haskell needed them*, the concept stops feeling arbitrary.

## The Minimum Theory You Actually Need

You don't need category theory. You need two things:

**Functor** - a box that holds a value, where you can apply a function to the value inside without taking it out of the box. A list is the most familiar example: `map(fn, [1, 2, 3])` applies `fn` to each element and gives you a new list back - you never left the "list box". `Optional[T]` is another one: if there's a value inside, apply the function; if it's `None`, do nothing and return `None`. The box shape is always preserved.

```python
# map: apply a plain function to the value inside the box
# fn takes a plain value, returns a plain value
maybe_name = Some("alice")
maybe_upper = maybe_name.map(str.upper)  # Some("ALICE")
maybe_none  = Nothing.map(str.upper)     # Nothing - fn never called
```

**Monad = Functor + `bind`** - the only difference from a functor is what kind of function you pass in. With `map`, the function returns a plain value and the container wraps it back up. With `bind`, the function itself returns a boxed value - and `bind` flattens the result so you don't end up with a box inside a box (`Maybe[Maybe[str]]`).

```python
# map: fn returns a plain value -> container wraps it
Some("9").map(int)              # Some(9)

# bind: fn returns a Maybe itself -> no double-wrapping
def parse_int(s: str) -> Maybe[int]:
    return Some(int(s)) if s.isdigit() else Nothing

Some("9").bind(parse_int)       # Some(9)  - not Some(Some(9))
Some("x").bind(parse_int)       # Nothing  - short-circuits here
Some("9").bind(parse_int).bind(parse_int)  # still Some(9), not Some(Some(Some(9)))
```

That's it. The rest is just applying this pattern to different kinds of failure.

The three monad laws (left identity, right identity, associativity) are the rules that guarantee `bind` chains always behave predictably - the same way the rules of arithmetic guarantee that `2 + 3 + 4` always equals `4 + 3 + 2`. You don't need to memorize them; what matters is that they exist, and that the `returns` library obeys them, so you can refactor pipelines without worrying about subtle ordering bugs.

## Where Python Actually Benefits

After going through all of this, we landed on three patterns where monads genuinely earn their place in Python code.

### Result: Railroad-Style Error Handling

The problem this solves is multi-step pipelines where each step can fail. The typical Python approach ends up looking like this:

```python
def process(user_id: str):
    try:
        uid = int(user_id)
    except ValueError:
        return {"error": "Bad ID"}
    try:
        user = db.get(uid)
    except DBError as e:
        return {"error": str(e)}
    try:
        profile = api.fetch(user.email)
    except NetworkError as e:
        return {"error": str(e)}
    return {"user": user, "profile": profile}
```

The same error-handling pattern repeats three times. The happy path is buried. The return type is `dict` in all cases, which tells the caller nothing.

The `Result` monad version using the `returns` library:

```python
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind

@safe
def parse_id(raw: str) -> int:
    return int(raw)

@safe
def get_user(uid: int) -> User:
    return db.get(uid)

@safe
def fetch_profile(user: User) -> Profile:
    return api.fetch(user.email)

def process(raw: str) -> Result[Profile, Exception]:
    return flow(raw, parse_id, bind(get_user), bind(fetch_profile))
```

The `@safe` decorator wraps a regular function so that if it raises, you get `Failure(exception)` instead of a thrown exception. `flow` threads the value through the pipeline; `bind` skips subsequent steps if any step has already failed.

The return type `Result[Profile, Exception]` is now self-documenting. Callers handle it with pattern matching:

```python
match process("123"):
    case Success(profile):
        render(profile)
    case Failure(ValueError()):
        show_error("Invalid ID format")
    case Failure(e):
        log_and_show_generic_error(e)
```

The failure case is impossible to ignore - it's in the type.

### Maybe: Escaping the None Pyramid

Nested optional attribute access is a common place where `None` checks stack up:

```python
street = None
if order is not None:
    if order.user is not None:
        if order.user.address is not None:
            street = order.user.address.street
```

With `Maybe`:

```python
from returns.maybe import Maybe

def get_street(order) -> Maybe[str]:
    return (
        Maybe.from_optional(order)
        .bind_optional(lambda o: o.user)
        .bind_optional(lambda u: u.address)
        .bind_optional(lambda a: a.street)
    )
```

`Nothing` propagates automatically through the chain - if any step returns `None`, every subsequent step is skipped. No nesting, no repeated checks.

This is most useful in data transformation pipelines and API response parsing where deeply nested optionals are common.

### Reader: Dependency Injection Without Pollution

The `Reader` monad (implemented as `RequiresContext` in `returns`) solves a specific architectural problem: threading configuration or services through a call stack without passing them as arguments everywhere or reaching for globals.

```python
from returns.context import RequiresContext

def get_user(uid: int) -> RequiresContext:
    return RequiresContext(lambda env: env.db.query(uid))

# Inject at the program boundary:
result = get_user(42)(env=prod_env)

# Trivially testable:
result = get_user(42)(env=mock_env)
```

The function is pure. Dependencies are explicit. You inject the real environment at the outermost layer and a mock environment in tests. This maps cleanly onto clean architecture: pure domain logic at the core, effects at the edges.

## The Honest Decision Framework

We tried to be direct about when not to use them.

Use `Result` when you have 6+ step pipelines with repeated error-handling boilerplate, when you want the failure contract visible in the return type, or when you're building a functional core with effects at the edges.

Don't use monads when you have 2-3 steps (a simple `if` is clearer), when your framework already handles errors (Django, FastAPI), when the team is unfamiliar with the pattern and the learning cost outweighs the benefit, or when you need stack traces for debugging unexpected bugs - exceptions are better there.

Scott Wlaschin, who popularised Railway-Oriented Programming (the pattern `Result` implements), wrote a follow-up post in 2019 titled ["Against Railway-Oriented Programming"](https://fsharpforfunandprofit.com/posts/against-railway-oriented-programming/) walking back some of the enthusiasm. His point: don't use `Result` for unexpected errors where you need a stack trace, don't reach for it when a simple `if` or a framework's built-in error handling already does the job. Reserve it for expected, domain-level failures. Worth reading if you find yourself tempted to wrap everything.

## What the Talk Was Really About

We didn't set out to convert anyone to functional programming. The goal was to demystify something that has an undeserved reputation for being inaccessible, and to give people a practical decision framework rather than either evangelism or dismissal.

The process of building the talk was genuinely useful for us - it forced a level of clarity that reading alone wouldn't have. We had to resolve every ambiguity, find concrete examples for every abstract claim, and figure out how to explain the same concept at multiple levels of familiarity.

If there's a concept you've been avoiding because it seems hard, committing to explain it to others is a reliable way to actually learn it.

## Credit Where It's Due

A lot of resources on monads are either too abstract (category theory papers) or too shallow ("it's just a design pattern!"). Arjan Egges from [ArjanCodes](https://arjancodes.com) was the exception. His article [Python Functors and Monads: A Practical Guide](https://arjancodes.com/blog/python-functors-and-monads) and the companion video [What the Heck Are Monads?!](https://www.youtube.com/watch?v=Q0aVbqim5pE) were the single biggest reason this topic finally clicked for us. The examples are grounded, the pace is right, and he doesn't hide behind Haskell to explain concepts that apply just as well in Python. If you're starting from zero, go there first.

## Resources

- [`returns` library](https://github.com/dry-python/returns) - The production-grade FP toolkit for Python (4,200+ stars)
- [Railway-Oriented Programming](https://fsharpforfunandprofit.com/rop/) - Scott Wlaschin's original writeup (F#, but concepts translate directly); also see his 2019 ["Against Railway-Oriented Programming"](https://fsharpforfunandprofit.com/posts/against-railway-oriented-programming/) for the honest counterbalance
- [Python Functors and Monads: A Practical Guide](https://arjancodes.com/blog/python-functors-and-monads) by Arjan Egges (ArjanCodes) - the resource that made this whole topic finally click for us. If you want a gentler on-ramp before diving into `returns`, start here. He also has a companion video: [What the Heck Are Monads?!](https://www.youtube.com/watch?v=Q0aVbqim5pE)

---

*The talk was given at [Warsaw IT Days 2026](/speaking/2026-warsaw-it-days/) alongside [Mateusz Zaremba](https://www.linkedin.com/in/mateusz-zaremba/). First run of this material in front of a live audience - always the real test.*
