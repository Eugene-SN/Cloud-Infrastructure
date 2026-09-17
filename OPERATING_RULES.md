# Cloud Infrastructure — Operating Rules

## Project identity

- **Project name:** Cloud Infrastructure
- **Primary repository:** `Eugene-SN/Cloud-Infrastructure`
- **GitHub workflow:** ON
- **Primary VPS node:** `edge`
- **Current FQDN:** `edge.escloud.us`
- `edge` is a logical, location-agnostic node name. Do not encode provider/datacenter/country into target-state naming.

## Project scope

Cloud Infrastructure is the public/cloud-facing layer of one personal infrastructure composed of:

- **Home Infrastructure** — general-purpose home compute/service plane centered on Proxmox VE and home-network services;
- **Personal Agents Infrastructure (PAI)** — local AI/agent/data-processing plane centered on `ai-node`;
- **Cloud Infrastructure** — external 24/7 VPS layer for public routability, foreign location, Internet-facing services, cloud AI integrations, external coordination and off-site roles.

Cloud Infrastructure should complement Home Infrastructure and PAI rather than duplicate them without a concrete requirement.

## Historical baseline invariant

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains the canonical historical/as-is snapshot of the pre-reinstall legacy VPS.

- Keep historical names such as `nl-core-vds` and legacy paths unchanged in that artifact.
- Do not reinterpret it as current runtime state after the 2026-09-16 rebuild.
- Do not treat the historical deployment as the target architecture.

## Functional scaffold versus selected implementation

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a global capability/requirements scaffold, not an independent final Architecture Contract.

Rules:

- do not infer a product choice merely because a capability exists in the scaffold;
- preserve explicitly accepted product anchors from `DECISIONS.md` unless a concrete incompatibility or changed requirement appears;
- distinguish finite infrastructure services from continuously evolving user-specific n8n/agent workflows;
- select unresolved mechanisms from actual requirements/dependencies rather than filling roadmap stages with speculative products.

## Implementation stages and work branches

Completed canonical stages:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — Stage 0 — COMPLETE / ACCEPTED;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — Stage 1 — COMPLETE / ACCEPTED;
- `02 — Edge Core Applications` — Stage 2 — COMPLETE / ACCEPTED with `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Current canonical branch/stage:

- `02.5 — Remaining Functional Scope Reconciliation & Research` — **ACTIVE / RESEARCH-ONLY**.

Accepted/planned post-Stage-02.5 roadmap:

- `03 — Edge Hermes Agent Runtime` — Hermes only; product/role/host-native placement selected;
- `04 — Edge Cross-site Connectivity Foundation`;
- `05 — Edge Cross-site Data & Knowledge Services`;
- `06 — Edge Remaining Infrastructure Services` — conditional; remove/renumber at Stage 02.5 closure if no service is selected;
- `07 — Edge Backrest & Recovery`;
- `08 — Edge Maintenance & Update` — Semaphore/update workflow plus separate Codex `update.escloud.us` substage;
- `09 — Edge Monitoring, Heartbeats & Alerts`;
- `10 — Edge Cloud Portal` — separate Codex `app.escloud.us` implementation substage;
- `11 — Edge Final Integrated Infrastructure Acceptance`.

After Stage 11, **Automation & User Workflows** is a continuous post-infrastructure workstream, not another infrastructure-completion stage.

The historical thematic Stage 3–7 grouping is no longer authoritative.

## Mandatory lifecycle for every implementation stage

Every new implementation-stage branch starts with analysis/design, not installation.

Before stage-dependent runtime mutation, perform in order:

1. **REQUIREMENTS REVIEW** — read current state, accepted decisions and relevant capability requirements.
2. **SERVICE / PRODUCT SELECTION** — research only unresolved choices; do not reopen accepted products without a concrete reason.
3. **STAGE COMPOSITION ACCEPTANCE** — explicitly record included/excluded products/mechanisms.
4. **STAGE ARCHITECTURE / DEPLOYMENT CONTRACT** — define only topology, runtime placement, paths, ingress/auth/storage relationships, dependencies and recovery path required for that stage.
5. **IMPLEMENTATION**.
6. **VERIFY** — verify properties, not merely command return codes.
7. **ACCEPTANCE** — mark complete only after the whole stage passes.
8. **PERSISTENCE** — update canonical repository state and read back critical writes.
9. **BRANCH TRANSITION** — only after acceptance may ChatGPT propose the next branch and starter prompt.

A completed subtask is not permission to leave a branch while its accepted scope remains incomplete.

## Current work checkpoint

Current canonical branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Current facts:

1. Stage 0 preservation/recovery is complete.
2. Stage 1 clean rebuild/base platform is complete and accepted.
3. Stage 2 Core Applications is complete and accepted.
4. `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.
5. Stage 02.5 is research-only; no new production service deployment/configuration mutation is authorized.
6. Remaining Standalone Core Services research is complete: **Hermes Agent is SELECTED** as the only Stage 3 service.
7. Current next research block is **Cross-site Connectivity Foundation**.
8. No Stage 3 production branch opens until all Stage 02.5 deliverables are explicitly accepted and canonical files are read back.

