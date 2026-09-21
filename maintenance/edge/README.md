# Edge Maintenance

Maintained Stage 7B source for the single `edge` node. The design keeps the
accepted `Semaphore -> Ansible -> native driver` chain and has no scheduler,
timer, unattended updater, or background update daemon.

## Model

- 16 update units: 1 APT, 5 native, 6 Docker, 4 CLI/agent.
- 23 monitored components. The eight APT-managed components are details of
  `APT_EDGE`; they are never standalone actions.
- Docker rows keep application/runtime version, configured repository/track,
  running digest, remote digest, and update reason as distinct fields.
- `update.escloud.us` is the only operator launch surface.

`/var/www/maintenance-status/actions.json` is a generated runtime artifact, not
a second configuration source. `scripts/maintenance-actions-render` joins the
canonical update-unit definition, Semaphore template mapping and root-owned
manual enablement registry, validates their exact 16-target agreement and
atomically replaces the artifact on every Refresh. No `actions.json` copy is
kept under `/opt/edge-maintenance/dashboard`.

`playbooks/semaphore-refresh.yml` delegates to the same canonical
`/opt/edge-maintenance/scripts/maintenance-refresh` pipeline used by direct
runtime refreshes; it does not maintain a second orchestration sequence.

## Safety boundary

Individual templates are exposed only through the manual dashboard controls.
Execution remains fail-closed: `/etc/edge-maintenance/manual-driver-enablement.json`
must explicitly enable each fixed unit. Master Batch has a separate `master`
gate. Its single Semaphore task performs a fresh pre-scan, validates the exact
16-target cache, skips current targets, executes available targets sequentially,
continues after isolated driver failures, runs a complete post-scan and requires
both status and health acceptance before reporting success. Semaphore self-update
remains individual-only because restarting the orchestrator from its own batch
would interrupt acceptance. A pending reboot blocks dispatch and also prevents a
completed batch from being reported as accepted.

The canonical Semaphore sudo allowlist is `config/semaphore-sudoers`. It must be
installed as `/etc/sudoers.d/91-semaphore-edge-maintenance`; Master post-scan and
health validators are part of the required command set. Compose drivers always
force service recreation after pinning the exact scanned digest so a movable tag
cannot leave the previous image running.

Host package updates follow the same manual-only boundary. Install
`config/apt-periodic-manual-only.conf` as
`/etc/apt/apt.conf.d/99-edge-maintenance-manual-only` and mask
`apt-daily.timer`, `apt-daily.service`, `apt-daily-upgrade.timer`,
`apt-daily-upgrade.service` and `unattended-upgrades.service`. This disables
autonomous metadata refresh and package installation without affecting the
explicit `apt-get` calls made by the `APT_EDGE` driver.

The first operator-initiated run of each driver is its runtime acceptance:
review the displayed version, backup/rollback and health checks, then launch it
from `update.escloud.us`. No other launch surface is supported.
