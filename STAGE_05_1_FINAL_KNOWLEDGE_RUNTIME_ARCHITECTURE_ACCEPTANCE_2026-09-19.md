# 05.1 — Final Knowledge Runtime Architecture Acceptance

**Date:** 2026-09-19  
**Status:** COMPLETE / ACCEPTED / SUPERSEDING TARGET ARCHITECTURE  
**Project:** Cloud Infrastructure  
**Primary repository:** `Eugene-SN/Cloud-Infrastructure`

`STAGE05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE=PASS`

## Purpose

This record is the latest applicable Stage 05.1 architecture decision. It preserves the accepted PVE-centered Knowledge Fabric and refines runtime placement and Stage 5 execution after the PVE resource-readiness audit.

It supersedes conflicting runtime-placement and Stage-branch wording in:

- `STAGE_05_KNOWLEDGE_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_1_KNOWLEDGE_RECONCILIATION_TARGET_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`.

Historical audit evidence and non-conflicting topology/path decisions remain valid.

## Fresh PVE resource evidence

`PVE_OBSIDIAN_RESOURCE_READINESS_AUDIT=PASS`.

Confirmed PVE runtime at acceptance time:

- CPU: Intel Core i3-N305, 8 physical cores / 8 CPUs, up to 3.8 GHz;
- RAM: ~15 GiB total, ~8.8 GiB used, ~6.5 GiB available;
- swap: 8 GiB total, ~2.4 GiB used, ~5.6 GiB free;
- load average around 0.6–1.0 during the audit;
- PVE manager: `9.2.20`;
- canonical Knowledge storage remains the dedicated `pve/knowledge` 32 GiB ext4 LV mounted at `/srv/knowledge`.

The current 8 GiB host swap is sufficient for the accepted Obsidian LXC target. No PVE host swap expansion is planned in Stage 05.2 merely because root storage has free capacity. Revisit host swap only if fresh post-deployment evidence shows real memory pressure or swap exhaustion.

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

No direct edge ↔ ai-node Syncthing peer is required under the current topology because edge -> Home/PAI reachability itself depends on CT300 hosted on PVE.

## Final runtime roles

### PVE — canonical Knowledge + full Obsidian application node

PVE owns:

- canonical RW vault `/srv/knowledge/obsidian`;
- Syncthing hub;
- canonical administrative/recovery authority;
- primary Home Backrest/Restic Knowledge recovery chain;
- CT220/OpenClaw canonical read-only Knowledge source.

Stage 05.2 adds a dedicated lightweight LXC whose role is the **single full server-side Obsidian application runtime** for the canonical vault.

Accepted LXC resource target:

| Resource | Target |
|---|---:|
| CPU | 1 vCPU |
| RAM | 1024 MiB |
| LXC swap limit | 512 MiB |
| rootfs | ~4 GiB |
| onboot | yes |

The canonical vault remains on the existing dedicated PVE Knowledge LV. It is bind-mounted RW into the Obsidian LXC; it must not be copied into or made dependent on the LXC rootfs.

The LXC provides:

- full Obsidian runtime against the canonical vault;
- Obsidian File Recovery;
- Obsidian index/metadata model;
- Obsidian CLI availability where supported by the running app;
- core plugins and future explicitly selected plugins;
- private browser-access UI at `obsidian.lan`.

`obsidian.lan` is private Home/NetBird access only. Stage 05.2 does not create a public Internet Obsidian UI.

### Obsidian runtime packaging inside the LXC

**Placement is accepted; packaging mechanism remains a Stage 05.2 design gate.**

Current preference is to avoid unnecessary nested containerization, but native Linux installation is not assumed superior without verification because browser access still requires a display/streaming layer.

Stage 05.2 must compare:

1. official native Obsidian Linux package/AppImage + native Selkies/session management;
2. LinuxServer Obsidian/Selkies container inside the dedicated LXC.

Select the simpler, better-supported and easier-to-update stable path. Do not choose native merely for aesthetic purity if it requires more custom display/session plumbing. No full desktop environment is required.

### ai-node — secondary PAI/application replica

ai-node remains:

- active RW non-canonical replica `/srv/ai-data/knowledge/obsidian`;
- local Knowledge source for n8n;
- future OCR/RAG/local-agent/AI consumers.

