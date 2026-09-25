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
**Stage 7 — Edge Maintenance & Update — COMPLETE / ACCEPTED**  
**Stage 7A — Home Maintenance Framework Port — COMPLETE / ACCEPTED**  
**Stage 7B — Edge Update Drivers & Recovery — COMPLETE / ACCEPTED**  
**Stage 7C — update.escloud.us Dashboard Adaptation — COMPLETE / ACCEPTED**  
**Stage 8 — Edge Monitoring, Heartbeats & Alerts — COMPLETE / ACCEPTED**  
**Stage 9 — Edge Cloud Portal — COMPLETE / ACCEPTED**  
**Stage 10 — Edge Final Integrated Infrastructure Acceptance — COMPLETE / ACCEPTED**  
**Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion — COMPLETE / ACCEPTED**  
**Stage 12 — Nextcloud Cloud Drive & Private Workspace Access — COMPLETE / ACCEPTED**  
**Stage 13 — Backrest WebUI Ingress — COMPLETE / ACCEPTED**  
**Stage 14 — Edge Cloud Portal Modernization & Sovereign Control Deck — COMPLETE / ACCEPTED**

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
`STAGE07_SEMAPHORE_SAME_ORIGIN_UI=PASS` on 2026-09-21.
`STAGE07_OPS_HOSTNAME_RETIREMENT=PASS` on 2026-09-21.
`STAGE07B_MANUAL_ONLY_CLEANUP=PASS` on 2026-09-21.  
`STAGE07_FINAL_ACCEPTANCE=PASS` on 2026-09-21.  
`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS` on 2026-09-23.
`STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS` on 2026-09-23.
`STAGE08_FINAL_ACCEPTANCE=PASS` on 2026-09-22.  
`STAGE09_FINAL_ACCEPTANCE=PASS` on 2026-09-22.  
`STAGE10_FINAL_ACCEPTANCE=PASS` on 2026-09-22.  
`STAGE11_FINAL_ACCEPTANCE=PASS` on 2026-09-22.  
`STAGE12_FINAL_ACCEPTANCE=PASS` on 2026-09-23.  
`STAGE13_FINAL_ACCEPTANCE=PASS` on 2026-09-23.

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

- `edge` is an ordinary host-native NetBird service peer on NetBird `0.79.0`;
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

Stages 5, 6 and 7 are complete and accepted. The current finite infrastructure stage is Stage 8.

1. **Stage 8 — Edge Monitoring, Heartbeats & Alerts**;
2. **Stage 9 — Edge Cloud Portal**, including separate Codex `app.escloud.us` substage;
3. **Stage 10 — Edge Final Integrated Infrastructure Acceptance**;
4. post-infrastructure **Automation & User Workflows** as a continuous workstream.

Backrest-before-Semaphore remains mandatory as a Stage sequencing and deployment/testing safety prerequisite: verified backup/restore must exist before maintenance tooling is deployed and exercised. It does not imply an automatic Backrest run before every production update. Per-update backups are component-specific only where justified by the actual update/recovery path. Monitoring remains late-stage so it is built once against the substantially complete inventory. `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

Stage 7 accepted target direction: Edge Maintenance is derived from the accepted Home Maintenance implementation on CT1000. Preserve the proven Semaphore + Ansible/native-script architecture, version/status cache model, fixed-target dispatch, per-component update-driver pattern, post-update refresh/acceptance flow and dashboard where applicable. Replace Home/PVE-specific inventory, VMID/PCT/QGA logic, collectors and drivers with edge-specific equivalents. `update.escloud.us` begins as an adapted copy of the existing Home Maintenance dashboard source rather than a greenfield frontend.

Stage 07.2 update-ownership correction: Maintenance/Semaphore remains manual for components without an accepted upstream-native automatic owner, but it must not compete with supported native update lifecycles. Current native-owned paths are Codex managed-daemon auto-update, Hermes native cron update plus conditional settlement timer, Antigravity native background self-update, and Ubuntu security updates through package-owned `apt-daily*` / `unattended-upgrades`. Normal/third-party APT, Docker workloads and other non-native-auto components remain operator-triggered through `update.escloud.us`. Semaphore itself has no schedules and never autonomously launches manual targets.

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
- the same public origin exposes the full Semaphore UI at `https://update.escloud.us/project/1/history`; the dashboard's Semaphore button opens that route, and Semaphore's public `web_host` is `https://update.escloud.us/`;
- Semaphore API and WebSocket traffic remain on `/api/` and `/api/ws`; verified WebSocket upgrade returns HTTP 101 for live task output;
- 23 component version rows and 24 maintenance rows including aggregate `APT_EDGE`;
- Hysteria2 `app/vX.Y.Z` release-tag normalization corrected; current Hysteria2 status is `CURRENT`;
- `CHECK_FAILED=0`;
- dashboard action contract remains read-only: refresh enabled, update template count `0`, Master Batch disabled, automatic updates disabled;
- dashboard → Semaphore → canonical GitHub playbook → local collector/cache → dashboard E2E passed;
- no real production component update was executed during Stage 7A;
- bounded production non-regression passed after E2E.

Authoritative Stage 7A record: `STAGE_07A_READONLY_FRAMEWORK_DEPLOYMENT_2026-09-21.md`.

Stage 7 public-ingress redirect correction record: `STAGE_07_UPDATE_INGRESS_REDIRECT_FIX_2026-09-21.md`.

Stage 7 same-origin Semaphore UI record: `STAGE_07_SEMAPHORE_SAME_ORIGIN_UI_2026-09-21.md`.

Stage 7 retired-hostname cleanup record: `STAGE_07_OPS_HOSTNAME_RETIREMENT_2026-09-21.md`.

