# Cloud Infrastructure — Current State

## Canonical checkpoint

**Stage 0 — COMPLETE / ACCEPTED**  
**Stage 1 — COMPLETE / ACCEPTED**  
**Stage 2 — Edge Core Applications — COMPLETE / ACCEPTED**  
**Stage 02.5 — Remaining Functional Scope Reconciliation & Research — COMPLETE / ACCEPTED**  
**Stage 3 — Edge Cross-site Connectivity Foundation — COMPLETE / ACCEPTED**  
**Stage 4 — Edge Hermes Agent Runtime — COMPLETE / ACCEPTED**  
**Stage 05.1 — Cross-project Knowledge Reconciliation & Target Architecture — COMPLETE / ACCEPTED**  
**Stage 05.2 — PVE Canonical Obsidian Runtime & WebUI — COMPLETE / ACCEPTED**  
**Stage 05.3 — Edge Knowledge Replication & Data Integration — COMPLETE / ACCEPTED**  
**Stage 5 — Knowledge Fabric Runtime Deployment — COMPLETE / ACCEPTED**
**Stage 6 — Edge Backrest & Recovery — COMPLETE / ACCEPTED**  
**Stage 7 — Edge Maintenance & Update — IN PROGRESS**  
**Stage 7A — Home Maintenance Framework Port — COMPLETE / ACCEPTED**  
**Stage 7B — Edge Update Drivers & Recovery — IN PROGRESS**

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.  
`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS` on 2026-09-18.  
`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-18.  
`STAGE05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE=PASS` on 2026-09-19.  
`STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS` on 2026-09-19.  
`STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS` on 2026-09-20.  
`STAGE05_FINAL_ACCEPTANCE=PASS` on 2026-09-20.  
`STAGE4_FINAL_ACCEPTANCE=PASS` on 2026-09-18.
`STAGE07A_READONLY_DASHBOARD_SEMAPHORE_E2E=PASS` on 2026-09-21.
`STAGE07_UPDATE_ROOT_REDIRECT_FIX=PASS` on 2026-09-21.

`STAGE4F_STABLE_DOCKER_BRIDGE_HARDENING=PASS` on 2026-09-19.

Primary repository: `Eugene-SN/Cloud-Infrastructure`.

Completed recovery workstream, now merged into `main`:

`04.3 — Edge Hermes Stage 4 Recovery, Completion & Final Acceptance`

Git checkpoint: merge commit `c4d402175ea1a049f20a93ab77daa0b068071277` on `main`.

Stage 4 — Edge Hermes Agent Runtime is **COMPLETE / ACCEPTED**. Final record: `STAGE_04_FINAL_ACCEPTANCE_2026-09-18.md`.

Stage 02.5 final acceptance record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

## Stage 02.5 accepted research state

### Hermes

**Hermes Agent — SELECTED.**

Accepted direction:

- persistent cloud-side agent runtime on `edge`;
- runs in parallel with n8n rather than replacing it;
- preferred host-native placement under `core`;
- Hermes invokes Codex/Antigravity directly rather than through CloudCLI;
- user-specific n8n/Hermes workflows remain post-infrastructure work.

### Cross-site Connectivity Foundation

**Existing self-hosted NetBird — SELECTED / REUSE EXISTING.**

Detailed acceptance record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Current accepted/runtime state:

- `edge` is an ordinary host-native NetBird service peer on NetBird `0.78.2`;
- `edge` NetBird IPv4 is `100.105.178.187/16`;
- Home CT300 remains the Home routing/control-plane foundation;
- `edge -> Home/PAI` through the existing `Home LAN 192.168.1.0/24` resource is verified;
- `edge` does not receive the Home Internet `0.0.0.0/0` resource;
- `edge` keeps direct VPS-provider Internet/default routing and public IPv4 `45.92.156.17`;
- Home `.lan` split DNS is consumed by `edge`; `pve.lan -> 192.168.1.3` is verified;
- LAN-wide clientless Home/PAI -> `edge` routing is **not part of the baseline**: VM100 and MikroTik remain unchanged because current Home/PAI consumers can use the existing public VPS IP or `escloud.us` / service-subdomain ingress;
- `edge.lan` is intentionally not created because it adds no useful access path for the current architecture;
- clientless gateway routing to the NetBird overlay is deferred and requires a concrete private-only workload before any VM100/MikroTik change;
- direct WireGuard/Tailscale remain rejected as duplicate private backbones; AmneziaWG remains contingency only for a demonstrated NetBird transport failure.

Stage 3 is COMPLETE / ACCEPTED. Final record: `STAGE_03_ACCEPTANCE_2026-09-18.md`. Control-plane grouping/policy, host-native `edge` enrollment, private Home routing, split DNS, direct P2P recovery, CT300 recovery and full `edge` reboot persistence are verified. VM100/MikroTik routing/firewall state was not mutated.

### Data / knowledge project boundary

Stage 5 is **COMPLETE / ACCEPTED**.

Authoritative records:

- `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_2_FINAL_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

