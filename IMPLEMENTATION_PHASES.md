# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stage 0–3 COMPLETE / ACCEPTED. Stage 4 is IN PROGRESS.

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

04 — Edge Hermes Agent Runtime

### Scope

Deploy Hermes after Stage 3 connectivity is accepted so the stage can verify the complete practical Hermes capability set, human WebUI access, direct cloud executors, Mattermost collaboration/control, machine integration and real local-vLLM use in one coherent acceptance.

Requirements:

- use the upstream-recommended Hermes installation path at deployment time; do not invent an independent version-selection policy;
- host-native runtime under core by default;
- persistent upstream-supported lifecycle/state;
- retain the full practical upstream-supported Hermes tool/runtime capability set rather than an intentionally reduced core path;
- deploy the Hermes Web Dashboard as the normal human UI;
- publish it at https://hermes.escloud.us through existing Xray/nginx/TLS/Authelia;
- keep the Dashboard backend loopback-only by default and do not expose port 9119 directly;
- keep the n8n machine interface local/private rather than creating a public Hermes API;
- preserve the project-wide Authelia policy for service subdomains except explicitly accepted native-client services such as `mail.escloud.us` and the Stage 4 Mattermost endpoint `chat.escloud.us`;
- direct Hermes access to Codex and Antigravity without CloudCLI as proxy;
- stable machine interface for n8n invocation/result/status;
- infrastructure acceptance of n8n -> Hermes -> Codex/AGY -> Hermes -> n8n;
- deploy a lightweight private Mattermost server only after its dedicated deep-research/design gate is accepted;
- integrate Mattermost with Hermes natively and with other compatible edge services through the simplest supported interfaces;
- verify real Hermes -> vLLM inference;
- no user-specific automation workflows beyond minimum integration acceptance probes.

### Authoritative Stage 4 execution substages

These substages are the canonical sequence. A short list of immediate next tasks must not be treated as the full remaining Stage 4 scope.

#### Stage 4A — Hermes core runtime and Full Setup capability completion

- upstream installation/provenance;
- AI-Node vLLM provider;
- Qwen3.8 model-native reasoning/replay;
- terminal/tool calling;
- full practical local toolchain;
- Browser Use/managed Chromium;
- real functional verification/normalization of remaining Full Setup surfaces: CUA, Vision, TTS, Web Search/Extract and Image Generation.

Accepted so far:
- STAGE4_HERMES_QWEN38_REASONING_NORMALIZATION=PASS
- STAGE4_HERMES_SYSTEM_TOOLCHAIN_NORMALIZATION=PASS

#### Stage 4B — Direct Codex and Antigravity executor integration

- verify bundled Codex skill and standalone Codex CLI under real core runtime;
- establish the correct Antigravity skill/integration path if no bundled skill exists;
- prove harmless Hermes -> Codex CLI and Hermes -> Antigravity CLI delegation;
- do not route through CloudCLI.

#### Stage 4C — Hermes Web Dashboard, ingress and auth

- persistent Dashboard backend;
- loopback-only backend unless a concrete incompatibility requires otherwise;
- https://hermes.escloud.us through Xray/nginx/shared TLS/Authelia;
- WebSocket and session persistence;
- reconcile Hermes-native remote-dashboard auth with Authelia without preselecting Nous OAuth;
- keep n8n machine API private/local.

#### Stage 4D — Mattermost deep research and deployment design

**Status: COMPLETE / ACCEPTED.**

Research record: `STAGE_04_MATTERMOST_RESEARCH_BRIEF_2026-09-18.md`  
Acceptance record: `STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

Accepted target:

- Mattermost Team Edition;
- current official Mattermost Docker Compose pattern;
- separate Mattermost application and dedicated PostgreSQL containers;
- local persistent `/srv` state;
- reuse existing Xray -> host nginx -> shared TLS;
- public human URL `https://chat.escloud.us`;
- no Authelia in front of Mattermost; use Mattermost-native client authentication;
- Mattermost/PostgreSQL backends remain private;
- enable free TPNS for official mobile clients;
- Mattermost Calls is excluded from current Stage 4;
- no Preview all-in-one image, bundled nginx, Kubernetes, HA, external search/object storage or custom push stack without a later concrete requirement;
- exact service-to-Mattermost integration mechanisms remain intentionally unresolved until Stage 4E, where all current native/upstream-supported options are compared and the best supported path is selected.

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`

#### Stage 4E — Private Mattermost deployment and native service integrations

After accepted Stage 4D design:

- deploy the current stable Mattermost Team Edition using the current official Docker Compose pattern with a dedicated PostgreSQL container;
- keep application/database backends private and persist state under the accepted local `/srv` layout;
- publish `https://chat.escloud.us` through existing Xray -> host nginx -> shared TLS **without Authelia**;
- enable and verify TPNS with official mobile clients;
- leave Mattermost Calls disabled and do not open Calls-specific ports;
- audit every deployed/selected Cloud service for a **developer-provided/native Mattermost integration or explicitly supported standard protocol integration**;
- where such an integration exists, select it, document it and verify it;
- where it does not exist, leave that service **unintegrated with Mattermost in the current project** and record the possibility only as a future out-of-project task;
- do not use custom plugins, source patches, shim services, direct DB coupling, bespoke bridges, compatibility hacks or an n8n-mediated bridge as a substitute for missing upstream integration;
- fixed native integrations already confirmed by research:
  - Hermes ↔ Mattermost: Hermes built-in Mattermost gateway adapter (REST API v4 + WebSocket);
  - n8n → Mattermost: n8n official built-in Mattermost integration/node for its supported actions;
  - Mattermost → Stalwart: Mattermost standard SMTP integration using Stalwart as the SMTP service;