Stage 7B historical deployment remains accepted; Stage 07.2 supersedes only its blanket manual-only ownership policy and fixed 16-target current model.

Stage 07.2 status: **COMPLETE / ACCEPTED** with `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS` on 2026-09-23. The execution-path failure in Task 23 was diagnosed (runtime schema check drift in manual-update), corrected by synchronizing the deployed `/opt/edge-maintenance/scripts/` with canonical `origin/main`, and re-verified through real operator-triggered Semaphore Master Batch Task 26 (RC=0). Post-scan gate originally passed with 18/18 targets `CURRENT` and `REBOOT_REQUIRED=0`; after the accepted CloudCLI retirement on 2026-09-23, the current model is 17 actionable manual targets / 24 monitored components. Current health passes with 9 system services, 4 user services, 9 compose units (10 containers), 2 SQLite databases and PostgreSQL readiness.

Current Stage 07.2 maintenance state:
- ownership policy: native-first; Maintenance execution plane: strictly manual;
- generated target model: `update_units_v5`;
- raw Maintenance collector: 24 rows; Hermes/Codex/CloudCLI are not collected;
- Maintenance: exactly 17 actionable manual targets: `APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`, `SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`, `STALWART`, `BULWARK`, `NEXTCLOUD`, `NEXTCLOUD_POSTGRESQL`, `NEXTCLOUD_REDIS`, `ANTIGRAVITY`;
- all 17 Maintenance rows have `update_owner=maintenance_manual`;
- Hermes, Codex and Ubuntu security updates are native-owned outside Maintenance: Hermes native cron + settlement, Codex managed-daemon `pid-update-loop`, Ubuntu package-owned unattended-upgrades;
- `actions.json` schema 10 contains exactly 17 manual components, `execution_mode=manual_only`, `auto_update=false`;
- Master Batch and `--plan-only` require schema-2 enablement;
- Stage 8 `edge-monitor` uses `/var/www/maintenance-status/maintenance.json` as the authoritative maintenance source;
- Semaphore has no Hermes/Codex update templates; Refresh remains ID 1 and Master ID 18;
- Rclone manual update uses upstream `rclone selfupdate --stable` and restarts `projects-webdav.service`;
- Nextcloud application/PostgreSQL/Redis remain separate manual targets;
- Bulwark tracks `ghcr.io/bulwarkmail/webmail:latest`; actual image replacement remains operator-triggered;
- final corrective acceptance: `STAGE07_2_CORRECTIVE_MIGRATION=PASS`, RC=0;
- real execution acceptance: `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS` (Semaphore task 26, RC=0);
- Stage 07.2 historical audit remains accepted; current post-retirement runtime is 17 actionable targets / 24 monitored components with CloudCLI removed;
- current post-retirement maintenance acceptance: 17 actionable targets, 24 monitored components, no CloudCLI target/template/runtime references;
- authoritative record: `STAGE_07_2_FINAL_CURRENT_STATE_ACCEPTANCE_2026-09-23.md`.


Implementation/deployment checkpoint: `STAGE_07B_DRIVER_SCAFFOLD_DEPLOYMENT_2026-09-21.md`.

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

## 2026-09-23 reboot/SSH lifecycle correction

A later controlled reboot exposed a separate ~90-second late-shutdown stall unrelated to Docker: `multipathd.service` reported shutdown but remained in `stop-sigterm` until its 90-second stop timeout elapsed.

Fresh storage/runtime audit proved that edge has no multipath maps and no device-mapper devices; root is ordinary ext4 on `/dev/vda1`. `multipathd.service` was therefore disabled from `sysinit.target` while the Ubuntu `multipath-tools` package remains installed. The static/inactive `multipathd.socket` and helper queueing unit remain non-owning/inactive.

Final combined reboot acceptance on 2026-09-23:
- reboot request: `05:29:27 MSK`;
- reboot target reached: `05:29:39.188 MSK` (~12.2 s after request);
- previous journal stopped: `05:29:39.260 MSK`;
- new kernel: `05:29:45.786 MSK` (~6.5 s later);
- `network-online.target`: `05:29:52.817 MSK`;
- SSH port 22 listening: `05:29:53.717 MSK`, ~7.9 s after new-kernel start and ~26.7 s after reboot request;
- full system startup: `18.348s`;
- `multipathd.service`: disabled/inactive and absent from current-boot execution;
- zero failed systemd units;
- Codex and Antigravity reboot persistence both passed.

Acceptance record: `EDGE_REMOTE_CLI_AND_REBOOT_LIFECYCLE_ACCEPTANCE_2026-09-23.md`.

## Authentication / ingress

### Authelia

- version `4.39.28`;
- backend `127.0.0.1:19091 -> 9091`;
- fresh operator/auth state;
- public `auth.escloud.us` accepted.

Protected private web namespace includes `n8n`, `code`, `app`, `backup`, `update`, `docs` and `cloud`. `backup.escloud.us` is active through the accepted Authelia gate; `docs.escloud.us` remains reserved/deferred and `sync.escloud.us` is retired. `mail.escloud.us` intentionally uses native mail-stack authentication. Stage 4D also accepts `chat.escloud.us` as an explicit native-client exception: Mattermost uses Mattermost-native authentication without Authelia.

## TLS

Shared Certbot lineage: `/etc/letsencrypt/live/escloud.us`.

Current SAN set includes `escloud.us`, `app.escloud.us`, `auth.escloud.us`, `backup.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, `code.escloud.us`, `docs.escloud.us`, `go.escloud.us`, `hermes.escloud.us`, `mail.escloud.us`, `n8n.escloud.us` and `update.escloud.us`. `update.escloud.us` has active HTTPS ingress through Authelia for both the maintenance dashboard and Semaphore UI. The former `ops.escloud.us` candidate is fully retired from edge runtime/configuration/certificate state and its public Cloudflare DNS A record is also deleted. `STAGE10_OPS_DNS_RETIREMENT_VERIFY=PASS`.

## Stage 2 applications

### n8n

- version `2.39.10`;
- backend `127.0.0.1:15678` only;
- public `https://n8n.escloud.us/` through Authelia;
- fresh application state at Stage 2 acceptance.

