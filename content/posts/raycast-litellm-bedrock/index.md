---
title: "Raycast AI with AWS Bedrock via LiteLLM Proxy"
date: 2026-02-23
description: "How to wire up Raycast AI to AWS Bedrock models using a local LiteLLM proxy as an OpenAI-compatible bridge, with auto-start setup for macOS, Linux, and Windows"
tags: ["raycast", "litellm", "aws-bedrock", "claude", "ai", "productivity", "macos", "linux", "windows"]
categories: ["Tools", "AI", "Productivity"]
---

Raycast AI is genuinely useful for quick questions, text transformations, and inline completions. The problem: it only supports a handful of built-in providers, and AWS Bedrock isn't one of them. You either pay for Raycast Pro and use their hosted models, or you bring your own OpenAI-compatible endpoint.

LiteLLM solves this cleanly. It runs a local proxy that speaks OpenAI's API format and translates requests to whatever backend you configure - including Bedrock. Raycast talks to `localhost:4000` thinking it's OpenAI, and LiteLLM handles the rest.

## Why This Approach?

A few reasons this setup makes sense if you're already in the AWS ecosystem:

1. **No Raycast Pro required**: Raycast supports custom OpenAI-compatible providers. LiteLLM is that provider.
2. **Bedrock billing**: If you're already paying for AWS, using Bedrock keeps costs consolidated and avoids another subscription.
3. **Model flexibility**: You can expose any Bedrock model - Claude 3.7, Sonnet 4, Sonnet 4.5, Sonnet 4.6 - and switch between them in Raycast's model picker.
4. **Always-on proxy**: Running LiteLLM as a launchd daemon means it starts at login and stays out of your way.

## The Architecture

| Component | Role |
|-----------|------|
| **Raycast** | Sends OpenAI-format requests to `localhost:4000` |
| **LiteLLM proxy** | Translates OpenAI API calls to Bedrock API calls |
| **AWS Bedrock** | Runs the actual Claude models |
| **launchd** | Keeps LiteLLM running at login |

## Prerequisites

- Raycast installed (free tier is fine)
- AWS CLI configured with credentials that have Bedrock access
- Python 3.10+ (for LiteLLM)
- Bedrock model access enabled in your AWS account for the Claude models you want

Check your AWS credentials work:

```bash
aws sts get-caller-identity
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelId, `claude`)].modelId'
```

## Step 1: Install LiteLLM

```bash
pip install litellm[proxy]

# Verify
litellm --version
```

## Step 2: Configure LiteLLM

Create `~/.config/litellm-config.yaml`:

```yaml
model_list:
  - model_name: anthropic.claude-3-7-sonnet-20250219-v1:0
    litellm_params:
      model: bedrock/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0
      max_tokens: 131072

  - model_name: anthropic.claude-4-0-20240620-v1:0
    litellm_params:
      model: bedrock/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0
      max_tokens: 200000

  - model_name: anthropic.claude-4-5-20240620-v1:0
    litellm_params:
      model: bedrock/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0
      max_tokens: 64000

  - model_name: anthropic.claude-sonnet-4-6
    litellm_params:
      model: bedrock/global.anthropic.claude-sonnet-4-6
      max_tokens: 1048576

litellm_settings:
  drop_params: true
```

A few things worth noting here:

- The `model_name` values are what Raycast will display in its model picker. I kept them close to the actual model IDs to avoid confusion.
- Claude Sonnet 4.6 uses a different naming convention - no date suffix, no version suffix. It's a global cross-region inference profile with a 1M token context window (currently in beta).
- `drop_params: true` tells LiteLLM to silently ignore any parameters that Bedrock doesn't support. Without this, some Raycast requests fail with parameter validation errors.

### Model Summary

| Model name in Raycast | Underlying Bedrock model | Context |
|-----------------------|--------------------------|---------|
| `anthropic.claude-3-7-sonnet-20250219-v1:0` | Claude 3.7 Sonnet (cross-region) | 131K |
| `anthropic.claude-4-0-20240620-v1:0` | Claude Sonnet 4 (cross-region) | 200K |
| `anthropic.claude-4-5-20240620-v1:0` | Claude Sonnet 4.5 (cross-region) | 64K |
| `anthropic.claude-sonnet-4-6` | Claude Sonnet 4.6 (global inference) | 1M |

## Step 3: Test the Proxy Manually