- additional directions (including Mattermost → n8n event/command flows) are enabled only if the actually deployed versions expose an upstream-supported counterpart for that direction;
- Codex/Antigravity remain behind Hermes; do not create direct Mattermost integrations for them unless their upstream later provides a native integration and a separate future task accepts it;
- keep CloudCLI as manual workspace;
- later monitoring/maintenance/backup services are integrated with Mattermost only if their own upstream provides a native/supported Mattermost path at the time their stage is implemented;
- verify native web/desktop/mobile client operation, push delivery, resource delta, persistence and non-regression.

#### Stage 4F — Hermes private machine interface and n8n agent integration

- enable minimum supported Hermes machine interface required by n8n;
- keep it local/private and authenticated;
- prove n8n invoke/result/status;
- prove n8n -> Hermes -> Qwen3.8/Codex/AGY -> Hermes -> n8n;
- no user-specific workflow logic beyond acceptance probes.

#### Stage 4G — Server-side integrated acceptance

Verify together:
- Hermes/vLLM/reasoning/tools;
- Codex/Antigravity;
- Dashboard + authenticated ingress;
- Mattermost + Hermes + n8n + Stalwart;
- private n8n machine interface;
- gateway lifecycle;
- NetBird/private PAI path;
- listeners/UFW/TLS/non-regression;
- persistence and, if justified, one controlled reboot.

#### Stage 4H — Final integration task: macOS Hermes Desktop

After all server-side components are accepted:
1. use supported Hermes Desktop on macOS;
2. test Remote Gateway first;
3. use intended remote URL https://hermes.escloud.us;
4. test self-hosted Session token first;
5. verify readiness, live chat/WebSocket and reconnect after app restart;
6. if incompatible, test minimum next supported username/password or OAuth mode without assuming Nous OAuth; alternative connection mode only after Remote Gateway itself is proven incompatible.

This remains the last Stage 4 integration task.

#### Stage 4I — Final Stage 4 acceptance and repository persistence

- final integrated acceptance record;
- update/read-back CURRENT_STATE, INVENTORY, ARCHITECTURE, IMPLEMENTATION_PHASES and applicable decisions;
- only then mark Stage 4 COMPLETE / ACCEPTED and open Stage 5.

## Stage 5 — Edge Knowledge Replication & Data Integration

### Work branch

`05 — Edge Knowledge Replication & Data Integration`

### Dependency boundary

Home Infrastructure owns the PVE canonical knowledge foundation. Personal Agents Infrastructure owns the `ai-node` local active replica and local AI producers/consumers. Cloud Infrastructure owns only the `edge` replica/data integration.

The previous permanent assumption that `ai-node:/srv/ai-data/knowledge/obsidian` must remain canonical is superseded for future architecture. Until Home Infrastructure explicitly accepts its migration, the existing `ai-node` vault remains the factual current runtime source.

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

If Home PVE canonical migration is not accepted at Stage 5 entry, **stop before mutation and reconcile the dependency**. Do not invent a parallel Cloud canonical/sync architecture.

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

## Stage 7 — Edge Maintenance & Update

### Work branch

`07 — Edge Maintenance & Update`

Deploy Semaphore and the maintenance/update workflow after Backrest acceptance. Audit/adapt the existing PVE/Home updater; do not copy PVE-specific implementation blindly.

Dedicated Codex substage:

**Stage 7C — Codex: build `update.escloud.us`**

This begins only after the real Semaphore/update backend, status model and control contract are known. `update.escloud.us` remains separate from `app.escloud.us`.

## Stage 8 — Edge Monitoring, Heartbeats & Alerts

### Work branch

`08 — Edge Monitoring, Heartbeats & Alerts`

Research/finalize and deploy production monitoring against the substantially complete infrastructure, including as selected external availability, cross-site connectivity health, selected Home/PVE/`ai-node` heartbeats, knowledge-sync health, Backrest health, Semaphore/update state and alert delivery.

Avoid a heavyweight metrics/logging platform unless concrete requirements justify it.

## Stage 9 — Edge Cloud Portal

### Work branch

`09 — Edge Cloud Portal`

Build `app.escloud.us` only after Stage 8 monitoring/status sources and the final service inventory are accepted.

Dedicated Codex substage:

**Stage 9C — Codex: build `app.escloud.us`**

The portal is navigation plus concise infrastructure/status presentation. It does not absorb detailed maintenance/update controls from `update.escloud.us`.

## Stage 10 — Edge Final Integrated Infrastructure Acceptance

### Work branch

`10 — Edge Final Integrated Infrastructure Acceptance`

Perform final server-wide acceptance only after all selected infrastructure services, cross-site connectivity/data integration, Backrest restore, Semaphore/update, monitoring/alerts, `app.escloud.us` and final cleanup are accepted.

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
Stage 4: **IN PROGRESS / NOT YET ACCEPTED**.

Current branch:

`04 — Edge Hermes Agent Runtime`