### CloudCLI — RETIRED

- CloudCLI `1.37.3` was fully retired from edge on 2026-09-23 after the operator rejected it for the current remote-workspace requirement;
- `cloudcli.service`, listener `127.0.0.1:18140`, npm package, `/home/core/.cloudcli`, `/srv/ai-workspace`, Maintenance target/template and Cloud Portal card are absent;
- `code.escloud.us` DNS/TLS/Authelia slot is intentionally preserved and currently returns an authenticated `503` placeholder for the planned T3 WebUI;
- acceptance marker: `CLOUDCLI_RETIREMENT_FINAL_ACCEPTANCE=PASS`.

### Codex CLI

- current version `0.156.0` official standalone runtime;
- fresh ChatGPT authorization;
- Remote Control through Unix control socket only; no public Codex network listener;
- native managed lifecycle is the sole Codex runtime owner: one managed app-server plus one native `pid-update-loop`;
- native auto-update is enabled and preserved;
- legacy custom `codex-cli-daemon.service` is removed;
- because the native PID backend does not persist across host reboot, a minimal enabled user oneshot `codex-remote-control-start.service` under `core` invokes only the supported `codex remote-control start --json` command at user-manager boot; it does not supervise the managed daemon;
- controlled reboot acceptance on 2026-09-23 verified exactly one managed app-server, one native updater and the control socket without manual Codex start.

### Antigravity CLI

- current runtime version `1.2.7`; Stage 4G accepted `1.2.6`, and Stage 2/4B accepted `1.2.5` historically;
- fresh Google OAuth;
- Remote Control instance `edge`;
- persistent user service accepted.

## Mail — production accepted

- Stalwart `0.16.23`;
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
- standalone Codex CLI `0.156.0` and current Antigravity CLI `1.2.7` remain available to `core`;
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
- historical Stage 6 CloudCLI workspace drift was resolved at that checkpoint; CloudCLI was subsequently fully retired on 2026-09-23 and `/srv/ai-workspace` plus `cloudcli.service` are now absent.

Acceptance record: `STAGE_06_7_FINAL_ACCEPTANCE_2026-09-21.md`.
Final Stage 6 acceptance record: `STAGE_06_FINAL_ACCEPTANCE_2026-09-21.md`.

## Current next step

Stage 7 — Edge Maintenance & Update — is **COMPLETE / ACCEPTED** with
`STAGE07_FINAL_ACCEPTANCE=PASS`.

Final Stage 7 acceptance reused the accepted Stage 7A and Stage 7B evidence and
closed Stage 7C with a fresh integrated read-only audit. The accepted runtime
contract is:

- historical Stage 7 acceptance used `update_units_v3`; current post-Stage-07.2 model is `update_units_v5` with 17 actionable update units / 24 monitored components / 8 non-actionable APT children after CloudCLI retirement;
- Refresh template ID `1` and manual Master Batch template `18` remain; CloudCLI template ID `15` is retired and absent;
- every real update remains manually initiated from `update.escloud.us`; Semaphore has zero schedules, no project update timer/cron launcher exists, and all Ubuntu periodic/unattended APT paths are masked/inactive with effective periodic values `0`;
- the dashboard uses one generated runtime action artifact and the four accepted groups: System Packages, Native Applications, Docker Applications, and CLI & Agent Applications;
- normalized `core` execution context remains relevant for Hermes, Codex and Antigravity; the former CloudCLI preflight is historical because CloudCLI is retired;
- that Stage 7 checkpoint resolved all 16 targets; current post-retirement Maintenance acceptance is 17 actionable targets with `CHECK_FAILED=0`, while update availability is ordinary mutable runtime state;
- Docker application-version / track / digest semantics remain valid;
- operator-triggered Master Batch Task 12 remains accepted with clean post-scan and health gates;
- public `update.escloud.us`, Authelia boundary, same-origin Semaphore API/UI, nginx, system/user services, Docker workloads and failed-unit gate all pass.

Final acceptance record: `STAGE_07_FINAL_ACCEPTANCE_2026-09-21.md`.

**Repository implementation-source reconciliation:** Stage 10 persisted the exact accepted runtime `maintenance/edge/scripts/manual-update` back to the canonical repository. The normalized `/home/core` `user_cli` execution context and Hermes fail-closed lazy-dependency verification are now present in both runtime and repository source.

The next finite infrastructure stage is **Stage 8 — Edge Monitoring, Heartbeats
& Alerts**.


## Stage 8 — Edge Monitoring, Heartbeats & Alerts — COMPLETE / ACCEPTED

Stage 8 is complete with `STAGE08_FINAL_ACCEPTANCE=PASS`.

Accepted/deployed runtime:

- one persistent host-native Python `edge-monitor.service`, enabled/active under systemd with `Restart=always` and accepted runtime `NRestarts=0`;
- cadences: FAST 5s, NORMAL 20s, SLOW 60s, OPERATIONS 300s;
- ordinary endpoint failures require two consecutive failed probes before `FAIL`;
- live atomic telemetry: `/run/edge-monitor/snapshot.json`;
- durable transition/notification state: `/var/lib/edge-monitor/state.json`;
- domains: EDGE, APPLICATIONS, HOME_PAI, KNOWLEDGE and OPERATIONS;
- direct dedicated Mattermost incoming webhook to the `Monitoring` channel, with notifications only on meaningful state changes and recovery;
- current Docker workload contract covers six running containers;
- Home/PVE and ai-node/vLLM reachability, Syncthing Knowledge state, Backrest freshness and Stage 7 maintenance metadata are monitored;
- Backrest freshness is derived from structured `/var/lib/backrest/oplog.sqlite` successful snapshot operations;
- Stage 7 `UPDATE_AVAILABLE` is informational and does not degrade monitoring; Stage 8 does not schedule Stage 7 Refresh;
- no Prometheus/Grafana/Loki/Gatus stack, monitoring database, receiver service, separate monitoring WebUI, external provider, independent vantage point or Home/PAI agent is deployed.

