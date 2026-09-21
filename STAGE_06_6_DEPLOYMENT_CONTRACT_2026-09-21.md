# Stage 06.6 — Edge Backrest & Recovery Deployment Contract

**Status:** ACCEPTED  
**Date:** 2026-09-21  
**Project:** Cloud Infrastructure  
**Node:** `edge`

## Basis

This contract follows the accepted Stage 6 expanded runtime audits of `edge` and `ai-node`, the accepted single-general-plan topology, the deployed dedicated Knowledge plans, and the operator correction that D5 general-state retention must use the same human-readable daily/weekly/monthly bucket policy as ai-node State rather than a rolling 180-day archive.

## Accepted edge backup topology

### Dedicated Knowledge chain — already deployed / accepted

- source: `/srv/knowledge`;
- schedule: `04:00/10:00/16:00/22:00` local;
- `skipIfUnchanged=true`;
- local retention: rolling `14d`;
- retention grouping: `host,tags`;
- monthly full-data repository check;
- monthly prune;
- no D5 copy;
- PVE remains the authoritative Knowledge/recovery node.

### General edge-state chain

One plan only:

- plan ID: `edge-state`;
- local repo: `/srv/backup/backrest/repositories/edge-state-local`;
- broad recovery roots:
  - `/etc`;
  - `/home/core`;
  - `/root`;
  - `/opt`;
  - `/srv`;
  - `/usr/local`;
  - `/var/lib`;
  - `/var/spool`;
  - `/var/www`;
- schedule: `01:00/07:00/13:00/19:00` local;
- local retention: all snapshots within `7d`, grouped by `host,tags`;
- after each successful local snapshot, copy to CT208/D5 through the existing append-only rest-server path;
- local retention is applied only after the D5 copy succeeds;
- no separate edge-system / edge-data plans;
- no recurring Restic full/bare-metal VPS chain.

### General exclusions

The general plan excludes data that is either a backup repository, separately protected Knowledge, or reproducible runtime/cache content:

- `/srv/backup/**`;
- `/srv/knowledge/**`;
- `/var/lib/docker/**`;
- `/var/lib/containerd/**`;
- `/var/lib/apt/lists/**`;
- `/var/lib/systemd/coredump/**`;
- `/home/core/.cache/**`;
- `/home/core/.npm/**`;
- `/home/core/.local/share/Trash/**`;
- `/root/.cache/**`;
- `/root/.npm/**`.

`/srv/backups` remains included because it is small and contains useful historical recovery artifacts.

## D5 retention

The edge general repository on CT208/D5 uses the same State-class bucket policy as ai-node:

- daily: 30;
- weekly: 8;
- monthly: 6;
- yearly: 0;
- grouping: `host,tags`;
- forget/prune is owned by CT208 with full repository access;
- edge remains append-only toward D5.

This supersedes the rejected proposal to keep all edge snapshots for a rolling 180 days.

## Application-consistent capture

A single self-recovering prepare wrapper creates a staging tree under:

`/var/lib/backrest-staging/edge-state/`

The wrapper must never leave a service stopped if preparation fails.

### n8n

- preserve the complete `/srv/n8n` recovery set, including the credential encryption-key state;
- create a consistent SQLite snapshot rather than relying on a racing raw live DB copy;
- determine current binary/execution filesystem mode from runtime config during implementation preflight;
- if mutable filesystem state requires a quiesce, use the shortest bounded quiesce needed.

### Authelia

- preserve config, secrets and data;
- create a consistent SQLite snapshot;
- retain the storage-encryption-key material required to decrypt restored DB content.

### Mattermost

- briefly stop the Mattermost application container, not PostgreSQL;
- create a transactionally consistent custom-format PostgreSQL dump;
- stage the application config/data/plugins/client-plugins/Bleve state while the application is quiesced;
- restart Mattermost before the Restic filesystem scan;
- raw PostgreSQL PGDATA is not the authoritative recovery artifact.

### Stalwart + Bulwark

- because the persistent mail state is small, use a brief bounded stop;
- stage the complete `/srv/mail` tree while quiesced;
- restart Stalwart, then Bulwark;
- avoid adding a separate database tooling layer unless runtime preflight proves the current backend requires it.

### Hermes / Codex / Antigravity / CloudCLI

- broad home-state capture remains enabled;
- known SQLite stores receive consistent staged copies;
- staged copies are authoritative during restore;
- no need to stop every agent service for the entire Restic run.

## Recovery ordering

1. rebuild a supported Ubuntu edge host;
2. restore host configuration/deployment definitions and required credentials;
3. restore general filesystem state;
4. overlay application-consistent staged DB/state artifacts;
5. restore Mattermost PostgreSQL using the staged dump;
6. restore staged mail state before starting Stalwart/Bulwark;
7. restore n8n/Authelia consistent SQLite state plus required encryption-key material;
8. restore agent SQLite state as the authoritative DB copies;
9. restore/reconnect independent Knowledge synchronization separately;
10. start services in dependency order and run application-level verification.

## Repository/key recovery

Backrest configuration, Restic repository passwords and D5 access credentials must be recoverable independently of the destroyed edge VPS. GitHub stores only sanitized engineering state; secret-bearing recovery material remains outside the public repository.

## Provider image policy

There is no recurring Restic bare-metal edge chain. After the complete Cloud Infrastructure build is finally accepted, the operator creates one provider-panel golden VPS snapshot outside Backrest.

## ai-node accepted optimization work

The Stage 6 cross-project audit also accepted these corrections without redesigning the established ai-node backup architecture:

1. `ai-node-tier-copy` retention grouping becomes `host,tags`, not `host,paths,tags`;
2. pai-n8n receives application-consistent SQLite staging;
3. `ai-node-full-system` excludes `/var/lib/containerd/**` and `/var/lib/docker/**`;
4. after successful D5 copy, the local full repository retains the latest two full snapshots;
5. the bare-metal restore helper is corrected to the current mount layout:
   - `/srv/ai-data`;
   - `/srv/g-data`;
   - `/srv/backup`;
   - `/srv/scratch`;
   - `/srv/hdd`;
   - `/mnt/data-cloud`.

Existing ai-node D5 State retention remains daily30 / weekly8 / monthly6 / yearly0. Existing Full D5 retention remains weekly6 / monthly3 / yearly0. Dedicated ai-node Knowledge remains local-only rolling 14d.

## Deployment sequencing

Stage 6 implementation proceeds in bounded CHECK → CHANGE → VERIFY units:

1. exact edge consistency-wrapper preflight;
2. CT208 edge repository/access/retention contract;
3. edge local general repo + plan + tier-copy deployment;
4. application-consistency wrapper deployment and controlled capture;
5. ai-node accepted corrections;
6. isolated real restore and application usability acceptance;
7. final non-regression/reboot only if required;
8. canonical repository persistence and Stage 6 final acceptance.

A usable isolated restore is mandatory before Stage 7.
