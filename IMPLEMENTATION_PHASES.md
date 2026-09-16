# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED

This document is the canonical implementation-stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

The global functional scaffold defines **what capabilities the server should eventually provide**, but it is not a complete service/product inventory and it is not a final architecture.

Each implementation stage is handled in its own work branch. Work inside a stage is split into two classes before further deployment:

1. **KNOWN / ACCEPTED BASELINE** — functions, products and operating scenarios already explicitly accepted or already proven in the preserved legacy deployment.
2. **UNRESOLVED SCOPE** — functions for which the product, mechanism, topology or useful inclusion is genuinely not yet decided.

The project must implement these classes in this order whenever dependencies permit:

1. **REQUIREMENTS / BASELINE REVIEW** — read accepted decisions, current state, the global scaffold and preserved migration material; classify stage items as already known/accepted versus genuinely unresolved.
2. **LEGACY IMPLEMENTATION RECONSTRUCTION** — for accepted carry-forward services, inspect `migration-reference/`, the sensitive recovery archive where needed, and the historical baseline. The previous working configuration/scenario is the default implementation reference, not a blank-sheet design exercise.
3. **KNOWN / ACCEPTED DEPLOYMENT** — after a narrowly scoped compatibility/recovery check, deploy and verify already accepted components that do not depend on unresolved choices. Do not delay known work merely to finish unrelated product research.
4. **UNRESOLVED SERVICE / PRODUCT SELECTION** — discuss and compare alternatives only for requirements that remain genuinely unresolved or where a concrete incompatibility/changed requirement justifies replacing an accepted implementation.
5. **REMAINING STAGE COMPOSITION ACCEPTANCE** — explicitly decide the unresolved in-scope/out-of-scope items and selected mechanisms.
6. **STAGE-SCOPED ARCHITECTURE / DEPLOYMENT CONTRACT** — define only the topology, paths, ingress/auth/storage relationships and recovery path still needed for the remaining work. Already deployed accepted baseline becomes an input, not something to redesign without cause.
7. **REMAINING DEPLOYMENT** — implement the unresolved/selected remainder.
8. **VERIFY / ACCEPT** — verify the complete stage properties and record factual state.
9. **PERSIST** — update `DECISIONS.md`, `CURRENT_STATE.md`, `ARCHITECTURE.md` and other canonical docs as needed.
10. **BRANCH TRANSITION** — only after the current stage is fully accepted may ChatGPT propose the next work branch and its starter prompt.

Additional rules:

- Do **not** open a new work branch merely because one subtask inside the current stage is complete.
- Do **not** make the user choose again from scratch when a product/scenario has already been accepted and preserved. Start from the old working implementation, then propose concrete retain / simplify / optimize / change options.
- Historical versions are evidence, not pins. At deployment/update time use the current supported stable release/channel unless a concrete compatibility reason requires otherwise.
- Containerized deployment through Docker + Compose is the default for suitable application services because it provides the preferred cleanliness, lifecycle control and update path. Host-native deployment remains appropriate where it is materially simpler or better suited to the service; such exceptions should be justified rather than assumed.

---

## Stage 0 — Discovery, preservation and migration preparation

### Work branch

`00 — Cloud Infrastructure Architecture Discovery & Target Design`

### Purpose

- audit the legacy VPS;
- establish the cross-project Cloud Infrastructure role;
- build the preliminary global functional scaffold;
- screen obvious duplicate/unwanted capabilities;
- preserve expensive-to-reconstruct state;
- choose the migration method and prepare recovery paths.

### Accepted outcome

**COMPLETE / PASS.**

- historical legacy baseline created and retained;
- preliminary functional scaffold created;
- provider-level full VPS backup completed;
- credential-bearing migration archive downloaded and independently verified;
- sanitized `migration-reference/` accepted in GitHub;
- clean provider-level Ubuntu rebuild selected;
- recovery paths verified.

The global scaffold remains intentionally incomplete at product-selection level. Unresolved products/services are selected later, stage by stage.

---

## Stage 1 — Base `edge` Platform

### Work branch

`01 — Edge Clean Rebuild & Base Platform Deployment`

### Goal

Create the smallest stable standalone platform on which all later Cloud Infrastructure capabilities can be added without redesigning the host.

### Functional scope

The Stage 1 capability scope currently includes:

- clean supported Ubuntu substrate;
- hostname `edge`;
- networking/firewall/SSH baseline;
- Docker + Compose container/runtime foundation;
- normalized persistent-directory and ownership conventions;
- public HTTP/HTTPS ingress foundation;
- TLS/certificate handling;
- Xray;
- Hysteria2;
- plausible public/decoy page;
- Authelia common web-auth foundation;
- initial private Cloud Infrastructure page;
- basic backup of the new base state;
- clean extension points for later public WebUI, private WebUI, machine APIs, webhooks, working storage, Home/PAI connectivity and monitoring.