Current accepted runtime:

- PVE Knowledge filesystem is the dedicated `pve/knowledge` 32 GiB ext4 LV mounted at `/srv/knowledge`; the Obsidian vault is `/srv/knowledge/obsidian`;
- PVE remains the authoritative Knowledge/recovery node and Syncthing hub;
- CT210 `obsidian` remains the single full server-side Obsidian runtime/WebUI at private `https://obsidian.lan`;
- ai-node remains an active RW replica at `/srv/ai-data/knowledge/obsidian`;
- edge is an active RW replica at `/srv/knowledge/obsidian`;
- accepted live topology is PVE ↔ ai-node plus PVE ↔ edge; no direct edge ↔ ai-node Syncthing peer exists;
- edge Syncthing `2.1.5` runs as `syncthing@core.service`, enabled at boot;
- edge dials PVE at `tcp://192.168.1.3:22000`;
- edge Syncthing GUI/API and listener are loopback-only at `127.0.0.1:8384` and `127.0.0.1:22000`; global/local discovery, relays and NAT traversal are disabled;
- edge `/srv/knowledge` is `core:core 0755`; `/srv/knowledge/obsidian` is `core:core 2775`;
- Hermes, Codex and Antigravity run under `core` and use the local host path directly;
- edge n8n binds `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`; container user `node` is UID/GID `1000:1000`;
- existing `n8n_hermes` network remains unchanged;
- PVE → edge, edge → PVE, and edge → PVE → ai-node propagation passed;
- controlled edge outage/reconnect and PVE/edge conflict preservation passed;
- whether the conflict copy itself reached ai-node before cleanup was not directly captured and remains **UNKNOWN**; normal edge → PVE → ai-node propagation was independently verified;
- controlled edge reboot acceptance passed with Knowledge converged, n8n healthy and Stage 4 user services active;
- OpenClaw/CT220 relationship remains unchanged;
- no edge Obsidian runtime/WebUI was added;
- external client-access implementation remains outside Stage 5.

Acceptance markers:

- `STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS`;
- `STAGE05_FINAL_ACCEPTANCE=PASS`.

## Final remaining roadmap

Stages 5 and 6 are complete and accepted. The current finite infrastructure stage is Stage 7.

1. **Stage 7 — Edge Maintenance & Update**, including separate Codex `update.escloud.us` substage;
2. **Stage 8 — Edge Monitoring, Heartbeats & Alerts**;
3. **Stage 9 — Edge Cloud Portal**, including separate Codex `app.escloud.us` substage;
4. **Stage 10 — Edge Final Integrated Infrastructure Acceptance**;
5. post-infrastructure **Automation & User Workflows** as a continuous workstream.

