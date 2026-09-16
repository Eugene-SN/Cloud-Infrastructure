# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED

This document is the canonical implementation-stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

The global functional scaffold defines **what capabilities the server should eventually provide**, but it is not a complete service/product inventory and it is not a final architecture.

Each implementation stage is handled in its own work branch. At the beginning of every stage branch, before architecture-dependent deployment, the project must perform a stage-scoped design cycle:

1. **REQUIREMENTS REVIEW** — read the accepted global scaffold/current state and determine the exact functional requirements that belong to this stage.
2. **SERVICE / PRODUCT SELECTION** — review candidate services and implementation mechanisms for unresolved requirements in this stage. Already accepted products are reused without replacement research unless a concrete incompatibility or changed requirement appears.
3. **STAGE COMPOSITION ACCEPTANCE** — explicitly decide what is in scope, what is out of scope, and which products/mechanisms are selected for this stage.
4. **STAGE ARCHITECTURE / DEPLOYMENT CONTRACT** — define only the topology, runtime placement, paths, ingress/auth/storage relationships and recovery path needed to implement this stage.
5. **DEPLOYMENT** — mutate runtime only after the stage composition/contract is accepted.
6. **VERIFY / ACCEPT** — verify the required properties and record the resulting factual state.
7. **PERSIST** — update `DECISIONS.md`, `CURRENT_STATE.md`, `ARCHITECTURE.md` and other canonical docs as needed.
8. **BRANCH TRANSITION** — only after the current stage is fully accepted may ChatGPT propose the next work branch and its starter prompt.

Do **not** open a new work branch merely because one subtask inside the current stage is complete.

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
- container/runtime foundation where required;
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

### Required next activity in branch 01

Before further Stage 1 deployment, continue in the same branch and perform the Stage 1 design cycle:

- review the exact Stage 1 functional requirements;
- identify which Stage 1 implementation choices are already accepted and which remain unresolved;
- research/discuss unresolved services/mechanisms only for Stage 1;
- explicitly accept the Stage 1 service/product composition;
- define the Stage 1 scoped architecture/deployment contract;
- then deploy and verify the remaining Stage 1 foundation.

Examples of still-unresolved or not-yet-finalized Stage 1 implementation details include, as applicable:

- target firewall implementation/policy;
- Docker/Compose usage and target runtime layout;
- normalized target persistent directories and ownership;
- nginx deployment details and ingress relationships;
- TLS/ACME mechanics and certificate distribution;
- Xray/Hysteria2 target configuration/restoration/adaptation;
- public decoy implementation;
- Authelia deployment/integration details;
- implementation of the initial private Cloud page;
- implementation of the initial base-state backup.

Some products in this list are already accepted globally (for example nginx, Xray, Hysteria2 and Authelia); their **replacement selection** need not be reopened without a concrete reason, but their Stage 1 implementation contract still must be discussed and accepted before deployment.

Stage 1 is complete only after all required Base Platform components are deployed, verified and explicitly accepted.

---

## Stage 2 — Core Applications

### Future work branch

`02 — Edge Core Applications`

Create this branch **only after Stage 1 / branch 01 is fully accepted**.

At the beginning of the branch, run the same stage design cycle before deployment. The current functional scaffold suggests this stage may include:

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

Several of these products are already accepted globally, but the complete Stage 2 composition, integration details, runtime placement and any unresolved adjacent products/mechanisms must still be reviewed in Stage 2 before deployment.

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

Create only after Stage 2 acceptance. Begin with stage-specific requirements analysis and service/product selection.

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

Create only after Stage 3 acceptance. Begin with stage-specific requirements analysis and product research.

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

Create only after Stage 4 acceptance. Begin with stage-specific requirements analysis and product/service selection.

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

Create only after the primary system has reached production acceptance. Begin with requirements review; deploy only capabilities with demonstrated value.

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

The next work must occur in branch `01`: Stage 1 requirements review → Stage 1 service/product selection → Stage 1 scoped architecture/deployment contract → remaining Base Platform deployment → verification → Stage 1 acceptance.

Only after that acceptance should the project open:

`02 — Edge Core Applications`.
