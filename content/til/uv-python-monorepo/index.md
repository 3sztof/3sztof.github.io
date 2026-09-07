---
title: "uv makes Python monorepos actually pleasant"
date: 2026-07-03
description: "uv's workspace support turns a tangle of Poetry environments and per-Lambda pip installs into a single lockfile and a one-command install. Here's what the setup looks like in practice."
tags: ["python", "uv", "monorepo", "packaging", "tooling"]
categories: ["TIL"]
draft: false
---

## The before: a tangle of virtualenvs

Some context first: this is a serverless project on AWS, built from a handful of [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) functions plus a shared library and an admin CLI. Each Lambda is deployed as its own bundle of code and dependencies, which is exactly where the pain lived - every function needs its dependencies packaged and isolated for upload, and getting that right across many functions is fiddly.

The project started with Poetry and a `requirements.txt` per Lambda - one virtualenv per function, each managed separately, a CDK Python stack handling the build coordination. On paper this is standard; in practice it meant that adding a dependency to the shared library required updating multiple `requirements.txt` files, the per-function virtualenvs drifted from each other over time, and the CDK build logic for packaging functions was tangled with the infrastructure code in a way that made the whole thing harder to operate. There was no clean separation between "build this" and "deploy this."

## Workspaces: one lockfile, one venv

[uv](https://github.com/astral-sh/uv) workspaces changed all of that. The workspace declaration lives in one root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = [
    "src/my_core",
    "src/lambda_one",
    "src/lambda_two",
    "src/lambda_three",
    "src/lambda_four",
    "src/lambda_five",
    "src/cli",
]
```

Each member is a normal package with its own `pyproject.toml`. The shared library (`my_core`) is just another member - no special status. Lambda packages and CLI declare it as a workspace dependency:

```toml
[project]
dependencies = ["my_core"]

[tool.uv.sources]
my_core = { workspace = true }
```

`uv sync --all-extras --all-packages` installs everything into a single shared virtualenv with a single lockfile. Changes to `my_core` are reflected immediately across all packages - no reinstall, no version bump, no drift.

## Building Lambda layers with `uv export`

The part that replaced the bespoke build logic: `uv export --no-dev` from a specific package's directory produces a flat `requirements.txt` with only that package's transitive dependencies. Whatever IaC tool you're using - CDK, Pulumi, Terraform, anything else - can call this during deployment to build the Lambda layer ZIP. It works cleanly across machines - macOS ARM for local development, Linux EC2 for CI, Windows too - without any platform flags needed, since the target execution environment is specified in the IaC rather than the export step. This is a general dependency bundling concern for any distributed compute setup where each function needs its own isolated bundle.

## Running tests across the workspace

One gotcha for CI: to run `pytest` across all packages, the right invocation is `uv run --all-packages pytest`, not activating the venv and running pytest directly. Both work, but the latter bypasses uv's path management and can produce confusing import errors when packages reference each other.

The lockfile (`uv.lock`) is a single file for the whole workspace. Committing it makes `uv sync` fully reproducible - CI install from cache takes about 3 seconds.

## Beyond the monorepo: `uv tool` and `uvx`

Two uv features that aren't monorepo-specific but became load-bearing anyway.

`uv tool install` puts a Python CLI on your PATH, system-wide, in its own isolated environment - no manual venv, no `pipx`, no polluting a global site-packages. For the admin CLI in this project, `uv tool install --editable ./src/cli` from the repo root makes the command available everywhere while staying editable against the workspace source; previously this needed a wrapper script or a carefully-ordered `pip install -e`. But it's not limited to local source - you can install straight from a Git URL:

```bash
uv tool install git+https://github.com/your-org/internal-tool
```

That one line is quietly transformative for internal tooling. You can ship a hacky-but-useful CLI to your team without publishing a package, standing up a private index, or maintaining any of that machinery - point people at the repo and they're one command from having it installed and running.

Its sibling `uvx` (alias for `uv tool run`) runs a tool in an ephemeral environment without installing it at all - fetch, run, discard. It's become the de-facto way to launch MCP servers, especially [FastMCP](https://github.com/PrefectHQ/fastmcp)-based ones: `uvx some-mcp-server` in a config file just works, no install step for the user to get wrong.

## The other half: a dedicated admin CLI

Moving the build and operational logic into a dedicated admin CLI (separate from the IaC) was the other half of this improvement. The IaC describes what to provision; the CLI handles `build`, `deploy`, `migrate`, `seed`. Keeping those concerns separated made the project substantially easier to maintain and hand off.

- [uv workspaces documentation](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- [uv workspace dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [uv tools documentation](https://docs.astral.sh/uv/concepts/tools/)
- [uv guide: using tools](https://docs.astral.sh/uv/guides/tools/)
- [uv guide: AWS Lambda integration](https://docs.astral.sh/uv/guides/integration/aws-lambda/)
- [FastMCP](https://github.com/PrefectHQ/fastmcp)