Backrest-before-Semaphore remains mandatory as a Stage sequencing and deployment/testing safety prerequisite: verified backup/restore must exist before maintenance tooling is deployed and exercised. It does not imply an automatic Backrest run before every production update. Per-update backups are component-specific only where justified by the actual update/recovery path. Monitoring remains late-stage so it is built once against the substantially complete inventory. `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

Stage 7 accepted target direction: Edge Maintenance is derived from the accepted Home Maintenance implementation on CT1000. Preserve the proven Semaphore + Ansible/native-script architecture, version/status cache model, fixed-target dispatch, per-component update-driver pattern, post-update refresh/acceptance flow and dashboard where applicable. Replace Home/PVE-specific inventory, VMID/PCT/QGA logic, collectors and drivers with edge-specific equivalents. `update.escloud.us` begins as an adapted copy of the existing Home Maintenance dashboard source rather than a greenfield frontend.

Stage 7B manual-execution requirement: every real update is operator-initiated manually from `update.escloud.us` only. Do not create or enable update timers, cron jobs, systemd update services, background update daemons, unattended update jobs, scheduled update execution, or any equivalent path that can start a real update without an explicit user action in the page. This also applies to Stage 7B acceptance testing: a newly implemented driver is exposed in `update.escloud.us`, the user inspects it and manually starts the test update there. Semaphore remains the backend executor only.

Stage 7A is COMPLETE / ACCEPTED. Current accepted edge maintenance foundation:
- Semaphore Community `2.19.12-012ed06-1788086239`, host-native, `semaphore.service` active/enabled as `semaphore:semaphore`;
- Semaphore listener `127.0.0.1:3000` only;
- project ID `1`: `Edge Maintenance`;
- repository ID `1`: canonical `https://github.com/Eugene-SN/Cloud-Infrastructure.git`, branch `main`;
- inventory ID `1`: `Edge Localhost`;
- environment ID `1`: `Edge Read-only`;
- refresh template ID `1`: `01. Refresh — Edge Maintenance Status`, playbook `maintenance/edge/playbooks/semaphore-refresh.yml`;
- adapted Home dashboard/status baseline on loopback `127.0.0.1:18070`;
- public `https://update.escloud.us/` ingress through the existing Xray -> nginx -> Authelia path; the backend port remains loopback-only and is not published by UFW;
- the backend root redirect is relative (`Location: /status/`), so the internal port is never exposed in the browser URL;
- 23 component version rows and 24 maintenance rows including aggregate `APT_EDGE`;
- Hysteria2 `app/vX.Y.Z` release-tag normalization corrected; current Hysteria2 status is `CURRENT`;
- `CHECK_FAILED=0`;
- dashboard action contract remains read-only: refresh enabled, update template count `0`, Master Batch disabled, automatic updates disabled;
- dashboard → Semaphore → canonical GitHub playbook → local collector/cache → dashboard E2E passed;
- no real production component update was executed during Stage 7A;
- bounded production non-regression passed after E2E.

Authoritative Stage 7A record: `STAGE_07A_READONLY_FRAMEWORK_DEPLOYMENT_2026-09-21.md`.

Stage 7 public-ingress redirect correction record: `STAGE_07_UPDATE_INGRESS_REDIRECT_FIX_2026-09-21.md`.

## Host / foundation

