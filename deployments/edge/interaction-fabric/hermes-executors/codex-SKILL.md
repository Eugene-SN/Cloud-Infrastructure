---
name: codex
description: "Operator-selected standalone Codex command on edge."
version: 2.0.0
author: Cloud Infrastructure
platforms: [linux]
---

# Explicit Codex

Only the operator selects Codex. Ordinary Hermes tasks stay on default vLLM/Qwen.
Never autonomously launch Codex, choose it by complexity, fall back, fan out,
cross-review, substitute AGY, or use delegate_task as a specialist router.

The installed command-only native plugin owns `/codex TASK` and takes precedence
over this same-name skill. Its handler launches the shared one-shot
`/usr/local/bin/edge-ai-exec` directly, with backend fixed to codex before parsing.
No Hermes inference is involved in native command dispatch. Loading this skill
through `/skill codex` or natural language is guidance, not deterministic dispatch;
tell the operator to use the command. Do not execute a second model-controlled path.

Default: existing core HOME/auth, cwd `/home/core/projects/cloud-infrastructure`,
timeout300s, Codex read-only sandbox, approval_policy never, foreground non-PTY.
For authorized edits the operator sends JSON, e.g.:

```text
/codex {"task":"Implement the explicitly requested change","cwd":"/absolute/project","permission_mode":"workspace-write","timeout":600}
```

`full-access` explicitly maps to danger-full-access; never choose it automatically
after a sandbox failure. Supported optional fields: model, effort, output_mode,
schema, request_id, action=cancel. Cancellation requires the original request_id.
The fixed helper uses native `codex exec`, stdin, --json, --ephemeral, -C,
--output-schema when supplied, and --output-last-message for the final result.
It reports native exit/error/timeout; no fallback or reviewer runs afterward.

Standalone ChatGPT login and accepted service MCP/web/repository tools remain
Codex-owned. This is not a Hermes model-provider integration. Non-Git cwd is
supported by --skip-git-repo-check; PTY and scratch git init are not requirements.

This installed user-modified skill is versioned in Cloud Infrastructure. Hermes
native bundled sync preserves user edits; upstream source remains unmodified.
