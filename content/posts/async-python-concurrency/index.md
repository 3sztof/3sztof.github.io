---
title: "Async Python: Concurrency Without The Headaches"
date: 2025-07-17
description: "A summary of key resources for mastering asynchronous programming in Python"
tags: ["python", "asyncio", "concurrency", "programming"]
categories: ["Development", "Python"]
---

## Presentation Overview

Recently, I had the opportunity to present a talk titled "Async Python: Concurrency Without The Headaches" at [EuroPython 2025](https://ep2025.europython.eu/) alongside my colleague Mateusz Zaremba. Our presentation provided a practical guide to asynchronous programming in Python, breaking down complex concepts into digestible explanations with clear examples. As a DevOps Engineer at AWS and Mateusz as an Application Architect at Ørsted, we shared our expertise on making async Python more approachable and less intimidating.

For more information about the conference and my speaking engagement, check out my [EuroPython 2025 speaking page](/speaking/2025-europython/).

## Special Thanks to EuroPython

I want to extend a heartfelt thank you to the EuroPython conference organizers, participants, and the entire EuroPython Society for making this event possible. The conference provided an incredible platform for knowledge sharing, networking, and community building. The dedication of the volunteers and staff created a welcoming environment that fostered learning and collaboration among Python enthusiasts from across Europe and beyond.

## Key Points from the Presentation

### Understanding Async Programming

- **Why Async?** Traditional synchronous code blocks execution, while asynchronous programming allows tasks to yield control, enabling non-blocking execution and improved efficiency.
- **Concurrency vs. Parallelism**: The presentation clarified the difference between these often confused concepts, explaining when each is appropriate.

### When to Use Async

- **Ideal for I/O-bound tasks**: Network requests, file operations, and database queries
- **Not recommended for**: CPU-bound tasks like heavy computations, 3D rendering, or image/video processing

### Core Async Components

1. **`async def`**: Defines a coroutine function
2. **`await`**: Pauses execution until an awaitable completes
3. **Event Loop**: The "heart" of async execution that manages tasks

### Common Pitfalls

The presenters highlighted several common mistakes:
- Forgetting to await coroutines
- Mixing blocking code with async code
- Not using debug mode when troubleshooting

### Practical Examples

The presentation included several code examples demonstrating:
- Basic coroutine definition and execution
- Using `asyncio.gather()` to run multiple tasks concurrently
- How mixing blocking code with async code can negate performance benefits
- Using asyncio debug mode to identify issues

### Real-World Use Cases

Async Python shines in several scenarios:
- Reading files (using aiofiles)
- Downloading files from the web (using aiohttp)
- Running database queries (using SQLAlchemy with AsyncSession)
- Running web servers (using FastAPI)

### Making Async Simpler

The presenters introduced Asyncer, a library that simplifies working with async code:
- `@asyncify`: synchronous functions callable in async context
- `@runnify`: makes async functions easily callable from synchronous code

## Key Takeaways

1. Async Python excels for I/O-bound tasks
2. The event loop is single-threaded yet enables concurrency
3. Be cautious when mixing blocking code with async code
4. Async Python is powerful but can become complex if not approached carefully
5. Consider whether async is appropriate for your specific use case

## When Not to Use Async

- Simple, short-running scripts
- CPU-bound applications
- When dependent libraries aren't async-ready
- When your team isn't familiar with async patterns

## Useful Resources

For those looking to dive deeper into asynchronous Python programming, here are the invaluable resources shared during the presentation:

1. [Official Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html) - The comprehensive guide to Python's asyncio library, including tutorials, reference materials, and examples.

2. [Real Python: Async IO in Python](https://realpython.com/async-io-python) - An excellent tutorial that breaks down asyncio concepts with practical examples and clear explanations.

3. [Real Python: Python Async Features](https://realpython.com/python-async-features) - A deeper dive into Python's asynchronous features beyond just asyncio.

4. [Asyncer](https://asyncer.tiangolo.com) - A library that makes asyncio even more user-friendly, created by the author of FastAPI.

5. [Python Concurrency with asyncio](https://www.manning.com/books/python-concurrency-with-asyncio) - A comprehensive book on mastering asyncio for production applications.

6. [Trio](https://trio.readthedocs.io/) - An alternative async library focused on usability and correctness.

## Feedback

Did you find this summary helpful? Have you implemented asyncio in your projects? I'd love to hear about your experiences with asynchronous Python programming!

Please share your thoughts through this [feedback form](https://pulse.aws/survey/QC6S258J).
