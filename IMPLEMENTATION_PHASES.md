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

These substages define the complete Stage 4 scope. Execution is dependency-driven rather than numeric, but Stage 4 is not complete until every applicable substage below is accepted.

#### Stage 4A — Hermes core runtime and Full Setup capability completion

**Status: IN PROGRESS.**

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

Remaining Stage 4A core gate:

- perform a fresh core-agent regression of the accepted Qwen3.8/vLLM mode: model/server-native reasoning, no persistent Hermes reasoning-effort override, `reasoning_echo=true`, terminal tool call, session resume/reasoning replay and local vLLM reachability;
- resolve or explicitly characterize the controlled gateway stop/restart exit-status defect before final lifecycle acceptance.

#### Stage 4B — Direct Codex and Antigravity executor integration

**Status: NEXT / PENDING ACCEPTANCE.**

- keep Hermes' main/default runtime on the accepted local custom Qwen3.8/vLLM route;
- verify the bundled Codex skill and standalone Codex CLI under the real `core` runtime;
- use the official optional `antigravity-cli` skill from the installed Hermes upstream tree; install it into the live Hermes skill set only if the read-only inventory proves it is not already installed;
- prove harmless Hermes -> terminal -> `codex exec` delegation in a temporary git workspace;
- prove harmless Hermes -> terminal -> `agy --print` delegation in a temporary workspace;
- verify that the executor calls are visible in Hermes tool events/output and that each executor produces its expected test artifact/result;
- reuse existing standalone Codex and Antigravity authentication; do not route through CloudCLI and do not switch the main Hermes runtime to Codex app-server for this acceptance.

#### Stage 4C — Hermes Web Dashboard, ingress and auth

**Status: PENDING.**

- persistent Dashboard backend;
- loopback-only backend unless a concrete incompatibility requires otherwise;
- `https://hermes.escloud.us` through Xray/nginx/shared TLS/Authelia;
- WebSocket/session persistence;
- reconcile the actual Hermes remote-dashboard credential path with Authelia without preselecting Nous OAuth;
- keep the n8n machine API private/local.

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

**Status: PENDING.**

- enable the minimum supported Hermes machine interface required by n8n;
- keep it local/private and authenticated;
- prove n8n invoke/result/status;
- prove `n8n -> Hermes -> Qwen3.8/Codex/AGY -> Hermes -> n8n`;
- no user-specific workflow logic beyond acceptance probes.

#### Stage 4G — Server-side integrated acceptance

**Status: PENDING.**

Verify together:

- Hermes/vLLM/reasoning/tools;
- Codex/Antigravity;
- Dashboard + authenticated ingress;
- Mattermost + Hermes + n8n;
- private n8n machine interface;
- clean gateway lifecycle;
- NetBird/private PAI path;
- listeners/UFW/TLS/non-regression;
- persistence and one controlled reboot only if justified by the final lifecycle changes.

Stalwart remains an independent accepted mail service; Mattermost SMTP is not part of the target integration.

#### Stage 4H — Final integration task: macOS Hermes Desktop

**Status: PENDING / LAST INTEGRATION TASK.**

1. use supported Hermes Desktop on macOS;
2. test Remote Gateway against `https://hermes.escloud.us`;
3. test the self-hosted session credential first;
4. verify readiness, live chat/WebSocket and reconnect after app restart;
5. use the minimum next supported credential/connection mode only if the simple Remote Gateway path proves incompatible.

#### Stage 4I — Final Stage 4 acceptance and repository persistence

**Status: PENDING.**

- final integrated acceptance record;
- reconcile/read back `CURRENT_STATE.md`, `INVENTORY.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PHASES.md`, `OPERATING_RULES.md`, `AGENTS.md` and applicable decisions;
- mark Stage 4 COMPLETE / ACCEPTED only after the whole Stage 4 contract passes;
- only then open Stage 5.

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
