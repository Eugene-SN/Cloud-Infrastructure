# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. deployment of known/accepted dependency-ready components;
4. research/selection only for genuinely unresolved mechanisms or concrete incompatibilities;
5. remaining stage-composition acceptance;
6. stage-scoped architecture/deployment contract;
7. remaining deployment;
8. verify/accept;
9. persist accepted current state/decisions/architecture;
10. branch transition only after complete stage acceptance.

Do not reopen accepted products without a concrete reason. Historical versions are evidence, not automatic pins. Docker + Compose are the default runtime for suitable application services; host-native remains valid where materially simpler.

---

## Stage 0 — Discovery, preservation and migration preparation

### Work branch

`00 — Cloud Infrastructure Architecture Discovery & Target Design`

### Status

**COMPLETE / ACCEPTED.**

Accepted outcome:

- historical legacy VPS baseline retained unchanged;
- preliminary functional scaffold created;
- provider full-VPS backup completed;
- sensitive migration-preservation archive created, externally copied and verified;
- sanitized `migration-reference/` accepted in GitHub;
- clean provider-level Ubuntu rebuild selected;
- recovery paths verified.

---

## Stage 1 — Base `edge` Platform

### Work branch

`01 — Edge Clean Rebuild & Base Platform Deployment`

### Status

**COMPLETE / ACCEPTED.**

Final acceptance:

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted Stage 1 composition:

- clean Ubuntu 26.04.1 LTS `edge` substrate;
- provider networking retained in its verified working form;
- key-only root SSH through `ssh.socket`;
- journald 500 MiB persistent-use ceiling;
- Docker Engine + Compose foundation;
- normalized `/opt`, `/srv`, `/etc`, `/var/www` path convention;
- nginx public HTTP and loopback HTTPS-fallback foundation;
- Certbot/ACME shared `escloud.us` TLS lifecycle;
- Xray public TCP/443 VLESS/TLS endpoint;
- Hysteria2 public UDP/443 endpoint and file masquerade;
- accepted `ES Cloud — Private Workspace` public masking page;
- Authelia common web-auth foundation at loopback backend `127.0.0.1:19091`;
- UFW public-exposure contract;
- restored `maintctl` and `vpnctl` operational entrypoints;
- documented extension-point contract;
- verified same-VPS Stage 1 base-state recovery checkpoint.

The full private Cloud Infrastructure portal is intentionally deferred to Stage 2 rather than deploying a temporary Stage 1 implementation. Stage 1 accepts the working Authelia/private-ingress boundary as sufficient foundation.

Stage 1 local checkpoint:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

This local checkpoint is not off-host DR and does not replace the later Backrest/Restic direction.

---

## Stage 2 — Core Applications

### Next work branch

`02 — Edge Core Applications`

### Status

**NEXT / NOT STARTED.**

Use the accepted-first workflow. Reconstruct/deploy already accepted carry-forward products first where their implementation is known and independent; compare alternatives only for genuinely unresolved adjacent mechanisms.

Current Stage 2 scope/candidates:

- Stalwart;
- Bulwark;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Backrest;
- Semaphore;
- maintenance page;
- full private Cloud Infrastructure portal.

Several are already accepted product anchors. Their preserved legacy configuration is the default engineering reference where applicable, but current stable releases/update paths should be used unless compatibility requires otherwise.

Intended Stage 2 production checkpoint: a practically complete standalone `edge` core providing VPN/DPI-bypass connectivity, mail, web services, common authentication, automation, subscription cloud AI, backup management, maintenance, and private portal/status surfaces.

---

## Stage 3 — Monitoring & Human Interaction

### Future work branch

`03 — Edge Monitoring & Human Interaction`

**NOT STARTED.**

Candidate scope includes external uptime/dead-man monitoring, job/backup checks, notifications, portal status integration, Universal Capture Inbox, human-in-the-loop approvals, mail-triggered automation and optional messaging frontend. Avoid heavy observability without demonstrated need.

---

## Stage 4 — Files, Sync & Obsidian

### Future work branch

`04 — Edge Files, Sync & Obsidian`

**NOT STARTED.**

Unresolved scope includes VPS working storage, MacBook/iPhone/iPad/`ai-node` access, web file browsing/editing, selected-directory synchronization, Filestash vs alternatives, Syncthing role, and free/self-hosted Obsidian synchronization.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless superseded by a later ACCEPTED decision.

---

## Stage 5 — Information & Cloud AI

### Future work branch

`05 — Edge Information & Cloud AI`

**NOT STARTED.**

Candidate scope includes feed/vendor/release monitoring, document watchers, structured Internet ingestion, bounded AI research, long-running coding/agent workflows, Hermes only if later accepted, Capture Inbox agent workflows and approval gates.

Do not duplicate compute-heavy PAI OCR/ASR/translation/local inference on `edge` without a concrete reason.

---

## Stage 6 — Home & PAI Integration

### Future work branch

`06 — Edge Home & PAI Integration`

**NOT STARTED.**

Select connectivity only after real cross-site flows are known. Scope may include private/cross-site connectivity, Russia↔external-VPS testing, task handoff, durable retry/store-and-forward, local vLLM access, document-pipeline orchestration, result/file exchange, selected off-site backup copies and Home heartbeat/status integration.

Home/PAI connectivity is not an `edge` foundation requirement.

---

## Stage 7 — Optional Capabilities

### Future work branch

`07 — Edge Optional Capabilities`

**NOT STARTED.**

Deploy only capabilities with demonstrated value after the primary system reaches production acceptance. Candidates may include password/2FA vault, additional messaging/control UI, limited secondary/failover behavior and other explicitly accepted late capabilities.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **NEXT / NOT STARTED**.

The next canonical branch is:

`02 — Edge Core Applications`

The earlier prematurely opened `02 — Edge Functional Composition & Deferred Capabilities` remains non-canonical historical context and must not be reused as the Stage 2 branch.
