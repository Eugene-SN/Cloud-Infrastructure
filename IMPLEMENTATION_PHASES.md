# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED chronology with later-stage scope subject to stage-entry review.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. deployment of known/accepted dependency-ready components;
4. research/selection only for genuinely unresolved mechanisms or concrete incompatibilities;
5. stage-composition acceptance;
6. stage-scoped architecture/deployment contract;
7. deployment;
8. verification/acceptance;
9. persistence/read-back in GitHub;
10. branch transition only after complete stage acceptance.

Do not reopen accepted products without a concrete reason. Historical versions are evidence, not automatic pins. Docker + Compose are the default runtime for suitable application services; host-native remains valid where materially simpler.

---

## Stage 0 — Discovery, preservation and migration preparation

### Work branch

`00 — Cloud Infrastructure Architecture Discovery & Target Design`

### Status

**COMPLETE / ACCEPTED.**

Accepted outcome includes the historical legacy baseline, provider backup, sensitive migration-preservation archive, sanitized `migration-reference/`, clean-rebuild decision and verified recovery paths.

---

## Stage 1 — Base `edge` Platform

### Work branch

`01 — Edge Clean Rebuild & Base Platform Deployment`

### Status

**COMPLETE / ACCEPTED.**

Final acceptance:

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted composition includes Ubuntu substrate, SSH, journald policy, Docker/Compose, nginx, Certbot/TLS lifecycle, Xray, Hysteria2, public masking page, Authelia ingress/auth foundation, UFW, `maintctl`/`vpnctl`, extension-point contract and the Stage 1 recovery checkpoint.

---

## Stage 2 — Core Applications

### Work branch

`02 — Edge Core Applications`

### Status

**COMPLETE / ACCEPTED.**

Final acceptance:

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted Stage 2 production set:

- Authelia clean reinitialization;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark;
- accepted mail migration, DNS/DKIM/TLS/public-protocol contract and external bidirectional E2E verification.

Backrest, Semaphore, the maintenance page and the full private `app.escloud.us` portal were explicitly removed from Stage 2 completion scope after their dependency on a substantially complete final service inventory was recognized.

They are deferred to late-stage Operations & Lifecycle work in this accepted dependency order:

1. near-final `app.escloud.us` portal after the service inventory stabilizes;
2. Backrest backup/restore policy and acceptance;
3. Semaphore + maintenance page developed/tested together using the PVE/Home updater as an engineering reference adapted for `edge`;
4. final server-wide acceptance and cleanup.

---

## Stage 3 — Monitoring & Human Interaction

### Historical/planned work branch

`03 — Edge Monitoring & Human Interaction`

### Status

**NOT STARTED — SCOPE MUST BE REVALIDATED BEFORE BRANCH OPENING.**

The original candidate scope was:

- external uptime/availability monitoring;
- dead-man/heartbeat monitoring from Home/PVE/PAI;
- selected job/backup-health checks;
- notifications/alert delivery;
- portal status integration;
- Universal Capture Inbox;
- human-in-the-loop approvals;
- mail-triggered automation;
- optional messaging frontend.

After the accepted late-stage portal/Backrest/Semaphore deferral, this list no longer maps cleanly to one deployment stage:

- portal status integration belongs with the late portal work;
- backup-health integration depends on late Backrest deployment;
- Universal Capture Inbox / approvals / mail-triggered automation overlap Stage 5 Information & Cloud AI workflows and existing n8n/mail capabilities;
- external monitoring, heartbeats and alert delivery remain the clearest independent Stage 3 capability group.

Therefore do **not** open the historical Stage 3 branch automatically. First perform a short post-Stage-2 scope-reconciliation/research checkpoint and decide whether Stage 3 should remain one stage, be narrowed to external monitoring/notifications, or have human-interaction workflow work moved to the stage where its concrete consumers exist.

Avoid heavy observability without demonstrated need.

---

## Stage 4 — Files, Sync & Obsidian

### Planned work branch

`04 — Edge Files, Sync & Obsidian`

### Status

**NOT STARTED.**

Unresolved scope includes VPS working storage, MacBook/iPhone/iPad/`ai-node` access, web file browsing/editing, selected-directory synchronization, Filestash vs alternatives, Syncthing role, and free/self-hosted Obsidian synchronization.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless superseded by a later ACCEPTED decision.

---

## Stage 5 — Information & Cloud AI

### Planned work branch

`05 — Edge Information & Cloud AI`

### Status

**NOT STARTED.**

Candidate scope includes feed/vendor/release monitoring, document watchers, structured Internet ingestion, bounded AI research, long-running coding/agent workflows, Hermes only if later accepted, Capture Inbox agent workflows and approval gates.

Do not duplicate compute-heavy PAI OCR/ASR/translation/local inference on `edge` without a concrete reason.

---

## Stage 6 — Home & PAI Integration

### Planned work branch

`06 — Edge Home & PAI Integration`

### Status

**NOT STARTED.**

Select connectivity only after real cross-site flows are known. Scope may include private/cross-site connectivity, Russia↔external-VPS testing, task handoff, durable retry/store-and-forward, local vLLM access, document-pipeline orchestration, result/file exchange, selected off-site backup copies and Home heartbeat/status integration.

Home/PAI connectivity is not an `edge` foundation requirement.

---

## Stage 7 — Optional Capabilities

### Planned work branch

`07 — Edge Optional Capabilities`

### Status

**NOT STARTED.**

Deploy only capabilities with demonstrated value after the primary system reaches production acceptance. Candidates may include password/2FA vault, additional messaging/control UI, limited secondary/failover behavior and other explicitly accepted late capabilities.

---

## Late-stage Operations & Lifecycle

Exact stage number/name remains intentionally unset until the intervening functional stages are reconciled.

Accepted dependency order:

1. `app.escloud.us` private portal/status home after the service inventory is substantially complete;
2. Backrest + Restic repository/retention/restore acceptance;
3. Semaphore + maintenance page together, using working Backrest pre-update backups during update testing;
4. final server-wide integrated acceptance and cleanup.

Portal scope is determined from the actual final service inventory. Baseline intent is unified navigation plus simple useful status/monitoring, potentially including a collapsed-by-default Home Infrastructure summary if it is useful and simple. Do not precommit a heavy monitoring stack.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **COMPLETE / ACCEPTED**.  

**Next action:** short post-Stage-2 scope reconciliation/research before creating the next implementation branch. The historical `03 — Edge Monitoring & Human Interaction` title is not automatically authoritative for the remaining capability grouping after accepted late-stage deferrals.