Before wiring up Raycast, verify LiteLLM works:

```bash
litellm --config ~/.config/litellm-config.yaml --port 4000
```

In another terminal:

```bash
curl http://localhost:4000/v1/models | python3 -m json.tool
```

You should see all four models listed. Then test an actual completion:

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic.claude-sonnet-4-6",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}]
  }'
```

If that works, kill the manual process and move on to the launchd setup.

## Step 4: Run LiteLLM as a LaunchAgent

Running LiteLLM manually every time is annoying. A launchd daemon starts it at login and restarts it if it crashes.

Create `~/Library/LaunchAgents/com.litellm.proxy.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.litellm.proxy</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/litellm</string>
    <string>--config</string>
    <string>/Users/YOUR_USERNAME/.config/litellm-config.yaml</string>
    <string>--port</string>
    <string>4000</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>AWS_PROFILE</key>
    <string>default</string>
    <key>TAVILY_API_KEY</key>
    <string>YOUR_TAVILY_API_KEY_HERE</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>/tmp/litellm.log</string>

  <key>StandardErrorPath</key>
  <string>/tmp/litellm.err</string>
</dict>
</plist>
```

Adjust the `litellm` path to match your installation (`which litellm`), and replace `YOUR_TAVILY_API_KEY_HERE` with your actual key if you use Tavily for web search tools.

Load and start it:

```bash
launchctl load ~/Library/LaunchAgents/com.litellm.proxy.plist
launchctl start com.litellm.proxy
```

Check it's running:

```bash
launchctl list | grep litellm
tail -f ~/Library/Logs/litellm.log
```

To reload after config changes:

```bash
launchctl unload ~/Library/LaunchAgents/com.litellm.proxy.plist
launchctl load ~/Library/LaunchAgents/com.litellm.proxy.plist
```

## Step 5: Configure Raycast

Raycast stores its AI provider config at `~/.config/raycast/ai/providers.yaml`. You can edit this directly.

```yaml
providers:
  - id: litellm
    name: LiteLLM
    base_url: http://localhost:4000
    models:
      - id: anthropic.claude-3-7-sonnet-20250219-v1:0
        name: "Claude 3.7"
        context: 200000
        abilities:
          temperature:
            supported: true
          vision:
            supported: true
          system_message:
            supported: true
      - id: anthropic.claude-4-0-20240620-v1:0
        name: "Claude 4.0"
        context: 200000
        abilities:
          temperature:
            supported: true
          vision:
            supported: true
          system_message:
            supported: true
      - id: anthropic.claude-4-5-20240620-v1:0
        name: "Claude 4.5"
        context: 200000
        abilities:
          temperature:
            supported: true
          vision:
            supported: true
          system_message:
            supported: true
      - id: anthropic.claude-sonnet-4-6
        name: "Claude Sonnet 4.6"
        context: 1048576
        abilities:
          temperature:
            supported: true
          vision:
            supported: true
          system_message:
            supported: true
```

The `id` under each model must exactly match the `model_name` in `litellm-config.yaml` - that's how Raycast tells LiteLLM which model to route to.

After saving, restart Raycast (Cmd+Q, then reopen). Your models should appear in the AI model picker.

## The Bug That Cost Me an Hour

When I first set up Sonnet 4.5, I used this in `litellm-config.yaml`:

```yaml
model: bedrock/converse_like/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

The `converse_like/` prefix is a LiteLLM routing hint for models that use Bedrock's Converse API format. Sounds reasonable. But Raycast kept throwing:

```
Error: api_base is required for custom OpenAI-compatible providers
```

The error was misleading - `api_base` was set correctly. The actual problem was that `converse_like/` routing broke LiteLLM's ability to construct the endpoint URL, which Raycast interpreted as a missing base URL.

The fix: remove `converse_like/` entirely. Standard `bedrock/arn:...` routing works fine for these cross-region inference profiles.