Final Stage 08.3 acceptance used a monitor-only synthetic probe and proved the complete transition contract without stopping production services: initial `OK` was silent; two consecutive failed NORMAL probes produced one `OK → FAIL` notification; unchanged `FAIL` produced no duplicate; recovery produced one `FAIL → OK` notification. The original monitor config SHA256 `91bacef62dbf5076b405b3b08512aa85ab6bb03ca0c887b7f86521cdd78133c5` was restored exactly and all synthetic artifacts were removed. Final production state was all five domains `OK`, `OVERALL_STATE=OK`, `NRestarts=0`, and zero failed systemd units.

Known accepted limitation: because monitoring is intentionally hosted only on `edge`, complete loss of edge or its external connectivity cannot itself be reported while the node is unreachable.

Final acceptance record: `STAGE_08_FINAL_ACCEPTANCE_2026-09-22.md`.

## Stage 10 — Edge Final Integrated Infrastructure Acceptance — COMPLETE / ACCEPTED

Stage 10 is complete with `STAGE10_FINAL_ACCEPTANCE=PASS`.

The bounded final integrated audit completed with zero fresh failures and no runtime mutations or disruptive tests. Current services, containers, listeners, ingress/TLS/auth, NetBird/Home/PAI connectivity, Knowledge integration, Backrest state, maintenance/manual-only controls, monitoring and the Stage 9 portal all passed their fresh integration gates. Prior destructive/recovery evidence from Stages 3–9 was reused rather than repeated.

Stage 10 also closed the known Stage 7 persistence gap by writing the exact accepted runtime `maintenance/edge/scripts/manual-update` into the canonical repository and reconciling current mutable version facts. Historical acceptance records remain unchanged.

Final acceptance record: `STAGE_10_FINAL_ACCEPTANCE_2026-09-22.md`.

## Current next step

Stage 10 remains a valid COMPLETE / ACCEPTED checkpoint for the currently deployed baseline, including final hygiene cleanup. A newly identified repository/history gap shows that some previously deployed or considered infrastructure capabilities were not fully carried into the canonical roadmap.

The active next stage is **Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion**.

Stage 11 will:
- reconcile legacy baseline, migration-reference material, canonical repository state, current runtime and available project history;
- identify forgotten, omitted or incorrectly classified infrastructure services/tools;
- distinguish historical-only/superseded components from capabilities still useful before user workflows;
- research current upstream options only where the earlier product choice is no longer authoritative or the capability was never accepted;
- deploy and accept only selected missing infrastructure capabilities;
- preserve Stage 10 as the accepted pre-Stage-11 baseline rather than mixing new deployment work into Stage 10.

If Stage 11 changes material infrastructure boundaries, return to Stage 10 afterward for a bounded re-acceptance of only the affected integration surfaces. If Stage 11 concludes with no material deployment changes, the existing Stage 10 acceptance remains sufficient.

**Automation & User Workflows** begins only after Stage 11 completion and any required bounded Stage 10 re-acceptance.

Post-Stage-10 recovery checkpoint: the one-time provider golden VPS snapshot required by the accepted Stage 6 recovery contract was created successfully by the operator after `STAGE10_FINAL_ACCEPTANCE=PASS`. This is a recovery checkpoint only; it does not create a new infrastructure stage or alter Stage 10 acceptance.

Final Stage 10 hygiene cleanup is also complete. `STAGE10_FINAL_BASELINE_CLEANUP=PASS` and `STAGE10_PRODUCTION_NON_REGRESSION=PASS` with zero cleanup failures, final RC=0 and `REBOOT_REQUIRED=NO`. The cleanup removed verified temporary/audit artifacts, superseded stage rollback material, package/download caches and the obsolete Codex 0.154.0 standalone release while preserving production state, active runtime caches, fallback kernel, logs, Restic caches and current recovery mechanisms. Root filesystem free space increased by 1,900,048,384 bytes (1.77 GiB), from 132 GiB available / 15% used to 133 GiB available / 14% used.


## Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion — COMPLETE / ACCEPTED

Stage 11 is complete.

Accepted outcome:

- forgotten/omitted legacy capabilities were reconciled against current runtime and architecture;
- Nextcloud personal cloud-drive plus private SMB workspace access were split into planned Stage 12;
- `backup.escloud.us` was retained as a small deferred Backrest WebUI ingress task;
- `docs.escloud.us` was retained as deferred WenTian technical publishing, to begin only when a useful EN/RU translated corpus exists;
- `go.escloud.us` and `sync.escloud.us` were retired;
- legacy Filestash, public Syncthing UI, Homepage, Cockpit, Maintenance Center, old monitoring/socket-proxy, speedtest surface, legacy Codex runner, browser-stack and old same-VPS Restic architecture remain historical only;
- runtime cleanup audit found no remaining legacy listeners, systemd units, containers/images, filesystem paths, nginx references or Authelia references;
- the shared `escloud.us` certificate lineage was reissued without `sync.escloud.us`;
- Xray/Hysteria TLS copies were synchronized;
- corrected local and public HTTPS E2E verification passed;
- final DNS verification reports both `go.escloud.us` and `sync.escloud.us` absent;
- nginx config valid, production containers healthy, zero failed systemd units.

