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

Current recovery workstream:

`04.3 — Edge Hermes Stage 4 Recovery, Completion & Final Acceptance`

Git branch: `04.3-edge-hermes-recovery-completion`.

Stage 4 — Edge Hermes Agent Runtime remains **IN PROGRESS / NOT YET ACCEPTED**.

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

Fresh expanded read-only audit on 2026-09-18 confirms the following current runtime.

### Hermes core

- official upstream git install under `/home/core/.hermes/hermes-agent`;
- Hermes `0.21.3 (2026.9.14)`, branch `main`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, clean worktree;
- main provider `AI-Node vLLM` -> `http://192.168.1.30:8000/v1`;
- model `qwen3.8-27b-fp8`, Chat Completions mode, verified context `195216`;
- Qwen3.8 model-native reasoning/replay accepted; `config.yaml` SHA256 remains `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- terminal backend `local`;
- system toolchain/browser normalization accepted, including managed Chromium and `cua-driver 0.28.2`;
- `hermes-gateway.service` is enabled and currently active under `core`; current `NRestarts=0`;
- Mattermost environment is configured and its token validates successfully as bot `hermes`;
- standalone Codex CLI `0.154.0` and Antigravity CLI `1.2.5` remain available to `core`;
- Web Search/Extract, Edge TTS and Vision functional probes are PASS; CUA is accepted as `NOT_APPLICABLE_HEADLESS_EDGE`; Image Generation remains configured but is non-blocking for Stage 4 acceptance; fresh core Qwen3.8/vLLM regression is accepted with `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS`.
- Stage 4B executor read-only audit is accepted: `STAGE4B_EXECUTOR_READONLY_AUDIT=PASS`.
- Actual Hermes local terminal child context is clean for standalone executors: cwd `/home/core`, `HOME=/home/core`, `HERMES_HOME=/home/core/.hermes`, core local bin on PATH, and no `OPENAI_BASE_URL`, `OPENAI_API_KEY` or `CODEX_*` environment override.
- Codex CLI `0.154.0` exposes native headless `codex exec` capabilities including JSON/ephemeral/sandbox/skip-git/output-last-message/model controls and uses the existing standalone OAuth state with no custom provider/MCP override.
- Antigravity CLI `1.2.5` raw help confirms native headless print mode plus JSON/stream-JSON, timeout, model, effort, sandbox/permission and conversation controls; its existing local auth/state is reused.
- Accepted Stage 4B target: foreground non-PTY one-shots by default (`codex exec`; `agy -p/--print` with structured output), background only for long/parallel jobs, PTY only for interactive TUI.
- Trusted-executor policy is accepted: no blanket sandbox/container/workspace-only/network restriction under `core`; critical high-impact mutations require operator approval at the Hermes/orchestration instruction layer before delegation, while ordinary non-critical work should remain frictionless.
- Stage 4B direct executor integration is COMPLETE / ACCEPTED: `STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS`; final record `STAGE_04B_FINAL_ACCEPTANCE_2026-09-18.md`.
- Codex CLI `0.154.0`: real foreground non-PTY `codex exec` delegation accepted; random repository context was read by Codex and consumed by Hermes; post-test recovery/non-regression PASS.
- Antigravity CLI `1.2.5`: real foreground non-PTY `agy -p --output-format json` delegation accepted; `status=SUCCESS`, real random file context returned and consumed exactly by Hermes; full-access policy accepted.
- Hermes `stream-json` Tirith warning contamination remains a known non-blocking machine-output defect to address/reconcile in Stage 4F.
- Dashboard/private machine interface and final macOS Remote Gateway acceptance remain pending.

Known lifecycle defect from the expanded audit: a controlled systemd stop/restart sends SIGTERM and Hermes logs the shutdown context, but the process exits status `1`; systemd records `Failed with result 'exit-code'` before the requested restart succeeds. The currently running service is healthy, but this graceful-stop defect must be resolved or explicitly understood before final Stage 4 acceptance.

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
- production n8n remained at workflows `0`, executions `0`, one Mattermost credential;
- n8n and Mattermost health remained PASS after the probe;
- throwaway host/container artifacts were removed;
- acceptance record: `STAGE_04E_N8N_MATTERMOST_INTEGRATION_ACCEPTANCE_2026-09-18.md`;
- marker: `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`.

Stage 4E is **COMPLETE / ACCEPTED**. Final bounded non-regression passed with `STAGE4E_FINAL_NON_REGRESSION=PASS`; final acceptance record: `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`. The official iOS Mattermost/mobile TPNS gate is operator-accepted PASS, and the `mattermost-ai` disposition is complete and accepted.

Detailed accepted records remain authoritative for completed substages; the expanded audit does not retroactively rewrite historical records.

Stage 4 remains **IN PROGRESS / NOT YET ACCEPTED**.

## Recovery / preserved state

- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- migration-preservation archive: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, retained outside GitHub for legacy-reference/recovery use; do not indiscriminately restore legacy credentials.

## Stage 4C Dashboard deployment — 2026-09-18

**CURRENT RUNTIME — DEPLOYED; FUNCTIONAL ACCEPTANCE PENDING.**

- Public URL: `https://hermes.escloud.us`; DNS `45.92.156.17`.
- Hermes exact source remains `d177b119e9c56c9ddc0b7379ffce52341ec06584`; upstream automatic frontend build completed successfully.
- Core user-systemd `hermes-dashboard.service` active/enabled, `NRestarts=0`, backend exclusively `127.0.0.1:9119`. No public TCP/9119 listener.
- Existing Xray TLS -> nginx `127.0.0.1:8080 proxy_protocol` -> Dashboard; HTTP redirects to HTTPS; WebSocket forwarding configured. No Hermes nginx auth_request.
- Public `/api/status` returns HTTP 200, `auth_required=true`, exactly `auth_providers=["self-hosted"]`, `auth_flows=["cookie","native_pkce"]`.
- Anonymous root redirects to login; login page loads; anonymous `/api/auth/me` denied with HTTP 401.
- OIDC authorization redirect verified against issuer `https://auth.escloud.us`, client `hermes-dashboard`, exact callback `https://hermes.escloud.us/auth/callback`, code flow and PKCE/S256. PKCE cookie Secure/HttpOnly verified. This is not yet a completed browser callback.
- Authelia v4.39.27 OIDC activated after native validation of staged configuration; discovery now HTTP 200. Public client, token auth none, explicit consent, one_factor, scopes openid/profile/email/offline_access, authorization-code and refresh-token grants. Existing access_control unchanged.
- Certbot 4.0.0 expanded the existing `escloud.us` lineage through its existing `webroot` / `/var/www/letsencrypt` mechanism. All original 12 SANs retained plus Hermes; current certificate expires 2026-12-17. Existing deploy hook completed TLS distribution and Xray/Hysteria/Stalwart restarts. No second lineage or nginx Certbot plugin.
- Gateway remains active/enabled, `NRestarts=0`; public status reports Mattermost connected. This is a bounded state check, not a rerun of accepted E2E tests.
- Main Hermes config SHA256 unchanged: `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`; Dashboard settings are isolated in its user-systemd environment.
- Root-only recovery snapshot: `/srv/backups/edge-stage4c/recovery-20260918T171719Z`; contains original Authelia configuration and ingress/config/TLS archive. Application rollback retains the valid expanded certificate.

