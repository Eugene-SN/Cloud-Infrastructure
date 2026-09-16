# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED

This document is the canonical implementation-stage chronology for Cloud Infrastructure / `edge`.

## Terminology: work branches are not implementation stages

Chat/project work-branch numbers and implementation-stage numbers are different coordinate systems and must never be inferred from each other.

Current/planned work-branch chronology:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — discovery, target composition, preservation planning and initial architecture work;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — provider clean rebuild, fresh-substrate acceptance and architecture-independent minimal host bootstrap;
- `02 — Edge Functional Composition & Deferred Capabilities` — finish unresolved functional/service choices and deferred capability decisions;
- `03 — Edge Architecture Contract & Topology` — only after branch 02 is closed; define the final Architecture Contract and deployment topology.

A branch number does **not** mean the corresponding implementation stage is complete or active. In particular, work performed in branch `01` completed only the clean substrate and minimal architecture-independent bootstrap portion of implementation Stage 1; it did not deploy the full Stage 1 service foundation.

## Sequencing principles

1. `edge` should become useful as a standalone cloud node before Home/PAI integration is required.
2. Foundation choices must leave clean extension points for later capabilities without installing those capabilities prematurely.
3. Each implementation stage should end in a usable, verified state; later stages must not be required to make earlier stages operational.
4. Cross-site connectivity is deliberately late because its correct form depends on actual data/task flows.
5. Optional services remain late and must not delay the core platform.
6. Architecture-dependent Stage 1 service deployment remains gated by closure of functional composition and acceptance of the Architecture Contract.

---

## Stage 0 — Preservation, migration decision and deployment contract

### Purpose

Before destructive migration, make the legacy `nl-core-vds` recoverable and decide the migration method.

### Accepted outcome

**COMPLETE / PASS.**

- provider-level full VPS backup completed;
- credential-bearing migration archive downloaded and independently verified;
- sanitized `migration-reference/` accepted in GitHub;
- clean provider-level Ubuntu rebuild selected and executed;
- fresh Ubuntu substrate accepted as node `edge`.

Stage 0 does not imply that the full Stage 1 application/service foundation has been deployed.

---

## Stage 1 — Base `edge` Platform

### Goal

Create the smallest stable platform on which all later Cloud Infrastructure capabilities can be added without redesigning the host.

### Functional scope

- Ubuntu;
- hostname `edge`;
- networking/firewall/SSH;
- Docker + Compose where required;
- normalized persistent-directory and ownership conventions;
- nginx;
- HTTPS/TLS;
- Xray;
- Hysteria2;
- plausible public/decoy page;
- Authelia common web-auth foundation;
- initial private Cloud Infrastructure page;
- basic backup of the new base state.

### Extension points to reserve, not pre-install

Stage 1 must leave clean places/interfaces for:

- public WebUI;
- private WebUI;
- machine APIs;
- webhooks;
- working storage;
- Home/PAI connectivity;
- monitoring/status integration.

`edge` must remain autonomously useful without Home/PAI connectivity.

### Current progress

**PARTIAL.**

Already accepted:

- clean Ubuntu substrate;
- hostname `edge` / `edge.escloud.us`;
- provider networking as currently working;
- key-only SSH access through accepted `ssh.socket` activation;
- minimal architecture-independent host bootstrap;
- journald 500 MiB persistent-use ceiling;
- basic host health/non-regression acceptance.

Not yet completed merely because the substrate exists:

- target firewall contract;
- Docker/Compose target runtime;
- normalized target persistent-directory layout;
- nginx/TLS target ingress;
- Xray/Hysteria2 target deployment;
- public decoy page;
- Authelia target deployment;
- initial private Cloud page;
- new-base backup implementation.

Those architecture-dependent items remain pending functional-composition closure and the accepted Architecture Contract.

---

## Stage 2 — Core Applications

After the Stage 1 foundation is accepted, deploy the core standalone services:

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

### Production checkpoint

At the end of Stage 2, `edge` should provide a practically complete standalone core:

- VPN/DPI-bypass connectivity;
- mail;
- web services;
- common authentication;
- automation;
- subscription cloud AI;
- backup management;
- maintenance;
- portal/status surfaces.

This is the first major standalone production checkpoint.

---

## Stage 3 — Monitoring + Human Interaction

Add capabilities that improve operational control before more complex data/AI integration:

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

Do not introduce a heavy centralized observability stack without a demonstrated need.

---

## Stage 4 — Files / Sync / Obsidian

Only after the base runtime and core application consumers are stable, choose and deploy the data-access layer:

- Filestash vs alternatives;
- WebDAV/SMB/SFTP/other appropriate protocol;
- MacBook/iPhone/iPad access;
- `ai-node` access;
- selected working storage;
- web file browsing/editing;
- Syncthing or alternative synchronization;
- Obsidian synchronization;
- explicit source-of-truth, conflict and versioning model.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes that.

---

## Stage 5 — Information + Cloud AI

After a working data layer exists, add active information and cloud-agent workflows:

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

Only after `edge` and Home/PAI are independently stable:

- select the simplest adequate private/cross-site connectivity;
- test NetBird/WireGuard behavior on the real Russia ↔ external-VPS path if considered;
- consider authenticated HTTPS over the Home public IP where simpler/adequate;
- task handoff;
- durable retry/store-and-forward;
- local vLLM access for selected flows;
- OCR/translation/OEM-document pipeline orchestration;
- file/result exchange;
- selected off-site Home/PAI backup copies if accepted;
- Home heartbeat/status integration with Stage 3 monitoring.

**Invariant:** Home connectivity is not a foundation requirement for `edge`; it is a late integration layer over two already working infrastructures.

---

## Stage 7 — Optional

Only after production acceptance of the primary system:

- password/2FA vault;
- additional messaging/control UI;
- limited secondary/failover behavior;
- other explicitly accepted late capabilities.

Optional services must not block or complicate the core deployment.

---

## Current gating order

The current project must follow this order:

1. complete work branch `02 — Edge Functional Composition & Deferred Capabilities`;
2. then open/complete `03 — Edge Architecture Contract & Topology`;
3. use the accepted Architecture Contract to finish the remaining implementation Stage 1 service foundation;
4. accept Stage 1;
5. proceed to implementation Stage 2, then Stage 3–7 in the order above unless a later explicit ACCEPTED decision changes the sequence.

Do not jump from the minimal clean substrate directly to Stage 2 applications merely because work branch `02` has that number.