- logical node/FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- KVM x86_64, 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- public IPv4 `45.92.156.17/24`; no public/global IPv6 on `ens3`; IPv6 remains enabled for link-local/NetBird overlay use;
- timezone `Europe/Moscow`;
- root SSH key-only through `ssh.socket`;
- Docker Engine `29.8.1`, Compose `5.5.1`, containerd `2.3.5`; Docker `live-restore=false`; production containers use `restart=unless-stopped`;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27` on public TCP/443 with nginx fallback;
- Hysteria2 `2.12.3` on public UDP/443;
- UFW active: default deny incoming, allow outgoing, deny routed;
- intentional public TCP listeners: 22, 80, 443, 25, 465, 993; UDP 443;
- application WebUI backends remain loopback-only unless explicitly accepted otherwise.

Shared trusted service/operator account `core`: UID/GID `1000:1000`, password locked, full non-interactive root via `sudo` (`NOPASSWD: ALL`); no `docker` group membership is required. `core` linger remains enabled for persistent user services.

## Core privilege model

Accepted corrective record: `CORE_FULL_ROOT_SUDO_ACCEPTANCE_2026-09-18.md`.

- `core` remains UID/GID `1000:1000` with a locked password;
- `/etc/sudoers.d/90-core-root` grants `core ALL=(ALL:ALL) NOPASSWD: ALL`;
- non-interactive root execution through `sudo -n` is verified;
- no separate `docker` group membership is required;
- critical high-impact mutations remain subject to the existing operator-approval policy at the orchestration/instruction layer.

## Reboot lifecycle correction

The Stage 1 `live-restore: true` setting was superseded on 2026-09-18 after Stage 3 reboot testing proved it caused an approximately 90-second late-shutdown delay on the current `edge` runtime.

Accepted current state:

- `/etc/docker/daemon.json`: `"live-restore": false`;
- post-fix reboot total boot time: `13.842s`;
- previous-journal-stop to new-kernel gap: `4.203s` (previously ~94s);
- Docker/containerd active after reboot;
- Authelia, Bulwark, n8n and Stalwart all auto-started via `restart=unless-stopped`;
- zero failed systemd units.

Acceptance record: `EDGE_REBOOT_LIFECYCLE_FIX_ACCEPTANCE_2026-09-18.md`.

## Authentication / ingress

### Authelia

- version `4.39.27`;
- backend `127.0.0.1:19091 -> 9091`;
- fresh operator/auth state;
- public `auth.escloud.us` accepted.

Protected private web namespace includes `n8n`, `code`, future `app`, `backup`, `ops`, `update`, `docs`, `cloud` and `sync`. `mail.escloud.us` intentionally uses native mail-stack authentication. Stage 4D also accepts `chat.escloud.us` as an explicit native-client exception: Mattermost uses Mattermost-native authentication without Authelia.

## TLS

Shared Certbot lineage: `/etc/letsencrypt/live/escloud.us`.

Current SAN set includes `escloud.us`, `app.escloud.us`, `auth.escloud.us`, `backup.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, `code.escloud.us`, `docs.escloud.us`, `hermes.escloud.us`, `mail.escloud.us`, `n8n.escloud.us`, `ops.escloud.us`, `sync.escloud.us` and `update.escloud.us`. `update.escloud.us` has active HTTPS ingress through Authelia; its application backend remains loopback-only at `127.0.0.1:18070`.

## Stage 2 applications

### n8n

- version `2.39.7`;
- backend `127.0.0.1:15678` only;
- public `https://n8n.escloud.us/` through Authelia;
- fresh application state at Stage 2 acceptance.

### CloudCLI

- version `1.37.3` under `/home/core/.local`;
- backend `127.0.0.1:18140` only;
- public `https://code.escloud.us/` through Authelia;
- fresh local application/auth state at acceptance.

### Codex CLI

- version `0.154.0` official standalone runtime;
- fresh ChatGPT authorization;
- Remote Control through Unix control socket only;
- no public Codex network listener.

### Antigravity CLI

- current runtime version `1.2.7`; Stage 4G accepted `1.2.6`, and Stage 2/4B accepted `1.2.5` historically;
- fresh Google OAuth;
- Remote Control instance `edge`;
- persistent user service accepted.

## Mail — production accepted

- Stalwart `0.16.22`;
- Bulwark `1.9.2`;
- loopback web backends: Stalwart `127.0.0.1:18083`, Bulwark `127.0.0.1:18084`;
- public mail protocols: TCP/25 SMTP, TCP/465 SMTPS submission, TCP/993 IMAPS;
- `es@escloud.us` useful mailbox/account/address-book/calendar/identity state migrated with fresh credentials;
- fresh Stalwart/Bulwark auth/session/DKIM material;
- MX/PTR/SPF/DKIM/DMARC accepted;
- Gmail outbound and inbound bidirectional E2E verification passed.

## Stage 2 final integrated acceptance

