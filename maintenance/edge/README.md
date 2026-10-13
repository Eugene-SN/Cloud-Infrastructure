# Edge Maintenance

Current contract (2026-10-01 after Plane Part 1): 16 manual targets, 9 Docker units, 23 monitored components. PLANE is an official-release unit using `plane_compose`, manual helper `scripts/update-plane`, Git playbook `playbooks/updates/plane.yml`, and Semaphore template 21. Current/latest stable v1.4.2 CURRENT; preflight checks native vendor/site graphs, public routes/variables and actual Backrest recovery contents, and real updates require a completed backup before migration. No scheduled Plane update. Full contract: `../../deployments/plane/README.md`; acceptance: `../../PLANE_PART_1_ACCEPTANCE_2026-10-01.md`. Shared PostgreSQL and every other update driver remain. Earlier stage target counts below are historical checkpoints.

Current source for the single `edge` maintenance/update subsystem.

After the 2026-10-13 Weblate deployment, the manifest contains 18 manual
targets, 11 Docker units and 25 monitored components. `WEBLATE` and
`WEBLATE_VALKEY` are separate Compose targets and Semaphore templates 22 and 23.

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

Maintenance contains exactly 18 actionable manual targets:

`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`,
`SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`,
`STALWART`, `BULWARK`, `NEXTCLOUD`, `PLANE`,
`NEXTCLOUD_REDIS`, `WEBLATE`, `WEBLATE_VALKEY`.

`HERMES`, `CODEX` and `ANTIGRAVITY` do not appear in raw Maintenance version rows,
`maintenance.json`, `actions.json`, the Maintenance dashboard or Semaphore
update templates.

`actions.json` contains exactly the 18 manual actions, has
`execution_mode=manual_only`, and `auto_update=false`.

`update.escloud.us` remains the operator launch surface. Semaphore is the
manual executor/orchestrator and has no autonomous update schedule.

## Stage 12 targets

Rclone uses upstream `rclone selfupdate --stable`, followed by restart of the
persistent `core` user service `projects-webdav.service`.

Nextcloud application, shared PostgreSQL and Redis are distinct manual Compose targets; Plane reuses the shared PostgreSQL unit and has its own coherent release unit.
The Nextcloud application action recreates both `app` and `cron`.

Bulwark tracks upstream stable through `ghcr.io/bulwarkmail/webmail:latest`.
Changing the tracked tag does not itself update/recreate the running container;
the actual image update remains operator-triggered.

## Master Batch

Master Batch derives its 18-target plan from `config/update-units.json`.
Both real execution and `--plan-only` require the accepted schema-2
`/etc/edge-maintenance/manual-driver-enablement.json`.

Semaphore remains `individual_only` because updating the running orchestrator
inside its own batch could interrupt final acceptance.
When its row is `UPDATE_AVAILABLE`, the precheck stops before any update with
`INDIVIDUAL_UPDATE_REQUIRED|DETAIL=SEMAPHORE`. A pending reboot also prevents
dispatch. These are existing preconditions, not driver or cleanup failures.
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

A manual component update requires:

- the target to be one of the 18 manifest units;
- schema-2 enablement to permit the target;
- a fresh `UPDATE_AVAILABLE` row;
- explicit operator initiation.

Read-only Refresh never chains into a component update.
