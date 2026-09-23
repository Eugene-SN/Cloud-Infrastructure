# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stages 0–7 COMPLETE / ACCEPTED. Stage 8 is the current finite infrastructure stage.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage follows the accepted-first lifecycle. Repository persistence goes directly to the latest `main` by default; use a branch or pull request only when the operator explicitly requests one:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. research only for genuinely unresolved mechanisms or concrete incompatibilities;
4. explicit stage-composition acceptance;
5. stage-scoped architecture/deployment contract and recovery path;
6. deployment;
7. verification and explicit acceptance;
8. persistence/read-back in GitHub;
9. coherent commit/push/read-back on `main` only after complete stage acceptance.

Do not reopen accepted products without a concrete incompatibility or changed requirement. Docker + Compose remain the default for suitable application services; host-native placement is preferred where containerization materially complicates the supported operating model or integration with existing host-native executors.

## Scope semantics — minimum acceptance, not minimal installation

A stage scope lists the required outcomes that must be closed before acceptance. It is **not** an exhaustive feature whitelist for products deployed in that stage.

For already selected services:

- deploy the normal, broadly useful upstream-supported capability set appropriate to the service's long-lived role;
- install shared local dependencies that make those normal capabilities usable when doing so has no material downside;
- do not choose a deliberately minimal/slim service profile merely because the immediate acceptance test uses fewer features;
- do not use "not needed for the current/core Stage path" as an exclusion criterion;
- defer only capabilities with a concrete reason such as external credentials/subscriptions, mutually exclusive architecture, duplication, unsupported/alpha maturity with material cost, heavy unrelated dependencies, or explicit user decision.

This does not move user-specific workflows into infrastructure stages; it ensures the underlying service does not need routine re-installation each time a new workflow starts using another normal capability.

## Completed stages

### Stage 0 — Discovery, preservation and migration preparation

Historical stage label: `00 — Cloud Infrastructure Architecture Discovery & Target Design`
Status: **COMPLETE / ACCEPTED**.

Accepted outcome included the historical legacy baseline, provider backup, the then-created sensitive migration-preservation archive, sanitized `migration-reference/`, clean-rebuild decision and verified recovery paths. The temporary archive is now absent and was declared no longer required on 2026-09-19; it must not be recreated.

### Stage 1 — Base `edge` Platform

Historical stage label: `01 — Edge Clean Rebuild & Base Platform Deployment`
Status: **COMPLETE / ACCEPTED**.

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted composition includes Ubuntu substrate, SSH, journald policy, Docker/Compose, nginx, Certbot/TLS lifecycle, Xray, Hysteria2, public masking page, Authelia ingress/auth foundation, UFW, `maintctl`/`vpnctl`, extension-point contract and the Stage 1 recovery checkpoint.

### Stage 2 — Core Applications

Historical stage label: `02 — Edge Core Applications`
Status: **COMPLETE / ACCEPTED**.

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted production set:

- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark.

### Stage 02.5 — Remaining Functional Scope Reconciliation & Research

Historical stage label: `02.5 — Remaining Functional Scope Reconciliation & Research`
Status: **COMPLETE / ACCEPTED / RESEARCH-ONLY**.

Final acceptance record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`

Accepted results include:

- Hermes Agent selected;
- existing self-hosted Home NetBird selected/reused as the Cloud ↔ Home/PAI private fabric;
- PVE canonical knowledge foundation assigned to Home Infrastructure ownership rather than being redesigned inside Cloud Infrastructure;
- Cloud Stage 5 defined as `edge` replica/data integration against the accepted Home knowledge contract;
- the then-current blanket Apple-device/Obsidian exclusion was later superseded in part by the accepted 2026-09-19 Knowledge Fabric architecture: edge is the future external client-data endpoint, while exact client access remains separately unresolved;
- Backrest/Restic and Semaphore retained as accepted lifecycle directions;
- monitoring/heartbeats/alerts deferred to their dedicated late infrastructure stage;
- optional password/2FA, messaging/control and other user/workflow capabilities classified as deferred/optional rather than blockers;
- the empty conditional old Stage 6 slot removed and all later stages normalized before Stage 3 opens.

---

# Final post-Stage-02.5 deployment roadmap

## Stage 3 — Edge Cross-site Connectivity Foundation

**Status:** COMPLETE / ACCEPTED.

`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Final record: `STAGE_03_ACCEPTANCE_2026-09-18.md`.

Accepted outcome includes host-native NetBird on `edge`, private `edge -> Home/PAI` routing through CT300, Home `.lan` split DNS, provider-local public/default Internet preservation, no Home Internet exit assignment, no VM100/MikroTik mutation, no `edge.lan`, deferred LAN-wide clientless reverse routing, direct P2P recovery and final reboot persistence.

### Stage label

`03 — Edge Cross-site Connectivity Foundation`

