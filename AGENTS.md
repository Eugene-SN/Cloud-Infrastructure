# AGENTS.md — Cloud Infrastructure

These are durable project-specific rules for any agent working in this repository.

## Required context before work

Read, in this order when relevant:

1. `OPERATING_RULES.md`
2. `DECISIONS.md`
3. `CURRENT_STATE.md`
4. `IMPLEMENTATION_PHASES.md`
5. `FUNCTIONAL_SCAFFOLD_DRAFT.md`
6. `ARCHITECTURE.md`
7. `INVENTORY.md`
8. `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` when legacy/as-is VPS facts are needed.

## Current checkpoint invariant

Current canonical work remains in:

`01 — Edge Clean Rebuild & Base Platform Deployment`

The clean provider rebuild and minimal substrate/bootstrap subset are accepted, but **Base Platform Deployment is not complete**. Do not move to a later work branch until Stage 1 is fully deployed, verified and accepted.

The prematurely opened `02 — Edge Functional Composition & Deferred Capabilities` is not the canonical continuation point.

## Stage workflow invariant

Each implementation stage has its own work branch. Every stage branch begins with design/discussion before deployment:

1. review the exact functional requirements for that stage;
2. research/discuss unresolved service/product/mechanism choices for that stage;
3. explicitly accept the stage composition;
4. define the stage-scoped architecture/deployment contract and recovery path;
5. deploy;
6. verify;
7. accept and persist current state/decisions;
8. only then propose the next work branch.

A completed subtask inside a branch is not sufficient reason to leave that branch when the branch/stage scope remains incomplete.

## Functional scaffold invariant

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a broad capability scaffold, not a complete product inventory or final architecture.

- Do not infer a service/product from a capability unless an explicit ACCEPTED decision already selected it.
- Unresolved products are selected at the beginning of the implementation stage where they are needed.
- Do not preselect future-stage services simply to fill an architecture diagram.
- Already accepted products should not be re-compared without a concrete incompatibility, regression or changed requirement.

## Stable project rules

- Treat `nl-core-vds` as the historical/as-is host name and `edge` as the current target/live logical node name.
- Never rewrite the historical baseline to use target-state naming.
- Cloud Infrastructure must complement Home Infrastructure and Personal Agents Infrastructure; do not duplicate Home/PAI functionality merely because it can run on a VPS.
- Do not infer that an installed legacy service belongs in the target state, and do not infer that an unused legacy service is unnecessary.
- Do not convert a detailed proposal into accepted architecture without an explicit ACCEPTED decision.
- Preserve accepted decision chronology; do not convert hypotheses, candidates or rejected/superseded proposals into current state.
- Fresh runtime/configuration outranks historical reference for factual state.

## Accepted core application choices

Unless a later decision supersedes them, do not search for replacements for:

- Xray
- Hysteria2
- n8n
- CloudCLI
- nginx
- Stalwart + Bulwark
- Authelia
- Codex CLI
- Antigravity CLI

Authelia is intended as the common web-authentication entry point under `escloud.us`. Native application authentication may be disabled only where that operating mode is explicitly supported and does not break application/API/session semantics.

These accepted product names do not by themselves determine runtime placement, domain mapping, storage paths or all integration details; those are decided in the relevant stage.

## Knowledge/Obsidian invariant

The canonical Obsidian knowledge vault remains on `ai-node` at:

`/srv/ai-data/knowledge/obsidian`

Do not make `edge` a new canonical source of truth by assumption. The role of `edge` for Obsidian is unresolved and belongs to Stage 4 analysis. The chosen method must avoid paid Obsidian Sync and must not combine multiple primary synchronization mechanisms for the same vault.

## Files and synchronization

Filestash, SFTPGo, Syncthing, Self-hosted LiveSync/CouchDB and other file/sync implementations are **not accepted merely because they appeared in a proposal**. Evaluate unresolved choices in Stage 4 from concrete requirements, including:

- VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web browsing/editing of selected VPS files;
- cloud-agent workspaces;
- synchronization of working files/scripts and, separately, Obsidian needs.

Do not conflate task transport for cloud AI CLIs with general file synchronization.

## Private connectivity

NetBird/WireGuard or any other private-backbone mechanism is not accepted solely from a proposal. Select it in Stage 6 after the actual cross-site flows are known and validate it on the real Russia ↔ external-VPS path where relevant.