Acceptance markers:

- `STAGE11_LEGACY_ARTIFACT_CLEANUP_AUDIT=PASS`;
- `STAGE11_SYNC_TLS_CLEANUP_FINAL_VERIFY=PASS`;
- `STAGE11_FINAL_ACCEPTANCE=PASS`.

Stage 10 remains the accepted pre-Stage-11 baseline; no broad Stage 10 re-acceptance is required because Stage 11 runtime mutation was limited to retired TLS namespace cleanup and bounded non-regression passed.

**Subsequent implementation:** Stage 12 and Stage 13 are now COMPLETE / ACCEPTED.


## Stage 12 — Nextcloud Cloud Drive & Private Workspace Access — COMPLETE / ACCEPTED

Stage 12 is complete and accepted.

Accepted runtime:

- Nextcloud `34.0.4.1` / `34.0.4` is deployed at `/opt/nextcloud/compose.yaml`;
- application backend is loopback-only at `127.0.0.1:18080`;
- persistent Nextcloud state is under `/srv/nextcloud`;
- the portable user-visible cloud files tree is `/srv/cloud`, bound into the accepted Nextcloud user's `files` directory while Nextcloud metadata/version/trash state remains outside that path;
- public cloud endpoint is `https://cloud.escloud.us/` through the existing Xray -> nginx ingress;
- macOS Nextcloud native client/File Provider acceptance passed; iPad client behavior was also validated;
- the originally deployed Samba/SMB workspace implementation was rejected for this topology because clientless Home LAN access to the edge NetBird overlay would require production Home routing/firewall changes or an extra proxy;
- Samba and all Stage 12 operational traces were fully removed: packages, binaries, units, listeners, firewall rules, config/state/cache/log paths and installation APT cache are absent;
- Home VM100, MikroTik and CT300 were not modified for workspace access;
- direct workspace access is instead provided by rclone WebDAV `1.75.1`;
- WebDAV publishes exactly `/home/core/projects/`, owned `core:core`, and nothing else;
- `projects-webdav.service` is an enabled persistent `core` user service bound only to `127.0.0.1:18081`;
- public workspace endpoint is `https://go.escloud.us/` through Xray TLS -> nginx -> rclone;
- WebDAV uses protocol-native HTTP Basic authentication over HTTPS; Authelia is intentionally not inserted into the WebDAV client protocol path;
- local and public `PROPFIND/MKCOL/PUT/GET/MOVE/DELETE` E2E passed;
- the shared `escloud.us` certificate lineage was expanded to include `go.escloud.us` and the existing deploy hook synchronized Xray/Hysteria2/Stalwart;
- macOS Finder connection is accepted and configured for automatic login-time connection using the native server connection + Keychain path;
- macOS network-store `.DS_Store` suppression was selected client-side rather than adding server-side cleanup automation;
- zero failed systemd units at final server acceptance.

Acceptance markers:

- `STAGE12_NEXTCLOUD_CORE_FINAL_AUDIT=PASS`;
- `STAGE12_SAMBA_FULL_REMOVAL=PASS`;
- `STAGE12_PROJECTS_WEBDAV_LOCAL_ACCEPTANCE=PASS`;
- `STAGE12_GO_WEBDAV_PUBLIC_INGRESS_DEPLOYMENT=PASS`;
- `STAGE12_FINAL_ACCEPTANCE=PASS`.

Authoritative final record: `STAGE_12_FINAL_ACCEPTANCE_2026-09-23.md`.

## Stage 13 — Backrest WebUI Ingress — COMPLETE / ACCEPTED

Stage 13 is complete and accepted.

Accepted runtime:

- existing Backrest remains host-native and loopback-only at `127.0.0.1:9898`;
- public endpoint: `https://backup.escloud.us/`;
- ingress path: Xray TLS :443 -> nginx `127.0.0.1:8080` -> Authelia -> Backrest `127.0.0.1:9898`;
- TCP/80 redirects to HTTPS;
- existing Authelia `one_factor` policy, DNS and shared TLS identity were reused without modification;
- no new public listener or UFW rule was introduced;
- Backrest-native bearer-token behavior is preserved behind Authelia;
- Backrest config SHA remained `984b4b996e73b82fe99c5a2339c8d6a5dcf6b09da2219729dfb7c56bb015fa55`;
- Backrest PID remained `1044`, `NRestarts=0`;
- backup engine, repositories, schedules, retention and restore behavior were unchanged;
- final server-side deployment marker: `STAGE13_SERVER_SIDE_INGRESS_DEPLOYMENT=PASS`;
- authenticated browser E2E confirmed the real Backrest WebUI and existing repositories/plans/history are visible;
- zero failed systemd units at final server-side acceptance.

The first deployment verifier failure was a graceful-nginx-reload generation race: an immediate request reached an old worker and the automatic rollback restored the prior state. The corrected deployment retained the same vhost and used bounded route polling; the first poll saw the old default route and the second observed the new `301`, proving the production configuration itself was correct.

Final marker:

- `STAGE13_FINAL_ACCEPTANCE=PASS`.

Authoritative final record: `STAGE_13_FINAL_ACCEPTANCE_2026-09-23.md`.

## Current next step

No finite infrastructure stage is active after Stage 13. The next normal workstream is **Automation & User Workflows**. The separate WenTian technical publishing task at `docs.escloud.us` remains deferred until a useful translated corpus exists.



## T3 persistent remote workspace — accepted 2026-09-23

T3 persistent remote workspace is **COMPLETE / ACCEPTED**.

Current accepted state:

