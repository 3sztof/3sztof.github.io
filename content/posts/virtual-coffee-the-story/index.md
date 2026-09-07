---
title: "Collide: How an Introvert Built a Machine to Meet People"
date: 2026-06-12
description: "A physics lab had a clever little tool for introducing strangers over lunch. I never used it, but the idea stuck - so I rebuilt it from the ground up, ran it for years, and watched it introduce people who'd never have met otherwise. This is that story."
tags: ["serverless", "aws", "python", "react", "side-project", "building-in-public", "community"]
categories: ["Development"]
draft: false
---

I am not a natural at meeting people.

If you put me in a room full of strangers, my instinct is to find the one person I already know, or failing that, the wall. I'm the kind of person who has interesting colleagues two desks away that I never actually talk to, because starting the conversation requires a small activation energy I rarely have lying around.

So this is the slightly absurd story of how I dealt with that the only way I know how: I built a machine to do the hard part for me. And then a lot of other people started using it too.

> **Quick disclaimer up front:** this is my personal passion project. It runs on AWS, and it has happily introduced people at places I've worked - but it is not an Amazon product, not an AWS product, not affiliated with or endorsed by anyone. It's a non-commercial thing I build in my own time because I enjoy it. It's also **not open-source** - it might be one day, at [github.com/3sztof/collide](https://github.com/3sztof/collide), but for now it's deliberately closed (more on why later; follow along on [my GitHub](https://github.com/3sztof) if you're curious). With that out of the way:

## The Idea Came From a Physics Lab

Back in 2018 I spent a summer at CERN as a summer student, and somewhere in there I came across a tool they had called [LunchCollider](https://home.cern/news/news/cern/colliding-ideas-over-lunch).

The premise was beautifully simple. CERN is enormous and wildly diverse - thousands of people from everywhere, working on everything. You could spend years there and never meet the person whose work would change yours. So a few CERNies built a tiny tool: register in the morning, an algorithm pairs you with a random stranger, and at noon you meet them for lunch. That's it. No idea who you'd get. You just showed up and talked to a human you'd never otherwise have met.

The idea lodged itself somewhere in my head and refused to leave. *(If any current CERN folks or alumni are reading this and know where LunchCollider stands today - still running? long gone? - I'd genuinely love to hear from you.)*

What got me wasn't the technology. It was the realisation that the awkward thing - approaching a stranger - could be **outsourced to a system**. The algorithm makes the introduction. You just have to show up. For someone wired like me, that reframing was a small revelation. The friction I'd always treated as a personal failing was just a missing piece of software.

## So I Built My Own

The CERN tool was a brilliant idea wrapped in a very simple package. I wanted it for my own circle - so I did the obvious engineer thing and built my own version.

The first one was *embarrassingly* basic, and I mean that literally: a shared document with a list of names, and a stupid little Python script I ran by hand every Monday morning to shuffle people into pairs and fire off the emails. No database. No UI. No schedule. Just me, a script, and a recurring Monday chore I'd signed myself up for.

And it worked **immediately**. The first round went out, people actually had their coffees, and the next week more people asked to be added. There's a very specific joy in watching a thing you hacked together in an afternoon do exactly the small useful thing you hoped it would.

> Lesson one of building things people use: the embarrassing version that ships beats the elegant version that doesn't.

I called it Virtual Coffee. The name made perfect sense at the time - it was the lockdown era, everything was virtual, every "coffee" was a video call. The name fit the moment exactly. Hold that thought, because the name becomes important later.

As it caught on, the manual Monday ritual stopped scaling - and "remember to run the script" is a terrible foundation for something people are starting to rely on. So it grew up, one layer at a time:

- First, **automation**: serverless functions on AWS so the matching ran itself instead of waiting for me to wake up on Monday.
- Then **email at scale**, wired through SES so the invitations went out reliably without me in the loop.
- Then **proper CI/CD and deployment automation**, which is what let it spread from my immediate circle to multiple teams and offices across EMEA.

What started as a Monday chore quietly became infrastructure.

## The Part I Didn't Expect

Here's the thing nobody warns you about when you build something people like: it grows, and the *feedback* grows faster than the code.

Virtual Coffee went from a handful of people to many times that. And the part that genuinely floored me - still does - is the sheer volume of stories that came back. People telling me they'd met someone three teams over they'd never have crossed paths with. People who found a collaborator, a mentor, occasionally a genuine friend. Early-career folks who ended up having coffee with people far more senior than they'd ever have dared approach on their own.

None of those connections were rare luck. They were *manufactured on purpose*, every week, by a piece of software quietly doing the introduction so two nervous people didn't have to.

That feedback is the fuel. The constructive criticism, and especially the little "you won't believe who I got paired with this week" anecdotes, are the entire reason I cared about it then and care about it now. The tech is fun to build. The stories are why it's worth building.

## And Then It Died

I'd love to tell you it ran happily ever after. It didn't.

Side projects have a half-life, and Virtual Coffee hit its. The tech debt piled up faster than I could pay it down. The time and motivation I had for it drained away. And as it got popular, expectations started to outpace what one person could realistically maintain in their spare time - everyone wanted the next feature, and I was the entire engineering department.

And there was a subtler pressure I didn't see coming. When something you built for fun starts genuinely working, some of the enthusiasm curdles into a particular kind of expectation: *why not make it real?* Turn it into a product, spin up a team, put processes around it.

It's meant kindly - a compliment, even - but it fundamentally misreads what a passion project *is*. I didn't build it to found something; I built it because I enjoyed building it. Not every good thing needs to become a company, and not every engineer who makes a useful toy wants to become its full-time maintainer, product manager, and support desk. Explaining that - repeatedly, to well-meaning people who genuinely didn't get why I'd refuse the "obvious" next step - was its own quiet drain.

So between the tech and the maintenance and those piling expectations, I had to do the honest thing and re-prioritise. I have a day job - the work I was actually hired to do - and it needed my focus more than a coffee-matcher did.

So I let it die on purpose. The OG Virtual Coffee had crossed the line from *joy* to *burden* - and a half-maintained thing that people depend on is worse than an honestly dead one. For the better part of **three years**, it stayed dead. The thing I was proudest of building became a thing I felt slightly guilty about not maintaining.

## The "Find Out" Phase

What brought it back wasn't nostalgia. It was an experiment, and a faintly ridiculous one.

By 2026, AI-assisted coding had gotten genuinely good. I had a graveyard of unrealised features and fallen-dream ideas from the original Virtual Coffee, and I had a question I actually wanted answered: **could GenAI maintain something deliberately over-engineered?**

So I did the responsible thing and found out. The first revival was pure FAFO energy - I rebuilt it as absurdly as I could on purpose: a custom serverless-functions framework running on Kubernetes (EKS) with ArgoCD, every bell, every whistle, a setup no sane person would choose for a coffee-pairing app. The point wasn't the app. The point was to see whether AI could keep a genuinely complicated system alive.

And here's the thing - **it could.** Not magically, and not on its own. But given a strong harness - real tests, CI/CD, pre-commit hooks, steering documents, and a human with enough engineering intuition to smell when something was off (strong vibes, rigorously applied) - it was reliable. That was the realisation that flipped this from a stunt into a project worth taking seriously.

So I tore down the ridiculous version and started again, properly this time.

## The Homecoming (and the New Name)

Restarting it properly meant fixing the thing that had always nagged me: the name.

"Virtual Coffee" was a child of the pandemic - *virtual* meaning video calls, *coffee* meaning the lockdown ritual we were all clinging to. But the thing it had become wasn't about lockdown, or video calls, or even coffee. It was about colliding people who'd otherwise stay in their own orbits. The name had become a cage.

So I went back to where the idea came from. CERN's tool was the Lunch**Collider** - named, with a physicist's sense of humour, after the particle colliders that smash things together to see what new emerges. That's exactly what this does to people. The new name was obvious, and it was a homecoming:

**Collide.**

## What Collide Actually Is

Same core loop, rebuilt from the ground up on a saner architecture than the FAFO version. People opt in, the system pairs them on a schedule, the matches land as real meetings, feedback flows back. That loop was never the problem - it worked from the very first manual Monday.

And to be clear about what "rebuilt properly" means: this is not a weekend project. As of June 2026, Collide is **1000+ commits, hundreds of pull requests, 70+ [OpenSpec](/posts/openspec-agentic-dev/) specifications, and 58k+ lines of code** - the kind of scope that could be a respectable small product in its own right.

Everything *around* the loop is where the reinvention happened. Where LunchCollider was a clever idea in a barebones wrapper, Collide is a proper, ground-up build. A little tech candy, since this is still a developer blog:

- **Fully serverless on AWS.** No box to keep alive, no server to patch. The whole thing sleeps at zero cost and wakes up on a schedule to do its work. Running it for a community costs roughly the price of one real coffee per month.
- **A genuinely clever matching algorithm.** This is the heart of it, and the bit I'm proudest of. It's not a shuffle. It's history-aware (it remembers who met whom, so you don't get the same person twice), it's fair (it forms trios when the numbers are odd, so nobody's ever left out), and - the part I love most - it's **configurable on a spectrum from "people you already know" to "complete strangers."** You can tune how adventurous the matchmaking is. The default leans hard toward **new connections**, because that's the entire point: serendipity, engineered on purpose. There's more going on under the hood than I'll spell out here, but that's the soul of it.
- **A modular video-bridge backend.** A match isn't much use without somewhere to actually meet, so Collide can provision the meeting itself - and the video layer is pluggable: [Jitsi Meet](https://jitsi.org/jitsi-meet/) for a fully self-hosted, no-account option, or [Amazon Chime](https://aws.amazon.com/chime/) when you want managed AWS-native meetings. Same abstraction, swap the backend by config.
- **Calendar invites that actually land in your calendar.** Getting a real `.ics` invite to arrive correctly - so the meeting shows up on both people's calendars, not as a sad link in an email body - was genuinely one of the hardest integrations in the whole project. The `email.mime` + SES path is riddled with non-obvious gotchas; I wrote the whole thing up separately in [Sending .ics calendar invites via AWS SES from a Python Lambda](/posts/aws-ses-ics-python-lambda/).
- **A real frontend.** A modern React single-page app, so opting in and setting your preferences is a few clicks, not an edit to a list someone else maintains.
- **`cld`, a first-class CLI.** Deployment and day-to-day maintenance run through a purpose-built command-line tool. Modern Python makes this almost too easy - [Typer](https://typer.tiangolo.com/) turns type-hinted functions into a polished CLI with basically no ceremony, so "give this project proper operator tooling" went from a chore to an afternoon.
- **A hard rule: zero external dependencies.** Every integration point - corporate SSO, third-party SSO flows, the video backend, notifications - is abstracted behind a config entry rather than a hard-wired vendor call. Nothing outside AWS is *required* to run it. This is the design principle I'm most opinionated about: AWS as a platform gives you every primitive you need to build genuinely complex, fully self-contained systems if you choose to. You don't have to reach outside the fence. Treating integrations as swappable configuration instead of baked-in assumptions is what makes the whole thing portable enough to hand to someone else's org with their own identity provider and their own constraints.
- **Built to be handed over.** Infrastructure as code, a real test suite, the works - designed so someone who isn't me can stand up their own instance for their own group.

Here's the promised "more on why later": it's not open-source *yet*, and that's deliberate - not because it isn't ready (it's live in production), but because open-sourcing something that runs inside real organisations comes with grey-zone questions I'd rather answer carefully than trip over. If Virtual Coffee taught me anything, it's that the organisational and communication issues burn you, not the code. So it stays closed for now, on purpose.

## The Real Problem Isn't the Algorithm

Here's the uncomfortable truth I had to make peace with: none of the clever engineering above is what makes or breaks Collide. I could show you the matching algorithm, walk you through the history-aware fairness logic, brag about the serverless bill - and it would all be beside the point.

Because the entire thing succeeds or fails on one axis: **does it feel good to use?**

Think about what you're actually asking of someone. You're putting *another meeting* on the calendar of a person who almost certainly already has too many. Nobody is short on meetings. Nobody wakes up wishing a stranger had been added to their week. The default answer to "want another commitment?" is *no* - and every ounce of friction you introduce is one more reason to reconfirm that no. The value only exists on the far side of actually showing up and having a genuinely good time. Everything before that moment is pure cost, borne on faith.

That means the whole game is comfort. A confusing opt-in flow, an email that reads like spam, a pairing that lands at a terrible time, a preference you can't easily change, one meeting that felt awkward with no easy way to say "not like that again" - any single one of those spoils it *before the person is ever convinced it was worth their attention*. The UX itch kills the project long before the algorithm gets a chance to be brilliant. You don't get to show people the magic if they bounced off the sign-up screen.

And the genuinely hard part - the part that makes this an interesting problem and not just a CRUD app - is that **you cannot satisfy everyone at once, because people want contradictory things.**

- Some people want to meet total strangers. Others only want a gentle nudge toward colleagues they already half-know. The same "successful match" is a delight to one and a mild anxiety to the other.
- Some want it weekly and are annoyed when it's not. Others find weekly relentless and want monthly, or want to pause without feeling like they quit.
- Some love the surprise and never want to see who they got in advance. Others need context to feel safe walking into the conversation.
- Some read a warm, chatty invitation email as friendly. Others read the exact same email as trying too hard.

Every knob you add to please one group adds a decision - and a potential wrong default - for everyone else. Turn all the knobs into settings and you've built a configuration nightmare that nobody finishes. Pick sensible defaults and you've quietly told some fraction of people "this isn't for you." There's no setting that makes it universally comfortable, and pretending otherwise is how you end up with something technically impressive that people politely stop using.

So the real work of Collide isn't the code I'm proud of. It's the relentless, unglamorous chipping away at friction: making opt-in a few clicks, making preferences obvious and changeable, making the invitation feel like a warm introduction rather than a system notification, making it trivially easy to skip a week or dial the adventurousness down, and choosing defaults that are inviting to the nervous majority without being boring to the bold. Getting that right is far harder than the matching algorithm ever was - and it's the only part that actually decides whether the thing lives.

The algorithm is the heart. But the UX is the reason anyone lets it near their calendar at all.

## How I Actually Decide: Tenets

So how *do* you decide, when every choice pleases someone and annoys someone else? The thing that saved me wasn't a clever framework - it was writing down what the project is *for*, in plain language, before touching a single trade-off.

Start with a one-sentence framing of the problem as the world *without* you: today, someone who'd benefit from meeting a new colleague has to notice the urge, find a plausible person, muster the courage to reach out, and schedule it themselves - so they almost never do. Collide's entire reason to exist is to collapse that into "opt in once, and the introduction just happens." Any feature that doesn't serve that is a distraction, no matter how many people ask for it.

Then comes the part that does the real work: a short list of **tenets** - simple, non-technical rules that encode the project's priorities and let me resolve the contradictions *consistently*. These aren't architecture principles; they're product and UX principles a non-engineer could read and nod along to. They're not buried in a design doc, either - they're right there in the app's About panel, because they're a promise to users as much as a guide for me. Here are Collide's, verbatim:

- **People over process.** The goal is human connection, not productivity metrics. No agenda, no deliverables, no follow-up action items.
- **Low friction, high impact.** Remove the social barrier of "I should reach out but never do." The system does the reaching out for you.
- **Cross-pollination by default.** The algorithm deliberately mixes departments, teams, and seniority levels. Homogeneous groups are a missed opportunity.
- **Respect people's time.** Timezone-aware scheduling, a short default meeting, one-click pause. Nobody should feel obligated when life gets busy.
- **Opt-in, not opt-out.** Participation is always voluntary. The system earns trust by being useful, not by being mandatory.
- **The organizer takes initiative.** One person owns the calendar invite. Clear ownership prevents the "someone else will do it" problem.

The magic of a list like this is that it turns a thousand micro-arguments into one look-up. "Should this preference be a setting or a smart default?" isn't a fresh debate every time - I check the tenets and the answer usually falls out. When a proposed feature genuinely threatened *cross-pollination by default*, that wasn't a vibe, it was a documented conflict - and the tenets are exactly what let me review it against the vision *before* building it, and decide it needed guardrails or shouldn't ship at all. They're also how you say *no* gracefully: "great idea, but it fights *low friction*, so not this one."

And - this matters - **tenets can change.** They're not scripture. But changing one has to be a *conscious, documented decision*, not quiet drift. The moment your defaults start creeping toward "whoever complained loudest last week," the product loses its spine. Write them down, keep them visible, and when the vision genuinely evolves, evolve them on purpose. A consistent vision that occasionally, deliberately shifts beats a vision that erodes one accommodating exception at a time.

## Build the Ambitious Thing

Forget the coffee app for a second. Here's the real pitch: **build the ambitious thing you don't quite know how to build yet.**

That gap between what you can do today and what the idea demands is where all the learning lives. I didn't know serverless, or SES at scale, or half the infrastructure this runs on - I learned it *because* a silly coffee-matcher kept demanding it. A project you actually care about is the best curriculum there is.

And treat your organisation as a sandbox. Every company, lab, or team is full of small, human-shaped problems nobody's assigned to fix. You don't need a mandate or a budget - just hack together the embarrassing version and let it grow only if people reach for it. How your org reacts is its own culture test: the best places encourage building in the margins (a genuine shoutout to AWS here); the worst slap a "shadow IT" label on it and teach everyone not to try. That reaction tells you a lot about whether it's a place worth staying.

If you'd rather not build your own, that's what Collide is for - I'll share updates as it evolves. If you've run something like this, or you're a CERN alum who knows what became of the original LunchCollider, [get in touch](https://www.linkedin.com/in/3sztof/) or [follow along](https://github.com/3sztof). I love the collision stories most of all.

Because here's what building this really taught me: in the vibecoding era, shipping code is easy. Shipping something people *actually* want, in a form so intuitive they never think about it - that's the hard part, and it doesn't come from the editor. It comes from talking to people. Anyone can build. Building the *right* thing is still stubbornly human work.

So go build the thing. Then show up, and talk to the stranger - because the machine only ever handled the easy part.
