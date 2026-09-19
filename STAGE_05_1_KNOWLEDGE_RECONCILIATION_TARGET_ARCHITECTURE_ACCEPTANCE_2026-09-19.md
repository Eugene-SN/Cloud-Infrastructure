# 05.1 — Cross-project Knowledge Reconciliation & Target Architecture

**Date:** 2026-09-19  
**Status:** COMPLETE / ACCEPTED / RESEARCH-ARCHITECTURE ONLY  
**Project:** Cloud Infrastructure  
**Primary repository:** `Eugene-SN/Cloud-Infrastructure`

`STAGE05_1_KNOWLEDGE_RECONCILIATION_TARGET_ARCHITECTURE=PASS`

## Purpose

Stage 5 is intentionally split across two Cloud Infrastructure work branches to keep implementation context bounded:

- **05.1 — Cross-project Knowledge Reconciliation & Target Architecture** — read-only reconciliation, architecture, role definition and implementation planning;
- **05.2 — Edge Knowledge Replication & Data Integration** — runtime deployment, cross-project integration, verification and final Stage 5 acceptance.

05.1 performs no production mutation.

## Supersession note

This record supersedes only the overly restrictive mutation-boundary wording in the earlier intermediate record:

`STAGE_05_KNOWLEDGE_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`

The earlier statement that Cloud Stage 5 must mutate **edge only** is not the intended rule.

Correct interpretation:

- Stage 5 / branch 05.2 is centered on deploying and integrating the new edge Knowledge node;
- PVE may be inspected and changed where required for the planned edge ↔ PVE integration, Syncthing peer/folder authorization, topology correctness, verification and non-regression;
- ai-node is **not redesigned** in Stage 5 and does not receive the future Obsidian WebUI in this stage;
- OpenClaw behavior/integration on PVE is **not redesigned** in Stage 5;
- unrelated Home/PAI redesign remains out of scope.

All other accepted architectural content from the earlier record remains valid unless this record states otherwise.

## Fresh reconciliation evidence

The expanded read-only cross-project audit completed before architecture acceptance.

### PVE / Home

- `PVE_STAGE5_ENTRY_AUDIT=PASS`;
- canonical vault `/srv/knowledge/obsidian`;
- backing storage `pve/knowledge`, ext4, 32 GiB;
- Syncthing `2.1.5`, folder ID `knowledge-obsidian`, `sendreceive`;
- PVE ↔ ai-node active, 100% completion, no conflict/versioning residue;
- CT220 canonical Knowledge consumption read-only;
- CT206 no current Knowledge dependency;
- CT208 Backrest/Restic Knowledge backup/restore policy verified.

### ai-node / PAI

- `AI_NODE_STAGE5_ENTRY_AUDIT=PASS`;
- active RW non-canonical replica `/srv/ai-data/knowledge/obsidian`;
- Syncthing `2.1.5`, healthy PVE relationship;
- n8n confirmed RW consumer through `/home/node/knowledge-canonical`;
- current local ownership/PAI runtime preserved.

### edge / Cloud

- `EDGE_STAGE5_ENTRY_AUDIT=PASS`;
- no current Syncthing installation or Knowledge tree;
- no public Syncthing listeners/rules;
- sufficient local ext4 capacity;
- edge can reach PVE and ai-node TCP/22000 over the accepted NetBird/Home path;
- Hermes runs as `core` UID/GID `1000:1000`;
- n8n runs as numeric UID/GID `1000:1000`.

Assistant verifier failures during the audit were test-harness defects only; no production failure or mutation occurred.

## Accepted Knowledge Fabric topology

```text
ai-node active RW replica
/srv/ai-data/knowledge/obsidian
           ^
           | existing Home LAN Syncthing
           |
           v
PVE canonical RW hub
/srv/knowledge/obsidian
           ^
           | Syncthing over accepted edge -> Home path
           |
           v
edge active RW replica
/srv/knowledge/obsidian
```

PVE remains the canonical administrative/recovery authority and the Syncthing hub.

A direct edge ↔ ai-node Syncthing relationship is not required in the accepted topology because current edge -> Home/PAI reachability itself depends on CT300 hosted on PVE. If the PVE host is unavailable, edge loses that Home LAN route as well; nominal Syncthing full mesh would not create an independent physical/network failure path.

## Canonical semantics

PVE being canonical means:

- authoritative administrative/recovery reference;
- canonical Home backup/restore authority;
- hub used to reconcile the distributed Knowledge Fabric.

It does **not** mean ai-node or edge require PVE online for local application use. Secondary replicas remain locally RW and continue local workload operation while disconnected; cross-node convergence resumes when connectivity returns.

## Node roles

### PVE — canonical Knowledge/data/recovery hub

Current/accepted:

- canonical RW vault `/srv/knowledge/obsidian`;
- Syncthing hub;
- canonical Home Knowledge backup/restore source;
- CT220/OpenClaw canonical read-only Knowledge source.

