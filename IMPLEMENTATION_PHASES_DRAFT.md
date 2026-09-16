# Cloud Infrastructure — Implementation Phases Draft

**Status:** PROPOSED / discussion draft

This document groups the accepted functional scaffold into implementation stages by dependency and operational risk. It is not yet an accepted deployment plan and does not decide clean rebuild versus in-place optimization.

## Sequencing principles

1. `edge` should become useful as a standalone cloud node before Home/PAI integration is required.
2. Foundation choices must leave clean extension points for later capabilities without installing those capabilities prematurely.
3. Each stage should end in a usable, verified state; later stages must not be required to make earlier stages operational.
4. Cross-site connectivity is deliberately late because its correct form depends on actual data/task flows.
5. Optional services remain late and must not delay the core platform.

---

## Stage 0 — Preservation, migration decision and deployment contract

### Purpose

Before any runtime mutation, turn the legacy `nl-core-vds` state into a recoverable source for the target `edge` deployment and decide between clean rebuild and in-place optimization.

### Required outputs

- final inventory of data/configuration that must survive;
- export/backup of accepted service state;
- verified access to required credentials/auth state;
- restore/read-back verification of critical backups;
- final target service inventory for Stage 1/2;
- explicit migration decision: clean Ubuntu rebuild or in-place optimization;
- recovery path for preserving working Xray/Hysteria2 access during migration.

### Legacy state categories to review

At minimum:

- Xray configuration and TLS material;
- Hysteria2 configuration and TLS material;
- nginx configuration;
- DNS/domain/certificate information needed for rebuild;
- Stalwart persistent mail state and configuration;
- Bulwark persistent state/configuration;
- Authelia configuration/data/secrets;
- n8n workflows/credentials/database and encryption-related state;
- CloudCLI configuration/state that is intentionally retained;
- Codex CLI authentication/configuration/state worth retaining;
- Antigravity authentication/configuration if already present by migration time;
- any user-created scripts still judged useful;
- current service manifests/documentation needed only as migration reference.

Do not preserve legacy implementation artifacts merely because they exist. Maintenance Center, Homepage and other rejected implementation layers should not become restore requirements.

---

## Stage 1 — Base `edge` platform and public-access foundation

### Goal

Create the smallest stable platform on which all later Cloud Infrastructure capabilities can be added without redesigning the host.

### Functional scope

- target hostname/taxonomy (`edge`);
- supported Ubuntu base;
- host networking and firewall baseline;
- SSH administrative access;
- Docker/Compose runtime where required by accepted applications;
- persistent-directory and ownership conventions;
- nginx;
- managed HTTPS/TLS model;
- Xray;
- Hysteria2;
- public plausible/decoy endpoint;
- Authelia common web-auth foundation;
- skeleton/private Cloud Infrastructure portal entry point;
- initial backup capability sufficient to protect the new base state.

### Design requirement

Stage 1 must reserve clean extension points for:

- service subdomains;
- public webhooks;
- machine-only interfaces;
- future Home/PAI connectivity;
- future working storage;
- monitoring/status integration;
- Backrest/Semaphore/portal extensions.

It must not require Home/PAI connectivity to operate.

---

## Stage 2 — Core user services and operations plane

### Goal

Restore/add the accepted applications that make `edge` useful in everyday operation before advanced automation is introduced.

### Functional scope

- Stalwart + Bulwark;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Backrest as backup-management layer;
- Semaphore;
- Cloud maintenance page;
- expanded private Cloud portal replacing Homepage;
- service health/version/status surfaces needed by the portal.

### Acceptance idea

At the end of Stage 2 the VPS should already provide:

- working DPI-bypass connectivity;
- mail;
- authenticated web access;
- automation engine;
- subscription cloud-AI execution;
- backup management;
- maintainable operational UI.

This is the minimum complete standalone `edge` platform.

---

## Stage 3 — External monitoring and human interaction layer

### Goal

Use the independent cloud failure domain and improve everyday control without creating a heavy observability stack.

### Functional scope

- external availability monitoring;
- Home/PVE/PAI heartbeat/dead-man endpoints or receivers;
- selected backup/job-health checks;
- alert delivery;
- portal status integration;
- Universal Capture Inbox entry points;
- human-in-the-loop approval flows;
- mail-triggered automation and system mail transport;
- optional messaging interface where it materially improves mobile operation.

### Boundary

Do not introduce full centralized metrics/log replication unless a concrete later need appears.

---

## Stage 4 — Working storage, file access, synchronization and Obsidian

### Goal

Create the user/agent working-data layer after the base runtime and operational interfaces are stable.

### Functional scope

- selected VPS working storage;
- access from MacBook, iPhone/iPad and `ai-node`;
- web file browsing/editing;
- access by n8n/CloudCLI/agents where required;
- selected-directory synchronization;
- free/self-hosted Obsidian synchronization while keeping the canonical vault on `ai-node`;
- explicit conflict/versioning/source-of-truth rules.

### Research prerequisite

Before implementation, compare Filestash and alternatives, filesystem/mount protocols, synchronization mechanisms and the role of `edge` in Obsidian sync.

---

## Stage 5 — Continuous information intake and cloud-agent workflows

### Goal

Turn `edge` from a hosted-service node into an active 24/7 information and AI work node.

### Functional scope

- RSS/feed intake;
- website/vendor/release monitoring;
- documentation-change detection;
- structured Internet ingestion workflows;
- bounded scheduled/event-driven AI research;
- long-running coding/agent workflows;
- Hermes evaluation/deployment if accepted after focused research;
- Capture Inbox routing into knowledge/AI workflows;
- approval gates for selected agent actions.

### Boundary

Do not duplicate PAI compute-heavy OCR/ASR/translation/local inference on `edge`.

---

## Stage 6 — Cloud ↔ Home/PAI integration and durable orchestration

### Goal

Connect the now-stable cloud node to Home/PAI only for flows that have demonstrated value.

### Functional scope

- select the simplest adequate private/cross-site transport;
- validate real Russia ↔ external-VPS connectivity characteristics where relevant;
- durable store-and-forward semantics;
- `edge` task submission to PAI;
- status/result return paths;
- local vLLM access for selected cloud-agent workflows;
- OEM/PDF/OCR/translation pipeline orchestration;
- working-file/result exchange;
- selected geographically independent Home/PAI backup copies if accepted;
- integration of Home heartbeat/status publication with Stage 3 monitoring.

### Boundary

The cross-site transport is an implementation detail of real flows, not an independent product goal.

---

## Stage 7 — Optional late additions

Implement only after the primary system is stable and there is demonstrated value.

Candidates:

- password/2FA vault;
- richer messaging/bot control UI;
- limited failover/secondary endpoint behavior;
- other capabilities explicitly accepted after the core system is in production.

Do not let optional services block or complicate the core deployment.

---

## Migration-path decision checkpoint

The clean-rebuild versus in-place decision belongs at Stage 0, after preservation requirements are explicit.

### Clean rebuild is favored when

- a large portion of the legacy deployment is being replaced or removed;
- current filesystem/service layout reflects superseded architecture;
- production configuration has significant drift from Git/source-of-truth;
- custom legacy services would otherwise have to be carefully dismantled;
- the target wants a new hostname/taxonomy and normalized directory/runtime structure;
- recoverable persistent state can be exported and restored independently of the old OS installation.

### In-place optimization is favored when

- most current services and runtime layout remain target-compatible;
- preserving live state in place materially reduces migration risk;
- application state is difficult to export/restore safely;
- legacy drift/obsolete components are limited enough that cleanup is simpler than rebuilding.

No migration choice is accepted by this draft.