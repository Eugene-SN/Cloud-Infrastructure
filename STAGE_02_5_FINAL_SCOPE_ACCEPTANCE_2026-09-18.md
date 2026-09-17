# Stage 02.5 — Final Scope Acceptance

**Date:** 2026-09-18  
**Status:** ACCEPTED  
**Runtime mutation:** NO

## Purpose

This record closes `02.5 — Remaining Functional Scope Reconciliation & Research` and defines the final dependency-aware scope before Stage 3 opens.

Stage 02.5 remains a planning/research checkpoint only. It performed no Cloud production deployment.

## Final capability disposition

| Capability | Disposition | Deployment / ownership |
|---|---|---|
| Cross-site private connectivity | **SELECTED / REUSE EXISTING** — self-hosted NetBird | Cloud Stage 3; Home CT300 remains the routing/control-plane foundation |
| Cloud agent runtime | **SELECTED** — Hermes Agent | Cloud Stage 4 |
| Local inference for Hermes | **SELECTED dependency** — existing `ai-node` vLLM | private exposure/integration in Cloud Stage 4 after Stage 3 |
| Canonical Obsidian / knowledge storage | **MOVED TO HOME INFRASTRUCTURE OWNERSHIP** | Home Infrastructure designs, deploys and accepts the PVE canonical knowledge foundation |
| `edge` knowledge role | **SELECTED ROLE** — active synchronized working replica / producer, not canonical authority | Cloud Stage 5 after fresh cross-project audit |
| Server-side knowledge synchronization mechanism | **REUSE HOME ACCEPTED MECHANISM BY DEFAULT** | selected/accepted in Home Infrastructure; Cloud Stage 5 verifies compatibility before extending it to `edge` |
| Apple-device Obsidian integration | **REMOVED FROM CLOUD SCOPE** | separate late Home Infrastructure user-integration stage after core infrastructure/workflow work |
| Working-file/web-file product on `edge` | **NOT PRESELECTED** | add only if Stage 5 audit proves a concrete Cloud-side requirement not already met by the accepted Home/data architecture |
| Backrest + Restic | **SELECTED DIRECTION** | Cloud Stage 6; exact repository/off-site topology is stage-specific |
| Semaphore + maintenance/update workflow | **SELECTED** | Cloud Stage 7 |
| `update.escloud.us` | **SELECTED UI RESPONSIBILITY** | separate Codex substage inside Stage 7 after backend contract exists |
| Monitoring / heartbeats / alerts | **DEFERRED TO DEDICATED INFRASTRUCTURE STAGE** | Cloud Stage 8; product/topology research occurs against the real deployed inventory |
| `app.escloud.us` portal | **SELECTED LATE PRESENTATION LAYER** | Cloud Stage 9 after monitoring/status sources exist |
| Password/2FA service | **DEFERRED / OPTIONAL** | not part of finite Cloud build without a changed requirement; 2FAuth remains rejected |
| Messaging/bot frontend | **DEFERRED TO USER WORKFLOWS** | post-infrastructure unless a dedicated infrastructure dependency later appears |
| RSS/feed automation | **REUSE n8n / workflow layer** | post-infrastructure |
| Website/document change detection | **DEFERRED TO WORKFLOWS** | use n8n first; add a dedicated product only if a real workflow proves it necessary |
| Bounded AI research/search/capture utilities | **DEFERRED TO WORKFLOWS** | no standalone SearXNG/Karakeep-style service by assumption |
| Generic server-control UI such as Portainer/Cockpit | **REJECTED** | no duplicate control plane |
| Limited secondary/failover Cloud endpoint | **DEFERRED** | only with a concrete later failure requirement |

## Knowledge ownership boundary

The previous Cloud planning assumption that `ai-node:/srv/ai-data/knowledge/obsidian` permanently remains canonical is superseded as a **future architecture constraint**.

Current runtime is not rewritten by this planning decision: until Home Infrastructure completes and accepts its migration, the existing `ai-node` vault remains the factual current source.

The accepted cross-project direction is:

```text
Home Infrastructure
    PVE 24/7
    canonical live knowledge host / synchronization hub
              ^
              |
      accepted server-side sync
        /                 \
       /                   \
PAI / ai-node            Cloud / edge
active RW replica        active RW replica
local AI producer        24/7 cloud producer
```

Ownership after Home-side acceptance:

- **Home Infrastructure** owns PVE canonical storage layout, PVE-side sync service, Home consumers and Home-side backup integration.
- **Personal Agents Infrastructure** owns the `ai-node` active RW replica and local n8n/OpenClaw/vLLM/OCR/RAG consumers/producers.
- **Cloud Infrastructure** owns the `edge` active RW replica and n8n/Hermes/cloud-AI producer/consumer integration.

