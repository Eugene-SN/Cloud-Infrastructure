# Stage 04 — Hermes Post-Setup Baseline — 2026-09-18

**Status:** READ-ONLY AUDIT COMPLETE / STAGE 4 IN PROGRESS / NOT YET ACCEPTED

This record captures the factual Hermes state after the upstream installer and operator-driven Full Setup wizard. It is not a final Stage 4 acceptance record and does not convert unresolved wizard choices into accepted architecture.

## Installation / provenance

- owner/runtime account: `core:core`, UID/GID `1000:1000`;
- Hermes home: `/home/core/.hermes`;
- source checkout: `/home/core/.hermes/hermes-agent`;
- launcher: `/home/core/.local/bin/hermes`;
- install method: official upstream `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` executed as `core`;
- reported version: `Hermes Agent v0.21.3 (2026.9.14) · upstream d177b119`;
- branch: `main`;
- commit: `d177b119e9c56c9ddc0b7379ffce52341ec06584`;
- origin: `https://github.com/NousResearch/hermes-agent.git`;
- worktree: CLEAN;
- managed uv: `0.12.16`;
- managed Python: `3.11.16`;
- Node.js: `v22.22.1`;
- npm: `9.2.0`.

File permissions at audit:

- `~/.hermes` = `0700 core:core`;
- `config.yaml` = `0600 core:core`;
- `.env` = `0600 core:core`;
- launchers = `0755 core:core`.

Audit hashes:

- `config.yaml`: `a8178c0603b4b1346b8bdb8c1091d32485f9788aca2154ac3846a96b2ed81163`;
- `.env`: `ac1e755781f085d3eb6d0ed94de046dc50bde2c0a24cff3c9e978a98a3f08c09`;
- `hermes-gateway.service`: `91e7ed874b6e82c7a5449d4e6891e6747677c663a0f3290486a9e9bbf62bdfff`.

No secret values are stored in this repository record.

## Main inference configuration

The Full Setup wizard configured the accepted private PAI endpoint as a named custom provider:

- display name: `AI-Node vLLM`;
- provider: `custom`;
- model: `qwen3.8-27b-fp8`;
- base URL: `http://192.168.1.30:8000/v1`;
- API mode: `chat_completions`;
- API key: none;
- configured context length: `195216`.

Fresh Stage 4 audit confirmed:

- NetBird route from `edge` to `192.168.1.30` remains active;
- `GET /v1/models` returns exactly the expected model;
- vLLM reports `max_model_len=195216`;
- provider/context configuration therefore matches current PAI runtime.

The wizard originally wrote `agent.reasoning_effort: none`, which disabled Qwen3.8 thinking. This was corrected on 2026-09-18 after a direct vLLM probe and Hermes runtime testing.

Accepted current reasoning state:

- `agent.reasoning_effort` is **unset**;
- `model.reasoning_echo: true`;
- Hermes therefore leaves reasoning effort to the model/server-native Qwen3.8 policy;
- direct vLLM probe without a Hermes override returned HTTP 200 with non-empty reasoning;
- Hermes effective runtime resolver returned `None` for the reasoning override;
- real Hermes turn 1 completed with a terminal tool call and `reasoning_tokens=45`;
- resumed turn 2 used the same session ID and completed with `reasoning_tokens=34`;
- reasoning/tool replay continuity is therefore verified across turns;
- accepted post-normalization `config.yaml` SHA256: `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`.

Acceptance marker: `STAGE4_HERMES_QWEN38_REASONING_NORMALIZATION=PASS`.

## Terminal / agent defaults

Current relevant settings include:

- terminal backend: `local`;
- terminal cwd: `.`;
- terminal timeout: `180s`;
- agent max turns: `150`;
- compression enabled, threshold `0.5`;
- built-in memory enabled;
- user-profile memory enabled;
- delegation max iterations `250`;
- telemetry shared metrics disabled;
- automatic update checks enabled.

Host-native local terminal remains aligned with the Stage 4 requirement to reuse existing host Codex/Antigravity binaries and their user context.

## Wizard-selected tools

Current selected configuration:

- Web Search/Extract backend: `exa`, tier `free`;
- Browser backend: `browser-use`;
- Computer Use backend: `cua`;
- Image Generation provider: `openai-codex`;
- Image Generation model: `gpt-image-2-medium`;
- TTS default: Edge TTS;
- Vision reported available by Hermes Doctor.

Hermes Doctor reports `web search (exa)` and `web extract (exa)` as available despite the earlier setup-summary warning about missing premium-provider keys. Treat the Doctor/runtime result as the stronger current signal.

Image Generation is **not currently usable**: the wizard selected `openai-codex`, but Hermes Doctor reports no Hermes-managed OpenAI Codex authentication. This is separate from the existing standalone Codex CLI auth at `~/.codex/auth.json`.

