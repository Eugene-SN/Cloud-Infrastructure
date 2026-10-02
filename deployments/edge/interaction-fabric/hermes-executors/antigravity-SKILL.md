---
name: antigravity
description: "Operator-selected standalone Antigravity command on edge."
version: 1.0.0
author: Cloud Infrastructure
platforms: [linux]
---

# Explicit Antigravity

Only the operator selects Antigravity. Hermes default remains vLLM/Qwen. Never
autonomously launch AGY, route by complexity, fall back, fan out, cross-review,
substitute Codex, or use delegate_task as a specialist router.

Use the native command `/antigravity TASK`, owned by the command-only plugin.
Backend is fixed before parsing. It reuses `/usr/local/bin/edge-ai-exec` directly,
without Hermes inference, n8n, new listener or inference-provider integration.
`/skill antigravity` and natural-language skill loading only load instructions;
direct the operator to the slash command, never launch a model-controlled variant.

Default: existing core HOME/Google OAuth, explicit project cwd, timeout300s,
non-PTY `agy -p`, --output-format json, --mode plan and --sandbox, without blanket
permission bypass. AGY's native plan is guidance using read tools, not Codex's
filesystem read-only sandbox. AGY may produce a plan or soft-deny an action;
do not claim that its terminal sandbox makes the workspace immutable.

For operator-authorized implementation:

```text
/antigravity {"task":"Implement the explicitly requested change","cwd":"/absolute/project","permission_mode":"full-access","timeout":600}
```

That explicit choice uses accept-edits and --dangerously-skip-permissions. There
is no Codex-equivalent workspace-write mode. Optional fields: model, effort,
output_mode, schema, request_id, action=cancel. Native --json-schema supplies
structured_output; JSON and stream-json exist upstream, but the common helper
uses one final JSON envelope. Only native SUCCESS plus RC0 is completion;
denied_actions, errors and timeout return failure, with no alternate executor.

AGY's native timeout can return partial output: the helper's process-group
deadline wins. Native session/auth history and accepted service MCPs remain
AGY-owned. This custom installed skill survives native Hermes updates and is
versioned in Cloud Infrastructure; it does not modify the upstream checkout.