Final recovery run proved foundation services, Stage 2 applications, mail, public ingress/listeners, loopback backend contract, UFW, readiness/health, TLS/DNS/DKIM identity and accepted config non-regression.

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

## Stage 4 — Hermes Agent Runtime (complete / accepted)

Fresh expanded read-only audit on 2026-09-18 confirms the following current runtime.

### Hermes core

- official upstream git install under `/home/core/.hermes/hermes-agent`;
- Hermes `0.21.3 (2026.9.14)`, branch `main`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, clean worktree;
- main provider `AI-Node vLLM` -> `http://192.168.1.30:8000/v1`;
- model `qwen3.8-27b-fp8`, Chat Completions mode, verified context `195216`;
- Qwen3.8 model-native reasoning/replay accepted; current `config.yaml` SHA256 is `fe2f0fead4781ed28d0c4bf61720bdc52a6b31a41040a477afe6351b5df2f824` after preserving Dashboard theme `rose` and restoring the accepted model semantics;
- terminal backend `local`;
- system toolchain/browser normalization accepted, including managed Chromium and `cua-driver 0.28.2`;
- `hermes-gateway.service` is enabled and currently active under `core`; current `NRestarts=0`;
- Mattermost environment is configured and its token validates successfully as bot `hermes`;
- standalone Codex CLI `0.154.0` and current Antigravity CLI `1.2.7` remain available to `core`;
- Web Search/Extract, Edge TTS and Vision functional probes are PASS; CUA is accepted as `NOT_APPLICABLE_HEADLESS_EDGE`; Image Generation remains configured but is non-blocking for Stage 4 acceptance; fresh core Qwen3.8/vLLM regression is accepted with `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS`.
- Stage 4B executor read-only audit is accepted: `STAGE4B_EXECUTOR_READONLY_AUDIT=PASS`.
- Actual Hermes local terminal child context is clean for standalone executors: cwd `/home/core`, `HOME=/home/core`, `HERMES_HOME=/home/core/.hermes`, core local bin on PATH, and no `OPENAI_BASE_URL`, `OPENAI_API_KEY` or `CODEX_*` environment override.
- Codex CLI `0.154.0` exposes native headless `codex exec` capabilities including JSON/ephemeral/sandbox/skip-git/output-last-message/model controls and uses the existing standalone OAuth state with no custom provider/MCP override.
- At Stage 4B acceptance, Antigravity CLI `1.2.5` raw help confirmed native headless print mode plus JSON/stream-JSON, timeout, model, effort, sandbox/permission and conversation controls; `1.2.6` later passed bounded Stage 4G E2E, and current `1.2.7` preserves the accepted CLI contract in the 2026-09-19 post-acceptance reconciliation.
- Accepted Stage 4B target: foreground non-PTY one-shots by default (`codex exec`; `agy -p/--print` with structured output), background only for long/parallel jobs, PTY only for interactive TUI.
- Trusted-executor policy is accepted: no blanket sandbox/container/workspace-only/network restriction under `core`; critical high-impact mutations require operator approval at the Hermes/orchestration instruction layer before delegation, while ordinary non-critical work should remain frictionless.
- Stage 4B direct executor integration is COMPLETE / ACCEPTED: `STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS`; final record `STAGE_04B_FINAL_ACCEPTANCE_2026-09-18.md`.
- Codex CLI `0.154.0`: real foreground non-PTY `codex exec` delegation accepted; random repository context was read by Codex and consumed by Hermes; post-test recovery/non-regression PASS.
- Stage 4B accepted Antigravity CLI `1.2.5` with real foreground non-PTY `agy -p --output-format json`; `1.2.6` re-passed the same integration boundary through n8n/Hermes in Stage 4G. Current `1.2.7` is a post-acceptance runtime update; its version/CLI contract were reconciled on 2026-09-19 without reopening historical Stage 4 E2E.
- Hermes `stream-json` Tirith warning contamination remains a known CLI constraint; the accepted Stage 4F interface uses native HTTP JSON and is unaffected.
- Dashboard/OIDC, private n8n machine interface, bounded integrated acceptance and macOS Remote Gateway are COMPLETE / ACCEPTED.

