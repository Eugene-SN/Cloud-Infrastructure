# Stage 5 — Knowledge Fabric Target Architecture Acceptance

**Timestamp:** 2026-09-19T18:01:00+03:00  
**Status:** ACCEPTED TARGET ARCHITECTURE / IMPLEMENTATION NOT STARTED  
**Project:** Cloud Infrastructure  
**Primary repository:** `Eugene-SN/Cloud-Infrastructure`

`STAGE5_KNOWLEDGE_ARCHITECTURE_ACCEPTANCE=PASS`

## Purpose

This record fixes the cross-project Knowledge Fabric target architecture so future Home Infrastructure and Personal Agents Infrastructure work can converge on the same model. It does **not** declare Stage 5 runtime deployment complete.

The accepted architecture describes PVE, `ai-node` and `edge`, while Cloud Stage 5 implementation scope is limited to `edge`. PVE/ai-node target roles are reference contracts for future work and non-regression checks.

## Fresh Stage 5 entry evidence

The expanded read-only reconciliation completed on 2026-09-19 without production mutation.

### PVE / Home

- `PVE_STAGE5_ENTRY_AUDIT=PASS`;
- canonical vault: `/srv/knowledge/obsidian`;
- backing storage: `pve/knowledge`, ext4, 32 GiB;
- canonical directory ownership: `root:knowledge-sync` mode `2775`;
- Syncthing `2.1.5`, folder ID `knowledge-obsidian`, mode `sendreceive`;
- PVE ↔ ai-node completion 100%, active connection, no conflict/versioning residue;
- CT220 consumes the canonical vault read-only;
- CT206 has no Knowledge dependency;
- CT208 Backrest `1.14.1` / Restic `0.19.1`, read-only source, accepted backup/restore and production policy.

### ai-node / PAI

- `AI_NODE_STAGE5_ENTRY_AUDIT=PASS`;
- active RW non-canonical replica: `/srv/ai-data/knowledge/obsidian`;
- Syncthing `2.1.5`, folder ID `knowledge-obsidian`, mode `sendreceive`;
- PVE peer connected, completion 100%, no conflict/versioning residue;
- n8n is a confirmed RW consumer through `/home/node/knowledge-canonical`;
- local Knowledge ownership is `eugene:pai-data`;
- the old writable SMB share `pai-knowledge` still exists but does not make ai-node canonical.

### edge / Cloud

- `EDGE_STAGE5_ENTRY_AUDIT=PASS`;
- root filesystem ext4, ~155 GiB usable, ~135 GiB free at audit time;
- Syncthing not installed/configured;
- no public Syncthing listeners or firewall rules;
- NetBird route from edge to both PVE `192.168.1.3:22000` and ai-node `192.168.1.30:22000` is reachable;
- Hermes runs as host user `core` UID/GID `1000:1000`;
- n8n container runs as numeric UID/GID `1000:1000`;
- no existing `/srv/knowledge` tree;
- no Stage 5 production mutation has occurred.

Assistant verifier failures encountered during audit were harness defects only and are not production failures.

## Accepted data topology

The Knowledge Fabric uses PVE as the canonical data/synchronization hub:

```text
ai-node active RW replica
/srv/ai-data/knowledge/obsidian
           ^
           |  existing Home LAN Syncthing
           |
           v
PVE canonical RW hub
/srv/knowledge/obsidian
           ^
           |  Syncthing over accepted edge -> Home NetBird path
           |
           v
edge active RW replica
/srv/knowledge/obsidian
```

No direct Syncthing peer between `edge` and `ai-node` is required in the accepted target.

Reason: the current edge -> Home/PAI path itself depends on CT300 hosted on PVE. If PVE is unavailable, the direct network path from edge into the Home LAN is also unavailable. A Syncthing full mesh would therefore add peer/state complexity without creating an independent failure path.

## Canonical semantics

`canonical` means:

- PVE is the authoritative administrative/recovery reference;
- PVE owns the canonical Home backup/restore policy;
- ambiguous disaster-recovery reconciliation starts from the accepted PVE canonical role.

`canonical` does **not** mean an online master required for local application operation.

Both secondary nodes remain locally usable while disconnected and accumulate local RW changes until synchronization resumes.

## Failure behavior

- edge unavailable: PVE ↔ ai-node continues;
- ai-node unavailable: PVE ↔ edge continues;
- CT300/NetBird path unavailable while PVE is otherwise alive: PVE ↔ ai-node continues; edge remains locally usable but cross-site convergence pauses;
- PVE host unavailable: ai-node and edge remain locally usable but cannot synchronize with each other under the current network topology;
- PVE Syncthing unavailable: secondary nodes remain locally usable; convergence resumes after the hub returns;
- returning nodes reconcile through Syncthing; simultaneous edits of the same file may create normal Syncthing conflict copies and must never be treated as silent merge.

## Node roles

### PVE — canonical data and recovery node

Current/accepted role:

- canonical vault `/srv/knowledge/obsidian`;
- Syncthing hub;
- Home canonical backup/restore source;
- CT220/OpenClaw canonical read-only source.

Obsidian application/runtime on PVE is **not required by this architecture and is not established by current evidence**. A future PVE UI/runtime may be evaluated separately but is not a Stage 5 requirement.

