---
title: "Pulumi Python vs AWS CDK: what actually changed when I migrated"
date: 2026-08-11
description: "After years of CDK, I migrated a full serverless project to Pulumi Python. The biggest practical surprise had nothing to do with the syntax."
tags: ["pulumi", "cdk", "iac", "aws", "python", "infrastructure"]
categories: ["Posts"]
draft: false
---

I've used AWS CDK since the early days - TypeScript CDK for production workloads, Python CDK for smaller projects. When I started a new serverless project from scratch - [Collide](/posts/virtual-coffee-the-story/), the team-matching app whose build I keep writing about here - I decided to use Pulumi Python instead. Not because CDK was failing me, but because I wanted to form a real opinion based on direct comparison rather than secondhand takes. This is what I found.

## Why Python over HCL

The first thing worth saying: both Pulumi and CDK let you write real Python instead of a DSL. This matters more than it sounds. HCL (Terraform) is a purpose-built configuration language that looks like code but isn't - you can't use standard libraries, you can't write real abstractions, you can't step through it in a debugger. Python is Python. You get the entire ecosystem, proper types, normal control flow, and tools that actually understand what you wrote.

If you're choosing between Pulumi Python and Terraform HCL, Python wins on expressiveness without much debate. The CDK vs Pulumi comparison is more nuanced because both give you real programming languages - CDK in TypeScript or Python, Pulumi in whichever you prefer.

## No CloudFormation layer

The most practically significant difference between CDK and Pulumi is that Pulumi doesn't use CloudFormation. CDK synthesizes to a CloudFormation template and CloudFormation executes it. Pulumi calls AWS APIs directly.

CloudFormation is genuinely good infrastructure - it has rollback guarantees, change sets, and deep AWS console integration. But it has a ceiling. Deployments are slow because CloudFormation polls for status. Error messages during failures are often one level of abstraction too far from the actual cause. And you're constrained to what CloudFormation supports, which occasionally lags the actual AWS API surface.

Pulumi's direct API approach is faster and produces better error messages. The rollback story is weaker - Pulumi doesn't automatically roll back on failure the way CloudFormation does. You get a partial deployment and need to re-run or clean up manually. Whether that tradeoff is worth it depends on your deployment patterns.

## The output/apply model - the thing that will catch you

This is where I spent the most unexpected time when starting with Pulumi.

In CDK, when you reference a resource attribute that isn't known at synthesis time - an ARN, an auto-generated name, an ID - you get a CDK token: a placeholder string like `${Token[MyBucket.Arn.123]}`. Tokens resolve during CloudFormation deployment. You can pass them around in Python as if they were strings, and CDK handles the late binding transparently.

In Pulumi, the equivalent is an `Output[T]`. When you write `bucket = aws.s3.Bucket(...)`, `bucket.arn` is not a string - it's an `Output[str]`. If you try to use it directly in a format string or pass it to a function expecting `str`, you get the object representation, not the value:

```python
# This silently gives you something like
# "<pulumi.output.Output object at 0x10f3a2d40>"
# in your Lambda environment variable - not the ARN
env_vars = {"BUCKET_ARN": bucket.arn}

# Correct - use Output.all() to unwrap multiple outputs together
env_vars = pulumi.Output.all(bucket.arn, table.name).apply(
    lambda vals: {"BUCKET_ARN": vals[0], "TABLE_NAME": vals[1]}
)
```

Once you understand the model it's actually more explicit than CDK tokens - you always know which values are resolved and which are deferred. But it catches you repeatedly until it becomes muscle memory, because the failure mode is silent: your Lambda just gets a stringified Python object as its env var and behaves strangely at runtime.

## Config and secrets

Pulumi has a first-class config system that's noticeably better than CDK's approach:

```python
config = pulumi.Config()
project_name = config.require("project-name")
db_password = config.require_secret("db-password")  # Returns Output[str], never plaintext
```

Secrets are encrypted at rest in the state file and never appear as plaintext in code, logs, or outputs. The CDK equivalent - SSM Parameter Store lookups or SecretsManager references - works but requires more boilerplate and behaves differently at synth time vs deploy time in ways that confuse people new to CDK.

## State management

Pulumi's self-managed state backend (S3 bucket + passphrase) is just a JSON file. You can inspect it, understand it, and manipulate it when necessary. The state file tracks every resource Pulumi manages and its current configuration.

This becomes relevant when things go wrong - and occasionally you will need to manipulate state directly. Which brings me to the worst experience I had with Pulumi.

## The DynamoDB GSI problem

This deserves its own section because it cost me several hours and the solution was not obvious.