Stage 5 / 05.2 may inspect and change PVE **where required to integrate edge correctly**, including:

- register/authorize edge Syncthing Device ID;
- share `knowledge-obsidian` with edge;
- make narrowly required Syncthing configuration changes for the accepted topology;
- verify canonical ownership, peer health, propagation and non-regression.

Stage 5 does **not** redesign OpenClaw or its accepted Knowledge relationship.

Obsidian application/runtime on PVE is not required by the current target and is not established by current evidence. It may be considered separately in the future.

### ai-node — secondary internal application/AI node

Current/accepted:

- active RW replica `/srv/ai-data/knowledge/obsidian`;
- n8n current RW consumer;
- local Knowledge source for future OCR/RAG/local-agent/PAI consumers.

Stage 5 preserves this runtime and performs only the checks necessary to prove end-to-end propagation/non-regression. It does **not** redesign ai-node.

Accepted future direction, outside Stage 5:

- ai-node is the preferred resource-rich host for a private Obsidian runtime/WebUI;
- possible private DNS endpoint `obsidian.lan`;
- access for LAN and NetBird-routed Home clients;
- no requirement for public native-client synchronization to ai-node.

OpenClaw direct fallback access to ai-node Knowledge is only a possible future option. Current simpler task flow remains: n8n reads local ai-node Knowledge and supplies required context to OpenClaw when invoking it.

### edge — secondary cloud/agent and future external-access node

Stage 5 / 05.2 target:

- active RW non-canonical replica `/srv/knowledge/obsidian`;
- `/srv/knowledge` = `core:core 0755`;
- `/srv/knowledge/obsidian` = `core:core 2775`;
- Syncthing runtime under trusted user `core`;
- Hermes, Codex and Antigravity direct RW host-path access;
- n8n RW bind target `/home/node/knowledge-canonical`;
- no Obsidian Desktop/runtime on edge;
- no Obsidian WebUI on edge;
- no public Syncthing management/transfer exposure.

Accepted future direction, **documented now but not implemented in Stage 5**:

- edge is the preferred Internet-reachable Knowledge/data access endpoint for iOS, macOS and Windows client applications because it is reachable from anywhere without requiring those clients to enable NetBird;
- exact third-party client, protocol and server-side access mechanism remains unresolved and requires separate requirements/research;
- future client access must use a dedicated client-facing mechanism and must not be implemented by exposing Syncthing publicly.

## Failure behavior

- edge unavailable: PVE ↔ ai-node continues;
- ai-node unavailable: PVE ↔ edge continues;
- edge↔Home NetBird/CT300 path unavailable while PVE remains alive: PVE ↔ ai-node continues; edge stays locally usable and accumulates changes;
- PVE host unavailable: ai-node and edge remain locally usable but cannot synchronize with each other under the current network topology;
- returning connectivity resumes normal reconciliation;
- simultaneous modifications of the same file on disconnected RW replicas may create standard Syncthing conflict copies; Stage 5 must test this without silent data loss.

## Stage 5 implementation boundary

05.2 implements the accepted server-side Knowledge Fabric integration.

Allowed scope:

- all edge deployment/configuration required by the target;
- PVE inspection and narrowly required PVE changes for edge Syncthing integration;
- PVE/ai-node verification and non-regression testing;
- end-to-end propagation through PVE to ai-node.

Explicitly excluded from Stage 5 implementation:

- redesign/reconfiguration of ai-node application architecture;
- deployment of the future ai-node Obsidian WebUI;
- redesign of OpenClaw or its current PVE Knowledge relationship;
- implementation of future iOS/macOS/Windows access through edge;
- unrelated Home/PAI service redesign;
- edge Knowledge backup policy deployment, which remains Stage 6.

## Stage 5 final acceptance intent

05.2 must prove at minimum:

- accepted edge persistent path/ownership;
- edge Syncthing runtime and persistence;
- PVE↔edge device/folder relationship;
- initial convergence;
- PVE -> edge propagation;
- edge -> PVE propagation;
- edge -> PVE -> ai-node propagation;
- Hermes RW;
- edge n8n RW;
- controlled conflict behavior without silent loss;
- controlled outage/reconnect;
- reboot persistence;
- no public Syncthing exposure;
- existing PVE↔ai-node relationship remains healthy;
- canonical PVE ownership remains correct;
- no unintended OpenClaw/ai-node redesign;
- synthetic test artifacts removed;
- repository persistence/read-back.

## Branch chronology

- **05.1 — Cross-project Knowledge Reconciliation & Target Architecture**: COMPLETE / ACCEPTED.
- **05.2 — Edge Knowledge Replication & Data Integration**: NEXT; implementation branch/chat after operator approves the proposed substage plan.

`STAGE05_1_KNOWLEDGE_RECONCILIATION_TARGET_ARCHITECTURE=PASS`