`edge` must remain autonomously useful without Home/PAI connectivity.

### Current progress

**IN PROGRESS / NOT ACCEPTED.**

Completed and accepted inside Stage 1:

- provider clean Ubuntu rebuild;
- hostname `edge` / `edge.escloud.us`;
- fresh-substrate acceptance;
- provider networking in its current working form;
- key-only SSH access through accepted `ssh.socket` activation;
- minimal architecture-independent host bootstrap;
- journald 500 MiB persistent-use ceiling;
- basic host health/non-regression acceptance.

**Important:** this completed only the **Edge Clean Rebuild** and minimal substrate/bootstrap portion of work branch `01`. It did **not** complete **Base Platform Deployment**.

### Accepted legacy foundation to reconstruct first

Before asking the user to choose new implementations, reconstruct and evaluate the preserved working Stage 1 baseline:

- **Docker Engine + Compose** as the primary application-service runtime;
- **nginx** as the accepted ingress/reverse-proxy anchor;
- **Xray** as the public TCP/443 VLESS/TLS endpoint with HTTP fallback semantics preserved unless deliberately changed;
- **Hysteria2** as the public UDP/443 endpoint with its masquerade behavior preserved unless deliberately changed;
- **Authelia** as the common web-auth foundation;
- the existing **`escloud.us` TLS lifecycle**: Certbot/ACME webroot, SAN certificate coverage for the required `escloud.us` names, renewal timer, and deploy-hook/certificate-copy mechanism feeding Xray/Hysteria2;
- existing public decoy/fallback behavior and nginx `127.0.0.1:8080 proxy_protocol` relationship;
- preserved VPN user/state-management logic (`vpnctl`) and useful maintenance logic from `maintctl`, adapting naming from the legacy node to `edge` rather than recreating behavior blindly.

The exact old credentials/private TLS material remain in the sensitive recovery plane, not GitHub. Restore selectively where continuity is desired.

### Required next activity in branch 01

Proceed in this order:

#### A. Known / accepted foundation

1. reconstruct the legacy Stage 1 implementation and dependencies from the preserved references;
2. derive the minimum required host package set from the actual consumers;
3. verify current upstream/Ubuntu compatibility and current stable release path;
4. decide only the runtime-placement exceptions that materially affect deployment (for example whether Xray/Hysteria2 remain host-native or move to containers while preserving the same external contract);
5. deploy and verify the accepted foundation components that do not depend on unresolved Stage 1 choices.

#### B. Unresolved Stage 1 choices

Only after/alongside the known baseline where dependencies require it, discuss the genuinely unresolved items, including:

- whether UFW remains useful on the new Docker host and the exact minimal firewall policy;
- normalized persistent-directory and ownership conventions for the new `edge` naming/model;
- whether the initial private Cloud page should be a minimal Stage 1 surface or deferred to the fuller Stage 2 portal implementation;
- exact Stage 1 basic-backup mechanism before the later full Backrest topology;
- any concrete optimization to the legacy TLS, ingress, VPN or auth implementation that has a demonstrated operational benefit.

Evidence from the preserved legacy host shows UFW was in fact active with default-deny incoming and explicit public-port rules. Therefore firewall treatment must be based on that evidence plus Docker/UFW interaction, not on an assumption that the old host had no firewall.

### Stage 1 package/runtime principle

Install packages because a selected Stage 1 component requires them, not as a generic toolbox. Reuse packages already present in the clean Ubuntu image. The expected additional foundation set is therefore small and consumer-driven; Docker packages come from Docker's supported stable Ubuntu repository, while ordinary host components should prefer Ubuntu's supported packages unless an upstream installation path is materially preferable.

Stage 1 is complete only after all required Base Platform components are deployed, verified and explicitly accepted.

---

## Stage 2 — Core Applications

### Future work branch

`02 — Edge Core Applications`

Create this branch **only after Stage 1 / branch 01 is fully accepted**.

Use the same accepted-first workflow: deploy/reconstruct already accepted carry-forward products first where their implementation is known and independent, then research only the genuinely unresolved Stage 2 items.

The current functional scaffold suggests this stage may include:

- Stalwart;
- Bulwark;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Backrest;
- Semaphore;
- maintenance page;
- full private Cloud page/portal.

Several of these products are already accepted globally. Their preserved legacy configuration is the first implementation reference where applicable; unresolved adjacent products/mechanisms are discussed separately rather than forcing a clean-sheet redesign.

