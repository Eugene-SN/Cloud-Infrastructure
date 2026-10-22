# Edge Maintenance

Current contract (2026-10-16): 19 manual targets, 12 Docker units and 22 permanent
containers. Runtime discovery uses the approved names in
`../../deployments/edge/docker/container-names.md`; Compose service keys and
dispatch target IDs stay unchanged. Plane updates assign a unique
`plane-migrator-<run-id>` name to the temporary `--rm` migration container.

Weblate discovery reads the registry manifest and its official
`org.opencontainers.image.version` label through the existing registry helper.
This also identifies an image rebuild with the same application version; it
does not depend on the Docker Hub tag-alias path used by other products.
Source: [official Weblate image labels](https://github.com/WeblateOrg/docker/blob/main/Dockerfile).

Plane Part 1 contract (2026-10-01): PLANE is an official-release unit using `plane_compose`, manual helper `scripts/update-plane`, Git playbook `playbooks/updates/plane.yml`, and Semaphore template 21. Preflight checks native vendor/site graphs, public routes/variables and actual Backrest recovery contents, and real updates require a completed backup before migration. No scheduled Plane update. Full contract: `../../deployments/plane/README.md`; acceptance: `../../PLANE_PART_1_ACCEPTANCE_2026-10-01.md`. Shared PostgreSQL and every other update driver remain. Earlier stage target counts below are historical checkpoints.

Current source for the single `edge` maintenance/update subsystem.

After the 2026-10-16 shared GitHub MCP deployment, the manifest contains 19 manual
targets, 12 Docker units and 26 monitored components. `GITHUB_MCP` is a permanent
Compose unit and Semaphore template 24; `WEBLATE` and `WEBLATE_VALKEY` remain templates 22 and 23.

## Ownership model

Stage 07.2 uses **native-first ownership**:

- a supported upstream/vendor-native automatic lifecycle remains authoritative when production-safe;
- Maintenance/Semaphore owns only components whose updates remain operator-controlled;
- native-auto products are deliberately absent from Maintenance rather than represented as disabled or monitor-only update targets.

Native automatic owners outside Maintenance:

- `HERMES` — Hermes native cron updater plus conditional settlement timer;
- `CODEX` — Codex managed-daemon updater / `pid-update-loop`;
- `UBUNTU_SECURITY` — package-owned `apt-daily*` / `unattended-upgrades`;
- `ANTIGRAVITY` — upstream-native background self-updater.

Normal and third-party APT updates remain manual through `APT_EDGE`. Automatic reboot is disabled.

## Maintenance target model

Generated target model: `update_units_v5`.

Maintenance contains exactly 19 actionable manual targets:

`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`,
`SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`,
`STALWART`, `BULWARK`, `NEXTCLOUD`, `PLANE`,
`NEXTCLOUD_REDIS`, `WEBLATE`, `WEBLATE_VALKEY`, `GITHUB_MCP`.

`HERMES`, `CODEX` and `ANTIGRAVITY` do not appear in raw Maintenance version rows,
`maintenance.json`, `actions.json`, the Maintenance dashboard or Semaphore
update templates.

`actions.json` contains exactly the 19 manual actions, has
`execution_mode=manual_only`, and `auto_update=false`.

`update.escloud.us` remains the operator launch surface. Semaphore is the
manual executor/orchestrator and has no autonomous update schedule.

## Refresh scope and task tracking (2026-10-22)

Individual update playbooks pass `--target TARGET` to the read-only refresh
before and after their driver. Only that target is discovered and replaced in
the existing caches. Non-APT targets skip the isolated APT index download and
unrelated release/registry lookups. `APT_EDGE` still refreshes its package
components and APT probe. Scan Updates and Master Batch retain full discovery.
The external Semaphore self-update completion refresh also selects `SEMAPHORE`.

Refresh writers share a lock to serialize cache merges. A partial refresh
requires a complete existing cache, updates the selected row's `checked_at`,
and preserves every other row and the last full scan's `generated_at`.
Individual dispatch checks the selected row's timestamp; Master Batch still
requires a fresh full scan. Partial refreshes therefore cannot make unrelated
stale results appear fresh.

The dashboard waits for Semaphore's actual terminal task status and, for its
self-update, the matching external operation result. It has no elapsed-time
limit that labels a running update as failed. Individual HTTP requests remain
bounded; unavailable responses show the existing reconnecting notification
and keep update controls disabled while tracking resumes. Layout and styling
are unchanged.

Isolated regression checks (no real updates or service restarts):

```bash
python3 maintenance/edge/tests/verify-target-refresh.py
node maintenance/edge/tests/verify-semaphore-dashboard.js
```

## Weblate readiness after updates (2026-10-22)

APT can restart Docker during package installation. Finishing APT does not
mean that Weblate has finished its own startup. The APT driver now waits for
Weblate's native Docker health status to leave `starting` and become `healthy`,
then runs `weblate check --deploy --fail-level ERROR` in the existing container.
The same acceptance runs after Weblate, shared PostgreSQL and Weblate Valkey
updates; Weblate itself also runs it before pulling/recreating its image.
Stopped or unhealthy containers and failed native checks fail the update.
There is no separate elapsed-time cutoff while Docker reports startup in
progress, and these checks do not restart the application.

Compose image cleanup follows this application acceptance, retaining the
existing recovery receipt if native checks fail. Checks do not guarantee
adapter translation quality or eliminate the expected interruption when an
operator updates Docker or the application itself.

The 2026-10-22 audit found Weblate already serving successfully after the APT
Docker restart, with separate `weblate.E027` errors on five root-owned custom
profile paths. Correcting only their ownership to the verified runtime UID/GID
1000 cleared the native errors without changing file contents or restarting.
Files deployed below `/app/data`, including the provider bind mount, must keep
that owner. Install profile files with explicit ownership and run management
commands as the container's default Weblate user. Do not fix this by silencing
`weblate.E027` or recursively changing unrelated mounts/secrets.
Upstream contract: [Weblate filesystem permissions](https://docs.weblate.org/en/weblate-2026.10.1/admin/install.html#file-permissions).

Regression check: `python3 maintenance/edge/tests/verify-weblate-readiness.py`.
It exercises long startup, dependency updates, stopped/unhealthy containers,
failed preflight and failed post-update checks without real updates/restarts.

## Stage 12 targets

Rclone uses upstream `rclone selfupdate --stable`, followed by restart of the
persistent `core` user service `projects-webdav.service`.

Nextcloud application, shared PostgreSQL and Redis are distinct manual Compose targets; Plane reuses the shared PostgreSQL unit and has its own coherent release unit.
The Nextcloud application action recreates both `app` and `cron`.

Bulwark tracks upstream stable through `ghcr.io/bulwarkmail/webmail:latest`.
Changing the tracked tag does not itself update/recreate the running container;
the actual image update remains operator-triggered.

## Master Batch

Master Batch derives its 19-target plan from `config/update-units.json`.
Both real execution and `--plan-only` require the accepted schema-2
`/etc/edge-maintenance/manual-driver-enablement.json`.

Semaphore remains `individual_only` because updating the running orchestrator
inside its own batch could interrupt final acceptance.
When its row is `UPDATE_AVAILABLE`, the precheck stops before any update with
`INDIVIDUAL_UPDATE_REQUIRED|DETAIL=SEMAPHORE`.
An outstanding reboot is informational: it permits dispatch and final update
acceptance, emits `MASTER_NOTICE=REBOOT_REQUIRED`, and remains visible in the
maintenance cache/dashboard and the final validator's `REBOOT_REQUIRED` field.
Master neither reboots the host nor clears the OS reboot marker.
The Master playbook displays both driver stdout and stderr, including the
specific precheck reason; a post-scan failure alone is not the primary cause
when dispatch never began.

## Semaphore self-update (2026-10-13)

The installed binary distribution remains in use, as supported by the
[upstream upgrade guide](https://semaphoreui.com/docs/admin-guide/upgrading).
The manual Semaphore task only dispatches a fixed transient systemd service
`edge-semaphore-update.service`; it reports `DISPATCHED`, not completed update.
The external service downloads the Community release and its matching official
checksum manifest, checks the candidate version, waits for all unfinished local
tasks (including `stopping`), then stops Semaphore, snapshots SQLite, installs
the binary, runs the native migration and starts Semaphore. A second dispatch
cannot replace an existing active unit. No permanent unit or timer is added.

`scripts/controller-update-state` records the operation and final outcome in
`/var/www/maintenance-status/controller-update.json`. The dashboard matches
that operation before reporting success. Completion requires both `/api/ping`
and the actual running process's version; migration/start/health failures
restore and verify the matched previous binary and SQLite database. Failure
before installation does not restart the service. A subsequent cache-refresh
failure is reported separately and does not undo a healthy update.

Matched private recovery files use `/var/backups/edge-maintenance/semaphore-*`
and `.sqlite` (0600), retaining the existing limit of two previous versions.
The helper has no Edge `ExecStartPre` hook and does not alter task records on
Edge startup. Orphan task 63 was stopped through Semaphore's native stop API.

Handler installation recovery is `/tmp/semaphore-handler-recovery` (0700),
with original files and ownership/mode metadata in `manifest.json`. Retain
this agreed recovery directory until operator acceptance. Restoring these
handler/page files does not require a service restart.

`semaphore-pve-fix.py` is an operator-run root installer for the audited CT1000
Home layout. It refuses drift in the audited manual driver, preserves the
Home release edition and existing `ExecStartPre` hook, uses a fixed transient
unit on PVE and the existing `.pre-update` recovery pair inside CT1000 (0600).
It patches the Home dashboard and common playbook without executing an update
or restarting services. Its files and permission metadata are recoverable from
the same `/tmp/semaphore-handler-recovery` location inside CT1000. Preparation
of this installer does not mean it has been applied on PVE.

Verification commands (isolated service/network boundaries):

```bash
python3 maintenance/edge/tests/verify-semaphore-update.py
node maintenance/edge/tests/verify-semaphore-dashboard.js
python3 maintenance/edge/tests/verify-semaphore-pve.py
ansible-playbook --syntax-check -i localhost, maintenance/edge/playbooks/updates/semaphore.yml
```

These checks cover dispatch, download failure, unfinished tasks, SQLite/binary
rollback, rollback failure and stale UI outcomes. They do not establish that a
real upgrade has completed; a real operator-initiated upgrade remains untested.

## Monitoring integration

Stage 8 `edge-monitor` consumes
`/var/www/maintenance-status/maintenance.json` as the authoritative update
state. Therefore its `UPDATE_AVAILABLE` count represents manual Maintenance
updates, not native updater drift.

## Safety boundary

Docker rows with `IMAGE_DIGEST_UPDATE` and equal known application versions
explain in the existing hover tooltip that a new Docker image build is available
and the application version is unchanged. Latest Stable keeps only the version
and its existing red update highlight; both digests remain in the tooltip.
Update discovery and dispatch are unchanged. The live dashboard has separate
styling changes, so deploy this
renderer change as a targeted patch rather than replacing its full HTML.

The generic Compose driver records previous image IDs before recreation and
keeps them when the update command fails. After native Docker health/wait
succeeds, scoped cleanup can delete an unused previous image and its recovery
receipt. This is not an archive of adapter-tested builds or automatic rollback.
For Weblate, no adapter translation check or fresh pre-update backup is part of
this driver. Existing Backrest preparation covers its coordinated database,
DATA_DIR and configuration; rollback after schema changes must account for
that matched recovery state, not assume an image-only downgrade is safe.

A manual component update requires:

- the target to be one of the 19 manifest units;
- schema-2 enablement to permit the target;
- a fresh `UPDATE_AVAILABLE` row;
- explicit operator initiation.

Read-only Refresh never chains into a component update.

## Update driver audit and correction (2026-10-13, Task 66)

Task 66 dispatched eight updates, with Hysteria2's cleanup reporting an error
after installation and Nextcloud rejecting its missing required CLI argument.
The correction isolates Xray/Hysteria2 function working directories and EXIT
cleanup inside subshells; the deployed maintctl delta is recorded in
`patches/maintctl-update-cleanup.patch`. The historical migration reference is
preserved, and the patch applies only to the two update functions.

Nextcloud dispatch passes the cached application version and image digest.
Equal application versions still run the existing image replacement path.
The final image is pulled by that digest and tagged for the existing Compose
track; app and cron are recreated with `--no-deps`, then native readiness and
both running image IDs are checked before the existing image cleanup. The
existing intermediate-major upgrade path remains; no automatic data downgrade
is introduced. Upstream lifecycle: https://github.com/nextcloud/docker#update-to-a-newer-version.

Backrest uses the existing `update-github-binary` helper rather than the absent
legacy downloader. Its official archive is `backrest_Linux_x86_64.tar.gz`;
the checksum manifest includes the release version. Candidate verification
uses `--version`, avoiding invocation of the application with a positional
`version` argument. Preparation failures do not touch the service. Installation
and health failures use the existing binary recovery path and verify service
activity after restoration.

Verification adds executable behavior tests for all 18 dispatch routes,
Nextcloud digest refresh/readiness, maintctl cleanup and Backrest download,
checksum, version, installation and health failures. It also checks live
Compose identities, native preflights, APT simulation and the complete health
validator. See `UPDATE_DRIVER_AUDIT_2026-10-13.md` for coverage and limits.
No real update, image pull, migration or service restart is part of this
verification. Runtime handler recovery is
`/tmp/semaphore-handler-recovery/drivers-task66` until operator acceptance.
