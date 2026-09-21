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

The first operator-initiated run of each driver is its runtime acceptance:
review the displayed version, backup/rollback and health checks, then launch it
from `update.escloud.us`. No other launch surface is supported.
