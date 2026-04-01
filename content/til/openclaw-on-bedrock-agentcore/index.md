---
title: "You can host OpenClaw on AWS Bedrock AgentCore"
date: 2026-03-31
description: "AWS published a sample showing how to run the OpenClaw agentic coding tool on Bedrock AgentCore Runtime - per-user serverless containers with persistent workspace."
tags: ["aws", "bedrock", "agentcore", "openclaw", "ai", "devops"]
categories: ["TIL"]
draft: false
---

[OpenClaw](https://github.com/openclawdev/openclaw) is probably the most talked-about agentic coding tool right now - and also one of the more divisive ones. It has an enormous and vocal community, but opinions on it range from "game changer" to "expensive footgun", and I haven't yet used it enough to have a real take either way.

What I did find interesting: AWS published an official sample repo showing how to run OpenClaw on [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/bedrock/agentcore/) - which gives each user their own isolated Firecracker microVM with a persistent workspace backed by S3. The architecture is surprisingly thoughtful: a Router Lambda handles webhook ingestion from Telegram and Slack, resolves user identity, and spins up per-user AgentCore sessions on demand. Serverless economics, no idle compute, full conversation history across sessions.

I'm planning to experiment with both and form an actual opinion. Two official AWS hosting approaches worth knowing about:

- **Serverless (AgentCore Runtime):** [aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore](https://github.com/aws-samples/sample-host-openclaw-on-amazon-bedrock-agentcore) - per-user Firecracker microVMs, no idle compute cost, S3-backed persistent workspace. More complex to set up, but scales cleanly.
- **Non-serverless (Lightsail):** [Amazon Lightsail quick start guide for OpenClaw](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-quick-start-guide-openclaw.html) - a persistent, mutable VM. Lower friction to get started, easier to tinker with, but you pay for idle compute. Better starting point if you just want something running quickly.
