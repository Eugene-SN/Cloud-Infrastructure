# Stage 04F — Private Hermes Machine Interface and n8n Acceptance

**Date:** 2026-09-18  
**Status:** COMPLETE / ACCEPTED  
**Marker:** `STAGE4F_PRIVATE_HERMES_MACHINE_INTERFACE=PASS`

## Research conclusion

The installed Hermes `0.21.3` source provides an upstream-native API Server with OpenAI-compatible `/v1/responses`, `/v1/chat/completions`, run/session APIs, native Bearer authentication and detailed health. This is the accepted n8n integration surface.

Rejected alternatives for this direction:

- `hermes mcp serve` is stdio-oriented and exposes messaging conversation operations rather than the required HTTP agent invocation;
- the optional Hermes n8n MCP integration operates in the opposite direction, Hermes -> n8n workflow management;
- webhooks are event-trigger/delivery oriented rather than the required synchronous agent response;
- CLI wrapping would require a custom host bridge and would inherit the known Tirith stdout contamination.

## Accepted runtime

- Hermes API Server binds only `172.19.0.1:8642` on the n8n Docker bridge.
- A narrow UFW rule permits only `172.19.0.0/16` to `172.19.0.1:8642` on `br-2bdcbc775588`.
- No nginx/public route and no public TCP/8642 listener exist.
- Unauthenticated capabilities request returns HTTP 401; authenticated request returns HTTP 200.
- n8n `2.39.7` uses its built-in HTTP Request node v4.5 and an encrypted `httpBearerAuth` credential `Hermes API - private n8n bridge`, ID `Hermes4FAuth01`.
- Published reusable workflow: `Hermes Machine Invocation`, ID `Hermes4FMachine01`.
- Supported selector values: `vllm`, `codex`, `antigravity`.

## End-to-end evidence

- `vllm`: n8n -> Hermes -> configured `qwen3.8-27b-fp8` remote vLLM -> Hermes -> n8n returned an exact random nonce with `tool_calls=[]`.
- `codex`: n8n -> Hermes/vLLM -> foreground non-PTY `codex exec` -> Hermes -> n8n returned an exact random file fact; structured response contained the real terminal tool call.
- `antigravity`: n8n -> Hermes/vLLM -> foreground non-PTY `agy -p --output-format json` -> Hermes -> n8n returned an exact random file fact; structured response contained the real Antigravity terminal tool call.

Markers:

- `STAGE4F_N8N_HERMES_VLLM_E2E=PASS`
- `STAGE4F_N8N_HERMES_CODEX_E2E=PASS`
- `STAGE4G_N8N_HERMES_ANTIGRAVITY_E2E=PASS`

The native HTTP API avoids strict JSONL parsing, so the known non-JSON Tirith warning from `hermes --format stream-json` does not contaminate n8n responses.

## Final n8n state

- exactly one production workflow: `Hermes4FMachine01`;
- exactly two production credentials: the accepted Mattermost credential and `Hermes4FAuth01`;
- all temporary acceptance workflows and random fact files removed;
- n8n healthy after final restart;
- credential data verified encrypted at rest.

Recovery snapshot root: `/srv/backups/edge-stage4f/recovery-20260918T174246Z`.