- official user service `t3code.service` under `core`;
- temporary compatibility pin `0.0.43-nightly.20260923.2150`;
- service-managed runtime on `127.0.0.1:3773`;
- project root `/home/core/projects`;
- T3 Connect is the primary client transport;
- managed relay client `cloudflared 2026.5.2`;
- T3 Connect remains desired/authenticated/linked with `publishAgentActivity=false`;
- macOS T3 Desktop and iPad T3 Code are accepted T3 Connect clients;
- `https://code.escloud.us` is the accepted browser surface through existing Xray/nginx/Authelia ingress;
- Codex ACP and Antigravity ACP are usable through T3;
- standalone `antigravity-cli-daemon.service` remains independent;
- the former T3 Desktop SSH transport/profile is retired;
- stale `/home/core/.t3/ssh-launch` artifacts were removed and no SSH-managed T3 runtime remains;
- controlled reboot acceptance passed: official service, service-owned runtime, nightly pin and relay/T3 Connect recovered automatically without operator restart/relink;
- relay startup is asynchronous to `t3 serve`; automatic reconciliation completed and registered four QUIC tunnel connections after reboot;
- post-reboot Mac/iPad T3 Connect, existing threads, Antigravity and `code.escloud.us` all passed.

Stable `0.0.42` is not the accepted persistent version because it reproduced old-thread projection decoding failures and an Antigravity local-health failure in this deployment. The nightly pin is temporary and should be re-evaluated against a later stable release, not downgraded blindly.

Authoritative record: `T3_PERSISTENT_REMOTE_WORKSPACE_ACCEPTANCE_2026-09-23.md`.



## 2026-09-24 — Maintenance Version Discovery v2 — COMPLETE / ACCEPTED

Post-Stage-07.2 corrective work on the Edge Maintenance version-discovery path is complete and accepted.

Current accepted state:

- persistent cross-run Docker remote-version cache is removed; stale remote data is not carried forward as a fallback;
- Docker Hub workloads, including `docker.n8n.io/n8nio/n8n:stable`, resolve current floating-tag state through the Docker Hub Tags API rather than Docker Hub Registry V2;
- Nextcloud and Redis exact patch versions are resolved from their official upstream release sources and bound to the floating image by Linux/amd64 descriptor digest;
- Bulwark remains resolved through GHCR registry metadata;
- GitHub-native latest versions use `github.com/.../releases/latest` redirects and do not depend on the GitHub REST release API;
- obsolete `EDGE_MAINTENANCE_FORCE_REGISTRY_COMPONENT` refresh behavior is removed;
- accepted runtime/repository collector blob: `19397985821a1204cde4333b40775bc0a4cef306`;
- canonical implementation commit: `46c3a3a9e8eb650eb4b1b050320d4df128eed49e`;
- normal post-commit Semaphore Refresh task 33 updated the template checkout to that commit;
- final refresh: 24 status rows, zero unresolved rows and zero failed checks;
- manual-only Maintenance execution and native-first ownership policy remain unchanged.

Acceptance marker: `VERSION_DISCOVERY_V2_FINAL_ACCEPTANCE=PASS`.

Authoritative record: `VERSION_DISCOVERY_V2_FINAL_ACCEPTANCE_2026-09-24.md`.

## 2026-09-25 — Nextcloud Update Architecture — COMPLETE / ACCEPTED

- acceptance marker: `NEXTCLOUD_UPDATE_ARCHITECTURE=PASS`;
- runtime remains Nextcloud `34.0.4`; no application update was executed;
- Maintenance now reports `34.0.4 -> 35.0.1` as `UPDATE_AVAILABLE`;
- deployment artifact resolved for the current target is `nextcloud:35.0-apache`;
- dedicated `nextcloud_compose` driver, actions renderer, framework contract and driver preflight all passed;
- update execution remains operator-initiated only.

Acceptance record: `NEXTCLOUD_UPDATE_ARCHITECTURE_ACCEPTANCE_2026-09-25.md`.

## 2026-09-25 — Maintenance update architecture audit corrections — ACCEPTED PARTIAL BASELINE

Confirmed and accepted runtime corrections from the ongoing update-architecture audit:

- PostgreSQL discovery for both Mattermost and Nextcloud no longer uses the installed major track as the latest-stable ceiling. Official latest-stable discovery reports PostgreSQL `18.6`; execution track resolves to `18-alpine` for the current stable major.
- Stalwart discovery no longer uses the installed `v0.16` series as the latest-stable ceiling. Official latest-stable discovery reports `0.16.23`; execution track remains `v0.16` for that current stable series.
- Runtime verification passed with `DISCOVERY_VERSION_CEILINGS_REMOVED=PASS`; no PostgreSQL or Stalwart service update was executed.
- Restic Maintenance ownership now uses the native standalone-binary updater `/usr/local/bin/restic self-update` instead of the generic GitHub binary replacement driver.
- Restic runtime verification passed with `RESTIC_NATIVE_SELF_UPDATE_DEPLOY_VERIFY=PASS`; installed version remained `0.19.1` and no Restic update was executed.
- Xray, Hysteria2 and Backrest custom binary-update ownership remains unchanged after audit because the wrappers preserve accepted service/config state while performing the required binary update; no change is accepted for those drivers.
- Xray upstream `.dgst` verification was explicitly rejected by the operator as unnecessary complexity for this deployment.

Acceptance markers:

- `DISCOVERY_VERSION_CEILINGS_REMOVED=PASS`
- `RESTIC_NATIVE_SELF_UPDATE_DEPLOY_VERIFY=PASS`

The broader update-architecture audit remains in progress; do not treat unresolved components as accepted changes.

## 2026-09-25 — Antigravity native auto-update ownership — COMPLETE / ACCEPTED

Runtime reconciliation completed successfully.

Accepted current state:

- Antigravity native background self-updater is the sole active update owner;
- native updater proof passed: official manifest reachable, updater enabled, background updater observed in logs, and `update_status.json` reported `success=true` / `Update successful, restart CLI to use`;
- Antigravity is absent from Maintenance version rows, generated manual targets, actions, Master Batch order, runtime enablement, and active Semaphore mappings;
- current Maintenance model is exactly 16 actionable manual targets / 23 monitored components / 0 manual CLI targets / `CHECK_FAILED=0`;
- retired Semaphore template ID 17 (`43. Update Antigravity CLI`) was removed completely;
- template 17 had zero historical tasks before deletion, so no task history was lost;
- Semaphore SQLite foreign-key check remained clean after deletion;
- no Antigravity update and no service restart was executed during ownership reconciliation.

Acceptance markers:

- `ANTIGRAVITY_NATIVE_AUTO_UPDATE_PROOF_AUDIT=PASS`
- `ANTIGRAVITY_ACTIVE_MODEL_GATE=PASS`
- `SEMAPHORE_TEMPLATE_17_CLEANUP_GATE=PASS`
- `ANTIGRAVITY_NATIVE_UPDATER_GATE=PASS`
- `ANTIGRAVITY_NATIVE_AUTO_UPDATE_OWNERSHIP=PASS`
- `ANTIGRAVITY_MANUAL_MAINTENANCE_REMOVED=PASS`

## 2026-09-25 — Stalwart rolling-minor update architecture — COMPLETE / ACCEPTED

Runtime deployment and verification completed successfully.

Accepted current state:

- Stalwart latest-stable discovery is independent of the deployed rolling-minor track;
- current runtime and latest stable are both `0.16.23`;
- current production image track remains `stalwartlabs/stalwart:v0.16`;
- dedicated `stalwart_compose` driver is deployed and executable;
- the driver preserves the current rolling-minor track for patch updates and can persist the next upstream-supported rolling-minor track when the operator initiates a future series upgrade;
- helper preflight passed against the real compose/runtime state;
- no Stalwart container recreate, restart, image change, compose rewrite, or version update occurred during acceptance.

Acceptance markers:

- `STALWART_LATEST_STABLE_DISCOVERY=PASS`
- `STALWART_ROLLING_MINOR_EXECUTION_ARCHITECTURE=PASS`
- `NO_SERVICE_MUTATION_GATE=PASS`


---

## 2026-09-25 — Edge Maintenance / Nextcloud current accepted state

- Maintenance target model: `update_units_v5`.
- Current manual actionable targets: 16.
- Current monitored components: 23.
- Current CLI targets: 0.
- Current refresh state: `CURRENT=23`, `UPDATE_AVAILABLE=0`, `CHECK_FAILED=0`.
- Master Batch accepted current model: `TOTAL=16`; `SEMAPHORE` remains `individual_only`.
- Antigravity is outside manual Maintenance under its native background updater.
- Nextcloud runtime: `35.0.1`; application track `nextcloud:35.0-apache`.
- Nextcloud `occ status`: installed, `maintenance=false`, `needsDbUpgrade=false`.
- Nextcloud schema check: clean (`[]`).
- `oc_federated_invites` schema drift was repaired by re-executing official `cloud_federation_api` migration `1016Date202502262004`; migration history remains singular.
- Canonical/runtime `update-nextcloud` blob: `f1c1d17c39b4e90c129a32d4f5bcdf45e3a40751`.
- Nextcloud updater now uses bounded application-readiness polling after container recreation; retry and fail-closed timeout semantics are accepted.
- Final clean Master regression: `16/16 CURRENT`, `RUN=0`, `SKIPPED_CURRENT=16`, post-scan PASS, health PASS, no component update executed.
- Acceptance marker: `TASK39_READINESS_INCIDENT_ACCEPTANCE=PASS`.

---

## 2026-09-25 — Maintenance service-name normalization

- Display names accepted:
  - `POSTGRESQL` → `PostgreSQL (Mattermost)`;
  - `NEXTCLOUD_POSTGRESQL` → `PostgreSQL (Nextcloud)`;
  - `NEXTCLOUD_REDIS` → `Redis (Nextcloud)`.
- Internal target IDs remain unchanged.
- Update drivers, execution order and lifecycle semantics remain unchanged.
- Maintenance rows are sorted by display `label` using case-insensitive ordering before `maintenance.json` is written; dashboard tables therefore render `SERVICE NAME` alphabetically.
- Accepted Docker table order: `Authelia`, `Bulwark`, `Mattermost`, `n8n`, `Nextcloud`, `PostgreSQL (Mattermost)`, `PostgreSQL (Nextcloud)`, `Redis (Nextcloud)`, `Stalwart`.
- Runtime/canonical alignment passed for `maintenance-targets-refresh` and `semaphore-templates.json`.
- Acceptance markers: `MAINTENANCE_SERVICE_NAME_NORMALIZATION=PASS`, `SERVICE_NAME_ALPHABETICAL_SORT=PASS`.


---

## 2026-09-25 — Nextcloud personal-file-cloud policy reconciliation

Current accepted Nextcloud policy after runtime reconciliation:

- Nextcloud Server: `35.0.1`; healthy, maintenance off, no DB upgrade pending.
- Primary working account: OIDC user `Eugene` via Authelia; local Database user `admin` is retained as recovery/bootstrap admin.
- Native-client access remains active; permanent filesystem tokens for macOS and iOS were preserved.
- Required file-cloud apps remain enabled: Files, DAV, Settings, Provisioning API, File Sharing, Deleted files, Versions, Dashboard, Notifications, user_oidc, Viewer, Webhook Listeners and Workflow Engine.
- `files_versions` is enabled as part of file data-safety semantics.
- Nextcloud-native TOTP and WebAuthn providers are disabled; `twofactor_backupcodes` remains enabled only because Nextcloud marks it always-enabled.
- Federation user functionality is disabled globally through `files_sharing`: outgoing/incoming server-to-server shares, outgoing/incoming server-to-server group shares and lookup-server use are all `no`.
- Always-enabled platform apps are retained rather than bypassed: `cloud_federation_api`, `federatedfilesharing`, `lookup_server_connector`, `oauth2`, `profile`, `twofactor_backupcodes`.
- OAuth2 has zero registered clients.
- Unused optional apps disabled by reconciliation: `logreader`, `privacy`, `serverinfo`, `twofactor_totp`, `twofactor_webauthn`.
- Existing disabled non-required apps remain disabled, including Activity, AppAPI, Teams/Circles, Comments, Federation, external storage, Office, Photos, Recommendations, Support, Usage Survey, User Migration, User Status and Weather Status.
- UI-oriented apps intentionally retained include Dashboard, Inter Fonts, Custom menu, PDF viewer, Text, Theming, Viewer and Related Resources.
- Integration-oriented apps intentionally retained include File Sharing, Share by mail, Notifications, Webhook Listeners and Workflow Engine.
- Global Dashboard layout is `files-favorites`; per-user Dashboard layout overrides were removed so both existing users inherit the same global policy.
- Background jobs remain on `cron`.
- Local health verification passed: `/status.php` HTTP 200 and unauthenticated DAV probe HTTP 401.
- Acceptance marker: `NEXTCLOUD_POLICY_RECONCILIATION_FINAL=PASS`.

Authoritative record: `NEXTCLOUD_POLICY_RECONCILIATION_ACCEPTANCE_2026-09-25.md`.


---

## 2026-09-25 — Nextcloud ↔ Mattermost file-sharing integration

Current accepted state:

- Nextcloud app `integration_mattermost 3.2.0` is installed and enabled.
- Mattermost user access tokens are enabled; the existing `eugene` account is connected from Nextcloud through its user-level encrypted token storage.
- Nextcloud connection verification passed for `https://chat.escloud.us`, Mattermost user `eugene`, and Nextcloud health.
- Global Dashboard layout currently includes `mattermost_notifications` in addition to `files-favorites`.
- The accepted primary use case is **Nextcloud Files -> Send to Mattermost -> select an existing relevant Mattermost channel**.
- No dedicated Mattermost channel is created merely for the integration.
- Dashboard notifications and unified Mattermost search are secondary conveniences, not the reason for retaining the app.
- A real file-send E2E remains pending until an actual relevant Mattermost channel/use case exists; this does not block the accepted integration design.

Marker: `NEXTCLOUD_MATTERMOST_FILE_SEND_USE_CASE_ACCEPTED`.


---

## 2026-09-25 — Nextcloud files-first WebUI policy

Current accepted state:

- Nextcloud system `defaultapp` is explicitly set to `files`.
- The `dashboard` app is disabled.
- Nextcloud now opens directly into Files after login instead of showing Dashboard.
- Dashboard widgets are no longer part of the active UI policy.
- `integration_mattermost` remains enabled.
- Mattermost file action remains enabled (`file_action_enabled=1`), so the accepted workflow **Nextcloud Files -> Send to Mattermost -> choose an existing relevant channel** is preserved.
- Nextcloud remained healthy after the change: maintenance off, no DB upgrade pending.

Acceptance marker: `NEXTCLOUD_FILES_DEFAULT_DASHBOARD_DISABLED=PASS`.


---

## 2026-09-25 — Stage 8 Monitoring Notification Model v2.3.3 — COMPLETE / ACCEPTED

- Production runtime SHA-256: `8bc25a8788bfd60f61c1cc1b62fd61e14f4c551f5ebfc3900f7c837b4dc3b714`.
- Mattermost `Monitoring` uses service-oriented correlated incident notifications with parent/child suppression.
- Notification posts are Blocks-only; duplicated top-level plain text is removed.
- Presentation is mobile-first and vertical; production cards do not use `column_set`.
- Accepted heading: large integrated severity title such as `### 🔴 Mattermost unavailable`; scope/category remains a separate small/subtle line.
- Incident metadata is `STARTED` plus optional `CONFIRMED` when meaningful.
- Recovery metadata is `DURATION` plus `RECOVERED`.
- Diagnostics remain collapsible.
- Final real-webhook synthetic E2E proved INCIDENT delivery, unchanged-incident deduplication and RECOVERED delivery with exactly two Mattermost posts.
- Final E2E did not mutate production durable state; service remained active/running and `overall_state=OK`.

Acceptance marker: `EDGE_MONITOR_NOTIFICATION_V2_3_3_FINAL_E2E=PASS`.

Authoritative record: `STAGE_08_MONITORING_NOTIFICATION_MODEL_V2_3_3_ACCEPTANCE_2026-09-25.md`.


---

## 2026-09-25 — Mattermost global message prune — COMPLETE / ACCEPTED

- All Mattermost message history was permanently removed through the Mattermost application API.
- Original corpus: 181 post rows.
- Final message state: `posts=0`, `threads=0`, `threadmemberships=0`, `fileinfo=0`.
- Active users and public/private/DM channel structures were preserved.
- Final preserved active inventory: 6 users, 2 public channels, 3 private channels, 4 DM channels, 0 group-DM channels.
- `ServiceSettings.EnableAPIPostDeletion` was restored to `false`.
- Mattermost returned healthy with API HTTP 200.
- `edge-monitor.service` was restored and healthy.
- Temporary recovery artifacts were removed only after final acceptance.

Acceptance marker: `MATTERMOST_GLOBAL_MESSAGES_PERMANENT_PRUNE=PASS`.

Authoritative record: `MATTERMOST_GLOBAL_MESSAGE_PRUNE_ACCEPTANCE_2026-09-25.md`.
