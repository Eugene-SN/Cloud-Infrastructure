# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stage 0–3 COMPLETE / ACCEPTED. Stage 4 is the next production stage.

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

`04 — Edge Hermes Agent Runtime`

### Scope

Deploy Hermes after Stage 3 connectivity is accepted so the stage can verify human WebUI access, cloud executors, machine integration and real local-vLLM use in one coherent acceptance.

Requirements:

- use the upstream-recommended Hermes installation path as published by Nous Research at deployment time; do not invent an independent version-selection policy;
- host-native runtime under `core` by default;
- persistent upstream-supported lifecycle/state;
- deploy the Hermes Web Dashboard as the normal human UI;
- publish the Dashboard at `https://hermes.escloud.us` through the existing Xray/nginx/TLS/Authelia service-ingress architecture;
- keep the Hermes Dashboard backend loopback-only by default (upstream default `127.0.0.1:9119`); do not expose port 9119 directly to the Internet;
- do not create a separate direct public Hermes API/backend listener merely for n8n;
- preserve the project-wide authentication rule: service subdomains are protected by Authelia; only the root landing page `escloud.us` remains unauthenticated;
- do not preselect Nous OAuth. Current Hermes Desktop supports self-hosted Remote Gateway credentials by session token as well as gated OAuth/username-password flows; test session token first and only add a Hermes-native gated provider if the actual installed build/reverse-proxy behavior requires it;
- direct Hermes access to Codex and Antigravity without CloudCLI as a proxy;
- stable machine interface for n8n invocation/result/status;
- minimal infrastructure acceptance of `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- inspect current `ai-node` vLLM bind/exposure and make only the minimum private-fabric change required;
- verify real `Hermes -> vLLM` inference;
- no user-specific automation/workflows in Stage 4.

### Final Stage 4 substage — macOS Hermes Desktop integration

After the server-side Hermes runtime, Web Dashboard, executors, n8n machine interface and vLLM path are accepted:

1. install/use the supported Hermes Desktop application on macOS;
2. test the simplest supported **Remote Gateway** mode first;
3. configure **Settings -> Gateways -> Remote gateway** with the remote Dashboard backend URL, intended to be `https://hermes.escloud.us`;
4. test the self-hosted **Session token** Remote Gateway credential first; verify backend readiness, real chat/WebSocket operation, and reconnect after application restart;
5. treat the remote backend as the running `hermes dashboard` service, not as the separate messaging gateway process;
6. if session-token Remote Gateway is incompatible with the actually installed Hermes build or the accepted nginx/Authelia reverse-proxy path, test the minimum next supported credential mode (username/password or OAuth) without assuming Nous OAuth in advance; evaluate a different connection mode only after Remote Gateway itself is proven incompatible.

This Desktop integration is the **last Stage 4 integration task**, not a user-specific workflow.

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

Next branch:

`04 — Edge Hermes Agent Runtime`
