# Stage 07A — Edge Read-only Maintenance Framework Deployment — 2026-09-21

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker: `STAGE07A_READONLY_DASHBOARD_SEMAPHORE_E2E=PASS`.

## Deployment evidence

Final marker:

`STAGE07A_EDGE_READONLY_FRAMEWORK_DEPLOYMENT=PASS`

Recovery continuation completed with `RC=0`.

The first deployment attempt stopped before Semaphore installation because the installer selected the Community archive but looked for its filename in the non-Community checksum manifest. Recovery confirmed no partial Semaphore artifacts and resumed from the exact failure point. The recovery installer used the SHA-256 digest attached to the selected GitHub release asset.

## Current runtime

- Semaphore Community `2.19.12-012ed06-1788086239`;
- host-native binary: `/usr/local/bin/semaphore`;
- systemd service: `semaphore.service`, active/enabled, zero restarts at acceptance;
- service identity: `semaphore:semaphore`;
- listener: `127.0.0.1:3000` only;
- config: `/etc/semaphore/config.json`;
- SQLite: `/var/lib/semaphore/database.sqlite`;
- worktree/runtime source: `/opt/edge-maintenance`;
- status webroot: `/var/www/maintenance-status`;
- Ansible `13.1.0`, ansible-core `2.20.1`.

Public ingress remains disabled.

## Read-only contract

The deployed framework successfully executed:

- version collector;
- status renderer;
- APT target probe/cache renderer.

Observed target model:

- 23 component version rows;
- 24 maintenance rows including aggregate `APT_EDGE`;
- 1 APT target;
- 23 native/component targets;
- no duplicate/missing target rows;
- dashboard/action configuration remains `read_only=true`;
- `auto_update=false`;
- no update or Master Batch template IDs are active;
- no production component update was executed.

## Initial status result

The first live refresh produced:

- CURRENT: 16;
- UPDATE_AVAILABLE: 8;
- CHECK_FAILED: 0;
- reboot-required: 0.

The initial collector exposed a Hysteria2 normalization defect: installed `2.12.3` was compared against upstream tag `app/v2.12.3`. The collector now strips the upstream `app/` namespace for Hysteria2; final accepted state is `CURRENT=v2.12.3`, `AVAILABLE=v2.12.3`, `STATUS=CURRENT`.

Other observed actionable rows are retained pending component-specific Stage 7B handling. A movable Docker tag may legitimately report an update when its remote digest changes even if the visible tag string is unchanged.

## Non-regression

At checkpoint acceptance:

- nginx active;
- Xray active;
- Hysteria2 active;
- Docker active;
- containerd active;
- NetBird active;
- Syncthing active;
- Backrest active;
- CloudCLI active;
- Semaphore active;
- Hermes gateway/dashboard user services active;
- n8n healthy;
- Mattermost healthy;
- PostgreSQL running;
- Stalwart healthy;
- Bulwark running;
- Authelia healthy;
- no failed systemd units.

`PRODUCTION_NON_REGRESSION_GATE=PASS`

## Final accepted E2E

Final accepted control path:

```text
adapted Home dashboard
  -> loopback nginx API proxy
  -> Semaphore project 1 / Refresh template 1
  -> canonical Cloud-Infrastructure GitHub repository
  -> maintenance/edge/playbooks/semaphore-refresh.yml
  -> local read-only edge collectors
  -> status.json / maintenance.json
  -> dashboard
```

Final runtime contract:

- Semaphore repository: `https://github.com/Eugene-SN/Cloud-Infrastructure.git`, branch `main`;
- refresh template: ID `1`, `01. Refresh — Edge Maintenance Status`;
- dashboard loopback endpoint: `127.0.0.1:18070`;
- public ingress: not configured;
- update template count: `0`;
- Master Batch: disabled;
- automatic updates: disabled;
- real component updates executed by Stage 7A: none;
- final maintenance summary: `TOTAL=24`, `CURRENT=17`, `UPDATE_AVAILABLE=7`, `CHECK_FAILED=0`, `REBOOT_REQUIRED=0`;
- production non-regression: PASS.

The dashboard-triggered Semaphore task completed successfully and advanced the generated status timestamp, proving the complete read-only E2E contract.

## Next finite work

Proceed to **Stage 7B — Edge Update Drivers & Recovery**. Preserve the accepted Stage 7A read-only boundary until each concrete component driver and its health/recovery contract are implemented and accepted.
