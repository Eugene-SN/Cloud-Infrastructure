# Backrest online backup policy

Accepted by the operator on 2026-10-18: backups must leave containers, host
services and application jobs running. This supersedes the old stopped-service
bundle contract. No hook may stop/start/restart/pause/kill/recreate workloads,
enter maintenance mode, or block new application work to take a backup.

`edge-state-prepare` is the canonical `/usr/local/sbin/edge-state-prepare`.
`edge-state-plan.json` is the non-secret Edge plan, applied through Backrest's
native GetConfig/SetConfig API with its current modno. No Backrest restart is
needed. Schedule and source selection are unchanged.

## Edge as a temporary backup buffer — 2026-10-26

Both existing success hooks now use `edge-tier-evacuate.py`. They copy all local
snapshots to the existing PVE REST repository, read back the destination, and
verify original snapshot identity plus tree, time, hostname and paths. Only then
are those explicit IDs forgotten locally and unused local packs pruned. A failed
copy or missing/mismatched destination record leaves the local snapshots intact.
No forget/tag/prune command is sent to append-only PVE. PVE retention is unchanged.

The local plans retain `policyKeepAll` deliberately: the success hook owns
conditional evacuation, so native retention cannot delete an uncopied snapshot.
State and Knowledge hooks share the transfer lock. Prepared state is removed
after verified evacuation when no local snapshots remain; the preparation lock
and generation timestamp protect a newer/in-progress staging generation.

Install the Python helper as `/usr/local/libexec/edge-tier-evacuate.py` and the
two existing hook entrypoints in `/usr/local/sbin/`, all root-owned mode 0755.
They reuse `/etc/backrest/edge-d5.env` and the existing repository passwords;
no new credentials, scheduler or service is required. Verify failure/deletion
boundaries with `python3 -B backup/edge/test_tier_evacuate.py`.

An empty local repository cannot reuse yesterday's packs when creating the next
backup. Each run therefore writes its full current source locally before PVE
copy deduplication; sufficient temporary free space is still required. A PVE
outage deliberately leaves pending local backups until transfer succeeds.

| State | Current collection | Recovery boundary |
|---|---|---|
| PostgreSQL globals and Mattermost/Nextcloud/Plane/Weblate databases | Native online pg_dumpall/pg_dump; archive lists checked with pg_restore | Each database dump is internally consistent; different dumps/files have different capture times |
| n8n/Authelia and agent SQLite databases | SQLite Online Backup; integrity_check; self-contained DELETE journal target | Each database is consistent; external files are separate live copies |
| Mattermost app files, Plane uploads/runtime, Weblate data/configuration | Live file copy while applications continue running | Best effort; not an atomic bundle with the database |
| Stalwart configuration/TLS and Bulwark files | Live file copy | Mail configuration recovery only |
| Stalwart live RocksDB store `/srv/mail/stalwart/lib` | **Excluded** | New backups do not provide mailbox/store recovery; old snapshots retain historical contents according to existing retention |
| PostgreSQL physical directory `/srv/postgres` | **Excluded** from the Edge Restic plan | Restore databases from native logical dumps, not a copied live PGDATA |
| Queues, cache and in-flight tasks | No application checkpoint or suspension | Tasks in progress are not part of the recovery guarantee |

Files that vanish while rsync reads a live application are reported as
`ONLINE_FILES_WARNING` (exit 24); other rsync errors fail preparation. A failed
preparation removes only its uncommitted `next.*` generation and preserves the
previous current generation. There is no service recovery trap because no
service lifecycle is changed.

## Hook audit

All six configured plans were inspected on both nodes, including repository
hooks (none configured) and indirect dependencies:

- Edge `edge-state`: `edge-state-prepare`, `edge-state-tier-copy`; the latter
  sources an assignments-only environment file and runs Restic copy/forget.
- Edge `edge-knowledge-local`: `edge-knowledge-retention` (copy, verify and reclaim
  locally, superseding its former local-only retention behavior).
- AI Node `ai-node-full-system`: `ai-node-full-prepare.py`, `ai-node-full-copy`.
  Preparation reads disk/package/unit metadata; its `systemctl list-unit-files`
  is read-only. It refuses a busy package manager instead of stopping it.
- AI Node `ai-node-workstation-state`: `ai-node-tier-copy prepare` and the same
  helper for copy/retention. Its service inventory is read-only.
- AI Node `ai-node-ai-state`: `ai-node-n8n-prepare` (online SQLite) and tier copy.
- AI Node `ai-node-knowledge-local`: `ai-node-knowledge-retention`.
- AI Node `backrest-volume-check`, called by the service and backup helpers,
  only checks the backup-volume sentinel and mount UUID. Sourced copy environment
  files contain assignments only. No AI Node changes were necessary.

The fix is confined to backup hooks and source selection. Application update and
restore drivers retain their separate operator-requested lifecycle.

## Verification and recovery

Run `python3 -B backup/edge/test_online_prepare.py` and `bash -n` on the hook.
The isolated tests deny unrecognised Docker/service commands, check successful
online preparation, vanished files and dump/copy failures. The old hook fails
this regression test on `docker stop mattermost`.

A real Backrest `edge-state` run is additionally checked with live Docker events,
container IDs/PIDs/start times/restart counts, Weblate health polling, dump
archive reads, SQLite integrity, stored snapshot contents and tier-copy outcome.
Results and runtime hashes are in `verification-2026-10-18.json`. These checks
validate backup collection and absence of observed lifecycle interruption; they
do not constitute an isolated full application restore or owner restore acceptance.

Recovery uses the selected snapshot's online dumps and available files, respecting
the limitations above. Never describe the v2 manifest as a jointly atomic cold
bundle. Do not silently restore the old stopping hook as a backup workaround.

## Primary mechanism references

- [Backrest hooks](https://garethgeorge.github.io/backrest/docs/hooks)
- [Backrest v1.14.1 native API](https://github.com/garethgeorge/backrest/blob/v1.14.1/internal/api/backresthandler.go)
- [PostgreSQL online dumps](https://www.postgresql.org/docs/18/backup-dump.html)
- [SQLite Online Backup API](https://sqlite.org/backup.html)
- [Weblate 2026.10 manual backup](https://docs.weblate.org/en/weblate-2026.10/admin/backup.html#manual-backup)
