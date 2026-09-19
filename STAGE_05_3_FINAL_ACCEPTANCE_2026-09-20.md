# Stage 05.3 — Edge Knowledge Replication & Data Integration — Final Acceptance

**Date:** 2026-09-20  
**Status:** COMPLETE / ACCEPTED  
**Stage 5 status:** COMPLETE / ACCEPTED

**Acceptance markers:**

- `STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS`
- `STAGE05_FINAL_ACCEPTANCE=PASS`

## Scope

Stage 05.3 completed the edge Knowledge replica and Cloud-side consumer integration while preserving the accepted PVE-centered Knowledge topology and the existing ai-node replica.

No edge Obsidian runtime/WebUI was introduced. No public Syncthing exposure was introduced.

## Final topology

```text
ai-node RW replica
/srv/ai-data/knowledge/obsidian
           ^
           | Syncthing
           v
PVE authoritative Knowledge hub
/srv/knowledge/obsidian
           ^
           | Syncthing over accepted edge -> Home route
           v
edge RW replica
/srv/knowledge/obsidian
```

No direct edge ↔ ai-node Syncthing peer exists.

## edge filesystem and Syncthing runtime

Accepted edge filesystem:

- `/srv/knowledge` — `core:core 0755`;
- `/srv/knowledge/obsidian` — `core:core 2775`.

Syncthing:

- version `2.1.5`;
- upstream `stable-v2` package channel;
- service `syncthing@core.service`;
- enabled and reboot-persistent;
- edge Device ID: `DPBP3KW-L5BEWJM-RPDDHO2-ON5AYFR-VEE4TP5-NOIOOES-NGJ3D4R-VJFXQAE`;
- PVE Device ID: `I6IHLDJ-2E2SH2D-RREAJIY-VFP7TG5-N4DKRDR-GDIUQHA-P2NHQ3O-MR4WOAY`;
- PVE dial target from edge: `tcp://192.168.1.3:22000`;
- folder ID `knowledge-obsidian`;
- folder type `sendreceive`;
- watcher enabled with 1 s delay;
- rescan interval 3600 s;
- `ignorePerms=false`;
- GUI/API `127.0.0.1:8384`;
- listener `127.0.0.1:22000`;
- global discovery disabled;
- local discovery disabled;
- relays disabled;
- NAT traversal disabled.

PVE authorizes the edge Device ID and shares the existing `knowledge-obsidian` folder. Existing PVE/ai-node device and folder configuration passed non-regression checks.

## Consumer integration

### Host consumers

Hermes, Codex and Antigravity run under `core` and use the local edge path directly:

`/srv/knowledge/obsidian`

No alias, symlink, API layer or extra mount is required.

### n8n

Container user `node` is UID/GID `1000:1000`.

Accepted bind:

`/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`

The earlier planning alias `/home/node/knowledge-canonical` was not deployed and is superseded.

n8n remained healthy after recreation and after full edge reboot. The existing private network remained unchanged:

- Docker network `n8n_hermes`;
- Linux bridge `n8n-hermes`;
- subnet `172.19.0.0/16`;
- gateway `172.19.0.1`.

## Propagation acceptance

Verified live:

- PVE → edge = PASS;
- edge → PVE = PASS;
- edge → PVE → ai-node = PASS;
- propagated synthetic deletion to edge = PASS;
- propagated synthetic deletion to ai-node = PASS.

## Outage and conflict acceptance

A controlled test stopped only edge Syncthing after a common baseline existed.

During the outage:

- edge wrote `STAGE05_3_CONFLICT_EDGE_VERSION`;
- PVE independently wrote `STAGE05_3_CONFLICT_PVE_VERSION`.

After edge Syncthing restart:

- PVE reconnection passed;
- the main file contained the PVE version;
- a `sync-conflict` file preserved the edge version;
- both versions were present on edge and PVE;
- folder convergence returned to idle with no pending items/pull errors;
- synthetic conflict artifacts were removed;
- cleanup propagated to edge and ai-node.

Whether the conflict-copy itself reached ai-node before cleanup was not directly captured and remains **UNKNOWN**. Normal edge → PVE → ai-node propagation was independently verified.

Markers:

- `CONTROLLED_EDGE_OUTAGE_RECOVERY=PASS`;
- `SYNCTHING_CONFLICT_PRESERVATION=PASS`;
- `EDGE_POST_OUTAGE_CONVERGENCE=PASS`;
- `STAGE05_3_OUTAGE_CONFLICT_ACCEPTANCE=PASS`.

## Reboot acceptance

Pre-reboot state passed for Syncthing, n8n, the Knowledge bind, Stage 4 user services and the `n8n_hermes` network contract.

After controlled edge reboot:

- Syncthing auto-started and reported local health OK;
- initial transient TLS/Hello EOF attempts occurred while the routed path recovered;
- PVE subsequently reported edge connected with Syncthing `v2.1.5`;
- edge subsequently reported PVE connected at `192.168.1.3:22000`;
- Knowledge converged with `needFiles=0`, `needDirectories=0`, `needDeletes=0`, `needBytes=0`, `pullErrors=0`;
- n8n returned running/healthy with the Knowledge bind;
- `n8n_hermes` remained intact;
- Hermes, Codex and Antigravity services remained active;
- Syncthing remained loopback-only locally.

The original reboot verifier hung because its local REST polling used no per-request timeout. That was a verifier defect, not a runtime failure.

Markers:

- `EDGE_SYNCTHING_REBOOT_RECOVERY=PASS`;
- `EDGE_KNOWLEDGE_POST_REBOOT_CONVERGENCE=PASS`;
- `EDGE_N8N_POST_REBOOT_RECOVERY=PASS`;
- `EDGE_STAGE4_NON_REGRESSION=PASS`;
- `STAGE05_3_EDGE_REBOOT_ACCEPTANCE=PASS`.

## Recovery checkpoints

Created during Stage 05.3:

- PVE Syncthing pre-authorization recovery checkpoint under `/var/backups/syncthing-knowledge-stage05-3/`;
- edge n8n pre-bind recovery checkpoint under `/srv/backups/edge-stage05-3/`.

These are stage recovery artifacts, not additional Knowledge replicas.

## Final accepted state

- PVE remains the authoritative Knowledge/recovery node and Syncthing hub;
- CT210 remains the accepted PVE Obsidian runtime/WebUI;
- ai-node remains an active RW PAI/application replica;
- edge is now an active RW Cloud/agent replica;
- all edge consumers use the standard `/srv/knowledge/obsidian` path where applicable;
- Stage 4 runtime/network contracts are preserved;
- external client-access implementation through edge remains future work outside Stage 5.

`STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS`

`STAGE05_FINAL_ACCEPTANCE=PASS`

## Next stage

`06 — Edge Backrest & Recovery`
