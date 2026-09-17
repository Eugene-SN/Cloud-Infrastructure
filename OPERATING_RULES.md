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

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a **global capability/requirements scaffold**, not a complete product list and not a final Architecture Contract.

It answers primarily **what useful functions `edge` should provide**, while many **how / with which service** decisions intentionally remain unresolved.

Rules:

- Do not infer a product choice merely because a capability exists in the scaffold.
- Preserve explicitly accepted global product choices from `DECISIONS.md` unless a concrete incompatibility or changed requirement appears.
- Select unresolved services/products during Stage 02.5 research from actual requirements and dependencies.
- Do not preselect later products merely to make the global architecture look complete.
- Distinguish infrastructure services from user-specific n8n/agent workflows; the latter are a post-infrastructure layer unless they prove to require a dedicated infrastructure service.

## Implementation stages and work branches

Completed canonical stages:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — Stage 0 — COMPLETE / ACCEPTED;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — Stage 1 — COMPLETE / ACCEPTED;
- `02 — Edge Core Applications` — Stage 2 — COMPLETE / ACCEPTED with `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Current canonical branch/stage:

- `02.5 — Remaining Functional Scope Reconciliation & Research` — **ACTIVE / RESEARCH-ONLY**.

The previous thematic Stage 3–7 grouping is historical planning context only and is not authoritative future deployment chronology.

Exact replacement stage numbering will be accepted only after Stage 02.5 completes the research matrix and normalized remaining service/product inventory.

## Mandatory lifecycle for every implementation stage

Every new implementation-stage branch starts with analysis/design, not installation.

Before stage-dependent runtime mutation, perform in order:

1. **REQUIREMENTS REVIEW** — read current state, accepted decisions and the relevant capability requirements; define the exact requirements for this stage.
2. **SERVICE / PRODUCT SELECTION** — research/discuss unresolved implementation alternatives for this stage. Do not re-open accepted products without a concrete reason.
3. **STAGE COMPOSITION ACCEPTANCE** — explicitly record what is included/excluded and the selected products/mechanisms.
4. **STAGE ARCHITECTURE / DEPLOYMENT CONTRACT** — define only the topology, runtime placement, paths, ingress/auth/storage relationships, dependencies and recovery path required for this stage.
5. **IMPLEMENTATION** — perform the runtime changes.
6. **VERIFY** — verify properties, not merely command return codes.
7. **ACCEPTANCE** — explicitly mark the stage complete only after the full stage scope passes.
8. **PERSISTENCE** — write accepted decisions and current state to the primary repository and read back critical writes.
9. **BRANCH TRANSITION** — only after acceptance may ChatGPT propose the next branch name and starter prompt.

A completed subtask is **not** permission to leave the current branch if the stage/branch title still contains unfinished scope.

## Current work checkpoint

Current canonical branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Current facts:

1. Stage 0 preservation/recovery is complete.
2. Stage 1 clean rebuild/base platform is complete and accepted.
3. Stage 2 Core Applications is complete and accepted.
4. `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.
5. Stage 02.5 is research-only; no production deployment/configuration mutation is authorized by this stage.
6. No post-Stage-2 production deployment branch is authoritative until Stage 02.5 deliverables are explicitly accepted.
7. Immediate next research block is `Remaining Standalone Core Services`.

## Stage 02.5 research-only gate

During Stage 02.5:

- do not deploy/install/configure new production services;
- do not mutate production DNS/firewall/runtime;
- read-only runtime inspection is allowed only when a concrete unknown factual state materially blocks a decision;
- do not reopen accepted product anchors without a concrete incompatibility or changed requirement;
- use current upstream/official documentation and releases for changing information, then maintainer evidence, then community evidence;
- classify unresolved capabilities as `SELECTED`, `REUSE EXISTING`, `DEFERRED`, `REJECTED` or, only when evidence is genuinely insufficient, `RESEARCH STILL REQUIRED`.

## Dependency-aware remaining roadmap

Post-Stage-2 deployment follows dependency direction rather than historical thematic grouping:

1. **Remaining Standalone Core Services** — full services that can be independently deployed/accepted on `edge` without future Home/PAI connectivity or late lifecycle layers.
2. **Cross-site Connectivity Foundation** — establish the required `edge ↔ ai-node ↔ PVE/Home` transport/reachability from real flows before deploying services that depend on it.
3. **Cross-site Data & Knowledge Services** — working-file access, web file management, selected-directory synchronization, Obsidian synchronization/relay/mirror and other connectivity-dependent data services.
4. **Remaining Infrastructure Services** — finish any other selected infrastructure components so the service inventory becomes substantially stable.
5. **Backrest & Recovery** — deploy/configure Backrest + Restic against the substantially complete system and prove restore.
6. **Semaphore & Maintenance / Update** — deploy Semaphore/update workflow after Backrest. `update.escloud.us` is a dedicated custom maintenance/update page implemented in a separate Codex substage after the backend contract is known.
7. **Monitoring, Heartbeats & Alerts** — deploy production monitoring after the service inventory, connectivity, Backrest and update subsystem substantially exist, so monitoring is built once against the finished infrastructure.
8. **`app.escloud.us` Portal** — build the final navigation/status dashboard after monitoring/status sources and final service inventory are known, in a separate Codex substage.
9. **Final Integrated Infrastructure Acceptance** — only after all selected infrastructure, connectivity/integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.
10. **Automation & User Workflows** — ongoing n8n/agent/user tasks after infrastructure acceptance; these continuously evolve and are not infrastructure-completion blockers.

## UI responsibility separation

- `ops.escloud.us` — Semaphore operational execution UI.
- `update.escloud.us` — dedicated custom maintenance/update page; separate Codex substage after real Semaphore/update backend/status/control interfaces are known.
- `app.escloud.us` — final Cloud Infrastructure navigation/status dashboard; separate Codex substage after monitoring/status sources and final service inventory are accepted.

Do not put detailed maintenance/update controls into `app.escloud.us` merely to consolidate pages.

## Connectivity sequencing

Do not deploy files/sync/Obsidian or other Home/PAI-dependent services before the required `edge ↔ ai-node ↔ PVE/Home` connectivity foundation is selected, deployed and accepted.

Connectivity technology is selected from real flows and operating conditions. NetBird, direct WireGuard, authenticated HTTPS or another simple mechanism may be considered; do not choose a private backbone first and then invent uses for it.

Connectivity means transport/reachability/endpoints. Application-level durable store-and-forward/retry for n8n/agent tasks is a later workflow concern and does not by itself define the connectivity foundation.

## Backup/update sequencing

- Backrest using Restic is the accepted backup-management direction.
- Backrest is deployed late against the substantially complete service inventory.
- A usable pre-update backup/restore path must be accepted before Semaphore/update testing.
- Semaphore and the maintenance/update workflow are developed/tested together.
- The existing PVE/Home updater is an engineering reference to audit and adapt for `edge`, not a template to copy blindly.

## Monitoring sequencing

Research the monitoring architecture during Stage 02.5, but deploy production monitoring late, after the services it must monitor substantially exist.

Monitoring may include `edge` service availability, external checks, selected Home/PVE/`ai-node` heartbeats, cross-site link health, file/sync health where useful, Backrest job health and Semaphore/update state.

Avoid heavyweight metrics/logging/observability stacks unless concrete requirements justify them.

## Obsidian invariant

Canonical Obsidian vault remains:

`ai-node:/srv/ai-data/knowledge/obsidian`

Do not make `edge` the canonical source of truth by assumption. Any `edge` role is selected separately as sync endpoint, relay/mirror, remote workspace, web/file gateway or no direct vault role.

## Runtime and placement defaults

- Docker + Compose are the default runtime for suitable application services.
- Host-native deployment remains valid where materially simpler or better suited to the service.
- Application WebUI backends normally bind loopback and are published through nginx.
- Use the accepted path convention: `/opt/<service>` runtime definitions/scripts, `/srv/<service>` persistent state, `/etc/<service>` host-native configuration, `/var/www/<site>` static web roots.
- Preserve the upstream-required internal container user/UID/GID where necessary rather than cosmetically remapping it.