```yaml
# Before (broken)
model: bedrock/converse_like/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0

# After (works)
model: bedrock/arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

## Claude Sonnet 4.6 Specifics

Sonnet 4.6 is worth calling out separately because it behaves differently from the other models in this config:

- **No date/version suffix** in the model ID - just `global.anthropic.claude-sonnet-4-6`
- **Global inference profile** - routes across regions automatically, no ARN needed
- **1M token context window** - currently in beta, but it works
- **Different naming convention** - signals a shift in how Bedrock names newer models

The 1M context is genuinely useful for Raycast's AI Chat when you're pasting in large files or long conversation histories. I set `context: 1048576` in the Raycast config so it knows the full window is available.

## Troubleshooting

### LiteLLM not starting

Check the error log:

```bash
tail -f ~/Library/Logs/litellm-error.log
```

Common causes: wrong path to the `litellm` binary in the plist, missing AWS credentials in the environment, or a port conflict on 4000.

### "Model not found" in Raycast

The `id` field in `providers.yaml` must exactly match the `model_name` in `litellm-config.yaml`. They're case-sensitive.

### AWS credential errors

The launchd environment doesn't inherit your shell's AWS config automatically. Make sure `AWS_PROFILE` is set in the plist's `EnvironmentVariables`, or use `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` directly if you're not using profiles.

### Slow first response

LiteLLM initializes its connection to Bedrock on the first request. Subsequent requests in the same session are faster. This is normal.

## Quick Tip: Auto-start LiteLLM on Boot

You don't want to manually start the proxy every time you log in. Here's how to set it up as a background service on each platform.

### macOS (launchd)

Create `~/Library/LaunchAgents/com.litellm.proxy.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.litellm.proxy</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/litellm</string>
    <string>--config</string>
    <string>/Users/YOUR_USERNAME/.config/litellm-config.yaml</string>
    <string>--port</string>
    <string>4000</string>
  </array>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>AWS_PROFILE</key>
    <string>default</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>/tmp/litellm.log</string>

  <key>StandardErrorPath</key>
  <string>/tmp/litellm.err</string>
</dict>
</plist>
```

Adjust the `litellm` path to match your installation (`which litellm`), and set `YOUR_USERNAME` to your macOS username.

Load and start it:

```bash
launchctl load ~/Library/LaunchAgents/com.litellm.proxy.plist
launchctl start com.litellm.proxy
```

Check it's running:

```bash
launchctl list | grep litellm
tail -f /tmp/litellm.log
```

To reload after config changes:

```bash
launchctl unload ~/Library/LaunchAgents/com.litellm.proxy.plist
launchctl load ~/Library/LaunchAgents/com.litellm.proxy.plist
```
### Linux (systemd)

Create `~/.config/systemd/user/litellm.service`:

```ini
[Unit]
Description=LiteLLM Proxy
After=network.target

[Service]
ExecStart=/usr/local/bin/litellm --config %h/.config/litellm-config.yaml --port 4000
Restart=on-failure
RestartSec=5
Environment=AWS_PROFILE=default

[Install]
WantedBy=default.target
```

Enable and start it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now litellm

# Check status
systemctl --user status litellm
journalctl --user -u litellm -f
```

Replace `/usr/local/bin/litellm` with the output of `which litellm` if it's installed elsewhere (e.g. `~/.local/bin/litellm` for pip user installs).

### Windows (Task Scheduler)

Open PowerShell as your regular user (not admin) and run:

```powershell
$action = New-ScheduledTaskAction `
  -Execute "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts\litellm.exe" `
  -Argument "--config $env:USERPROFILE\.config\litellm-config.yaml --port 4000"

$trigger = New-ScheduledTaskTrigger -AtLogon -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
  -ExecutionTimeLimit 0 `
  -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
  -TaskName "LiteLLM Proxy" `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -RunLevel Limited
```

Adjust the `-Execute` path to match your Python installation. To find it:

```powershell
Get-Command litellm | Select-Object -ExpandProperty Source
```

To manage the task later: open the `Task Scheduler` app and search for "LiteLLM Proxy" in the task library. AWS credentials on Windows are picked up from `%USERPROFILE%\.aws\credentials` automatically, so no extra environment setup needed if you've already run `aws configure`.


## Resources

- [LiteLLM Proxy Documentation](https://docs.litellm.ai/docs/proxy/quick_start) - Official proxy setup guide
- [LiteLLM Bedrock Provider](https://docs.litellm.ai/docs/providers/bedrock) - Bedrock-specific configuration
- [Raycast AI Extensions](https://developers.raycast.com/api-reference/ai) - Custom provider API reference
- [AWS Bedrock Claude Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) - Model availability and IDs

---

*If you're already running LiteLLM for other tools (Opencode, Claude Code, etc.), adding Raycast to the mix is essentially free - just add the provider config and you're done. The launchd setup is the one-time investment that makes everything else seamless.*
