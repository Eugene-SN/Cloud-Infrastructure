# Cloud Infrastructure — Architecture State

## Status

**Architecture status:** INCREMENTAL / STAGE-SCOPED DESIGN IN PROGRESS.

There is currently **no accepted full target Architecture Contract** for all Cloud Infrastructure stages.

The project has an accepted substrate, a preliminary global functional scaffold, several explicitly accepted product anchors, and unresolved service/product choices that must be decided only when their implementation stage begins.

This file records only current accepted architecture facts/invariants and the design process. It must not be used to preselect products for future stages.

## Current canonical checkpoint

Current implementation work remains in:

`01 — Edge Clean Rebuild & Base Platform Deployment`

Stage 1 is **IN PROGRESS**.

Completed/accepted subset:

- clean Ubuntu substrate;
- node identity `edge` / `edge.escloud.us`;
- provider networking in its current working form;
- key-only SSH with accepted `ssh.socket` activation;
- minimal architecture-independent host bootstrap;
- persistent journald-use ceiling `500M`.

Not yet complete:

- the Stage 1 requirements review;
- the complete Stage 1 service/product composition;
- the Stage 1 scoped architecture/deployment contract;
- the remaining Base Platform deployment and acceptance.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them without a concrete requirement.
2. `edge` must become independently useful before Home/PAI connectivity becomes a dependency.
3. Home/PAI integration remains a late implementation stage.
4. The historical `nl-core-vds` deployment is migration/reference context, not the target architecture.
5. Fresh runtime/configuration outranks historical reference when factual state differs.
6. The canonical Obsidian filesystem vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes it.
7. VPN/DPI-bypass functionality and any future private infrastructure backbone are separate concerns.
8. Single-operator simplicity is preferred over enterprise-style complexity without a demonstrated need.
9. Unresolved service/product choices are selected stage-by-stage, not globally precommitted in advance.

## Accepted global product anchors

The following product choices are already accepted and should not be replaced merely to reopen comparison work unless a concrete incompatibility or changed requirement appears:

- Xray;
- Hysteria2;
- nginx;
- n8n;
- CloudCLI;
- Stalwart + Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI.

Additional accepted directions:

- Backrest using Restic as the future backup-management direction;
- a dedicated Cloud Infrastructure portal replacing Homepage;
- maintenance page + Semaphore replacing the legacy custom Maintenance Center.

These are product/direction anchors only. They do **not** constitute a complete runtime topology, domain map, storage layout, authentication map or deployment contract.

## Global functional scaffold boundary

`FUNCTIONAL_SCAFFOLD_DRAFT.md` describes the broad capability set the final `edge` may need.

It deliberately leaves many products/mechanisms unresolved, including examples such as:

- file/storage access implementation;
- synchronization technology and Syncthing role;
- exact Obsidian synchronization mechanism;
- monitoring/notification implementation;
- Hermes role;
- messaging/bot frontend;
- private/site-to-site connectivity mechanism;
- selected off-site DR topology;
- other adjacent products not explicitly accepted in `DECISIONS.md`.

Do not convert scaffold candidates into architecture facts until the corresponding stage performs requirements review, product selection and explicit acceptance.

## Stage-scoped architecture model

Each implementation stage produces only the architecture needed for that stage.

Required sequence inside a stage:

1. review stage requirements;
2. select unresolved services/products/mechanisms;
3. accept the stage composition;
4. define a stage-scoped architecture/deployment contract;
5. deploy;
6. verify and accept;
7. persist the resulting accepted architecture here and in the decision/state documents.

Later stages may extend the architecture without invalidating already accepted earlier-stage contracts unless an explicit superseding decision is made.

## Stage 1 architecture work still required

Before remaining Base Platform deployment, branch `01` must resolve only the Stage 1 questions that are actually needed, including as applicable:

- target firewall policy/implementation;
- whether/where Docker + Compose is required for Stage 1;
- normalized persistent-directory/ownership conventions;
- nginx ingress model;
- TLS/ACME and certificate-consumer mechanics;
- Xray/Hysteria2 restoration/adaptation details;
- public decoy page implementation;
- Authelia deployment/integration details;
- initial private Cloud page implementation;
- base-state backup implementation;
- extension boundaries reserved for later APIs/webhooks/storage/monitoring/Home-PAI integration.

Some products here are already globally accepted; the open work is their Stage 1 implementation contract, not replacement research.

## Explicitly withdrawn premature proposal

The previous current-tree `ARCHITECTURE.md` proposal attempted to predefine future-stage details such as specific file/sync products, private-backbone preference, domain map, runtime placement and service topology before those stages had performed their required requirements/product-selection work.

That proposal is **withdrawn from current authority**. Git history preserves it for reference, but none of its unaccepted future-stage selections should be treated as current decisions.

Examples of choices that are **not accepted merely because they appeared in that proposal** include:

- SFTPGo as the final file layer;
- Self-hosted LiveSync + CouchDB as the final Obsidian sync mechanism;
- Syncthing as a selected general sync service;
- NetBird as the selected private backbone;
- the proposed complete domain map;
- the proposed complete Compose-project/runtime topology;
- the proposed future-stage authentication/port/path map.

Those topics return to unresolved status unless independently supported by an explicit ACCEPTED decision in `DECISIONS.md`.

## Architecture authority

For any implementation step, authority order is:

1. current user instruction;
2. latest applicable ACCEPTED decision;
3. `CURRENT_STATE.md` for confirmed current stage/runtime state;
4. this file for already accepted architecture/invariants;
5. `FUNCTIONAL_SCAFFOLD_DRAFT.md` for high-level capability intent;
6. `migration-reference/` and historical baseline for legacy implementation evidence only.

Do not deploy from a proposal simply because it is detailed.
