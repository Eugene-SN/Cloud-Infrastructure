# Stage 04 — Hermes System Toolchain Normalization Acceptance — 2026-09-18

**Status:** ACCEPTED SUBSTAGE / STAGE 4 REMAINS IN PROGRESS

## Scope

Normalize and verify the host-level dependencies and browser/tool execution surface selected during Hermes Full Setup, without changing the accepted model/provider/reasoning configuration.

## Accepted runtime

- `ripgrep 15.1.0` installed;
- `ffmpeg 8.0.1` installed;
- `build-essential`, `python3-dev`, `libffi-dev` installed;
- Playwright/Chromium system shared-library set installed;
- managed Chromium binary resolved under the `core` Playwright cache with no missing shared libraries;
- Hermes browser backend = `browser-use`;
- managed Browser Use CLI = `/home/core/.hermes/bin/browser-use`;
- real `browser_exec` loaded `https://example.com/` successfully through managed Chromium and returned the expected title/URL;
- browser runtime cleanup passed;
- `cua-driver 0.28.2` resolves for the actual `core` runtime at `/home/core/.local/bin/cua-driver`;
- Hermes source worktree is clean at `main@d177b119e9c56c9ddc0b7379ffce52341ec06584`;
- accepted Hermes config remained unchanged at SHA256 `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- `hermes-gateway.service` remained active/enabled.

## Recovery findings

Two verifier-only failures occurred during normalization:

1. a Node probe attempted `require("playwright")`, but Hermes' selected browser path uses the managed Browser Use CLI and `agent-browser`/CDP; installing a repo-local Node `playwright` package was not required;
2. a browser probe was launched as `core` while inheriting `cwd=/root`, causing npm/agent-browser `EACCES`. The production runtime was healthy once executed with the correct `core` HOME/PATH/cwd;
3. an initial final verifier checked `cua-driver` through root's PATH and falsely reported it absent. The authoritative `core` runtime resolves it correctly.

No rollback or reinstallation of the successful package/browser work was required.

## Runtime execution-context invariant

For host-native Hermes/Codex/Antigravity operations under `core`:

- `HOME=/home/core`;
- PATH must include `/home/core/.local/bin` and `/home/core/.hermes/bin`;
- use a `core`-accessible cwd, normally `/home/core`;
- Git state for the Hermes checkout must be checked as `core`, not by marking the repo safe for root.

## Acceptance

`HERMES_RIPGREP_RUNTIME=PASS`  
`HERMES_FFMPEG_RUNTIME=PASS`  
`HERMES_BUILD_TOOLCHAIN=PASS`  
`HERMES_PLAYWRIGHT_SYSTEM_DEPS=PASS`  
`HERMES_BROWSER_USE_CLI=PASS`  
`HERMES_MANAGED_CHROMIUM_BROWSER_EXEC=PASS`  
`HERMES_CUA_DRIVER_ENTRYPOINT=PASS`  
`HERMES_SOURCE_WORKTREE=PASS`

`STAGE4_HERMES_SYSTEM_TOOLCHAIN_NORMALIZATION=PASS`

This is a Stage 4 substage acceptance only. Stage 4 final acceptance remains pending.
