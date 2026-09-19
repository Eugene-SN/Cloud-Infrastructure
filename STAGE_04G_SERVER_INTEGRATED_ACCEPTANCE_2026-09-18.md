# Stage 04G — Server-side Integrated Acceptance

**Date:** 2026-09-18  
**Status:** COMPLETE / ACCEPTED  
**Marker:** `STAGE4G_SERVER_INTEGRATED_ACCEPTANCE=PASS`

## Bounded acceptance

This check reused accepted Stage 4A/B/D/E evidence and exercised only current integration boundaries and concrete regression signals.

- `hermes-gateway.service` and `hermes-dashboard.service` active/enabled, `NRestarts=0`.
- Native `/health/detailed`: Hermes `0.21.3`, gateway `running`, model/config/state DB healthy, `mattermost=connected`, `api_server=connected`.
- vLLM `/v1/models` exposes `qwen3.8-27b-fp8` over the accepted Stage 3 private path.
- Dashboard HTTPS, self-hosted OIDC, PKCE/S256 discovery, shared certificate SAN and loopback-only backend passed.
- Mattermost `/api/v4/system/ping` passed and the accepted n8n Mattermost credential remains present.
- Private Hermes API authentication/listener/UFW topology passed.
- n8n -> Hermes -> vLLM/Codex/Antigravity -> Hermes -> n8n E2E passed.
- Codex CLI remains `0.154.0`.
- Current Antigravity CLI is `1.2.6`; the version drift from the Stage 4B accepted `1.2.5` triggered and passed a fresh bounded E2E.
- No unintended public TCP/9119 or TCP/8642 listener exists.

## Model regression and recovery

The bounded audit detected that Dashboard interaction had changed the global Hermes model from the accepted custom vLLM route to `openai-codex`. Hermes automatic backups proved the change sequence.

The accepted Stage 4A settings were restored with native `hermes config set` commands and validated with `hermes config check`:

- `model.default=qwen3.8-27b-fp8`;
- `model.provider=custom`;
- `model.base_url=http://192.168.1.30:8000/v1`;
- `model.api_mode=chat_completions`;
- `model.reasoning_echo=true`;
- no persistent `agent.reasoning_effort`.

User-selected Dashboard theme `rose` was preserved. Current Hermes config SHA256 is `fe2f0fead4781ed28d0c4bf61720bdc52a6b31a41040a477afe6351b5df2f824`.

## Known accepted upstream constraint

Controlled systemd SIGTERM still produces Hermes graceful-shutdown logging followed by process exit status 1; systemd briefly records a failed stop before the requested restart succeeds. The service recovered active/enabled with `NRestarts=0`. No source patch and no `SuccessExitStatus=1` masking were introduced.