### Scope

Deploy and accept the minimum-risk NetBird private fabric required before connectivity-dependent application stages.

Requirements:

- host-native NetBird peer on `edge`;
- dedicated Cloud Infrastructure service-peer grouping/policy;
- `edge -> Home/PAI` through existing `Home LAN 192.168.1.0/24` resource;
- no `0.0.0.0/0` Home Internet resource for `edge`;
- preserve direct provider Internet/default route and public-service behavior on `edge`;
- reuse/verify existing CT300 NetBird routing and Site-to-VPN masquerade; do not add duplicate NAT;
- consume existing Home `.lan` split DNS from `edge`;
- verify private reachability to `ai-node`, PVE and selected Home targets;
- verify NetBird management/signal/relay availability, reboot persistence and public-service non-regression;
- keep VM100 and MikroTik unchanged for the baseline Stage 3 implementation;
- do not create `edge.lan`; Home/PAI reaches Cloud services through the VPS public IP or accepted `escloud.us` / service-subdomain ingress;
- treat LAN-wide clientless Home/PAI -> `edge` overlay routing as a deferred on-demand capability requiring a concrete private-only workload before any gateway mutation.

Stage 3 establishes the Cloud-to-Home private transport needed by later workloads while preserving the existing Home gateway plane. It does not own vLLM service bind/provider configuration beyond reachability.

## Stage 4 — Edge Hermes Agent Runtime

### Stage label

04.3 — Edge Hermes Stage 4 Recovery, Completion & Final Acceptance

### Scope

Deploy Hermes after Stage 3 connectivity is accepted so the stage can verify the complete practical Hermes capability set, human WebUI access, direct cloud executors, Mattermost collaboration/control, machine integration and real local-vLLM use in one coherent acceptance.

Requirements:

- use the upstream-recommended Hermes installation path at deployment time; do not invent an independent version-selection policy;
- host-native runtime under core by default;
- persistent upstream-supported lifecycle/state;
- retain the full practical upstream-supported Hermes tool/runtime capability set rather than an intentionally reduced core path;
- deploy the Hermes Web Dashboard as the normal human UI;
- publish it at https://hermes.escloud.us through existing Xray/nginx/TLS using accepted Hermes-native self-hosted OIDC with Authelia as IdP;
- keep the Dashboard backend loopback-only by default and do not expose port 9119 directly;
- keep the n8n machine interface local/private rather than creating a public Hermes API;
- preserve the project-wide Authelia policy for service subdomains except explicitly accepted native-client services such as `mail.escloud.us` and the Stage 4 Mattermost endpoint `chat.escloud.us`;
- direct Hermes access to Codex and Antigravity without CloudCLI as proxy;
- stable machine interface for n8n invocation/result/status;
- infrastructure acceptance of n8n -> Hermes -> vLLM/Codex/AGY -> Hermes -> n8n;
- deploy a lightweight private Mattermost server only after its dedicated deep-research/design gate is accepted;
- integrate Mattermost with Hermes natively and with other compatible edge services through the simplest supported interfaces;
- verify real Hermes -> vLLM inference;
- no user-specific automation workflows beyond minimum integration acceptance probes.

### Authoritative Stage 4 execution substages

These substages define the complete Stage 4 scope. Execution is dependency-driven rather than numeric, but Stage 4 is not complete until every applicable substage below is accepted.

#### Stage 4A — Hermes core runtime and Full Setup capability completion

**Status: COMPLETE / ACCEPTED.** Core acceptance is preserved; the already documented gateway stop constraint is tracked in Stage 4G, not a reason to repeat Stage 4A.

Accepted:

- upstream host-native installation/provenance;
- AI-Node vLLM provider and real inference path;
- Qwen3.8 model-native reasoning/replay;
- terminal/tool calling;
- host/system toolchain normalization;
- Browser Use + managed Chromium;
- `STAGE4_HERMES_QWEN38_REASONING_NORMALIZATION=PASS`;
- `STAGE4_HERMES_SYSTEM_TOOLCHAIN_NORMALIZATION=PASS`.

Fresh 2026-09-18 capability probe additionally proved:

- Web Search/Extract through Exa free tier: functional PASS;
- Edge TTS: functional PASS;
- Vision through the accepted custom Qwen3.8/vLLM route: functional PASS;
- Computer Use: `NOT_APPLICABLE_HEADLESS_EDGE` because the production host intentionally has no X11/Wayland desktop session; `cua-driver 0.28.2` itself is present;
- Image Generation remains configured but is non-blocking for Stage 4 acceptance because meaningful acceptance is inherently visual/manual and would otherwise require a separate Hermes Codex OAuth session solely for this optional capability.

Core Qwen3.8/vLLM regression is **COMPLETE / ACCEPTED**:

- direct vLLM model-native reasoning: PASS;
- direct Qwen tool-call path: PASS;
- Hermes -> Qwen terminal tool execution: PASS;
- resumed same-session continuity/reasoning replay: PASS;
- no persistent `agent.reasoning_effort` override;
- `model.reasoning_echo=true`;
- `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS`;
- acceptance record: `STAGE_04A_CORE_QWEN_VLLM_REGRESSION_ACCEPTANCE_2026-09-18.md`.

The controlled gateway stop/restart exit-status defect remains a documented upstream lifecycle constraint to carry into Stage 4G; it does not block proceeding to Stage 4B.

#### Stage 4B — Direct Codex and Antigravity executor integration

**Status: COMPLETE / ACCEPTED.**

Final record:

`STAGE_04B_FINAL_ACCEPTANCE_2026-09-18.md`

Final acceptance:

`STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS`

Accepted outcome:

- `STAGE4B_EXECUTOR_READONLY_AUDIT=PASS`;
- Hermes remains on the accepted local custom Qwen3.8/vLLM main runtime;
- standalone Codex CLI `0.154.0` integration accepted through foreground non-PTY `codex exec`;
- standalone Antigravity CLI `1.2.5` integration accepted through foreground non-PTY `agy -p/--print` with structured JSON output;
- existing standalone CLI authentication/state reused;
- no CloudCLI executor proxy and no switch to Codex app-server;
- trusted full-access executor policy accepted under `core`, with critical high-impact mutations gated by Hermes/operator approval instructions rather than blanket sandboxing;
- background/process lifecycle reserved for genuinely long-running/parallel work;
- PTY reserved for genuinely interactive TUI sessions;
- main Hermes config unchanged;
- gateway remained active with `NRestarts=0`;
- temporary test artifacts removed;
- Hermes `stream-json` Tirith stdout contamination retained as a non-blocking Stage 4F machine-interface constraint.

#### Stage 4C — Hermes Web Dashboard, ingress and auth

**Status: COMPLETE / ACCEPTED.**

- `https://hermes.escloud.us` through Xray/nginx/shared TLS to `127.0.0.1:9119`;
- persistent `hermes-dashboard.service` under `core`, active/enabled;
- Hermes-native self-hosted OIDC with Authelia `4.39.27` as IdP;
- one interactive provider, authorization-code PKCE/S256, browser and native Desktop flows;
- no nginx `auth_request`, Basic/Nous fallback or public TCP/9119;
- existing Certbot webroot lineage expanded to include `hermes.escloud.us`;
- real browser callback, authenticated Chat/session traffic and WebSocket HTTP 101 accepted;
- `STAGE4C_HERMES_DASHBOARD_OIDC_ACCEPTANCE=PASS`;
- record: `STAGE_04C_FINAL_ACCEPTANCE_2026-09-18.md`.

#### Stage 4D — Mattermost deep research and deployment design

**Status: COMPLETE / ACCEPTED.**

- research: `STAGE_04_MATTERMOST_RESEARCH_BRIEF_2026-09-18.md`;
- acceptance: `STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`;
- `STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`.

Accepted target remains Mattermost Team Edition, official Docker Compose pattern, dedicated PostgreSQL, local `/srv` state, existing Xray/nginx/shared TLS, native Mattermost auth with no Authelia, TPNS enabled and Calls excluded.

#### Stage 4E — Private Mattermost deployment and native service integrations

**Status: COMPLETE / ACCEPTED.**

Accepted:

- Mattermost Team `11.11.0` + PostgreSQL `18-alpine`;
- private application/database topology and persistent local state;
- public `https://chat.escloud.us` through Xray -> host nginx -> shared TLS;
- native Mattermost authentication without Authelia;
- TPNS server configuration at `https://push-test.mattermost.com`;
- Calls disabled;
- Hermes bot provisioning/channel normalization/E2E accepted;
- native n8n↔Mattermost integration accepted using the official built-in n8n Mattermost node;
- n8n E2E used the existing single credential/bot against an isolated throwaway clone and left production at 0 workflows / 0 executions;
- `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`;
- prepackaged `mattermost-ai` / Agents `2.6.1` explicitly disabled and verified (`STAGE4E_MATTERMOST_AGENTS_NORMALIZATION=PASS`);
- operator-accepted official iOS Mattermost/mobile TPNS gate (`STAGE4E_MATTERMOST_MOBILE_TPNS=PASS`);
- bounded final Stage 4E non-regression (`STAGE4E_FINAL_NON_REGRESSION=PASS`);
- final Stage 4E acceptance (`STAGE4E_FINAL_ACCEPTANCE=PASS`);
- Mattermost↔Stalwart SMTP explicitly reviewed and not required / not enabled.

Final record: `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`.

Custom plugins, source patches, shim services, direct DB coupling, bespoke bridges, compatibility hacks and n8n-mediated substitutes for missing upstream integrations remain prohibited.

