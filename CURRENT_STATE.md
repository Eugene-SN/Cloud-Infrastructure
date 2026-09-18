# Cloud Infrastructure — Current State

## Canonical checkpoint

**Stage 0 — COMPLETE / ACCEPTED**  
**Stage 1 — COMPLETE / ACCEPTED**  
**Stage 2 — Edge Core Applications — COMPLETE / ACCEPTED**  
**Stage 02.5 — Remaining Functional Scope Reconciliation & Research — COMPLETE / ACCEPTED**  
**Stage 3 — Edge Cross-site Connectivity Foundation — COMPLETE / ACCEPTED**

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.  
`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS` on 2026-09-18.  
`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-18.

Primary repository: `Eugene-SN/Cloud-Infrastructure`.

Next production branch:

`04 — Edge Hermes Agent Runtime`

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

The previous future-architecture constraint that `ai-node:/srv/ai-data/knowledge/obsidian` must permanently remain canonical is superseded.

**Current factual runtime remains unchanged until Home Infrastructure completes its migration.** The existing vault on `ai-node` remains the current source at this checkpoint.

Accepted future ownership boundary:

- **Home Infrastructure** owns the PVE 24/7 canonical knowledge foundation, PVE-side synchronization service, Home consumers and Home-side backup integration;
- **Personal Agents Infrastructure** owns the `ai-node` active RW synchronized replica and local n8n/OpenClaw/vLLM/OCR/RAG consumers/producers after Home cutover;
- **Cloud Infrastructure** owns only the `edge` active RW synchronized replica and n8n/Hermes/cloud-AI integration.

Cloud Stage 5 is therefore an integration stage. It must begin with a fresh expanded read-only Home/PAI/Cloud audit and must reuse the Home-accepted server-side synchronization mechanism by default.

If PVE canonical migration has not reached explicit Home acceptance when Stage 5 begins, Stage 5 stops before mutation and reconciles the dependency instead of creating a parallel canonical/sync architecture.

MacBook/iPhone/iPad Obsidian synchronization is completely outside Cloud Infrastructure scope and is assigned to a later separate Home Infrastructure user-integration branch.

## Final remaining roadmap

1. **Stage 4 — Edge Hermes Agent Runtime**;
2. **Stage 5 — Edge Knowledge Replication & Data Integration**;
3. **Stage 6 — Edge Backrest & Recovery**;
4. **Stage 7 — Edge Maintenance & Update**, including separate Codex `update.escloud.us` substage;
5. **Stage 8 — Edge Monitoring, Heartbeats & Alerts**;
6. **Stage 9 — Edge Cloud Portal**, including separate Codex `app.escloud.us` substage;
7. **Stage 10 — Edge Final Integrated Infrastructure Acceptance**;
8. post-infrastructure **Automation & User Workflows** as a continuous workstream.

The old conditional `Remaining Infrastructure Services` stage is removed because Stage 02.5 selected no additional standalone infrastructure product requiring that slot.

Backrest-before-Semaphore remains mandatory. Monitoring remains late-stage so it is built once against the substantially complete inventory. `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

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

Shared service account `core`: UID/GID `1000:1000`, password locked, no sudo/docker group. `core` linger is enabled for Antigravity Remote Control.

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

Protected private web namespace includes `n8n`, `code`, future `app`, `backup`, `ops`, `update`, `docs`, `cloud` and `sync`. `mail.escloud.us` intentionally uses native mail-stack authentication. Stage 4D also accepts `chat.escloud.us` as an explicit native-client exception: Mattermost will use Mattermost-native authentication without Authelia.

## TLS

Shared Certbot lineage: `/etc/letsencrypt/live/escloud.us`.

Current SAN set includes `escloud.us`, `app`, `auth`, `backup`, `chat`, `cloud`, `code`, `docs`, `mail`, `n8n`, `ops`, `sync.escloud.us`. `update.escloud.us` has been created in DNS for the future maintenance/update page; certificate/ingress activation remains deferred to Stage 7.

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

- version `1.2.5`;
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

## Stage 4 — Hermes Agent Runtime (in progress)

A post-setup read-only audit on 2026-09-18 confirmed the initial host-native Hermes installation under `core`.

Current confirmed baseline:

- official upstream git install under `/home/core/.hermes/hermes-agent`;
- reported version `0.21.3 (2026.9.14)`, branch `main`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, clean worktree;
- main inference provider `AI-Node vLLM` -> `http://192.168.1.30:8000/v1`;
- model `qwen3.8-27b-fp8`, Chat Completions mode, configured/verified context `195216`;
- terminal backend `local`;
- Qwen3.8 reasoning normalized and accepted: `agent.reasoning_effort` unset, `model.reasoning_echo=true`, model-native thinking + terminal tool call + resumed multi-turn reasoning replay verified; current config SHA256 `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- user `hermes-gateway.service` enabled and active under `core`, but no messaging platforms and no listeners yet on `8642` or `9119`;
- standalone Codex CLI `0.154.0` and Antigravity CLI `1.2.5` remain available to `core`;
- Dashboard/API/n8n integration and final macOS Remote Gateway integration remain pending;
- Hermes host/toolchain normalization accepted: `ripgrep`, `ffmpeg`, build/Python/libffi development dependencies and Chromium system libraries installed; `browser-use` backend and managed Chromium `browser_exec` verified end-to-end; `cua-driver 0.28.2` available under the actual `core` runtime; marker `STAGE4_HERMES_SYSTEM_TOOLCHAIN_NORMALIZATION=PASS`;
- wizard-selected `openai-codex` image generation is not currently usable because Hermes-managed Codex auth is absent.
- Mattermost is a mandatory Stage 4 private collaboration/control substage and its **core runtime is now DEPLOYED / ACCEPTED**. Stage 4D design is COMPLETE / ACCEPTED: Mattermost Team Edition, official Docker Compose pattern, separate dedicated PostgreSQL container, local `/srv` state, existing Xray/host-nginx/shared-TLS ingress, `https://chat.escloud.us` with Mattermost-native authentication and **no Authelia**, TPNS enabled for official mobile clients, Calls excluded. Mattermost integrations follow a strict native-only current-project rule. Execution order is Hermes first, n8n second, then a separate usefulness review for optional Mattermost↔Stalwart SMTP/email functionality. Hermes uses the official built-in Mattermost gateway; n8n uses its official Mattermost integration for supported operations. Stalwart SMTP is a confirmed capability but is **not yet accepted for activation**. Acceptance: `STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`;

Detailed factual record: `STAGE_04_HERMES_POST_SETUP_BASELINE_2026-09-18.md`.

Stage 4 remains **IN PROGRESS / NOT YET ACCEPTED**.

Mattermost Stage 4E core runtime is **ACCEPTED**: `STAGE4E_MATTERMOST_CORE_RUNTIME_ACCEPTANCE=PASS`. Runtime: upstream `mattermost/docker` commit `497414659ee7127677d2b91b44bb4f3ea9d14695`, Mattermost Team `11.11.0`, PostgreSQL `18-alpine`, Mattermost container healthy, PostgreSQL running, both `restart=unless-stopped`, host publication only `127.0.0.1:18065 -> 8065`; host ports `8065/8443/5432` are not published; Hermes gateway/config non-regression passed. Acceptance record: `STAGE_04E_MATTERMOST_CORE_RUNTIME_ACCEPTANCE_2026-09-18.md`.

## Recovery / preserved state

- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- migration-preservation archive: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, retained outside GitHub for legacy-reference/recovery use; do not indiscriminately restore legacy credentials.

## Current next step

Stage 4 — Edge Hermes Agent Runtime is **IN PROGRESS**. Follow the complete authoritative Stage 4A–4I sequence in `IMPLEMENTATION_PHASES.md`; do not collapse Stage 4 to only the immediate next test block. Continue from `STAGE_04_HERMES_POST_SETUP_BASELINE_2026-09-18.md`. Mattermost Stage 4D research/design is COMPLETE / ACCEPTED. **Stage 4E Mattermost core runtime is accepted. Current focus is Mattermost ingress + native application setup.** After public/native-client Mattermost acceptance: integrate Hermes first using the official Hermes Mattermost guide, then n8n, then discuss whether Mattermost email functionality via Stalwart is useful enough to enable. Do not reinstall Hermes or reopen Stage 3 transport unless a concrete incompatibility appears.
