# Stage 04A — Core Qwen3.8 / vLLM Regression Acceptance — 2026-09-18

**Status:** COMPLETE / ACCEPTED for the core Qwen3.8/vLLM path

## Scope

This acceptance re-verifies the primary Hermes agent execution path after the earlier Qwen reasoning-normalization work and subsequent Stage 4 changes.

The block failed later during executor inventory because the verifier attempted to execute the shell builtin `command` directly through `env`. That failure occurred after all Qwen/vLLM/Hermes core gates below had already passed and does not invalidate them.

## Accepted configuration

- Hermes commit: `d177b119e9c56c9ddc0b7379ffce52341ec06584`;
- Hermes worktree: clean;
- `config.yaml` SHA256: `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- main provider: `custom`;
- base URL: `http://192.168.1.30:8000/v1`;
- model: `qwen3.8-27b-fp8`;
- `model.reasoning_echo=true`;
- persistent `agent.reasoning_effort` override: absent;
- vLLM model count: 1;
- vLLM model ID: `qwen3.8-27b-fp8`;
- vLLM max model length: `195216`.

## Fresh runtime evidence

Direct vLLM model-native reasoning:

- HTTP 200;
- non-empty reasoning: 302 characters;
- final arithmetic answer: `1536`;
- gate: `VLLM_MODEL_NATIVE_REASONING_GATE=PASS`.

Direct vLLM Qwen tool-call path:

- HTTP 200;
- exactly one function call;
- function: `stage4_probe`;
- argument: `QWEN_TOOL_OK`;
- gate: `VLLM_QWEN_TOOL_CALL_GATE=PASS`.

Hermes Qwen tool execution:

- Hermes one-shot completed successfully;
- provider: `custom`;
- model: `qwen3.8-27b-fp8`;
- terminal side effect verified through a temporary marker file;
- turn 1 reasoning tokens: `526`;
- turn 1 API calls: `2`;
- session ID: `20260918_173157_c107d0`;
- gate: `HERMES_QWEN_TOOL_EXECUTION_GATE=PASS`.

Hermes session/reasoning continuity:

- resumed exact session ID `20260918_173157_c107d0`;
- turn 2 returned the marker from the previous turn without tool use;
- turn 2 reasoning tokens: `51`;
- turn 2 API calls: `1`;
- gate: `HERMES_SESSION_CONTINUITY_GATE=PASS`.

## Acceptance markers

- `DIRECT_VLLM_REASONING=PASS`;
- `DIRECT_VLLM_QWEN_TOOL_CALL=PASS`;
- `HERMES_QWEN_TOOL_EXECUTION=PASS`;
- `HERMES_QWEN_SESSION_CONTINUITY=PASS`;
- `HERMES_REASONING_ECHO_CONFIG=PASS`;
- `HERMES_REASONING_EFFORT_OVERRIDE=ABSENT`;
- `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS`.

The core Qwen3.8/vLLM path is accepted and does not need to be re-run while moving into Stage 4B unless a concrete regression appears.

## Remaining Stage 4A/4B work

Stage 4A still carries only non-core lifecycle bookkeeping already identified elsewhere (the upstream controlled-stop SIGTERM defect remains a Stage 4G lifecycle constraint).

The next active task is Stage 4B executor integration:

- recover the interrupted read-only executor inventory from the failure point only;
- verify Codex CLI and Antigravity CLI runtime/auth readiness;
- verify installed/bundled Hermes skill state;
- then prove Hermes -> Codex CLI and Hermes -> Antigravity CLI delegation using official skill patterns.