#### Stage 4F — Hermes private machine interface and n8n agent integration

**Status: COMPLETE / ACCEPTED.**

- upstream Hermes API Server selected after exact-source research;
- private Bearer-authenticated listener `172.19.0.1:8642` on the n8n Docker bridge;
- explicit Compose network `n8n_hermes` with stable Linux bridge `n8n-hermes`, subnet `172.19.0.0/16` and gateway `172.19.0.1`;
- narrow UFW allowance from `172.19.0.0/16` on `n8n-hermes`; no public listener or nginx route;
- n8n built-in HTTP Request v4.5 plus encrypted Bearer credential;
- published reusable workflow `Hermes Machine Invocation` supports `vllm`, `codex` and `antigravity` selectors;
- exact-value E2E PASS for remote vLLM, real Codex and real Antigravity;
- native HTTP JSON avoids Tirith `stream-json` stdout contamination;
- temporary acceptance workflows removed; production contains one Hermes workflow and two total credentials;
- `STAGE4F_PRIVATE_HERMES_MACHINE_INTERFACE=PASS`;
- post-acceptance network-identity hardening: `STAGE4F_STABLE_DOCKER_BRIDGE_HARDENING=PASS`;
- records: `STAGE_04F_PRIVATE_HERMES_MACHINE_INTERFACE_ACCEPTANCE_2026-09-18.md` and `STAGE_04F_NETWORK_IDENTITY_HARDENING_ACCEPTANCE_2026-09-19.md`.

#### Stage 4G — Server-side integrated acceptance

**Status: COMPLETE / ACCEPTED.**

Bounded integrated acceptance reused prior PASS evidence and verified the then-current boundaries: gateway/Dashboard persistence, vLLM, Codex, Antigravity `1.2.6`, Dashboard/OIDC/TLS, Mattermost, n8n, private API, listeners and configuration semantics. Current Antigravity runtime is `1.2.7` after a 2026-09-19 post-acceptance reconciliation; this does not rewrite the historical Stage 4G evidence.

A Dashboard-driven global model switch was detected as a real regression signal. The accepted Qwen3.8/custom-vLLM settings were restored with native Hermes commands, native-validated and re-proven through n8n E2E. Current config SHA256: `fe2f0fead4781ed28d0c4bf61720bdc52a6b31a41040a477afe6351b5df2f824`.

The known controlled SIGTERM exit-status-1 defect remains an accepted upstream constraint; restart recovery passes and no lifecycle masking was introduced.

`STAGE4G_SERVER_INTEGRATED_ACCEPTANCE=PASS`. Record: `STAGE_04G_SERVER_INTEGRATED_ACCEPTANCE_2026-09-18.md`.

#### Stage 4H — Final integration task: macOS Hermes Desktop

**Status: COMPLETE / ACCEPTED.**

- Remote Gateway target `https://hermes.escloud.us`;
- upstream native self-hosted OIDC/RFC8252 PKCE path;
- real native authorize/callback/token exchange;
- remote WebSocket HTTP 101 observed twice;
- authenticated remote Chat/session traffic and operator functional confirmation;
- no accidental local bundled backend and no public TCP/9119;
- `STAGE4H_MACOS_DESKTOP_REMOTE_GATEWAY=PASS`;
- record: `STAGE_04H_MACOS_DESKTOP_REMOTE_GATEWAY_ACCEPTANCE_2026-09-18.md`.

#### Stage 4I — Final Stage 4 acceptance and repository persistence

**Status: COMPLETE / ACCEPTED.**

- Stage 4A/B/C/D/E/F/G/H evidence reconciled;
- canonical current documents and latest applicable decision semantics normalized;
- historical audit/failure artifacts preserved without representing assistant harness defects as production failures;
- critical GitHub writes read back;
- `STAGE4_FINAL_ACCEPTANCE=PASS`;
- final record: `STAGE_04_FINAL_ACCEPTANCE_2026-09-18.md`.

Stage 5 is now eligible to begin under its own mandatory entry audit.

## Stage 5 — Knowledge Fabric Runtime Deployment

### Current status

**COMPLETE / ACCEPTED.**

- **05.1 — Cross-project Knowledge Reconciliation & Target Architecture:** COMPLETE / ACCEPTED.
- **05.2 — PVE Canonical Obsidian Runtime & WebUI:** COMPLETE / ACCEPTED.
- **05.3 — Edge Knowledge Replication & Data Integration:** COMPLETE / ACCEPTED.

Acceptance markers:

- `STAGE05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE=PASS`;
- `STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS`;
- `STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS`;
- `STAGE05_FINAL_ACCEPTANCE=PASS`.

Authoritative records:

- `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_2_FINAL_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

### Final accepted topology

- PVE = authoritative RW Knowledge/recovery node and Syncthing hub; vault `/srv/knowledge/obsidian` on the dedicated `pve/knowledge` filesystem.
- CT210 = single full server-side Obsidian runtime/WebUI for the PVE vault.
- ai-node = active RW PAI/application replica at `/srv/ai-data/knowledge/obsidian`.
- edge = active RW Cloud/agent replica at `/srv/knowledge/obsidian`.
- topology = PVE ↔ ai-node plus PVE ↔ edge; no direct edge ↔ ai-node peer.

### 05.3 final implementation

- edge paths: `/srv/knowledge core:core 0755`, `/srv/knowledge/obsidian core:core 2775`;
- Syncthing `2.1.5` under `core`, boot-persistent;
- edge initiates PVE connection to `tcp://192.168.1.3:22000`;
- edge Syncthing listener/API remain loopback-only; discovery/relay/NAT mechanisms are disabled;
- Hermes/Codex/Antigravity use `/srv/knowledge/obsidian` directly;
- n8n uses `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`;
- PVE → edge, edge → PVE and edge → PVE → ai-node propagation passed;
- outage/reconnect and conflict preservation passed;
- controlled edge reboot persistence passed;
- no public Syncthing and no edge Obsidian runtime/WebUI;
- synthetic test data was removed and cleanup propagated.

External client access through edge remains a future separately selected mechanism outside Stage 5.

Stage 5 completion advanced the workstream to Stage 6, which is now COMPLETE / ACCEPTED.

## Stage 6 — Edge Backrest & Recovery

### Stage label

`06 — Edge Backrest & Recovery`

**Status: COMPLETE / ACCEPTED.**

A usable isolated restore path was verified and accepted before Stage 7.

Accepted Stage 6 deployment contract:

`STAGE_06_6_DEPLOYMENT_CONTRACT_2026-09-21.md`

Current substage state:

- 6.1/6.2 expanded runtime and scope reconciliation: COMPLETE;
- dedicated edge Knowledge backup: DEPLOYED / ACCEPTED;
- 6.3/6.4/6.5 topology, consistency direction and retention policy: ACCEPTED;
- 6.6 deployment contract: ACCEPTED;
- 6.7 production general-plan deployment: COMPLETE / ACCEPTED (`STAGE06_7_FINAL_ACCEPTANCE=PASS`);
- 6.8 isolated restore/application usability: COMPLETE / ACCEPTED (`STAGE06_8_FINAL_ACCEPTANCE=PASS`);
- 6.9 final Stage 6 non-regression/persistence: COMPLETE / ACCEPTED (`STAGE06_9_FINAL_ACCEPTANCE=PASS`).

Accepted implementation contract:

- one edge general plan `edge-state`;
- broad persistent roots with targeted exclusions rather than enumerating every application directory;
- schedule `01/07/13/19`;
- local all-snapshots-within-`7d` retention grouped by `host,tags`;
- successful copy to CT208/D5 append-only rest-server before local retention;
- D5 retention owned by CT208: daily30, weekly8, monthly6, yearly0;
- self-recovering application-consistency staging for live transactional state;
- no recurring full/bare-metal edge Restic chain;
- one provider golden VPS snapshot only after final infrastructure acceptance;
- dedicated Knowledge remains independent at `04/10/16/22`, local rolling `14d`, no D5.

The same Stage 6 workstream also applies the accepted bounded ai-node backup corrections recorded in the deployment contract. These corrections do not redesign the existing ai-node D5 State/Full retention policies.

Stage 6.7 final acceptance record: `STAGE_06_7_FINAL_ACCEPTANCE_2026-09-21.md`. Accepted runtime includes production `edge-state` local+D5 backup flow and the bounded ai-node corrections with controlled `ai-node-ai-state` local-to-D5 verification.

Stage 6.8 final acceptance record: `STAGE_06_8_FINAL_ACCEPTANCE_2026-09-21.md`. Real D5 restores and application usability were verified for edge and ai-node without production overwrite.

Stage 6 final acceptance record: `STAGE_06_FINAL_ACCEPTANCE_2026-09-21.md`. Stage 6 is COMPLETE / ACCEPTED with `STAGE06_FINAL_ACCEPTANCE=PASS`.

## Stage 7 — Edge Maintenance & Update

**Status:** COMPLETE / ACCEPTED.

### Stage label

`07 — Edge Maintenance & Update`

Port and adapt the accepted Home Maintenance implementation from CT1000 rather than designing an independent maintenance framework. Preserve its proven architecture, Semaphore workflow, version/status model, fixed-target dispatch, per-component driver pattern, post-update refresh/acceptance model and dashboard wherever applicable. Replace only Home/PVE-specific inventory, VMID/PCT/QGA logic, collectors and update drivers with edge-specific equivalents.

Authoritative implementation principle:

