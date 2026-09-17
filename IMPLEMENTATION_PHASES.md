# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED chronology with later-stage scope subject to Stage 02.5 reconciliation.

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

## Stage 02.5 — Remaining Functional Scope Reconciliation & Research

### Work branch

`02.5 — Remaining Functional Scope Reconciliation & Research`

### Status

**NEXT / RESEARCH-ONLY / NO RUNTIME DEPLOYMENT.**

### Purpose

Stage 02.5 is the post-Stage-2 architecture/research checkpoint for the entire remaining Cloud Infrastructure roadmap. It exists because the original Stage 3–7 grouping predates several accepted decisions, especially the late deferral of `app.escloud.us`, Backrest, Semaphore and the maintenance page.

This checkpoint must reconcile **all remaining functional stages together**, rather than reviewing Stage 3 in isolation.

### Required work

1. Re-read the remaining capability backlog from `FUNCTIONAL_SCAFFOLD_DRAFT.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `CURRENT_STATE.md`, `INVENTORY.md` and this roadmap.
2. Remove capabilities already satisfied by accepted Stage 1/2 production state.
3. Re-evaluate the remaining tasks currently distributed across historical Stage 3–7 and late Operations & Lifecycle work.
4. Identify duplicated, misplaced, premature or dependency-inverted tasks and redesign the execution sequence where useful.
5. Preserve accepted dependency rules, including late portal deployment and Backrest-before-Semaphore update testing.
6. Research every remaining capability for which the functional requirement exists but the concrete implementation package/product/mechanism has not yet been selected.
7. Do not reopen already accepted product anchors merely to compare alternatives again; research only unresolved implementation details or a newly demonstrated incompatibility.
8. Do not deploy, configure, expose or mutate production services during Stage 02.5. Read-only runtime inspection is allowed only when necessary to resolve a concrete design question.

### Research domains

The research inventory must cover every still-unresolved functional domain, including at minimum:

- external uptime/availability monitoring;
- dead-man / heartbeat monitoring and alert delivery;
- notification channels and whether existing mail/n8n surfaces are sufficient;
- Universal Capture Inbox implementation surfaces;
- human-in-the-loop approval surfaces/mechanisms;
- mail-triggered automation patterns where product/mechanism choices remain unresolved;
- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` file-access mechanisms;
- selected-directory synchronization;
- Obsidian synchronization/mirror role for `edge` while `ai-node` remains canonical;
- continuous information intake/change detection additions beyond existing n8n capabilities;
- bounded cloud-AI research/agent orchestration additions;
- Hermes role, if any, relative to CloudCLI/Codex/Antigravity/n8n;
- durable `edge ↔ Home/PAI` task handoff/store-and-forward mechanism;
- eventual private/cross-site connectivity candidates driven by actual required flows;
- off-site/recovery topology details not already fixed by the accepted Backrest direction;
- optional messaging/control frontend;
- optional password/2FA vault;
- limited failover/secondary-endpoint role;
- any other capability present in the accepted scaffold that still has no selected concrete implementation.

The research must also explicitly determine when **no new package is needed** because an accepted existing component such as n8n, Stalwart/mail, nginx, Authelia, CloudCLI, Codex or Antigravity already satisfies the requirement adequately.

### Research method / output classification

For each unresolved capability, compare current maintained options against the actual single-operator Cloud Infrastructure requirements and classify the result as one of:

- `SELECTED` — concrete product/mechanism accepted for later implementation;
- `REUSE EXISTING` — no new service; satisfy the capability with an already deployed component;
- `DEFERRED` — useful but should be decided only after a later dependency becomes concrete;
- `REJECTED` — insufficient value or unnecessary duplication/complexity;
- `RESEARCH STILL REQUIRED` — only when evidence is genuinely insufficient to decide.

Selection criteria, in priority order:

1. correctness and fit to the real requirement;
2. simplicity;
3. minimum extra components/manual operations;
4. reliability/maintainability;
5. compatibility with the accepted `edge`, Home and PAI architecture.

Do not import enterprise observability/IAM/security layers without a concrete need.