### Intended production checkpoint

At the end of accepted Stage 2, `edge` should provide a practically complete standalone core:

- VPN/DPI-bypass connectivity;
- mail;
- web services;
- common authentication;
- automation;
- subscription cloud AI;
- backup management;
- maintenance;
- portal/status surfaces.

---

## Stage 3 — Monitoring + Human Interaction

### Future work branch

`03 — Edge Monitoring & Human Interaction`

Create only after Stage 2 acceptance. Reuse any already accepted/implemented mechanisms first, then select only unresolved monitoring and interaction components.

Current functional candidates include:

- external uptime monitoring;
- Home/PVE/PAI heartbeats;
- dead-man monitoring;
- backup/job checks;
- notifications;
- portal status integration;
- Universal Capture Inbox;
- human-in-the-loop approval workflows;
- inbound mail/attachment → n8n automation;
- outbound system mail;
- optional Telegram/messaging frontend if it materially improves mobile operation.

Do not preselect a heavy observability stack without a demonstrated need.

---

## Stage 4 — Files / Sync / Obsidian

### Future work branch

`04 — Edge Files, Sync & Obsidian`

Create only after Stage 3 acceptance. Begin from accepted requirements and any preserved useful implementation evidence, but research the products that remain unresolved.

Current unresolved scope includes:

- VPS working storage;
- MacBook/iPhone/iPad access;
- `ai-node` access;
- web file browsing/editing;
- network file/access protocol selection;
- Filestash vs alternatives;
- selected-directory synchronization;
- Syncthing vs alternatives;
- free/self-hosted Obsidian synchronization;
- explicit source-of-truth, conflict and versioning model.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes that.

No file/sync product that remains unresolved in current decisions is implicitly accepted by this phase description.

---

## Stage 5 — Information + Cloud AI

### Future work branch

`05 — Edge Information & Cloud AI`

Create only after Stage 4 acceptance. Deploy already accepted cloud-AI anchors using their accepted/preserved operating model where applicable; research only unresolved extensions.

Current functional candidates include:

- RSS/feed intake;
- vendor monitoring;
- firmware/release monitoring;
- document watchers/change detection;
- structured Internet ingestion;
- bounded AI research;
- long-running coding/agent workflows;
- Hermes only if later research accepts it;
- Capture Inbox → agent workflows;
- approval gates for selected agent actions.

Do not duplicate compute-heavy PAI OCR/ASR/translation/local inference on `edge` without a concrete reason.

---

## Stage 6 — Home / PAI Integration

### Future work branch

`06 — Edge Home & PAI Integration`

Create only after Stage 5 acceptance. Begin with analysis of the actual cross-site flows accumulated by earlier stages, then select the simplest adequate connectivity/orchestration mechanisms.

Current functional scope includes:

- private/cross-site connectivity selection;
- real Russia ↔ external-VPS testing for NetBird/WireGuard if considered;
- authenticated HTTPS over the Home public IP where simpler/adequate;
- task handoff;
- durable retry/store-and-forward;
- local vLLM access for selected flows;
- OCR/translation/OEM-document pipeline orchestration;
- file/result exchange;
- selected off-site Home/PAI backup copies if accepted;
- Home heartbeat/status integration.

**Invariant:** Home connectivity is not a foundation requirement for `edge`; it is a late integration layer over independently working infrastructures.

---

## Stage 7 — Optional Capabilities

### Future work branch

`07 — Edge Optional Capabilities`

Create only after the primary system has reached production acceptance. Deploy only capabilities with demonstrated value; unresolved optional products are selected only when their need is established.

Candidates may include:

- password/2FA vault;
- additional messaging/control UI;
- limited secondary/failover behavior;
- other explicitly accepted late capabilities.

Optional services must not block or complicate the core deployment.

---

## Current canonical checkpoint

The project is currently at:

**Stage 1 / work branch `01 — Edge Clean Rebuild & Base Platform Deployment` — IN PROGRESS.**

`Edge Clean Rebuild` is complete. `Base Platform Deployment` is not complete.

The prematurely opened work branch `02 — Edge Functional Composition & Deferred Capabilities` is **not** the canonical continuation point and must not be used to skip unfinished Stage 1 work.

The next work must occur in branch `01` and starts with reconstruction of the known/accepted Stage 1 legacy foundation, dependency/package analysis, and deployment of components whose behavior is already decided. Genuine unresolved Stage 1 choices are discussed separately when they become blocking or after the known baseline is in place.

Only after complete Stage 1 acceptance should the project open:

`02 — Edge Core Applications`.