- use the live CT1000 `/opt/maintenance-repo` implementation as the Stage 7 source baseline;
- do not copy Home credentials, PVE inventory or Home-specific target definitions;
- keep automatic real updates disabled by default;
- retain component-specific supported update paths and health checks rather than introducing a generic one-size-fits-all updater;
- do not create a second independent maintenance framework without a demonstrated incompatibility.

Stage decomposition:

- **Stage 7A — Home Maintenance Framework Port — COMPLETE / ACCEPTED:** Semaphore, Home-derived read-only framework/state cache and copied dashboard baseline are deployed and accepted. The dashboard → Semaphore → canonical GitHub refresh playbook → local collector/cache → dashboard E2E passed with no production update mutation.
- **Stage 7B — Edge Update Drivers & Recovery — COMPLETE / ACCEPTED:** the edge-specific individual drivers, Master Batch behavior, health/failure/recovery handling, generated action contract and controlled update acceptance are deployed. Every real update remains operator-initiated from `update.escloud.us`; canonical APT policy and masked systemd paths enforce the absence of unattended/scheduled package updates.
- **Stage 7C — Codex: adapt `update.escloud.us` — COMPLETE / ACCEPTED:** the Home-derived dashboard is adapted for the single edge node, four lifecycle groups, generated action contract, individual/selected/Master manual actions and same-origin Semaphore integration. Final integrated read-only acceptance passed.

`update.escloud.us` remains separate from `app.escloud.us`. It is the single Stage 7 operator origin: `/status/` is the custom maintenance dashboard and `/project/1/history` is the full Semaphore UI. The former `ops.escloud.us` candidate is fully retired from edge and its public DNS A record was confirmed absent during Stage 10 (`STAGE10_OPS_DNS_RETIREMENT_VERIFY=PASS`).

Acceptance planning: define each edge component's supported update path, health checks, failure reporting and rollback/recovery. Stage 6 precedes Stage 7 so a verified backup/restore capability exists before maintenance tooling is deployed and tested; this is a deployment/testing safety prerequisite, not a requirement to run Backrest before every production update. Add a per-update backup step only where a specific component/update path materially requires it. Verify one controlled update/recovery scenario after Stage 6.

Final Stage 7B checkpoint: the CT1000-derived 16-target Master Batch is deployed
as Semaphore template 18 and completed operator-triggered runtime acceptance.
Task 12 finished successfully with one PostgreSQL driver execution, 15 CURRENT
skips, a clean 16/16 post-scan, no pending reboot, and all final health gates
PASS. The host unattended-upgrade path is disabled by a canonical APT override
and masked/inactive systemd units. One atomic action artifact is generated on
every Refresh from the canonical unit, template-mapping and enablement inputs.
Inactive deployment duplicates and update residue were removed, followed by a
passing Refresh, contract suite and Master health gate.

Final Stage 7 acceptance: `STAGE07_FINAL_ACCEPTANCE=PASS`. The integrated
read-only closure verified manual-only execution, zero autonomous launch paths,
16/23 model integrity, normalized user CLI context, Stage 7C dashboard contract,
Task 12 Master evidence, public ingress and production non-regression. Hermes
remains one ordinary pending manual update because active lazy-dependency drift
is detected fail-closed.

## Stage 8 — Edge Monitoring, Heartbeats & Alerts

### Stage label

`08 — Edge Monitoring, Heartbeats & Alerts`

Research/finalize and deploy production monitoring against the substantially complete infrastructure, including as selected external availability, cross-site connectivity health, selected Home/PVE/`ai-node` heartbeats, knowledge-sync health, Backrest health, Semaphore/update state and alert delivery.

Avoid a heavyweight metrics/logging platform unless concrete requirements justify it.

**COMPLETE / ACCEPTED.** Final acceptance marker: `STAGE08_FINAL_ACCEPTANCE=PASS`.

The deployed implementation is one persistent host-native Python `edge-monitor.service` with 5s/20s/60s/300s collection cadences, two-failure confirmation for ordinary endpoint probes, atomic live state at `/run/edge-monitor/snapshot.json`, durable transition state under `/var/lib/edge-monitor/state.json`, structured Backrest freshness, Syncthing/Home/PAI health and direct transition/recovery-only Mattermost alerts. A controlled synthetic transition test proved failure confirmation, deduplication and recovery notification without stopping production services. No heavyweight monitoring stack or independent vantage point was added.

## Stage 9 — Edge Cloud Portal

### Stage label

`09 — Edge Cloud Portal`

**Status: COMPLETE / ACCEPTED.**

Final marker:

`STAGE09_FINAL_ACCEPTANCE=PASS`

Accepted runtime:

- dedicated `https://app.escloud.us` static portal;
- existing Xray -> nginx -> shared TLS ingress;
- existing Authelia `auth_request`;
- static root `/var/www/app.escloud.us`;
- same-origin read-only `/api/status` from Stage 8 `/run/edge-monitor/snapshot.json`;
- 5-second frontend polling with explicit LIVE / STALE (>30s) / UNAVAILABLE presentation;
- navigation to Hermes, n8n, CloudCLI, Mattermost, Mail and Maintenance;
- no backend service/container/database/second collector;
- no update mutation controls; Stage 7 execution remains on `update.escloud.us`.

Browser acceptance and controlled freshness fixtures passed. Stage 8 remained unchanged with NRestarts=0 and all final monitored domains OK. Zero failed systemd units.

Architecture record: `STAGE_09_ARCHITECTURE_ACCEPTANCE_2026-09-22.md`.

Final record: `STAGE_09_FINAL_ACCEPTANCE_2026-09-22.md`.

## Stage 10 — Edge Final Integrated Infrastructure Acceptance

### Stage label

`10 — Edge Final Integrated Infrastructure Acceptance`

**Status: COMPLETE / ACCEPTED.**

Final marker: `STAGE10_FINAL_ACCEPTANCE=PASS`.

The final bounded integrated acceptance reused prior destructive/recovery PASS evidence and performed only the fresh read-only checks required to reconcile the complete current runtime: system/user services, Docker workloads, listeners, ingress/TLS/auth, NetBird/Home/PAI connectivity, Knowledge integration, Backrest state, maintenance/manual-only controls, monitoring and the Stage 9 portal. `STAGE10_INTEGRATED_READONLY_AUDIT_V1` completed with zero fresh failures, no runtime mutations and no disruptive tests.

The known Stage 7 repository-source drift was closed by persisting the exact accepted runtime `maintenance/edge/scripts/manual-update`, including normalized `/home/core` execution context and Hermes lazy-dependency fail-closed verification. Current mutable version facts were reconciled without rewriting historical acceptance records.

Final record: `STAGE_10_FINAL_ACCEPTANCE_2026-09-22.md`.

Stage 10 closes acceptance of the currently deployed baseline. It remains a valid accepted checkpoint even if later Stage 11 work extends the infrastructure.

---

## Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion

### Stage label

`11 — Remaining Infrastructure Gap Reconciliation & Completion`

**Status: ACTIVE / ACCEPTED SCOPE.**

Purpose: perform one bounded reconciliation pass for infrastructure capabilities that were historically deployed, discussed, selected or expected before user workflows but were omitted, lost or incorrectly classified during the rebuild/repository bootstrap.

Stage 11 begins with research/reconciliation, not deployment.

Mandatory source order:
1. current runtime and actual configuration;
2. current canonical repository;
3. legacy baseline and `migration-reference/`;
4. Stage 0–10 acceptance/decision records;
5. available project conversation/history context;
6. current upstream documentation only where product/version/capability verification is required.

Stage 11 must classify each discovered capability as:
- `KEEP_CURRENT` — already present and sufficient;
- `HISTORICAL_ONLY` — intentionally superseded/removed;
- `MISSING_REQUIRED` — should exist before user workflows;
- `OPTIONAL_DEFER` — useful only with a concrete later workflow;
- `RESEARCH_REQUIRED` — current product/architecture choice unresolved.

Initial known reconciliation target: the legacy `cloud.escloud.us` file-access layer, where the historical baseline records Filestash over `/srv/cloud` but current canonical inventory incorrectly reduces the capability to an unresolved future service.

Do not redeploy legacy OpenCloud/Filestash or any other historical product merely because it existed. Re-evaluate whether the capability is still useful and choose the simplest current stable implementation that satisfies the accepted requirement.

After selection, deploy/accept only the capabilities classified `MISSING_REQUIRED`.

### Relationship to Stage 10

Stage 10 remains COMPLETE / ACCEPTED for the pre-Stage-11 clean production baseline.

If Stage 11 introduces material infrastructure changes, revisit Stage 10 afterward with a bounded integrated re-acceptance limited to the changed service/integration boundaries. Do not repeat unrelated Stage 3–10 destructive tests.

If Stage 11 makes no material deployment changes, no Stage 10 rerun is required.

---

## Post-infrastructure continuous workstream — Automation & User Workflows

This remains deliberately outside infrastructure completion. It begins only after Stage 11 and, where Stage 11 changed infrastructure, the required bounded Stage 10 re-acceptance.

Examples include n8n workflows, Hermes/agent workflows, Universal Capture Inbox, human approvals, mail-triggered automation, continuous vendor/document intake, bounded AI research, durable application-level store-and-forward/retry, messaging/bot commands and user-specific orchestration among n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

