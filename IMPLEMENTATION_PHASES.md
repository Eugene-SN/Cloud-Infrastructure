# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stage 0–4 COMPLETE / ACCEPTED. Stage 5 is the next finite infrastructure stage.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. research only for genuinely unresolved mechanisms or concrete incompatibilities;
4. explicit stage-composition acceptance;
5. stage-scoped architecture/deployment contract and recovery path;
6. deployment;
7. verification and explicit acceptance;
8. persistence/read-back in GitHub;
9. branch transition only after complete stage acceptance.

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

Branch: `00 — Cloud Infrastructure Architecture Discovery & Target Design`  
Status: **COMPLETE / ACCEPTED**.

Accepted outcome includes the historical legacy baseline, provider backup, sensitive migration-preservation archive, sanitized `migration-reference/`, clean-rebuild decision and verified recovery paths.

### Stage 1 — Base `edge` Platform

Branch: `01 — Edge Clean Rebuild & Base Platform Deployment`  
Status: **COMPLETE / ACCEPTED**.

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted composition includes Ubuntu substrate, SSH, journald policy, Docker/Compose, nginx, Certbot/TLS lifecycle, Xray, Hysteria2, public masking page, Authelia ingress/auth foundation, UFW, `maintctl`/`vpnctl`, extension-point contract and the Stage 1 recovery checkpoint.

### Stage 2 — Core Applications

Branch: `02 — Edge Core Applications`  
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

Branch: `02.5 — Remaining Functional Scope Reconciliation & Research`  
Status: **COMPLETE / ACCEPTED / RESEARCH-ONLY**.

