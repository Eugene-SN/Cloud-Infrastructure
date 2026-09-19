# Stage 04 — Edge Hermes Agent Runtime Final Acceptance

**Date:** 2026-09-18  
**Status:** COMPLETE / ACCEPTED  
**Final marker:** `STAGE4_FINAL_ACCEPTANCE=PASS`

## Accepted substages

| Substage | Status | Primary evidence |
|---|---|---|
| 4A — Hermes core / Qwen3.8 / vLLM | COMPLETE / ACCEPTED | `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS` |
| 4B — Direct Codex and Antigravity executors | COMPLETE / ACCEPTED | `STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS` |
| 4C — Dashboard, ingress and self-hosted OIDC | COMPLETE / ACCEPTED | `STAGE4C_HERMES_DASHBOARD_OIDC_ACCEPTANCE=PASS` |
| 4D — Mattermost research/design | COMPLETE / ACCEPTED | `STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS` |
| 4E — Mattermost deployment/native integrations | COMPLETE / ACCEPTED | `STAGE4E_FINAL_ACCEPTANCE=PASS` |
| 4F — Private Hermes machine interface and n8n | COMPLETE / ACCEPTED | `STAGE4F_PRIVATE_HERMES_MACHINE_INTERFACE=PASS` |
| 4G — Server-side integrated acceptance | COMPLETE / ACCEPTED | `STAGE4G_SERVER_INTEGRATED_ACCEPTANCE=PASS` |
| 4H — macOS Desktop Remote Gateway | COMPLETE / ACCEPTED | `STAGE4H_MACOS_DESKTOP_REMOTE_GATEWAY=PASS` |
| 4I — Repository normalization/final persistence | COMPLETE / ACCEPTED | canonical documents reconciled and critical writes read back |

## Final runtime

- Hermes Agent `0.21.3`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, host-native under `core`.
- Main model `qwen3.8-27b-fp8` at `http://192.168.1.30:8000/v1` through the accepted private fabric.
- Direct trusted Codex CLI `0.154.0` and Antigravity CLI `1.2.6` executors.
- Public Dashboard `https://hermes.escloud.us`, native self-hosted OIDC through Authelia, loopback backend, native browser/Desktop PKCE.
- Mattermost `https://chat.escloud.us` with native Mattermost auth, Hermes gateway integration and n8n native integration.
- Private authenticated Hermes API at `172.19.0.1:8642`, reachable only from the n8n Docker bridge.
- n8n production workflow `Hermes Machine Invocation` supports `vllm`, `codex` and `antigravity` selectors.
- No unintended public Dashboard or machine-interface backend listeners.

## Accepted constraints

- Hermes controlled SIGTERM exit status 1 is an upstream lifecycle defect; requested restarts recover correctly. It is documented and not masked.
- Tirith may write a non-JSON warning to stdout in CLI `stream-json`; the accepted n8n path uses native HTTP JSON and is unaffected.
- Image Generation remains optional/non-blocking and headless CUA remains not applicable.

Stage 5 may begin only from this persisted Stage 4 checkpoint and must follow its own research/reconciliation gate.