Known accepted upstream lifecycle constraint: a controlled systemd stop/restart sends SIGTERM and Hermes logs graceful shutdown, but the process exits status `1`; systemd briefly records `Failed with result 'exit-code'` before the requested restart succeeds. Recovery is healthy and persistent; no source patch or `SuccessExitStatus=1` masking is used.

### Mattermost

Stage 4D design, core runtime, ingress, native server configuration and Hermes↔Mattermost integration are accepted.

Current runtime:

- Mattermost Team `11.11.0`;
- PostgreSQL `18-alpine`;
- official `mattermost/docker` deployment at commit `497414659ee7127677d2b91b44bb4f3ea9d14695`;
- Mattermost healthy and PostgreSQL running;
- host publication only `127.0.0.1:18065 -> 8065`; PostgreSQL has no host binding;
- public `https://chat.escloud.us` through Xray -> host nginx -> shared TLS;
- WebSocket `/api/v4/websocket` returns `101 Switching Protocols`;
- Mattermost-native authentication; no Authelia;
- effective SiteURL supplied by `MM_SERVICESETTINGS_SITEURL=https://chat.escloud.us`;
- bot account creation enabled; public user creation disabled;
- TPNS configured at `https://push-test.mattermost.com`;
- Calls plugin disabled;
- Mattermost↔Stalwart SMTP is explicitly not required / not enabled;
- prepackaged `mattermost-ai` / Agents `2.6.1` remains installed but is explicitly **disabled**; runtime disabled-list verification and `config.json` `Enable=false` both passed. Acceptance record: `STAGE_04E_MATTERMOST_AGENTS_NORMALIZATION_ACCEPTANCE_2026-09-18.md`.

Hermes↔Mattermost accepted state:

- bot `hermes` / display name `Hermes Agent`, ID `sceogxkhh3nh9y89uc6eza9ije`;
- operator allowlist `mof5mc6w3jds8qp36b678qrzoc`;
- private service/home channel `hermes`, ID `6s6o3iftjprwfg5p4d1gg1bwho`;
- operator DM exists;
- real E2E response `HERMES_MATTERMOST_E2E_OK` passed;
- markers: `STAGE4E_HERMES_MATTERMOST_BOT_PROVISION=PASS`, `STAGE4E_HERMES_MATTERMOST_CHANNEL_NORMALIZATION=PASS`, `STAGE4E_HERMES_MATTERMOST_E2E=PASS`.

### n8n ↔ Mattermost

Status: **COMPLETE / ACCEPTED**.

Accepted state:

- n8n `2.39.7` healthy at `127.0.0.1:15678`;
- official built-in `n8n-nodes-base.mattermost` node, typeVersion `1`;
- one production `mattermostApi` credential: `Mattermost API - chat.escloud.us`, ID `16a0a988ad514ab1`;
- credential validates against `/api/v4/users/me` with HTTP 200 as bot `n8n`, ID `4ty8tfwmdir9mxkeua3n7658mc`;
- exactly one active Mattermost access token exists for `n8n`, description `n8n-native-mattermost`;
- operator DM channel ID `srzsm58fepgujjfnyxb8f7zo3o`;
- native-node E2E acceptance marker `N8N_MATTERMOST_NATIVE_E2E_OK_20260918T135107Z`;
- Mattermost database verified exactly one matching post authored by the `n8n` bot, post ID `1fgnm3fumbyy8b4usrrs41kouc`;
- the E2E workflow executed only against a throwaway SQLite/config clone under `/tmp`;
- the Stage 4E probe left production n8n at workflows `0`, executions `0`, one Mattermost credential at that checkpoint; current Stage 4F production state is one Hermes machine workflow and two credentials;
- n8n and Mattermost health remained PASS after the probe;
- throwaway host/container artifacts were removed;
- acceptance record: `STAGE_04E_N8N_MATTERMOST_INTEGRATION_ACCEPTANCE_2026-09-18.md`;
- marker: `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`.