## Current substrate contract

Accepted live substrate facts include:

- Ubuntu 26.04.1 LTS, `x86_64`, KVM;
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
- Docker Engine/Compose, nginx, Xray, Hysteria2, Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark are accepted current runtime components as documented in `CURRENT_STATE.md`.

Fresh runtime/configuration has priority over historical reference.

## Recovery model

Current recovery layers include:

1. provider-level whole-VPS backup / rollback path from Stage 0 where applicable;
2. external sensitive migration archive with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf` retained for selective legacy reference/recovery;
3. Stage 1 same-VPS recovery checkpoint `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, which is not complete host-loss DR;
4. future Backrest + Restic topology, still unresolved for off-site repository placement and final retention/restore policy.

`migration-reference/` is engineering context only and must not be used as an authoritative restore bundle.

## Source-of-truth and persistence rules

For project intent, use the latest applicable `ACCEPTED` decisions and canonical current documents. For factual runtime state, priority is:

1. fresh runtime audit;
2. actual live configuration;
3. current repository state;
4. historical docs/reference.

A discrepancy between these is drift and must be resolved explicitly rather than guessed.

Before modifying project files:

1. read current repository state;
2. avoid duplicate documents/facts;
3. update the canonical existing document for that topic;
4. read back critical writes.

Store structured state and decisions, not chat transcripts.

When returning to an earlier checkpoint after premature planning or branch transition:

- restore the earlier checkpoint as current state;
- remove or replace premature current-tree architecture/task/handoff artifacts that no longer apply;
- keep Git history intact unless the user explicitly requests history rewriting;
- mark superseded decisions clearly so they cannot be mistaken for current authority.

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

- Use the shared host service account **`core`** by default for Cloud Infrastructure application services, persistent service data and host-native service execution.
- Do not create one Unix account per service merely for isolation.
- Create or use a service-specific Unix account only when the application or its upstream-supported runtime explicitly requires that account identity or when using `core` would break the supported runtime contract.
- For containers, keep the image's required internal user/UID/GID when necessary; do not rename or remap an upstream container user merely to make it `core`.
- Host-side ownership of bind-mounted data should use `core` where compatible. If a container requires a specific numeric UID/GID for a bind mount, preserve that requirement rather than forcing `core` ownership; document the exception.
- Do not assume the numeric UID/GID of `core`; verify it from fresh runtime state before applying ownership changes.

## Shell block rule

Any terminal block whose output must be returned to chat uses a subshell, `set -Eeuo pipefail`, ASCII/English `BLOCK_NAME`, and green BEGIN/END delimiters including final RC.

Do not hide failures through `|| true`, global `set +e`, or stderr suppression. Handle expected non-zero statuses explicitly.

If a block fails or the terminal/session closes, first determine the failure point and side effects with a proportionate read-only recovery audit. Do not simply shorten scope or rerun already completed work.

Use `/tmp` for temporary test/audit artifacts and remove them after the task unless they become deliberate persistent artifacts.

## Verification

`RC=0` alone is not acceptance. Verify the minimum properties relevant to the change and use PASS/FAIL for important acceptance gates.

Avoid restart/reboot unless the change actually requires one.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without a demonstrated use case.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are separate from any future private infrastructure backbone.
- Any private backbone must be tested on the real Russia ↔ external-VPS path before acceptance; do not assume WireGuard-based connectivity will be reliable under DPI.
- Home/PAI connectivity must not become a foundation requirement for capabilities that are otherwise independently useful on `edge`, but it must exist before deploying services whose correctness explicitly depends on Home/PAI.
- Do not carry legacy service configuration forward blindly; use `migration-reference/` to understand prior logic and the external archive only where exact state/credentials are actually required.
- Do not open the next production deployment branch until Stage 02.5 deliverables are explicitly accepted and canonical files have been updated/read back.
