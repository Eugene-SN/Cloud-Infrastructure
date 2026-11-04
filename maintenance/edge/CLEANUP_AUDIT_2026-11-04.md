# Edge update cleanup audit — 2026-11-04

Scope: all 19 manual Maintenance units, the native Hermes/Codex/Antigravity
owners, and update-related artifacts on Edge. PVE was not accessed. This audit
was added to the authorized manual Stalwart 1.0.2 migration. Other service
updates were not initiated by this operation.

## Driver coverage

| Units | Cleanup after successful checks |
| --- | --- |
| N8N, AUTHELIA, MATTERMOST, POSTGRESQL, BULWARK, NEXTCLOUD_REDIS, WEBLATE, WEBLATE_VALKEY, GITHUB_MCP | Generic Compose driver captures previous IDs, recreates the selected service(s), waits for checks, then calls shared `docker-service-images.cleanup`. Weblate/PostgreSQL/Valkey also require native Weblate deployment checks. |
| NEXTCLOUD | Shared capture per upgrade step; final native readiness, version and both running image IDs precede shared cleanup. |
| STALWART | Shared capture; running version/image verification precedes cleanup. Failed updates preserve recovery state. The one-time 0.16→1.0 migration used the same cleanup after manual acceptance. |
| PLANE | Shared capture precedes vendor migration; native deployment/application checks precede cleanup. Native temporary directory and `--rm` migrator are cleaned. |
| XRAY, HYSTERIA2 | Existing `maintctl` checks precede removal of scoped recovery directories; EXIT traps remove downloads/work directories. |
| BACKREST | Shared native downloader removes work via EXIT and prior binaries after service checks. |
| SEMAPHORE | External updater verifies its running version/health and scoped refresh, then removes all previous binary/SQLite pairs. Failed unresolved operations retain recovery material. |
| RESTIC, RCLONE | Native self-update, then explicit `.old` deletion. See the limitation below. |
| APT_EDGE | Native upgrade calls `autoremove` and `clean`; no custom image archive is created. |

Installed handlers match the reviewed canonical source, with the one shared
cleanup correction below. No per-service replacement updater was introduced.
Native Hermes uses `--no-backup`; its installed wrapper matches the repository.
Native Antigravity deletes candidate/previous executable files after verified
readiness; installed source matches, and only `status.json`/`update.py` remain
in its state directory. Codex remains owned by its native installation manager.
Ubuntu security updates remain native package-manager work, not Docker images.

## Confirmed shared cleanup defect and correction

On this deployed Docker, `image inspect` can include `repository@digest` in
`RepoTags` as well as `RepoDigests`. The old helper submitted both the tag and
digest to one `docker image rm` call. Removing the tag removed the digest too;
the second argument then caused `No such image`, exit 1, and a false cleanup
failure after the old image had actually been deleted. This was observed while
cleaning the superseded Stalwart image; its stale receipt was reconciled.

The existing helper now removes one reference at a time, rechecking the image
and its live references before the next removal. Genuine Docker/list/removal
errors remain failures. No force-delete, global prune, retention rule, new
service or timer was added. Existing used-image, declared-build-input,
other-pending-operation and foreign-reference protections remain.

Verification: the new six-case fixture failed against the old helper and passes
against the correction. Cases cover tag/digest alias deletion, running/stopped
container protection, declared images, another pending receipt, foreign tags
and genuine removal errors. Existing 19-route dispatch, Stalwart rollback,
Nextcloud checks and native updater fixtures pass. Real scoped cleanup removed
two obsolete PDF worker images successfully.

## Removed artifacts and retained runtime

Removed:

- Stalwart 0.16.27 image `c429b311c93d…`; its exact registry digest was checked
  as retrievable before removal. The temporary image archive (104,795,648 bytes)
  was also removed; no old image archive is part of recovery.
