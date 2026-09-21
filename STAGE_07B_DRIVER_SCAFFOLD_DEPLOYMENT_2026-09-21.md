# Stage 07B — Edge Driver Scaffold Deployment — 2026-09-21

## Status

**IMPLEMENTED / DEPLOYED / READ-ONLY VERIFIED — NOT PRODUCTION-ACCEPTED**

Stage 7B remains IN PROGRESS. No component driver and no Master Batch run has
been accepted or executed by this checkpoint.

## CT1000-derived execution contract

The accepted Home implementation was inspected through its live maintenance
status, actions, Semaphore project/templates and task output. The edge port
preserves:

- one template per fixed target;
- an explicit allowlist and maximum five-minute cache age;
- no-op/deny behavior for non-actionable targets;
- sequential Master Batch execution with per-target results;
- failure isolation and a final status refresh;
- no Semaphore schedules or autonomous update launcher.

Home inventory, PVE/VMID/PCT/QGA logic and SSH execution were not copied.

## Edge implementation

- target manifest: 1 APT + 5 native + 6 Docker + 4 CLI/agent units;
- 23 monitored components; eight APT components are details of `APT_EDGE`;
- 16 per-unit Ansible playbooks and one Master Batch playbook;
- fail-closed `manual-update` and `master-batch-update` dispatchers;
- checksum-verified release artifacts for host-native binary candidates;
- exact deployed Compose file/service mapping for all six Docker units;
- product-native `update` commands for Hermes, CloudCLI, Codex and Antigravity;
- maintained static dashboard and atomic schema-v3 JSON generation.

Docker schema-v3 fields are `application_version`,
`available_application_version`, `image_repository`, `image_track`,
`running_image_digest`, `remote_image_digest` and `update_reason`. Allowed
reasons are `VERSION_UPDATE`, `IMAGE_DIGEST_UPDATE`, `CURRENT` and
`CHECK_FAILED`.

## Semaphore runtime

- ID 1: accepted read-only Refresh;
- IDs 2..17: 16 `[LOCKED]` individual update templates;
- ID 18: `[LOCKED]` Master Batch;
- schedules: 0;
- update-template task runs: 0;
- Master Batch task runs: 0.

`actions.json` remains schema 8 with `read_only=true`, `auto_update=false`,
all component `template_id=null`, `master_template_id=null` and
`driver_state=acceptance_pending`. The driver-acceptance registry is absent.
Thus the dashboard cannot dispatch a real update and direct Semaphore launch
fails before mutation.

## Read-only verification

- Bash, Python, JavaScript and all Ansible playbooks passed syntax checks;
- generated contract: `16 / 23 / 8`, group distribution `1 / 5 / 6 / 4`;
- APT child components have `actionable=false` and are absent from actions;
- PostgreSQL runtime `18.6` is distinct from track `18-alpine`;
- Stalwart runtime `0.16.22` is distinct from track `v0.16`;
- Mattermost runtime `11.11.0` is distinct from track `latest`;
- active dashboard update template IDs: 0;
- update timers/cron/Semaphore schedules: 0;
- failed systemd units after deployment: 0.

Pre-deployment recovery copy:
`/var/backups/edge-maintenance/stage7b-predeploy-20260921T120609Z`.

## Remaining acceptance work

All 16 source driver candidates exist; none is missing from Semaphore. All 16
remain deliberately unaccepted and non-executable from the dashboard. Each
must be reviewed and manually launched from `update.escloud.us` in a separate
authorized acceptance step, with product-specific health and recovery evidence.
Stalwart and Mattermost require especially explicit release-note/migration and
backup review before their gates can be opened. Master Batch is accepted only
after every included per-unit driver is accepted.

No production component update was executed by this checkpoint.

## Operator-requested action-surface correction

The subsequent operator review found that the acceptance-pending presentation
did not expose the individual buttons needed to perform those manual acceptance
runs and that Docker track/digest data made the tables inconsistent with
CT1000. The deployed correction now uses the same columns in all four groups:
`SCOPE`, `SERVICE NAME`, `INSTALLED`, `LATEST STABLE`, `STATUS`, and `ACTION`.
The single edge node address remains in the page header and is not repeated in
every service row.

All 16 individual template IDs (`2..17`) are connected. A button is enabled
only for a unit whose current status is `UPDATE_AVAILABLE`; current units show
`No update available`. Docker digest/tag data remains in the machine-readable
model but is no longer a visible table column. Exact stable application
versions are used where available, including Stalwart `0.16.23`; digest-only
PostgreSQL refreshes use the standard `Update Available` status without
inventing a new application version. The digest reason remains available in
the machine-readable model and technical tooltip.

Git-managed Hermes uses the same separation: the dashboard renders normalized
release versions such as `v0.21.3`, while installed and upstream Git refs remain
machine-readable and determine whether a same-version code refresh is
available. A ref-only change never appears as a fabricated version transition.

Docker registry snapshots reuse the last successful result for 30 minutes and
fall back to it when a registry probe fails. Repeated operator Refresh actions
therefore do not consume Docker Hub's anonymous pull quota and cannot starve a
subsequent manual image pull; local runtime versions and digests are still read
on every refresh.

The root allowlist is `/etc/edge-maintenance/manual-driver-enablement.json` and
contains exactly the 16 fixed targets. Master Batch remains disabled
(`master=false`, `master_template_id=null`) pending individual acceptance.
This correction enabled controls only; it executed no update task.
