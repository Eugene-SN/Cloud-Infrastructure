# Backrest online backup policy

Accepted by the operator on 2026-10-18: backups must leave containers, host
services and application jobs running. This supersedes the old stopped-service
bundle contract. No hook may stop/start/restart/pause/kill/recreate workloads,
enter maintenance mode, or block new application work to take a backup.

`edge-state-prepare` is the canonical `/usr/local/sbin/edge-state-prepare`.
`edge-state-plan.json` and `edge-knowledge-plan.json` are the non-secret plans,
applied through Backrest's native GetConfig/SetConfig API with its current modno. No Backrest restart is
needed. Schedule and source selection are unchanged.

## Direct backup to the existing PVE repository — 2026-10-29

Both plans use the Edge Backrest repo entry `edge-pve`, URI
`rest:http://192.168.1.14:8000/edge/`, Restic ID
`e293ee008a257664a7e568787463a9cbab5d0573daf53c5ebd92477d1960cec7`.
On CT208 the same repository remains `edge-d5` at
`/srv/backrest-storage/repositories/edge`. No repository initialization,
snapshot migration, historical tagging or chunker change is part of this change.
Instance `edge`, plan IDs, tags, source paths, exclusions and schedules are preserved.

Edge has no local backup repository or copy/evacuation hook. It retains only
Restic's `/root/.cache/restic` cache (excluded from backup) and online staging.
`policyKeepAll` stays enabled on both plans; Edge repo check/forget/prune schedules
are disabled. CT208 owns the unchanged daily30/weekly8/monthly6 retention,
grouped by `host,tags`, and prune after its Sunday 05:30 structural check succeeds.
That policy covers all tags in this repository, including Edge Knowledge, with
separate groups for historical hostname `edge.escloud.us` and current `edge`.
The transition preserves existing history; future scheduled retention still applies.

Backrest uses the latest snapshot matching `plan:<ID>,created-by:edge` as parent.
Unchanged files reuse their old blocks even when the copied parent was produced
with different chunker parameters. Changed/recreated files use PVE chunking and
may add extra blocks during the transition. There is no forced full backup.
The existing `skipIfUnchanged` field is preserved; this installed Backrest build
does not pass it through as a Restic flag. Repeated Knowledge snapshots reuse
the same content/tree blocks; the small snapshot records are retained normally.

Install `edge-state-finalize` as `/usr/local/sbin/edge-state-finalize`, root:root
0755. State's success hook passes the native `.SnapshotId` through `.ShellEscape`.
The helper reads that exact snapshot from the expected repository and verifies
its ID, tags, host and paths before deleting an older staging generation. It
holds the existing preparation lock, rejects symlinks and preserves a newer or
busy generation. It cannot run copy/forget/prune. Failed backup or readback
keeps staging; PVE unavailability causes a failed direct backup, without a hidden
local full-backup fallback. The prepare lifecycle bounds staging generations.

Credentials remain in `/etc/backrest/edge-d5.env`, `/etc/backrest/edge-d5-password`
and native protected Backrest repo.env. Do not print or commit their values.
No new account, service or scheduler is introduced. Finalizer tests:
`python3 -B backup/edge/test_direct_finalize.py`.
Execution plan and recovery boundaries:
`docs/superpowers/plans/2026-10-29-backrest-direct-pve.md`.

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

The 2026-10-18 audit inspected all six plans on both nodes and their indirect
dependencies. AI Node entries below retain the names from that historical audit;
this transition did not re-audit or change AI Node. Current Edge entries are:

- Edge `edge-state`: `edge-state-prepare`, `edge-state-finalize`; the latter
  reads the direct PVE snapshot and cleans only its saved staging generation.
- Edge `edge-knowledge-local`: direct PVE backup without an application hook.
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

The 2026-10-18 online-policy verification used Docker events, container lifecycle
state, Weblate health polling and stored database artifacts; its historical
results/hashes are in `verification-2026-10-18.json`. The direct-PVE transition
checked parent selection, history preservation, both real cycles, finalization,
selected native restores/SHA-256, database archive/integrity checks, unchanged
container lifecycle state and monitoring. Evidence is in
`verification-2026-10-29.json`. These checks
validate backup collection and absence of observed lifecycle interruption; they
do not constitute an isolated full application restore or owner restore acceptance.

Recovery uses the selected snapshot's online dumps and available files, respecting
the limitations above. Never describe the v2 manifest as a jointly atomic cold
bundle. Do not silently restore the old stopping hook as a backup workaround.

For Edge host loss, existing CT208 administrative access and its protected
`/etc/backrest/edge-d5-password` can unlock the Edge repository locally. Restore
Edge's protected credentials/configuration from the selected snapshot and apply
the current two canonical plans through native Backrest. A snapshot taken during
the transition can contain disabled old local repo entries; remove those entries
when reconciling it with this contract. Verify the existing repository GUID;
never initialize a replacement repository. Git contains no secret credentials.

## Primary mechanism references

- [Backrest hooks](https://garethgeorge.github.io/backrest/docs/hooks)
- [Backrest v1.14.1 native API](https://github.com/garethgeorge/backrest/blob/v1.14.1/internal/api/backresthandler.go)
- [PostgreSQL online dumps](https://www.postgresql.org/docs/18/backup-dump.html)
- [SQLite Online Backup API](https://sqlite.org/backup.html)
- [Weblate 2026.10 manual backup](https://docs.weblate.org/en/weblate-2026.10/admin/backup.html#manual-backup)