No server-side Obsidian runtime or Obsidian WebUI is planned on ai-node by default after this decision.

Stage 5 does not redesign ai-node. Existing n8n and future PAI consumers continue using the local replica.

OpenClaw keeps its current PVE canonical read-only Knowledge relationship. Direct OpenClaw fallback to ai-node remains optional future work and is not a Stage 5 requirement.

### edge — secondary Cloud/agent + future external client-access node

Stage 05.3 target:

- active RW non-canonical replica `/srv/knowledge/obsidian`;
- Hermes/Codex/Antigravity direct local access;
- edge n8n RW bind at `/home/node/knowledge-canonical`;
- no Obsidian WebUI;
- no Obsidian runtime in Stage 5.

Future accepted direction:

- edge is the global Internet-reachable Knowledge access endpoint for iOS, macOS, Windows and Android clients;
- exact third-party application/protocol/access service remains unresolved;
- external client-access implementation is not part of Stage 5;
- a future lightweight edge Obsidian runtime remains **conditional**, only if the selected client mechanism or an explicitly required edge-local File Recovery/API/index/plugin use case needs a running Obsidian process;
- do not expose Syncthing publicly as the client-access mechanism.

## Recovery model

Accepted layering:

```text
Live data:
  PVE canonical + ai-node replica + edge replica

Short-term Obsidian-native recovery:
  PVE full Obsidian runtime / File Recovery

Primary durable Knowledge recovery:
  PVE canonical Backrest/Restic chain

Additional independent/off-site protection:
  handled by accepted/future backup stages where justified
```

File Recovery complements rather than replaces Restic. Live replicas are availability/synchronization copies and are not treated as backups.

## Stage 5 branch structure

Stage 5 is now split into exactly three work branches:

### 05.1 — Cross-project Knowledge Reconciliation & Target Architecture

**Status: COMPLETE / ACCEPTED.**

Owns:

- cross-project audits;
- topology and role reconciliation;
- runtime placement decisions;
- Stage 5 architecture and sequencing.

### 05.2 — PVE Canonical Obsidian Runtime & WebUI

**Status: NEXT / IMPLEMENTATION NOT STARTED.**

Owns:

1. targeted PVE pre-mutation verification and recovery path;
2. creation of the new lightweight LXC;
3. accepted initial resource envelope: 1 vCPU / 1024 MiB RAM / 512 MiB swap / ~4 GiB rootfs / onboot;
4. RW bind mount of the existing canonical vault from `/srv/knowledge/obsidian`;
5. deployment-method design gate: native Obsidian+Selkies vs LinuxServer Obsidian/Selkies;
6. installation of current stable Obsidian full runtime;
7. persistent Obsidian state and canonical vault opening;
8. File Recovery verification;
9. Obsidian index/CLI/core-plugin verification;
10. private WebUI at `obsidian.lan`, reachable from Home LAN and NetBird-routed Home clients;
11. reboot persistence and real idle/active/reindex resource measurements;
12. PVE Syncthing, CT208 Backrest and CT220/OpenClaw non-regression;
13. cleanup and repository acceptance/read-back.

No ai-node redesign and no public external-client access is performed here.

### 05.3 — Edge Knowledge Replication & Data Integration

**Status: PLANNED / IMPLEMENTATION NOT STARTED.**

Owns all previously planned edge deployment work:

1. edge persistent Knowledge paths/ownership;
2. edge Syncthing deployment;
3. PVE ↔ edge Device ID/folder integration;
4. initial convergence;
5. Hermes/Codex/Antigravity local Knowledge access;
6. edge n8n RW bind/integration;
7. PVE -> edge, edge -> PVE and edge -> PVE -> ai-node propagation acceptance;
8. controlled conflict/outage/reconnect behavior;
9. edge reboot persistence;
10. no public Syncthing exposure;
11. PVE↔ai-node and OpenClaw non-regression;
12. synthetic-data cleanup and final Stage 5 acceptance.

Explicitly excluded from 05.3:

- external iOS/macOS/Windows/Android client-access implementation;
- edge Obsidian runtime unless a later accepted client-access design requires it;
- edge Obsidian WebUI;
- ai-node Obsidian runtime/WebUI;
- OpenClaw redesign;
- Stage 6 edge backup deployment.

## Acceptance marker

`STAGE05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE=PASS`