## Stage 02.5 research-only gate

During Stage 02.5:

- do not deploy/install/configure new production services;
- do not mutate production DNS/firewall/runtime;
- read-only runtime inspection is allowed only when a concrete unknown factual state materially blocks a decision;
- do not reopen accepted product anchors without a concrete incompatibility or changed requirement;
- use current official/upstream information first for changing facts, then maintainer evidence, then community evidence;
- classify unresolved capabilities as `SELECTED`, `REUSE EXISTING`, `DEFERRED`, `REJECTED` or, only when genuinely necessary, `RESEARCH STILL REQUIRED`.

## Hermes Stage 3 contract

Stage 3 is **Hermes-only**.

Accepted role separation:

- n8n = deterministic workflow/orchestration plane;
- Hermes = persistent cloud-side agentic reasoning/tool/delegation plane;
- CloudCLI = manual web/remote cloud-AI workspace;
- Codex CLI and Antigravity CLI = specialized executors that remain directly usable by the user and may be delegated to by Hermes;
- OpenClaw = local Home/PAI personal agent;
- vLLM on `ai-node` = local inference backend available to Hermes only after Stage 4 connectivity.

Preferred Hermes placement is **host-native under `core`**. This is a justified exception to Docker-by-default because containerization would complicate direct reuse of host-native Codex/Antigravity binaries and user/runtime/auth context. Reconsider only if Stage 3 finds a concrete upstream/compatibility reason.

Stage 3 must establish and verify an infrastructure-level path:

`n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`

Actual user-specific n8n/Hermes workflows are not part of Stage 3. Hermes -> local vLLM remains deferred until Stage 4.

Do not assign Hermes a public domain/listener by assumption.

## Connectivity sequencing

Stage 4 must determine real flows first, then select/deploy the minimum required `edge ↔ ai-node ↔ PVE/Home` transport/reachability.

NetBird, direct WireGuard, authenticated HTTPS or another simple mechanism may be considered. Do not choose a private backbone first and invent uses afterward. Validate candidate private-backbone behavior against real Russia ↔ external-VPS conditions.

Connectivity means transport/reachability/endpoints. Application-level durable store-and-forward/retry for n8n/agent tasks is a later workflow concern.

Do not deploy files/sync/Obsidian or other Home/PAI-dependent services before Stage 4 is accepted.

## Data/knowledge sequencing

Stage 5 covers connectivity-dependent working data services such as:

- VPS working-file access;
- web file management;
- MacBook/iPhone/iPad/`ai-node` access;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror.

Canonical Obsidian vault remains:

`ai-node:/srv/ai-data/knowledge/obsidian`

Do not make `edge` the canonical source of truth by assumption.

## Conditional Stage 6 rule

Stage 6 exists only if remaining Stage 02.5 research selects another full infrastructure service that belongs after Stage 5 and before lifecycle tooling.

Do not create an empty branch merely to preserve numbering. If no such service exists, remove Stage 6 and normalize downstream numbering before Stage 3 opens.

## Backup/update sequencing

- Backrest using Restic is the accepted backup-management direction.
- Backrest is deployed against the substantially complete service inventory.
- A usable backup/restore path must be accepted before Semaphore/update testing.
- Semaphore and maintenance/update workflow are developed/tested together.
- Existing PVE/Home update tooling is an engineering reference to audit/adapt, not copy blindly.
- `ops.escloud.us` remains Semaphore's operational execution UI.
- `update.escloud.us` is a dedicated custom maintenance/update page built in a separate Codex substage only after the backend/status/control contract is known.

## Monitoring sequencing

Research monitoring architecture during Stage 02.5, but deploy production monitoring only after the service inventory, connectivity, Backrest and update subsystem substantially exist.

Monitoring may include:

- `edge` service availability;
- external checks;
- selected Home/PVE/`ai-node` heartbeats;
- cross-site link health;
- file/sync health where useful;
- Backrest job health;
- Semaphore/update state;
- alert delivery.

Avoid heavyweight metrics/logging/observability stacks unless concrete requirements justify them.

## Portal sequencing

- `app.escloud.us` is the final Cloud Infrastructure navigation/status dashboard.
- It is built only after Stage 9 monitoring/status sources and final service inventory are accepted.
- It is a separate Codex substage.
- Do not put detailed maintenance/update controls into `app.escloud.us`; those remain on `update.escloud.us`.

## Post-infrastructure workflow rule

After Stage 11, user-specific automation can evolve independently:

- n8n workflows;
- Hermes/agent workflows;
- Capture Inbox;
- approvals;
- mail-triggered automation;
- continuous information intake/change detection;
- bounded AI research;
- durable application-level cross-site task handoff;
- messaging/bot commands;
- orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

These are not blockers for final infrastructure acceptance.

## Runtime and placement defaults

- Docker + Compose are default for suitable application services.
- Host-native deployment is valid where materially simpler or better aligned with the upstream/runtime integration contract.
- Application WebUI backends normally bind loopback and are published through nginx.
- Use accepted path convention: `/opt/<service>` runtime definitions/scripts, `/srv/<service>` persistent state, `/etc/<service>` host-native configuration, `/var/www/<site>` static web roots.
- Preserve upstream-required internal container UID/GID where necessary rather than cosmetically remapping it.

## Current substrate contract

Accepted live substrate facts include:

- Ubuntu 26.04.1 LTS, x86_64, KVM;
- hostname/FQDN `edge.escloud.us`, short hostname `edge`;
- kernel `7.0.0-31-generic` at current accepted state;
- 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- root filesystem ~155 GiB class;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64`, gateway `2a0c:b847:ffff::1`;
- SSH public-key access works; root password authentication is disabled;
- OpenSSH is socket-activated through `ssh.socket`;
- persistent journald-use ceiling is `500M`;
- provider-generated working Netplan/cloud-init networking remains authoritative unless a later concrete change requires otherwise;
- Docker/Compose, nginx, Xray, Hysteria2, Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark are accepted current runtime components as documented in `CURRENT_STATE.md`.

Fresh runtime/configuration has priority over historical reference.

## Recovery model

Current recovery layers include:

1. provider-level whole-VPS backup / rollback path from Stage 0 where applicable;
2. external sensitive migration archive with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf` retained for selective legacy reference/recovery;
3. Stage 1 same-VPS recovery checkpoint `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, which is not complete host-loss DR;
4. future Backrest + Restic topology, still unresolved for off-site repository placement and final retention/restore policy.

`migration-reference/` is engineering context only and must not be used as an authoritative restore bundle.

## Source-of-truth and persistence rules

For project intent, use latest applicable ACCEPTED decisions and canonical current documents. For factual runtime state, priority is:

1. fresh runtime audit;
2. actual live configuration;
3. current repository state;
4. historical docs/reference.

A discrepancy is drift and must be resolved explicitly rather than guessed.

Before modifying project files:

1. read current repository state;
2. avoid duplicate documents/facts;
3. update canonical existing documents for current state/architecture;
4. preserve historical acceptance/audit artifacts rather than rewriting them retroactively;
5. read back critical writes.

Store structured state and decisions, not chat transcripts.

## Decision semantics

Decision statuses:

- `PROPOSED`
- `ACCEPTED`
- `SUPERSEDED`
- `REJECTED`
- `DEPRECATED`

Latest applicable `ACCEPTED` decision has priority. `SUPERSEDED`, `REJECTED`, and `DEPRECATED` entries are historical only.

## Git and secrets

- Do not commit credentials or secrets to GitHub.
- Persistent non-secret configuration/design/runbooks may be stored in Git.
- Sensitive recovery state remains outside GitHub.
- Credentials present in working chat/configuration/diagnostic context are not automatically considered compromised; rotate only with evidence of exposure.

## Service account and ownership default

- Use shared host service account `core` by default for Cloud Infrastructure application services and host-native service execution.
- Do not create one Unix account per service merely for isolation.
- Use a service-specific account only where upstream/runtime requirements make it necessary.
- For containers, preserve upstream-required internal users/UID/GID.
- Verify numeric ownership before mutations rather than assuming it.

## Shell block rule

Any terminal block whose output must be returned to chat uses a subshell, `set -Eeuo pipefail`, ASCII/English `BLOCK_NAME`, and green BEGIN/END delimiters including final RC.

Do not hide failures through `|| true`, global `set +e`, or stderr suppression. Handle expected non-zero statuses explicitly.

If a block fails or the terminal/session closes, determine the failure point and side effects with a proportionate read-only recovery audit before retrying.

Use `/tmp` for temporary test/audit artifacts and remove them after the task unless they become deliberate persistent artifacts.

## Verification

`RC=0` alone is not acceptance. Verify the minimum properties relevant to the change and use PASS/FAIL for important acceptance gates.

Avoid restart/reboot unless actually required.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without demonstrated use.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are separate from any future private infrastructure backbone.
- Home/PAI connectivity must not become a foundation requirement for independently useful `edge` capabilities, but it must exist before services whose correctness depends on Home/PAI.
- Do not carry legacy configuration forward blindly; use `migration-reference/` for engineering context and the external archive only where exact state/credentials are actually required.
- Do not open the next production deployment branch until Stage 02.5 deliverables are explicitly accepted and canonical files have been updated/read back.