### ai-node — internal application/AI Knowledge node

Current role:

- active RW replica at `/srv/ai-data/knowledge/obsidian`;
- local Knowledge source for PAI workloads;
- n8n is already a confirmed RW consumer;
- future OCR/RAG/local-agent consumers may use the local replica directly.

Accepted future direction:

- ai-node is the preferred resource-rich host for a private Obsidian application/WebUI if such UI is deployed;
- target private DNS name may be `obsidian.lan`;
- access is intended for Home LAN and devices that reach the Home LAN through NetBird;
- this private WebUI does not make ai-node canonical and is not a public native-client synchronization endpoint.

OpenClaw on PVE keeps its current canonical read-only relationship. A direct OpenClaw -> ai-node Knowledge fallback is not required now. For n8n-driven tasks, the simpler default is for n8n to read its local ai-node replica and pass the required task context to OpenClaw.

### edge — cloud agent and external client-access data node

Stage 5 target:

- active RW non-canonical replica at `/srv/knowledge/obsidian`;
- `/srv/knowledge` owner `core:core`, mode `0755`;
- `/srv/knowledge/obsidian` owner `core:core`, mode `2775`;
- Syncthing runs under trusted Cloud account `core`;
- Hermes, Codex and Antigravity use the host path directly;
- n8n receives a RW bind mount, target path `/home/node/knowledge-canonical`;
- no Obsidian Desktop/runtime is required on edge;
- no Obsidian WebUI is deployed on edge.

Accepted future access role:

- edge is the preferred Internet-reachable data endpoint for iOS and other external client applications because it is continuously reachable without requiring users to enable NetBird;
- exact client application/protocol/access service remains unresolved and must be selected separately;
- any future public client-access service exposes only the required client protocol through the accepted edge ingress/security boundary;
- Syncthing GUI/transfer endpoints are not made public merely to support clients.

## Obsidian/runtime placement

The Knowledge tree is an Obsidian-compatible vault on all data nodes. The presence of the vault does not require the Obsidian GUI/runtime to run on every node.

Accepted placement direction:

- PVE: vault/canonical data node; no Obsidian runtime required now;
- ai-node: preferred future private Obsidian runtime/WebUI host;
- edge: no Obsidian runtime/WebUI in the current design.

This deliberately avoids Electron/browser-streaming resource cost on the resource-sensitive edge.

## Replication contract

- synchronization engine: existing Home Syncthing;
- folder ID: `knowledge-obsidian`;
- folder mode: `sendreceive`;
- PVE ↔ ai-node existing relationship remains unchanged;
- edge ↔ PVE is the Cloud extension;
- no direct edge ↔ ai-node Syncthing relationship in the accepted target;
- no second primary synchronization engine for the same server-side tree without a concrete incompatibility and explicit superseding decision;
- Syncthing GUI remains private/local;
- no public Syncthing listener is required by the architecture.

## Cloud Stage 5 mutation boundary

Cloud Stage 5 configures **edge only**.

It must not silently mutate:

- PVE storage/ownership;
- PVE Syncthing configuration;
- ai-node storage/ownership;
- ai-node Syncthing configuration;
- CT220/CT208 behavior;
- CT300/NetBird topology.

Important dependency: the audited PVE Syncthing config currently knows only ai-node. Syncthing requires the remote device/folder relationship to authorize a new edge peer. Therefore PVE-side edge Device ID registration/share is a **cross-project prerequisite**, not an edge-only mutation. It must be performed under Home Infrastructure or by a later explicit exception to this boundary. Cloud Stage 5 must stop at that gate rather than mutate PVE implicitly.

## Stage 5 acceptance intent

When the cross-project peer-registration prerequisite is satisfied, Stage 5 acceptance must prove at least:

- edge persistent RW replica exists at the accepted path;
- initial synchronization completes;
- PVE -> edge propagation works;
- edge -> PVE -> ai-node propagation works;
- controlled conflict behavior does not silently lose data;
- edge sync outage/reconnect works;
- reboot persistence works;
- Hermes can read/write the local replica;
- edge n8n can read/write the local replica;
- no public Syncthing management/transfer exposure is introduced;
- PVE/ai-node existing sync remains healthy;
- PVE canonical ownership remains unchanged;
- synthetic test artifacts are removed.

## Deferred access/UI work

The following are accepted architectural directions but are **not automatically part of current Stage 5 core acceptance**:

- selection/deployment of an Internet-facing third-party client access mechanism on edge for iOS/other external clients;
- private Obsidian WebUI on ai-node at `obsidian.lan`;
- any Obsidian runtime on PVE;
- direct OpenClaw fallback access to ai-node Knowledge.

They require their own requirements/selection work before deployment.

## Superseded scope wording

Older Cloud documents that state MacBook/iPhone/iPad Obsidian integration is completely outside Cloud Infrastructure are superseded in part:

- public/mobile client **data access via edge** is now an accepted future Cloud role;
- ai-node private Obsidian WebUI remains a PAI/Home-side future application concern;
- current Stage 5 core deployment remains edge server-side replication/data integration unless explicitly extended.

`STAGE5_KNOWLEDGE_ARCHITECTURE_ACCEPTANCE=PASS`