Stage 4E is **COMPLETE / ACCEPTED**. Final bounded non-regression passed with `STAGE4E_FINAL_NON_REGRESSION=PASS`; final acceptance record: `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`. The official iOS Mattermost/mobile TPNS gate is operator-accepted PASS, and the `mattermost-ai` disposition is complete and accepted.

Detailed accepted records remain authoritative for completed substages; the expanded audit does not retroactively rewrite historical records.

Stage 4 is **COMPLETE / ACCEPTED** with `STAGE4_FINAL_ACCEPTANCE=PASS`.

## Recovery / preserved state

- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- the sensitive migration-preservation archive was historically created at `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz` with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, but the temporary path is absent and the operator declared the archive no longer required on 2026-09-19. The hash is historical evidence only. Do not recreate the archive; `migration-reference/` is the retained sanitized engineering reference.

## Stage 4C/4F/4G/4H accepted runtime — 2026-09-18

### Dashboard and Desktop

- `https://hermes.escloud.us` is live through Xray/nginx/shared TLS to loopback `127.0.0.1:9119`.
- `hermes-dashboard.service` is active/enabled with `NRestarts=0`; no public TCP/9119 exists.
- Hermes native self-hosted OIDC is the only provider; Authelia `4.39.27` is the IdP; nginx does not use `auth_request` for Hermes.
- Browser OIDC callback, authenticated session/message traffic and WebSocket HTTP 101 were observed; the operator confirmed Dashboard operation.
- macOS Hermes Desktop completed native authorize/callback/token exchange and remote WebSocket connection twice; operator confirmed successful operation and reconnect.
- The existing Certbot webroot lineage includes `hermes.escloud.us`; no second lineage or nginx Certbot plugin exists.
- Acceptance records: `STAGE_04C_FINAL_ACCEPTANCE_2026-09-18.md` and `STAGE_04H_MACOS_DESKTOP_REMOTE_GATEWAY_ACCEPTANCE_2026-09-18.md`.

### Private n8n machine interface

- Hermes' upstream API Server binds only `172.19.0.1:8642` on the n8n Docker bridge with Bearer authentication and a narrow UFW rule; it has no public nginx route or public listener.
- n8n `2.39.7` production workflow `Hermes Machine Invocation` (`Hermes4FMachine01`) uses the built-in HTTP Request node and encrypted credential `Hermes4FAuth01`.
- Docker Compose now explicitly defines network `n8n_hermes`, Linux bridge `n8n-hermes`, subnet `172.19.0.0/16` and gateway `172.19.0.1`; the stable bridge name survives network-ID recreation.
- UFW permits `172.19.0.0/16 -> 172.19.0.1:8642/tcp` only on `n8n-hermes`; the obsolete `br-2bdcbc775588` rule is removed.
- Selector values `vllm`, `codex` and `antigravity` are supported.
- Exact random-value E2E passed for direct Hermes/vLLM response, real foreground Codex CLI and real foreground Antigravity CLI.
- Final production n8n state: one published Hermes workflow, Mattermost plus Hermes credentials, no acceptance/test workflow, healthy container.
- Acceptance records: `STAGE_04F_PRIVATE_HERMES_MACHINE_INTERFACE_ACCEPTANCE_2026-09-18.md` and `STAGE_04F_NETWORK_IDENTITY_HARDENING_ACCEPTANCE_2026-09-19.md`.

### Integrated acceptance

- Native Hermes detailed health reports gateway/model/config/state DB healthy and both Mattermost and API Server connected.
- The audit detected and corrected an operator/UI model switch away from vLLM. Accepted `qwen3.8-27b-fp8`/custom/chat-completions semantics were restored with native Hermes commands and re-proven through n8n E2E.
- Codex `0.154.0` and Antigravity `1.2.6` current runtime paths passed.
- Mattermost/n8n native integration, public Dashboard/OIDC, private listeners, TLS and Stage 3 vLLM reachability remained healthy.
- Acceptance record: `STAGE_04G_SERVER_INTEGRATED_ACCEPTANCE_2026-09-18.md`.

