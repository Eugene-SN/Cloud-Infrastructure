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

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a **global capability scaffold**, not a complete product list and not a final Architecture Contract.

It answers primarily **what useful functions `edge` should provide**, while many **how / with which service** decisions intentionally remain unresolved.

Rules:

- Do not infer a product choice merely because a capability exists in the scaffold.
- Preserve explicitly accepted global product choices from `DECISIONS.md` unless a concrete incompatibility or changed requirement appears.
- Select unresolved services/products only when their implementation stage begins and their actual consumers/constraints are known.
- Do not preselect Stage 4/5/6 services merely to make the global architecture look complete.

## Implementation stages and work branches

After the initial discovery/preservation work, implementation stages and work branches are stage-aligned.

Canonical sequence:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — Stage 0 discovery/preservation/migration preparation — COMPLETE;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — Stage 1 Base `edge` Platform — **CURRENT / IN PROGRESS**;
- `02 — Edge Core Applications` — Stage 2 — future, only after Stage 1 acceptance;
- `03 — Edge Monitoring & Human Interaction` — Stage 3 — future;
- `04 — Edge Files, Sync & Obsidian` — Stage 4 — future;
- `05 — Edge Information & Cloud AI` — Stage 5 — future;
- `06 — Edge Home & PAI Integration` — Stage 6 — future;
- `07 — Edge Optional Capabilities` — Stage 7 — future.

The prematurely opened `02 — Edge Functional Composition & Deferred Capabilities` is not the canonical continuation point. Its useful discussion may inform later decisions, but it does not close unfinished Stage 1 work.

## Mandatory lifecycle for every implementation stage

Every new implementation-stage branch starts with analysis/design, not installation.

Before stage-dependent runtime mutation, perform in order:

1. **REQUIREMENTS REVIEW** — read current state, accepted decisions and the relevant portion of the global functional scaffold; define the exact requirements for this stage.
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

`01 — Edge Clean Rebuild & Base Platform Deployment`

Current facts:

1. Stage 0 preservation/recovery is complete.
2. Provider-level clean Ubuntu rebuild is complete and accepted.
3. GitHub `migration-reference/` is accepted engineering context.
4. Architecture-independent minimal host bootstrap is accepted.
5. **Base Platform Deployment is not complete.**
6. Stage 1 requirements/service-selection work must continue in branch `01` before additional architecture-dependent deployment.
7. No later implementation branch is active.

`EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS` and `EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS` are subset acceptances inside Stage 1; they are not Stage 1 acceptance.

## Stage 1 transition gate

Do not leave branch `01` until all required Base Platform work is completed, including stage-specific design/selection, deployment, verification and acceptance.

Only after explicit Stage 1 acceptance should ChatGPT propose:

`02 — Edge Core Applications`

The Stage 2 branch must again begin with requirements analysis and service/product selection before deployment.

## Runtime mutation gate

The clean rebuild and minimal substrate bootstrap are accepted historical/current state.

For further Stage 1 work:

- architecture-independent checks/maintenance may be performed when explicitly scoped;
- architecture-dependent changes must wait until the relevant Stage 1 requirements, service/product choices and Stage 1 deployment contract are accepted;
- do not restore legacy services merely because their product names are globally accepted;
- do not deploy future-stage services early.

## Current substrate contract

Accepted live substrate facts include:

- Ubuntu 26.04.1 LTS, `x86_64`, KVM;
- hostname/FQDN `edge.escloud.us`, short hostname `edge`;
- kernel `7.0.0-31-generic` at substrate acceptance;
- 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- root filesystem ~155 GiB class;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64`, gateway `2a0c:b847:ffff::1`;
- SSH public-key access works; root password authentication is disabled;
- OpenSSH is socket-activated through `ssh.socket`;
- persistent journald-use ceiling is `500M`;
- provider-generated working Netplan/cloud-init networking remains authoritative unless a later concrete change requires otherwise.

Fresh runtime/configuration has priority over historical reference.

## Recovery model

Two independent recovery planes remain valid:

1. **Whole-VPS rollback:** confirmed provider-level backup.
2. **Selective recovery/migration:** external sensitive archive with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`.

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

## Service account and ownership default

- Use the shared host service account **`core`** by default for Cloud Infrastructure application services, persistent service data and host-native service execution.
- Do not create one Unix account per service merely for isolation.
- Create or use a service-specific Unix account only when the application or its upstream-supported runtime explicitly requires that account identity or when using `core` would break the supported runtime contract.
- For containers, keep the image's required internal user/UID/GID when necessary; do not rename or remap an upstream container user merely to make it `core`.
- Host-side ownership of bind-mounted data should use `core` where compatible. If a container requires a specific numeric UID/GID for a bind mount, preserve that requirement rather than forcing `core` ownership; document the exception.
- Do not assume the numeric UID/GID of `core`; verify it from fresh runtime state before applying ownership changes.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without a demonstrated use case.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are separate from any future private infrastructure backbone.
- Any private backbone must be tested on the real Russia ↔ external-VPS path before acceptance; do not assume WireGuard-based connectivity will be reliable under DPI.
- Home/PAI connectivity is a late integration layer and must not become a foundation requirement for an otherwise standalone-useful `edge`.
- Do not carry legacy service configuration forward blindly; use `migration-reference/` to understand prior logic and the external archive only where exact state/credentials are actually required.