## Gateway service

The Full Setup wizard installed and started:

`~/.config/systemd/user/hermes-gateway.service`

Current state:

- enabled;
- active/running;
- systemd linger already enabled for `core`;
- MainPID at audit: `26371`;
- `NRestarts=0`;
- no messaging platforms enabled;
- no listeners on `8642` or `9119`;
- gateway log explicitly reports no messaging platforms enabled.

The service is retained as factual current state. Stage 4 still needs the gateway/API machinery for the planned n8n machine interface, so it must not be removed merely because messaging is currently unused.

## Skills

The audit's `SKILL_DIR_COUNT=12` counts only top-level skill categories, not individual bundled skills. The installer previously synchronized 58 bundled skills.

The audit checks for direct paths such as `~/.hermes/skills/codex` were structurally incorrect for the current hierarchical skill layout and therefore the resulting `ABSENT` lines are **not authoritative**.

Upstream at the installed commit contains the bundled Codex skill at:

`skills/autonomous-ai-agents/codex/SKILL.md`

Antigravity is not bundled at that upstream path and remains a later Stage 4 integration item.

Existing executors confirmed:

- Codex CLI: `/home/core/.local/bin/codex`, version `0.154.0`, standalone auth file present;
- Antigravity CLI: `/home/core/.local/bin/agy`, version `1.2.5`;
- cua-driver: `0.28.2`.

## Host/browser/toolchain normalization

The Full Setup installer initially could not install several host packages because `core` intentionally has no sudo access. Stage 4 subsequently completed those host-level dependencies from the root administrative context while keeping Hermes itself owned/run by `core`.

Accepted current host/toolchain state:

- `ripgrep 15.1.0` installed and available as `/usr/bin/rg`;
- `ffmpeg 8.0.1` installed and available as `/usr/bin/ffmpeg`;
- `build-essential` installed;
- `python3-dev` installed;
- `libffi-dev` installed;
- Playwright/Chromium host shared-library dependency set installed;
- packaged Chromium at `/home/core/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome` has no unresolved shared libraries;
- Browser backend resolves to `browser-use`;
- Hermes-managed Browser Use CLI resolves to `/home/core/.hermes/bin/browser-use`;
- real Hermes `browser_exec` successfully launched the managed Chromium path, loaded `https://example.com/`, returned the expected page title/URL and cleaned up the runtime;
- `cua-driver 0.28.2` is available to the actual `core` runtime through `/home/core/.local/bin/cua-driver`;
- source checkout remains branch `main`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, clean worktree;
- accepted reasoning config remained unchanged at SHA256 `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- `hermes-gateway.service` remained active/enabled.

Execution-context invariant discovered during recovery:

- host-native Hermes/Codex/Antigravity probes under `core` must set `HOME=/home/core`, include `/home/core/.local/bin` and `/home/core/.hermes/bin` in PATH, and use a `core`-accessible cwd such as `/home/core`;
- root-owned cwd such as `/root` can produce false npm/agent-browser permission failures and must not be used to judge runtime health.

Acceptance marker: `STAGE4_HERMES_SYSTEM_TOOLCHAIN_NORMALIZATION=PASS`.

## Hermes Doctor

Static `hermes doctor` returned RC=0.

Confirmed healthy:

- Python 3.11.16 / SQLite 3.53.1;
- Hermes state databases / WAL;
- config version 45;
- custom inference endpoint configured;
- command installation;
- gateway supervision/linger;
- main tool registration;
- built-in memory.

Non-blocking Doctor findings:

- upstream Node workspace dependency advisories are present;
- no GITHUB_TOKEN for higher Skills Hub rate limits;
- no Hermes-managed Nous/OpenAI-Codex/MiniMax/xAI auth;
- image generation unavailable under the currently selected provider;
- several optional/unconfigured integrations unavailable.

Do **not** run `npm audit fix` or `hermes doctor --fix` by assumption. Any mutation must be Stage-4-scoped and separately verified.

## Still pending before Stage 4 acceptance

1. complete real functional capability verification for the remaining Full Setup tool surfaces (Computer Use/CUA, Vision, TTS, Web Search/Extract, Image Generation) and normalize only proven gaps;
2. verify the nested bundled Codex skill on the live host and install/verify the official Antigravity skill if required;
3. prove direct Hermes -> Codex CLI and Hermes -> Antigravity CLI delegation;
4. configure the Hermes API machine interface and prove `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
5. deploy the persistent Hermes Dashboard backend and publish `https://hermes.escloud.us` through nginx + Authelia;
6. test the final macOS Hermes Desktop Remote Gateway path, session credential behavior, live chat/WebSocket and reconnect persistence;
7. perform final Stage 4 non-regression/reboot acceptance.

No Stage 4 final acceptance is claimed by this audit.
