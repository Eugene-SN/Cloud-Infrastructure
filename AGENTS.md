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
8. Stage-specific acceptance records relevant to the current task
9. `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` only when legacy/as-is VPS facts are needed.

## Current checkpoint invariant

Current canonical work is:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Stage 0, Stage 1 and Stage 2 are complete and accepted. `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Stage 02.5 is **research-only**. Do not deploy/install/configure a new production service, mutate production DNS/firewall/runtime, or open the next production branch until all Stage 02.5 deliverables are explicitly accepted and canonical files are updated/read back.

Current next research block is **Cross-site Connectivity Foundation**. The earlier Remaining Standalone Core Services block is complete: Hermes Agent is selected as the sole Stage 3 service.

## Current planned stage order

- Stage 3 — `03 — Edge Hermes Agent Runtime`
- Stage 4 — `04 — Edge Cross-site Connectivity Foundation`
- Stage 5 — `05 — Edge Cross-site Data & Knowledge Services`
- Stage 6 — `06 — Edge Remaining Infrastructure Services` — conditional; remove/renumber if empty at Stage 02.5 closure
- Stage 7 — `07 — Edge Backrest & Recovery`
- Stage 8 — `08 — Edge Maintenance & Update`
- Stage 9 — `09 — Edge Monitoring, Heartbeats & Alerts`
- Stage 10 — `10 — Edge Cloud Portal`
- Stage 11 — `11 — Edge Final Integrated Infrastructure Acceptance`

After Stage 11, Automation & User Workflows is a continuous post-infrastructure workstream, not an infrastructure-completion stage.

The old thematic Stage 3–7 plan is historical only.

## Stage workflow invariant

Each implementation stage has its own work branch. Every stage branch begins with design/discussion before deployment:

1. review exact requirements/baseline for that stage;
2. research only genuinely unresolved product/mechanism choices;
3. explicitly accept stage composition;
4. define the stage-scoped architecture/deployment contract and recovery path;
5. deploy;
6. verify properties, not only command RC;
7. explicitly accept and persist current state/decisions;
8. only then propose the next work branch.

A completed subtask is not sufficient reason to leave a branch while accepted scope remains incomplete.

## Functional scaffold invariant

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a capability/requirements map, not an independent product inventory or chronology source.

- Do not infer a product merely because a capability exists.
- Do not preselect services to fill architecture diagrams or empty stages.
- Already accepted products should not be re-compared without a concrete incompatibility, regression or changed requirement.
- Separate finite infrastructure services from continually evolving n8n/agent workflows.

## Stable project rules

- Treat `nl-core-vds` as historical/as-is identity and `edge` as the current live logical node.
- Never rewrite historical baseline/audit artifacts to use target-state naming.
- Cloud Infrastructure complements Home Infrastructure and PAI; do not duplicate them merely because a function can run on a VPS.
- Do not infer that an installed legacy service belongs in target state.
- Do not convert proposals/candidates into accepted architecture without an explicit accepted decision.
- Preserve decision chronology and supersession semantics.
- Fresh runtime/configuration outranks historical reference for factual state.
- Single-operator simplicity, minimum components and upstream-supported mechanisms are preferred over enterprise complexity.

## Accepted product anchors

Unless a later accepted decision supersedes them, do not search for replacements for:

- Xray
- Hysteria2
- nginx
- Authelia
- n8n
- CloudCLI
- Codex CLI
- Antigravity CLI
- Stalwart + Bulwark
- Hermes Agent

Backrest + Restic is the accepted backup-management direction. Semaphore is the accepted operational execution product.

Product acceptance does not automatically determine all runtime placement, domains, storage paths or integration details; those are stage-scoped.

## Hermes Stage 3 invariant

Stage 3 is **Hermes-only**.

Role separation:

- n8n — deterministic workflow/orchestration plane;
- Hermes — persistent cloud-side agentic reasoning/tool/delegation plane;
- CloudCLI — manual web/remote cloud-AI workspace;
- Codex CLI and Antigravity CLI — specialized executors usable manually and delegatable by Hermes;
- OpenClaw — Home/PAI-side local personal agent;
- vLLM on `ai-node` — local inference backend, integrated with Hermes only after Stage 4 connectivity.

Preferred Hermes deployment is **host-native under `core`**. Docker is not preferred because it would complicate direct reuse of existing host-native Codex/Antigravity binaries and user/runtime/auth context. Reconsider only for a concrete upstream/runtime incompatibility.

Stage 3 should verify the infrastructure path:

`n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`

Do not implement user-specific n8n/Hermes workflows in Stage 3. Do not assume a public Hermes domain/listener.

## Knowledge/Obsidian invariant

Canonical Obsidian vault remains:

`ai-node:/srv/ai-data/knowledge/obsidian`

Do not make `edge` the canonical source of truth by assumption. File/sync/Obsidian implementations are selected for Stage 5 only after Stage 4 connectivity is accepted. Avoid paid Obsidian Sync and do not combine multiple primary synchronization mechanisms for one vault.

## Files and synchronization

Filestash, SFTPGo, Syncthing, Self-hosted LiveSync/CouchDB and other file/sync implementations are candidates only until explicitly accepted.

Stage 5 requirements include as appropriate:

- VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web browsing/editing of selected VPS files;
- cloud-agent access to the same working data;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror.

Do not conflate application task transport with general file synchronization.

## Private connectivity

Stage 4 selects connectivity from real flows and real operating conditions. NetBird, direct WireGuard, authenticated HTTPS or another simple mechanism remain candidates until accepted.

Validate tunnel/private-backbone behavior on the real Russia ↔ external-VPS path where relevant. Do not choose a backbone technology first and invent uses for it later.

Connectivity means transport/reachability/endpoints. Durable application-level task retry/store-and-forward is a later workflow concern.

## Lifecycle ordering invariants

- Backrest restore capability must be accepted before Semaphore/update testing.
- `update.escloud.us` is a dedicated maintenance/update page, separate from `app.escloud.us`, and is built as a separate Codex substage after the real backend contract is known.
- Production monitoring is deployed after the substantially complete service inventory, cross-site connectivity, Backrest and update subsystem exist.
- `app.escloud.us` is built as a separate Codex substage after monitoring/status sources and final service inventory are accepted.
- Final infrastructure acceptance follows all selected services, connectivity/data integration, backup/restore, maintenance/update, monitoring, portal and cleanup.