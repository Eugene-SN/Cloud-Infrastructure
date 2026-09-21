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
gate and remains disabled until individual runtime acceptance is complete.

The first operator-initiated run of each driver is its runtime acceptance:
review the displayed version, backup/rollback and health checks, then launch it
from `update.escloud.us`. No other launch surface is supported.
