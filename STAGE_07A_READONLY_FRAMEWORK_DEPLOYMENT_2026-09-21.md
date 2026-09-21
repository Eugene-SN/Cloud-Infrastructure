# Stage 07A — Edge Read-only Maintenance Framework Deployment — 2026-09-21

## Status

**DEPLOYMENT CHECKPOINT: PASS**

Stage 7A remains **IN PROGRESS**. This checkpoint accepts the local read-only framework deployment, but does not yet accept the final dashboard -> Semaphore -> refresh E2E contract and does not enable any real update action.

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

A specific collector normalization defect was found after deployment: installed Hysteria2 `2.12.3` is compared against upstream release tag `app/v2.12.3`, causing a false `UPDATE_AVAILABLE`. This is a Stage 7A collector defect, not an actual Hysteria update. It must be corrected before final Stage 7A acceptance.

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

## Next finite work

1. Correct only the Hysteria2 release-tag normalization and re-run the read-only refresh.
2. Create one Semaphore `Edge Maintenance` project with one read-only Refresh template.
3. Link the copied dashboard action contract to that project/template while keeping all update actions disabled.
4. Verify dashboard -> Semaphore -> refresh -> JSON -> dashboard E2E.
5. Only then consider Stage 7A COMPLETE / ACCEPTED and proceed to Stage 7B update drivers.
