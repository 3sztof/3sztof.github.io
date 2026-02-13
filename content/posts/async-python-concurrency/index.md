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

## Code Examples

Let's look at some practical code examples to illustrate the concepts discussed in the presentation.

### Synchronous vs. Asynchronous Code

First, let's compare synchronous and asynchronous approaches:

```python
# Synchronous (blocking) code
import time

def process_tasks(task_ids):
    results = []
    # Each task blocks until complete
    for task_id in task_ids:
        print(f"Processing task {task_id}...")
        time.sleep(1)  # Simulate waiting
        result = f"Result for task {task_id}"
        results.append(result)
    return results

# Takes 3 seconds total
results = process_tasks([1, 2, 3])
```

Now, the asynchronous version:

```python
# Asynchronous (non-blocking) code
import asyncio

async def process_task(task_id):
    print(f"Processing task {task_id}...")
    # Non-blocking
    await asyncio.sleep(1)
    return f"Result for task {task_id}"

async def process_tasks(task_ids):
    # Create and gather all tasks
    tasks = [process_task(task_id=id) for id in task_ids]
    # Takes only ~1 second total
    return await asyncio.gather(*tasks)

# Run the async function
results = asyncio.run(process_tasks([1, 2, 3]))
```

### Basic Async Pattern

Here's a simple example showing the basic async pattern:

```python
import asyncio
import time

async def fetch_data(delay: int, name: str) -> str:
    print(f"Starting to fetch {name}...")
    # Simulate API call with a delay
    await asyncio.sleep(delay)
    print(f"Finished fetching {name}!")
    return f"Data from {name}"

# Run the coroutine
async def main() -> None:
    result = await fetch_data(delay=1, name="API")
    print(result)

# Entry point
asyncio.run(main())
```

### Running Multiple Tasks Concurrently with gather()

The real power of async comes when running multiple tasks concurrently:

```python
import asyncio
import time

async def fetch_data(delay: int, name: str) -> str:
    print(f"Starting to fetch {name}...")
    # Simulate API call with a delay
    await asyncio.sleep(delay)
    print(f"Finished fetching {name}!")
    return f"Data from {name}"

async def main() -> None:
    start_time = time.time()
    
    # Run 3 tasks concurrently
    results = await asyncio.gather(
        fetch_data(delay=1, name="API 1"),
        fetch_data(delay=4, name="API 2"),
        fetch_data(delay=1, name="API 3"),
    )
    
    end_time = time.time()
    print(f"Total time: {int(end_time - start_time)} seconds")
    print(f"Results: {results}")

# This will print:
# Starting to fetch API 1...
# Starting to fetch API 2...
# Starting to fetch API 3...
# Finished fetching API 1!
# Finished fetching API 3!
# Finished fetching API 2!
# Total time: 4 seconds
# Results: ['Data from API 1', 'Data from API 2', 'Data from API 3']

asyncio.run(main())
```

### The Danger of Mixing Blocking Code with Async

Here's what happens when you mix blocking code with async:

```python
import asyncio
import time

async def fetch_data(delay: int, name: str) -> str:
    print(f"Starting to fetch {name}...")
    # Non-blocking wait
    await asyncio.sleep(delay)
    print(f"Finished fetching {name}!")
    return f"Data from {name}"

async def my_operation():
    print("Other operation...")
    # Blocking operation - this blocks the entire event loop!
    time.sleep(6)
    print("Operation complete!")
    return "Operation result"

async def main() -> None:
    start_time = time.time()
    
    # Run tasks concurrently
    results = await asyncio.gather(
        my_operation(),
        fetch_data(delay=1, name="API 1"),
        fetch_data(delay=4, name="API 2"),
        fetch_data(delay=1, name="API 3"),
    )
    
    end_time = time.time()
    print(f"Total time: {int(end_time - start_time)} seconds")
    print(f"Results: {results}")

# This will print:
# Other operation...
# Operation complete!  (after 6 seconds)
# Starting to fetch API 1...
# Starting to fetch API 2...
# Starting to fetch API 3...
# Finished fetching API 1!
# Finished fetching API 3!
# Finished fetching API 2!
# Total time: 10 seconds

asyncio.run(main())
```

### Using Debug Mode to Identify Issues

Debug mode can help identify issues like blocking operations:

```python
import asyncio
import time

async def blocking_coroutine():
    print("Starting potentially blocking operation")
    # This will be flagged in debug mode
    time.sleep(1)
    print("Finished blocking operation")

async def main():
    await blocking_coroutine()

# Method 1: Set event loop debug mode
asyncio.get_event_loop().set_debug(True)

# Method 2: Run with debug enabled
asyncio.run(main(), debug=True)

# Method 3: Environment variable
# PYTHONASYNCIODEBUG=1 python your_script.py
```

### Making Async Simpler with Asyncer

The Asyncer library makes working with async code much simpler:

```python
import asyncio
import time
from asyncer import asyncify, runnify

# Synchronous function to async
@asyncify
def slow_operation():
    # Blocking operation
    time.sleep(1)
    return "Operation complete"

# Make an async function easily callable from sync code
@runnify
async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"

# Using asyncify and runnify together
async def main():
    # This won't block the event loop!
    result = await slow_operation()
    print(result)

# Call directly from synchronous code
asyncio.run(main())
print(fetch_data())  # No need for asyncio.run()
```

### A Complete Real-World Example

Here's a more complete example showing how to handle multiple API requests concurrently:

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any

async def fetch_api(session: aiohttp.ClientSession, url: str, name: str) -> Dict[str, Any]:
    """Fetch data from an API endpoint."""
    print(f"Fetching data from {name}...")
    start = time.time()
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                elapsed = time.time() - start
                print(f"Finished {name} in {elapsed:.2f} seconds")
                return {"name": name, "data": data, "status": "success"}
            else:
                elapsed = time.time() - start
                print(f"Error from {name}: HTTP {response.status} in {elapsed:.2f} seconds")
                return {"name": name, "status": "error", "code": response.status}
    except Exception as e:
        elapsed = time.time() - start
        print(f"Exception from {name}: {str(e)} in {elapsed:.2f} seconds")
        return {"name": name, "status": "exception", "error": str(e)}

async def fetch_all_apis(urls: Dict[str, str]) -> List[Dict[str, Any]]:
    """Fetch data from multiple APIs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, url in urls.items():
            tasks.append(fetch_api(session, url, name))
        
        return await asyncio.gather(*tasks)

async def main():
    # Example API endpoints
    apis = {
        "users": "https://jsonplaceholder.typicode.com/users",
        "posts": "https://jsonplaceholder.typicode.com/posts",
        "comments": "https://jsonplaceholder.typicode.com/comments",
        "albums": "https://jsonplaceholder.typicode.com/albums",
        "photos": "https://jsonplaceholder.typicode.com/photos",
    }
    
    start = time.time()
    results = await fetch_all_apis(apis)
    elapsed = time.time() - start
    
    print(f"\nAll APIs fetched in {elapsed:.2f} seconds")
    
    # Process results
    for result in results:
        name = result["name"]
        status = result["status"]
        
        if status == "success":
            data_count = len(result["data"])
            print(f"{name}: Successfully fetched {data_count} items")
        else:
            print(f"{name}: Failed - {result.get('error', result.get('code', 'Unknown error'))}")

if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates:
- Concurrent API requests with proper error handling
- Using context managers with async code
- Timing operations to measure performance benefits
- Processing results after all operations complete

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