- PDF worker images `603669313be5…` (`a2da5f5-section-rules`) and
  `d7fe7e73d422…` (`9c9bbb375751-standalone`). No container used them, and the
  current deployment/Dockerfile declares Python, not either old worker image,
  as its build input. Shared cleanup preserved the active worker and its base.
- Codex 0.165.0 release: 755,675,973 bytes, explicitly approved after inventory.
  Current selection remained 0.166.0. The old history PIDs were gone, and no
  executable/cwd/root/maps/open-file process references remained before deletion.
- `/opt/nextcloud/.codex-push-rollback-20261016-2`: two obsolete config files,
  4,000 bytes; no service/config/bind-mount references. Explicitly approved.
- 23 exact reclaimable BuildKit cache IDs, explicitly approved. The first native
  pass removed 13; `--all` with the remaining exact ID filter removed 10 shared
  cache records. Native reported cache accounting was 331.7 MB + 1.778 GB; this
  is not a claim that all those bytes were unique filesystem space. All current
  container image IDs remained available.
- This migration's temporary targets, reverse-rehearsal store, diagnostic state,
  source checkout and utility image are removed after verification.

Retained current runtime: all deployed application images; the stopped on-demand
PDF worker is an accepted workload, not an orphan. Its Python digest
`504679006065…` is a declared current build dependency, even without a container.
The Weblate Valkey `complete_in_use` receipt tracks an image still in use.

Required Stalwart recovery data is `/srv/mail/stalwart-migration`: the original
cold data/config, original Compose, native forward state, receipt and runbook.
This preserves data/settings needed by native reverse migration. Old images
are fetched by exact digest only when recovery is initiated.

The scan found no previous application files in `/var/backups/edge-maintenance`
or `/var/backups/vpn-stack`, no `restic.old`/`rclone.old`, and no abandoned native
update directories in `/var/tmp`. `/tmp` contained this task's own active work,
which is removed at completion. Hermes manual configuration/plugin backups were
not classified as release-update leftovers or deleted as part of this audit.

## Limits and remaining mechanism findings

- Restic/Rclone `.old` deletion catches and ignores `OSError`. A permission or
  filesystem failure could therefore leave that file while the task reports
  success. Neither file exists now. This is a separate, unmodified finding;
  the authorized implementation correction targeted shared Docker cleanup.
- Native Codex retained a previous selected release. It was removed with explicit
  approval. Installed CLI help exposes no separate cleanup/retention switch;
  future native updates may create another previous release. No vendor patch,
  replacement updater or new cleanup timer was added.
- Native image cleanup handles captured service history; it is not a global
  garbage collector for unregistered manual builds. Their obsolete images need
  the same verified, scoped cleanup when such a deployment completes.
- Filename/metadata inspection covered update locations in `/opt` and `/srv/mail`
  through depth 5, `/var/backups`, known `/tmp`/`/var/tmp` update prefixes and
  the native owner locations above. This is not a classification of every file
  on Edge or deletion of unspecified historical application evidence.
- Concurrent operator tasks 94–106 updated other applications. Task 104 upgraded
  Docker and restarted it at 07:45:33 Europe/Minsk (04:45:33 UTC), changing
  unrelated container starts.
  Their identities therefore cannot be claimed unchanged across this operation.
  Task 103 Plane failed; task 106 Master failed its initial precheck on
  `WEBLATE_VALKEY:STABLE_UNRESOLVED`. These were not cleanup regressions or
  tasks launched by this operation, and were not repaired in this scope.

Validation scripts:

```bash
python3 -B maintenance/edge/tests/verify-image-cleanup.py
python3 -B maintenance/edge/tests/verify-update-drivers.py
python3 -B maintenance/edge/tests/verify-stalwart-update.py
python3 -B maintenance/edge/tests/verify-backrest-update.py
python3 -B maintenance/edge/tests/verify-semaphore-update.py
python3 -B maintenance/edge/tests/verify-native-release.py
```