DynamoDB's `UpdateTable` API only allows one Global Secondary Index to be **created or deleted** per call. (Throughput updates to existing GSIs aren't restricted - it's structural add/remove that's one-at-a-time.) This is a DynamoDB service-level constraint, not a Pulumi limitation - CDK/CloudFormation has the same restriction. The practical implication: if you add two GSIs to your table in one `pulumi up`, Pulumi issues the changes back-to-back, DynamoDB rejects the second with `LimitExceededException`, and you have to add them one at a time, running `pulumi up` between each and waiting for the new index to reach `IndexStatus=ACTIVE`.

That much I expected. Here's what actually bit me. On the change that reworked my table's sparse indexes, a single deploy tried to move more than one GSI at once. It crashed **partway through** - one index created, another dropped, and then the deploy died. Now the table's real shape didn't match the Pulumi state, and worse: because a backfill on a new GSI takes 10-15 minutes, my AWS credentials **expired mid-run**, so Pulumi couldn't even finish reconciling. Subsequent `pulumi up` runs then cheerfully reported "no changes" against a state that was quietly wrong - and the drift broke a live endpoint (`GET /users/me/matches`) because the index it queried wasn't actually there.

The recovery was manual and slightly nerve-wracking: I stopped running `pulumi up` entirely (every run was making it worse), created the missing GSIs by hand via the AWS API, hand-edited the Pulumi state file so it reflected the table's real indexes, and only *then* ran a deploy - which finally came back clean because state and reality agreed again. Keeping credentials fresh throughout was the other half of the fix; a backfill outliving your session token is a reliable way to corrupt state.

Two things compounded the pain, both worth knowing before you hit them:

**GSIs don't have a stable identity in Pulumi's diff.** Pulumi-aws is a bridge over the Terraform AWS provider, and Terraform *sets* get represented as *lists*. A plain reorder in your program is a no-op, but once state and program disagree about ordering - which is exactly what a `pulumi refresh` after external drift or a half-failed deploy produces - the GSIs get diffed positionally instead of by `name`, and Pulumi proposes deleting and recreating the *wrong* index. This is a known, still-open issue ([pulumi/pulumi-aws#2856](https://github.com/pulumi/pulumi-aws/issues/2856)). Avoid `pulumi refresh` in the middle of a multi-GSI migration.

**There's a dedicated resource, but it's experimental.** Pulumi now offers [`aws.dynamodb.GlobalSecondaryIndex`](https://www.pulumi.com/registry/packages/aws/api-docs/dynamodb/globalsecondaryindex/) as a standalone resource for exactly this class of problem, and the `Table` docs point you to it when GSI drift bites. Two caveats: it's explicitly labelled **experimental** as of this writing, and you must **not** mix it with inline `globalSecondaryIndexes` on the same table - the docs warn that combining them causes perpetual diffs and overwritten indexes. Its schema also differs from the inline form (a `keySchemas` block rather than flat hash/range keys). I stayed on inline definitions with the one-at-a-time discipline; if I were starting over on a GSI-heavy table, the separate resource would be tempting despite the experimental label.

## The Python idiom difference

CDK's Python bindings were designed after the TypeScript version and it shows. The `from_*` static constructors, the chained method calls for grants (`bucket.grant_read(lambda_fn)`), the props pattern with `**kwargs` - these are TypeScript idioms wearing Python clothes. They work, but they don't feel native.

Pulumi's Python API is designed as Python from the start. Resource classes are normal classes. Configuration is a dict. Outputs compose with standard functional patterns (`apply`, `Output.all`). It feels like Python rather than like a Python wrapper around something else.

## Overall

Both tools are genuinely good. CDK is AWS-native, AWS-backed, and if you're building primarily on AWS it's a rock-solid choice - the concept is fascinating and the implementation is mature. The L2 construct library, the community, the tight console integration: if you're already in the AWS ecosystem it's hard to argue against it.

I chose Pulumi for this project primarily to learn it firsthand rather than form an opinion from secondhand takes. What I found: it's a better fit for this specific use case. Deployment speed is noticeably faster because updates go directly to the AWS API rather than through CloudFormation's polling cycle. The state management is more transparent and easier to reason about when things go wrong. And for a Python-native project with no need for CloudFormation's rollback guarantees or the AWS console's stack view, the CloudFormation layer adds friction without adding much value.

If I were building infrastructure for a team with mixed IaC experience at an AWS shop, I'd reach for CDK. For a solo Python project where speed and directness matter more than ecosystem depth: Pulumi.

- [Pulumi Python documentation](https://www.pulumi.com/docs/languages-sdks/python/)
- [Pulumi Output and Input types](https://www.pulumi.com/docs/concepts/inputs-outputs/)
- [aws.dynamodb.GlobalSecondaryIndex (recommended approach)](https://www.pulumi.com/registry/packages/aws/api-docs/dynamodb/globalsecondaryindex/)
- [AWS CDK Python reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
