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

The candidate templates and all drivers may be installed while the dashboard
remains read-only. Execution is fail-closed: `/etc/edge-maintenance/driver-acceptance.json`
must explicitly accept each unit, and Master Batch has a separate `master`
gate. The shipped example accepts nothing. Creating templates does not accept
drivers and must not change `actions.json` template IDs.

Before any driver is accepted, run its `manual-update TARGET --preflight`,
review backup/rollback and health checks, then perform a separately authorized
manual runtime acceptance. Production updates are not part of source or
read-only deployment verification.