**ACCEPTED DECISION:** latest Stage 4C self-hosted OIDC deployment design in DECISIONS.md. Older forward-auth/session-token-first assumptions are superseded.

**PENDING EXTERNAL EVIDENCE:** real operator browser sign-in and successful callback, loaded authenticated Dashboard, actual Chat response, authenticated Chat/PTY WebSockets. Operator test requested. Stage 4C is **NOT ACCEPTED**, and no Stage 4C final PASS marker exists.

**RECOVERY FINDINGS:** before these mutations, local/root inspection confirmed no partial Dashboard/OIDC deployment, consistent with the reported previous block stopping at `CERTBOT_NGINX_PLUGIN_GATE=FAIL`, RC 40. Root-only evidence was subsequently obtained after the operator enabled sudo. Full previous-session transcripts are unavailable; reviewed GitHub commits and live state are the evidentiary boundary.

**ASSISTANT / TEST-HARNESS DEFECTS:** the old nonexistent nginx-plugin prerequisite and missing-path probes were verifier errors, not production regressions. One HTTP 502 probe during first frontend build occurred before backend readiness; readiness and subsequent public checks passed. Accepted Stage 4A/B/D/E E2E tests were not repeated.

## Current next step

1. Stage 4B is COMPLETE / ACCEPTED; do not rerun Qwen, executor read-only audits, Codex E2E or Antigravity E2E without a concrete regression signal.
2. Proceed to Stage 4C — Hermes Web Dashboard, ingress and auth.
3. Then complete Stage 4F private n8n machine-interface integration, carrying the known Hermes `stream-json` Tirith stdout contamination as a machine-interface constraint.
4. Carry the known upstream Hermes controlled-stop `SIGTERM -> exit 1` defect into Stage 4G; do not locally mask it with `SuccessExitStatus=1`.
5. Perform Stage 4G server-side integrated acceptance, Stage 4H macOS Hermes Desktop integration, and Stage 4I final Stage 4 persistence/acceptance.


Image Generation is non-blocking for Stage 4 and must not divert the critical path; any later image-quality acceptance is human/visual. Do not add a desktop stack solely to make CUA applicable on the headless `edge`.

Do not reopen Stage 3 transport or reinstall already accepted Stage 4 components without a concrete incompatibility.