### Required Stage 02.5 deliverables

Before Stage 02.5 closes, produce and accept:

1. a reconciled inventory of all remaining required/deferred/rejected capabilities;
2. a research matrix for every unresolved capability, including selected/reused/deferred/rejected outcome and rationale;
3. a normalized final service/product inventory for all remaining stages as far as evidence allows;
4. a revised dependency graph and execution order for the remaining implementation work;
5. revised stage names/numbers/scopes where the old Stage 3–7 grouping no longer fits;
6. explicit placement of late `app.escloud.us`, Backrest, Semaphore + maintenance page, and final integrated acceptance;
7. an explicit list of any questions intentionally left unresolved until a later stage and the dependency that blocks their decision;
8. updates/read-back of `IMPLEMENTATION_PHASES.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `INVENTORY.md` and other affected canonical project files.

Only after these deliverables are explicitly accepted should the next deployment branch be opened.

---

## Historical Stage 3 — Monitoring & Human Interaction

### Historical/planned work branch

`03 — Edge Monitoring & Human Interaction`

### Status

**NOT STARTED — HISTORICAL SCOPE SUBJECT TO STAGE 02.5 RECONCILIATION.**

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
- Universal Capture Inbox / approvals / mail-triggered automation overlap Information & Cloud AI workflows and existing n8n/mail capabilities;
- external monitoring, heartbeats and alert delivery remain a plausible independent capability group but must be confirmed by Stage 02.5.

Avoid heavy observability without demonstrated need.

---

## Historical Stage 4 — Files, Sync & Obsidian

### Historical/planned work branch

`04 — Edge Files, Sync & Obsidian`

### Status

**NOT STARTED — SUBJECT TO STAGE 02.5 RECONCILIATION.**

Unresolved scope includes VPS working storage, MacBook/iPhone/iPad/`ai-node` access, web file browsing/editing, selected-directory synchronization, Filestash vs alternatives, Syncthing role, and free/self-hosted Obsidian synchronization.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless superseded by a later ACCEPTED decision.

---

## Historical Stage 5 — Information & Cloud AI

### Historical/planned work branch

`05 — Edge Information & Cloud AI`

### Status

**NOT STARTED — SUBJECT TO STAGE 02.5 RECONCILIATION.**

Candidate scope includes feed/vendor/release monitoring, document watchers, structured Internet ingestion, bounded AI research, long-running coding/agent workflows, Hermes only if later accepted, Capture Inbox agent workflows and approval gates.

Do not duplicate compute-heavy PAI OCR/ASR/translation/local inference on `edge` without a concrete reason.

---

## Historical Stage 6 — Home & PAI Integration

### Historical/planned work branch

`06 — Edge Home & PAI Integration`

### Status

**NOT STARTED — SUBJECT TO STAGE 02.5 RECONCILIATION.**

Select connectivity only after real cross-site flows are known. Scope may include private/cross-site connectivity, Russia↔external-VPS testing, task handoff, durable retry/store-and-forward, local vLLM access, document-pipeline orchestration, result/file exchange, selected off-site backup copies and Home heartbeat/status integration.

Home/PAI connectivity is not an `edge` foundation requirement.

---

## Historical Stage 7 — Optional Capabilities

### Historical/planned work branch

`07 — Edge Optional Capabilities`

### Status

**NOT STARTED — SUBJECT TO STAGE 02.5 RECONCILIATION.**

Deploy only capabilities with demonstrated value after the primary system reaches production acceptance. Candidates include password/2FA vault, additional messaging/control UI, limited secondary/failover behavior and other explicitly accepted late capabilities.

---

## Late-stage Operations & Lifecycle

Exact stage number/name remains intentionally unset until Stage 02.5 reconciles the intervening functional stages.

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
Stage 02.5: **NEXT / RESEARCH-ONLY**.

The next canonical branch is:

`02.5 — Remaining Functional Scope Reconciliation & Research`

No production deployment branch after Stage 2 is authoritative until Stage 02.5 has reconciled the remaining capability/service inventory and accepted the revised roadmap.