Cloud does not redesign or independently duplicate the Home canonical storage service.

## Stage 5 mandatory entry audit

Cloud Stage 5 must begin with an **expanded read-only cross-project audit**. It must not rely on the Stage 02.5 planning hypothesis or on stale memory of the Home branch.

Before any synchronization mutation, Stage 5 must establish the fresh accepted state of:

### Home / PVE

- whether the PVE canonical knowledge migration has reached explicit Home acceptance;
- exact canonical filesystem/path and backing SSD/LV/filesystem;
- capacity and filesystem health relevant to the knowledge dataset;
- ownership, permissions and application-facing mount/export semantics;
- selected and currently running server-side synchronization mechanism, version and service placement;
- peer identity/configuration model and conflict/versioning behavior;
- current PVE ↔ `ai-node` synchronization status and health;
- behavior during peer outage/reconnect if already accepted by Home;
- CT206/file-access integration only where it remains relevant;
- CT208/Backrest protection of canonical knowledge and verified restore state;
- PVE/CT300/NetBird dependency and private route/DNS state required to reach the Cloud side.

### Personal Agents Infrastructure / `ai-node`

- exact local replica path;
- current sync service/peer configuration;
- replica health and last-known synchronization state;
- local ownership/permissions expected by n8n/OpenClaw/vLLM/OCR/RAG workloads;
- any producer-side conventions for drafts/exchange/canonical knowledge;
- evidence that `ai-node` is an active synchronized replica rather than the current canonical source after Home cutover.

### Cloud / `edge`

- Stage 3 NetBird routing/DNS acceptance remains non-regressed;
- Stage 4 Hermes and local-vLLM integration remains non-regressed;
- storage capacity and persistent path suitable for the `edge` replica;
- which Cloud services require RO vs RW access;
- whether a full replica or a bounded subset is justified by the accepted Home synchronization mechanism and actual workflows.

If the Home PVE canonical migration is not yet accepted when Cloud Stage 5 begins, Stage 5 must **stop before mutation** and reconcile the dependency instead of inventing a parallel canonical/sync architecture.

## Stage 5 implementation principle

Stage 5 is an integration stage, not a second knowledge-platform design project.

Default behavior:

1. audit the fresh Home/PAI contract;
2. reuse the accepted Home server-side sync mechanism when compatible;
3. add `edge` as a Cloud-side active RW replica/producer;
4. expose only the minimum required local paths to n8n/Hermes/tools;
5. verify bidirectional propagation, conflict behavior, outage/reconciliation and reboot persistence;
6. verify Home/PAI/Cloud non-regression;
7. do not add another primary synchronization engine for the same knowledge tree without a concrete incompatibility and an explicit superseding decision.

## Apple-device integration

MacBook/iPhone/iPad Obsidian synchronization is completely removed from the Cloud Infrastructure research and deployment matrix.

It belongs to a later, separate Home Infrastructure user-integration branch after the PVE canonical knowledge foundation and the main infrastructure/user-workflow layers exist. That future branch may independently research, test, select and deploy the then-current best Apple/Obsidian access mechanism.

Cloud Stage 5 must not select Self-hosted LiveSync/CouchDB, Remotely Save/WebDAV, iOS Syncthing clients or another user-device mechanism merely to satisfy Apple-device access.

## Final normalized Cloud roadmap

The conditional old Stage 6 slot is empty after final capability reconciliation and is removed before Stage 3 opens.

Final finite infrastructure stages:

1. **Stage 3 — Edge Cross-site Connectivity Foundation**
2. **Stage 4 — Edge Hermes Agent Runtime**
3. **Stage 5 — Edge Knowledge Replication & Data Integration**
4. **Stage 6 — Edge Backrest & Recovery**
5. **Stage 7 — Edge Maintenance & Update**
6. **Stage 8 — Edge Monitoring, Heartbeats & Alerts**
7. **Stage 9 — Edge Cloud Portal**
8. **Stage 10 — Edge Final Integrated Infrastructure Acceptance**

After Stage 10, user-specific n8n/Hermes/agent automation remains a continuous post-infrastructure workstream.

Apple-device/Obsidian integration is not a Cloud post-infrastructure stage; it belongs to Home Infrastructure.

## Stage 02.5 closure gates

- reconciled remaining capability inventory: **PASS**;
- disposition for unresolved capability families: **PASS**;
- normalized remaining service/product inventory: **PASS**;
- dependency order: **PASS**;
- final stage names/numbers/scopes: **PASS**;
- Backrest / maintenance / monitoring / portal / final acceptance placement: **PASS**;
- Apple-device integration project boundary: **PASS**;
- Stage 5 expanded cross-project audit requirement: **PASS**;
- intentionally unresolved implementation details are stage-specific rather than Stage 02.5 blockers: **PASS**.

`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`