Final acceptance record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`

Accepted results include:

- Hermes Agent selected;
- existing self-hosted Home NetBird selected/reused as the Cloud ↔ Home/PAI private fabric;
- PVE canonical knowledge foundation assigned to Home Infrastructure ownership rather than being redesigned inside Cloud Infrastructure;
- Cloud Stage 5 defined as `edge` replica/data integration against the accepted Home knowledge contract;
- Apple-device/Obsidian integration removed completely from the Cloud research/deployment matrix and deferred to a separate late Home Infrastructure user-integration stage;
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

### Work branch

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

### Work branch

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
- narrow UFW allowance from `172.19.0.0/16`; no public listener or nginx route;
- n8n built-in HTTP Request v4.5 plus encrypted Bearer credential;
- published reusable workflow `Hermes Machine Invocation` supports `vllm`, `codex` and `antigravity` selectors;
- exact-value E2E PASS for remote vLLM, real Codex and real Antigravity;
- native HTTP JSON avoids Tirith `stream-json` stdout contamination;
- temporary acceptance workflows removed; production contains one Hermes workflow and two total credentials;
- `STAGE4F_PRIVATE_HERMES_MACHINE_INTERFACE=PASS`;
- record: `STAGE_04F_PRIVATE_HERMES_MACHINE_INTERFACE_ACCEPTANCE_2026-09-18.md`.

#### Stage 4G — Server-side integrated acceptance

**Status: COMPLETE / ACCEPTED.**

Bounded integrated acceptance reused prior PASS evidence and verified current boundaries: gateway/Dashboard persistence, vLLM, Codex, current Antigravity `1.2.6`, Dashboard/OIDC/TLS, Mattermost, n8n, private API, listeners and configuration semantics.

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

## Stage 5 — Edge Knowledge Replication & Data Integration

### Work branch

`05 — Edge Knowledge Replication & Data Integration`

### Dependency boundary

Home Infrastructure owns the PVE canonical knowledge foundation. Personal Agents Infrastructure owns the `ai-node` local active replica and local AI producers/consumers. Cloud Infrastructure owns only the `edge` replica/data integration.

Home Infrastructure records `KNOWLEDGE_FABRIC_CANONICAL_CUTOVER=PASS` on 2026-09-18: PVE `/srv/knowledge/obsidian` is canonical and `ai-node:/srv/ai-data/knowledge/obsidian` is an active RW Syncthing replica. This is accepted cross-project evidence; a fresh Home/PAI runtime audit remains mandatory before Cloud Stage 5 deployment.

### Accepted dependency evidence reconciled on 2026-09-19

[Home Infrastructure CURRENT_STATE.md](https://github.com/Eugene-SN/Home-Infrastructure/blob/main/CURRENT_STATE.md) records:
- canonical PVE vault `/srv/knowledge/obsidian`, with `KNOWLEDGE_FABRIC_CANONICAL_CUTOVER=PASS`;
- Syncthing `2.1.5` on PVE and ai-node, direct static TCP/22000, sendreceive folder `knowledge-obsidian`;
- localhost-only management APIs, discovery/relays/NAT traversal and automatic self-upgrades disabled;
- bidirectional physical-content verification and approximately two-second Markdown propagation after watcher tuning;
- CT220 canonical read-only mount switched to PVE; obsolete canonical CIFS dependency removed;
- CT208 full-vault backup/restore accepted and PVE production backup policy enabled.

PAI records an independent local Knowledge backup with `KNOWLEDGE_AI_NODE_DEDICATED_LOCAL_BACKUP=PASS`. These existing acceptances remove the documentary uncertainty about Home cutover; they do not substitute for fresh health, permissions, conflict/outage and capacity checks before adding edge.

Cloud Stage 5 deployment remains unaccepted. Reuse Syncthing by default; do not reopen product selection without a demonstrated incompatibility.

### Mandatory Stage 5 entry audit

Before any synchronization/data mutation, Stage 5 must perform an **expanded read-only cross-project audit** and establish the fresh accepted Home/PAI state.

At minimum audit:

**Home/PVE**

- whether PVE canonical migration is explicitly accepted;
- exact canonical path/filesystem/backing SSD or LV;
- capacity/filesystem health;
- ownership/permissions and mount/export semantics;
- selected sync mechanism, version, runtime placement and peer model;
- conflict/versioning semantics;
- PVE ↔ `ai-node` sync health and accepted outage/reconnect behavior;
- relevant CT206 file-access integration if retained;
- CT208/Backrest knowledge protection and verified restore state;
- PVE/CT300/NetBird path/DNS dependencies needed by Cloud.

**PAI/`ai-node`**

- exact local replica path;
- sync peer/service configuration and health;
- local ownership/permissions expected by n8n/OpenClaw/vLLM/OCR/RAG;
- producer-side canonical/drafts/exchange conventions;
- proof that `ai-node` is an active replica rather than canonical after Home cutover.

**Cloud/`edge`**

- Stage 3 NetBird non-regression;
- Stage 4 Hermes/vLLM non-regression;
- persistent local storage/path for the Cloud replica;
- actual RO/RW consumers on `edge`;
- whether a full replica or bounded subset is justified.

If the fresh entry audit cannot confirm the accepted PVE canonical runtime and healthy PVE ↔ `ai-node` synchronization, **stop before mutation and reconcile the dependency**. Do not invent a parallel Cloud canonical/sync architecture.

### Implementation principle

Stage 5 is an integration stage, not a second knowledge-platform design project:

1. audit the fresh Home/PAI contract;
2. reuse the Home-accepted server-side synchronization mechanism by default;
3. add `edge` as an active RW replica/producer when compatible;
4. expose only the minimum required local paths to n8n/Hermes/tools;
5. verify bidirectional propagation, controlled conflict behavior, peer outage/reconciliation and reboot persistence;
6. verify Home/PAI/Cloud non-regression;
7. do not add another primary synchronization engine for the same knowledge tree without a concrete incompatibility and explicit superseding decision.

MacBook/iPhone/iPad Obsidian synchronization is **out of Cloud scope** and must not influence Stage 5 product selection.

## Stage 6 — Edge Backrest & Recovery

### Work branch

`06 — Edge Backrest & Recovery`

Deploy/configure Backrest + Restic against the substantially complete server. Define backup scope/exclusions, repository/off-site topology, retention/schedules, recovery procedures and verified restore acceptance.

A usable restore path is mandatory before Stage 7 update testing.

Planning checklist:
- inventory persistent state and restore ordering for mail, n8n credentials/workflows, Mattermost/PostgreSQL, Hermes, auth/TLS and host configuration;
- decide application-consistent capture, exclusions, off-host recovery topology and protected key recovery;
- retain the accepted independent edge Knowledge backup role: whole vault, no D5 tier-copy for that dedicated chain; planned windows 04:00/10:00/16:00/22:00 local, unchanged-snapshot skipping and monthly check/prune;
- reconcile the optional reduced non-canonical history (approximately three months) before activation; do not copy PVE's canonical one-year policy automatically;
- verify actual restore into an isolated destination, including application usability and access to required recovery keys.

Cloud-wide off-site disaster recovery is distinct from the dedicated local Knowledge chain. Same-host checkpoints alone do not close this stage.

## Stage 7 — Edge Maintenance & Update

### Work branch

`07 — Edge Maintenance & Update`

Deploy Semaphore and the maintenance/update workflow after Backrest acceptance. Audit/adapt the existing PVE/Home updater; do not copy PVE-specific implementation blindly.

Dedicated Codex substage:

**Stage 7C — Codex: build `update.escloud.us`**

This begins only after the real Semaphore/update backend, status model and control contract are known. `update.escloud.us` remains separate from `app.escloud.us`.

Acceptance planning: define each component's supported update path, pre-update backup gate, health checks, failure reporting and rollback/recovery. Verify one controlled update/recovery scenario after Stage 6, then build the UI against that tested contract.

## Stage 8 — Edge Monitoring, Heartbeats & Alerts

### Work branch

`08 — Edge Monitoring, Heartbeats & Alerts`

Research/finalize and deploy production monitoring against the substantially complete infrastructure, including as selected external availability, cross-site connectivity health, selected Home/PVE/`ai-node` heartbeats, knowledge-sync health, Backrest health, Semaphore/update state and alert delivery.

Avoid a heavyweight metrics/logging platform unless concrete requirements justify it.

Acceptance planning: select the monitoring implementation only after requirements are reconciled; distinguish Internet/service outages, loss of Home connectivity and unavailable inference. Verify meaningful failure and recovery notifications, backup freshness, synchronization health and maintenance suppression without repetitive unchanged-state alerts.

## Stage 9 — Edge Cloud Portal

### Work branch

`09 — Edge Cloud Portal`

Build `app.escloud.us` only after Stage 8 monitoring/status sources and the final service inventory are accepted.

Dedicated Codex substage:

**Stage 9C — Codex: build `app.escloud.us`**

The portal is navigation plus concise infrastructure/status presentation. It does not absorb detailed maintenance/update controls from `update.escloud.us`.

Acceptance planning: verify authenticated access, actual service links, current status and explicit stale/unavailable-data presentation using the accepted Stage 8 sources.

## Stage 10 — Edge Final Integrated Infrastructure Acceptance

### Work branch

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

Current branch:

`04.3 — Edge Hermes Stage 4 Recovery, Completion & Final Acceptance`

## Next finite infrastructure stage

Stage 4 is fully accepted on Git branch `04.3-edge-hermes-recovery-completion`. Stage 5 may now begin only through its mandatory expanded read-only entry audit.