Root recovery snapshots remain under `/srv/backups/edge-stage4c`, `/srv/backups/edge-stage4f` and `/srv/backups/edge-stage4f-network`.

### Post-acceptance runtime reconciliation — 2026-09-19

- Fresh read-only boundary reconciliation passed with `STAGE4_FINAL_BOUNDARY_RECONCILIATION=PASS`.
- Current Antigravity CLI is `1.2.7`; historical Stage 4G acceptance on `1.2.6` remains valid and unchanged.
- Hermes Gateway/Dashboard services are active/enabled; Dashboard self-hosted OIDC, PKCE/S256, loopback `127.0.0.1:9119`, private API `172.19.0.1:8642`, stable Docker bridge `n8n-hermes`, n8n workflow/credential inventory, UFW boundary and Mattermost/foundation non-regression all passed.
- Two attempted Antigravity smoke verifiers were classified as assistant test-harness defects (temporary-directory traversal and job-control/timeout behavior), not production regressions. No production mutation or service restart occurred.
- Stage 4 remains COMPLETE / ACCEPTED with `STAGE4_FINAL_ACCEPTANCE=PASS`; Stage 5 entry is eligible after this repository reconciliation.

## Stage 6 — Edge Backrest & Recovery — COMPLETE / ACCEPTED

Current accepted/deployed state:

- Backrest `1.14.1` and Restic `0.19.1` are active on edge;
- dedicated edge Knowledge repo/plan is deployed and accepted:
  - source `/srv/knowledge`;
  - schedule `04/10/16/22`;
  - rolling local `14d`;
  - grouping `host,tags`;
  - no D5 copy;
  - `EDGE_KNOWLEDGE_14D_FINAL_ACCEPTANCE=PASS`;
- expanded edge and ai-node backup audits passed;
- Stage 6.6 deployment contract is accepted in `STAGE_06_6_DEPLOYMENT_CONTRACT_2026-09-21.md`;
- **Stage 6.7 production general-plan deployment is COMPLETE / ACCEPTED** with `STAGE06_7_FINAL_ACCEPTANCE=PASS`;
- **Stage 6.8 isolated restore/application recovery is COMPLETE / ACCEPTED** with `STAGE06_8_FINAL_ACCEPTANCE=PASS`; real D5 restores and application usability were verified on edge and ai-node without production overwrite;
- edge `edge-state`: schedule `01/07/13/19`, local rolling `7d`, grouping `host,tags`, application-consistent staging, successful append-only D5 copy, D5 daily30/weekly8/monthly6/yearly0;
- accepted edge local/D5 snapshots for first production verification: `6e8747d3...` -> `0ff42011...`;
- ai-node bounded corrections are deployed and accepted: tier grouping `host,tags`, self-contained n8n SQLite staging, Docker/containerd full-backup exclusions, local full keep-last-2 after successful D5 copy, and corrected restore mount directories;
- controlled ai-node-ai-state local/D5 verification passed: `6be74a98...` -> `ea798442...`;
- dedicated Knowledge policies remain unchanged;
- no recurring edge full/bare-metal Restic chain is planned;
- a separate CloudCLI runtime drift remains known: `cloudcli.service` is restart-looping because `/srv/ai-workspace` is absent. It is not classified as a Backrest deployment failure and must be reconciled before final Stage 6 non-regression acceptance.

Acceptance record: `STAGE_06_7_FINAL_ACCEPTANCE_2026-09-21.md`.
Final Stage 6 acceptance record: `STAGE_06_FINAL_ACCEPTANCE_2026-09-21.md`.

## Current next step

Stage 6 is COMPLETE / ACCEPTED. Next finite infrastructure stage: **Stage 7 — Edge Maintenance & Update**.