Apple-device/Obsidian synchronization is not part of this Cloud workstream; it belongs to Home Infrastructure as a separate user-integration project/branch.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **COMPLETE / ACCEPTED**.  
Stage 02.5: **COMPLETE / ACCEPTED**.  
Stage 3: **COMPLETE / ACCEPTED**.  
Stage 4: **COMPLETE / ACCEPTED**. `STAGE4_FINAL_ACCEPTANCE=PASS`.
Stage 5: **COMPLETE / ACCEPTED**. `STAGE05_FINAL_ACCEPTANCE=PASS`.
Stage 6: **COMPLETE / ACCEPTED**. `STAGE06_FINAL_ACCEPTANCE=PASS`.
Stage 7: **COMPLETE / ACCEPTED**. `STAGE07_FINAL_ACCEPTANCE=PASS`.  
Stage 8: **COMPLETE / ACCEPTED**. `STAGE08_FINAL_ACCEPTANCE=PASS`.
Stage 9: **COMPLETE / ACCEPTED**. `STAGE09_FINAL_ACCEPTANCE=PASS`.  
Stage 10: **COMPLETE / ACCEPTED**. `STAGE10_FINAL_ACCEPTANCE=PASS`.  
Stage 11: **ACTIVE / ACCEPTED SCOPE**.

Current accepted checkpoint on `main`:

`Stage 10 — Edge Final Integrated Infrastructure Acceptance — COMPLETE / ACCEPTED`

## Current infrastructure stage

Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion — is active. User workflows follow Stage 11 and any required bounded Stage 10 re-acceptance.


---

## Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion

**Status:** COMPLETE / ACCEPTED. `STAGE11_FINAL_ACCEPTANCE=PASS`.

Stage 11 reconciles forgotten/omitted infrastructure capabilities against the accepted Stage 10 baseline. Current remaining work is bounded stale-artifact cleanup and canonical reconciliation; substantial deployments are split into later dedicated tasks.

## Stage 12 — Nextcloud Cloud Drive & Private Workspace Access

**Status:** COMPLETE / ACCEPTED. `STAGE12_FINAL_ACCEPTANCE=PASS`.

Working branch: `stage-12-nextcloud-cloud-drive`.

Accepted result:

- `cloud.escloud.us`: Nextcloud personal cloud drive, accepted with native-client E2E;
- portable user-visible cloud files: `/srv/cloud`; Nextcloud-specific persistent state: `/srv/nextcloud`;
- direct workspace access: WebDAV, not SMB;
- WebDAV target is exactly `/home/core/projects/`;
- rclone `1.75.1` runs as persistent `core` user service `projects-webdav.service` on loopback `127.0.0.1:18081`;
- public workspace endpoint: `https://go.escloud.us/` through existing Xray -> nginx ingress;
- WebDAV authentication: HTTP Basic over HTTPS;
- Samba/SMB implementation was rejected and fully removed after topology testing showed that clientless Home LAN access would require unwanted Home routing/firewall changes or a proxy;
- no Home Infrastructure mutation was made;
- local and public WebDAV `PROPFIND/MKCOL/PUT/GET/MOVE/DELETE` acceptance passed;
- macOS Finder access and automatic connection were accepted;
- final server health: Xray/Hysteria/nginx/WebDAV active, zero failed systemd units.

Authoritative final record: `STAGE_12_FINAL_ACCEPTANCE_2026-09-23.md`.

## Future task — Backrest WebUI ingress

**Status:** PLANNED / DEFERRED.

Publish the already-running Backrest WebUI at `backup.escloud.us` through the accepted ingress/auth architecture. This is an ingress/presentation task only; no replacement backup product is selected.

## Future task — WenTian technical publishing

**Status:** DEFERRED UNTIL CONTENT READY.

`docs.escloud.us` is reserved for a curated WenTian technical documentation library modeled functionally on Lenovo Press, focused on selected Product Guides and Datasheets translated to English and Russian. Do not deploy a placeholder CMS/DMS/site before a useful translated corpus exists. Publishing implementation is selected and deployed when the content set is ready.


---

## Stage 07.2 — Native Update Ownership Reconciliation

**Status: COMPLETE / ACCEPTED.**

Stage 07.2 is a corrective substage of the already accepted Stage 7 baseline.

Accepted result:

- native-first hybrid update ownership;
- Codex and Hermes are native-owned monitor-only Maintenance rows;
- Ubuntu security updates use package-owned unattended-upgrades;
- ordinary/third-party APT remains manual;
- Maintenance target model `update_units_v4`: 18 manual targets + 2 monitor-only native targets;
- Stage 12 Rclone and Nextcloud app/PostgreSQL/Redis included in Maintenance;
- Bulwark stable tracking corrected without executing the pending update;
- Semaphore template mapping reconciled;
- all manual preflights, Master plan-only and native-owner non-regression passed.

Final marker: `STAGE07_2_MAINTENANCE_SEMAPHORE_MIGRATION=PASS`.

Authoritative record: `STAGE_07_2_NATIVE_UPDATE_OWNERSHIP_ACCEPTANCE_2026-09-23.md`.
