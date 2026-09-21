# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stages 0–6 COMPLETE / ACCEPTED. Stage 7 is IN PROGRESS; Stage 7A is COMPLETE / ACCEPTED and Stage 7B is IN PROGRESS.

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

**Status:** IN PROGRESS.

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
- **Stage 7B — Edge Update Drivers & Recovery — IN PROGRESS:** replace the read-only action surface with accepted edge-specific update drivers, implement individual manual updates, Master Batch behavior, health/failure/recovery handling and controlled update/recovery acceptance. Every real update, including acceptance-test execution, must be started manually by the operator from `update.escloud.us`; no timers, cron, systemd update services, background update daemons, unattended/scheduled update jobs or other autonomous launch path are permitted.
- **Stage 7C — Codex: adapt `update.escloud.us`:** begin from the copied Home Maintenance dashboard implementation and refine it for Cloud/edge targets and presentation. This is an adaptation/refinement substage, not a greenfield frontend build.

`update.escloud.us` remains separate from `app.escloud.us`.

Acceptance planning: define each edge component's supported update path, health checks, failure reporting and rollback/recovery. Stage 6 precedes Stage 7 so a verified backup/restore capability exists before maintenance tooling is deployed and tested; this is a deployment/testing safety prerequisite, not a requirement to run Backrest before every production update. Add a per-update backup step only where a specific component/update path materially requires it. Verify one controlled update/recovery scenario after Stage 6.

## Stage 8 — Edge Monitoring, Heartbeats & Alerts

### Stage label

`08 — Edge Monitoring, Heartbeats & Alerts`

Research/finalize and deploy production monitoring against the substantially complete infrastructure, including as selected external availability, cross-site connectivity health, selected Home/PVE/`ai-node` heartbeats, knowledge-sync health, Backrest health, Semaphore/update state and alert delivery.

Avoid a heavyweight metrics/logging platform unless concrete requirements justify it.

Acceptance planning: select the monitoring implementation only after requirements are reconciled; distinguish Internet/service outages, loss of Home connectivity and unavailable inference. Verify meaningful failure and recovery notifications, backup freshness, synchronization health and maintenance suppression without repetitive unchanged-state alerts.

## Stage 9 — Edge Cloud Portal

### Stage label

`09 — Edge Cloud Portal`

Build `app.escloud.us` only after Stage 8 monitoring/status sources and the final service inventory are accepted.

Dedicated Codex substage:

**Stage 9C — Codex: build `app.escloud.us`**

The portal is navigation plus concise infrastructure/status presentation. It does not absorb detailed maintenance/update controls from `update.escloud.us`.

Acceptance planning: verify authenticated access, actual service links, current status and explicit stale/unavailable-data presentation using the accepted Stage 8 sources.

## Stage 10 — Edge Final Integrated Infrastructure Acceptance

### Stage label

`10 — Edge Final Integrated Infrastructure Acceptance`

Perform final server-wide acceptance only after all selected infrastructure services, cross-site connectivity/data integration, Backrest restore, Semaphore/update, monitoring/alerts, `app.escloud.us` and final cleanup are accepted.

Acceptance planning: reconcile runtime inventory with GitHub; verify access, ingress/TLS, service persistence, cross-site/data integration, recovery, update status, alerts and portal behavior. Record known accepted constraints separately from failures and remove only confirmed temporary artifacts. Any disruptive recovery/reboot scenario belongs to separately authorized implementation/acceptance work, not the current read-only audit.

Stage 10 closes the finite Cloud Infrastructure build.

---

## Post-infrastructure continuous workstream — Automation & User Workflows

This is deliberately not an infrastructure-completion stage. It begins only after Stage 10 and evolves continuously.

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
Stage 7: **IN PROGRESS**. Stage 7A is COMPLETE / ACCEPTED; Stage 7B is IN PROGRESS.

Current accepted checkpoint on `main`:

`Stage 7A — Home Maintenance Framework Port — COMPLETE / ACCEPTED`

## Current finite infrastructure stage

Stage 7 — Edge Maintenance & Update — is in progress. Continue with Stage 7B under the accepted manual-execution boundary; every real update must be initiated by the operator from `update.escloud.us`.
