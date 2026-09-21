# Stage 07A — Home → Edge Maintenance Porting Map — 2026-09-21

## Status

**ACCEPTED IMPLEMENTATION BASELINE / STAGE 7A IN PROGRESS**

This record converts the accepted Stage 7 reuse principle into an exact implementation map. It does not mark Stage 7A deployed or accepted.

## Authoritative Home source

Live source runtime:

- controller: CT1000 `maintenance`;
- worktree: `/opt/maintenance-repo`;
- branch: `main`;
- source HEAD: `6e7fa48c983a8549e8a5f0fa036006071a941df8`;
- source commit: `feat(ha): handle pending os reboot and staging in manual-update`;
- Semaphore: `2.18.29-91719b9-1785218410`;
- service model: host-native binary + systemd + SQLite;
- dashboard webroot: `/var/www/maintenance-status`.

The CT1000 repository has no remote. The Cloud implementation therefore ports the audited source contract into the Cloud Infrastructure canonical repository rather than depending on CT1000 as a deployment source.

## Porting rule

Preserve proven Home framework semantics where they are host-agnostic. Replace only Home/PVE-specific transport, inventory and service implementations.

Do not copy:

- CT1000/PVE SSH credentials or host keys;
- the Home Semaphore bearer token;
- Home SQLite database/runtime history;
- PVE VMID/PCT/QGA inventory logic;
- Home target definitions that do not exist on edge.

## File / responsibility map

| Home implementation | Edge Stage 7A treatment |
|---|---|
| `scripts/maintenance-status-render` | preserve the same `VERSION|` parsing, atomic status JSON write and summary model |
| `scripts/maintenance-versions-collector` | preserve output/status contract; replace PVE/guest workers with edge-local APT/native/Docker/Git/user-tool collectors |
| `scripts/maintenance-targets-refresh` | preserve `maintenance.json` contract and isolated fresh APT simulation; replace SSH/PVE/QGA probing with local edge probing |
| `playbooks/versions.yml` | preserve orchestration shape; execute edge collector locally through explicit non-interactive sudo |
| `playbooks/maintenance-refresh.yml` | preserve refresh chain |
| `scripts/manual-update` | not activated in Stage 7A; Stage 7B ports only applicable component-specific patterns |
| `scripts/master-batch-update` | not activated in Stage 7A; Stage 7B adapts cache preflight/dispatch to final edge targets |
| `dashboard/index.html` | copy/adapt immediately; retain status/action API model and polling |
| `dashboard/actions.json` | copy/adapt with `read_only=true`, update/master actions disabled until Stage 7B acceptance |
| Home nginx `/status/` | preserve static status contract; Cloud public ingress deferred until local Stage 7A acceptance |
| Home nginx `/api/` token injection | preserve architectural idea only; generate a new edge-local token later, never copy Home token |
| Home Semaphore UI proxy | future `ops.escloud.us`; not required for first local read-only deployment |

## Stage 7A read-only component inventory

The first edge collector covers the installed surface without executing updates:

### System / APT

- NGINX
- CERTBOT
- UFW
- DOCKER_ENGINE
- DOCKER_COMPOSE
- CONTAINERD
- NETBIRD
- SYNCTHING
- aggregate `APT_EDGE` simulation status

### Native / upstream

- XRAY
- HYSTERIA2
- BACKREST
- RESTIC

### Docker applications

- N8N
- AUTHELIA
- MATTERMOST
- POSTGRESQL
- STALWART
- BULWARK

### Git / user-space / maintenance

- HERMES
- CLOUDCLI
- CODEX
- ANTIGRAVITY
- SEMAPHORE

This inventory is the Stage 7A status surface, not yet the final Stage 7B update-target list. A component may remain visible but not update-managed when its supported lifecycle is deliberately external or unresolved.

## Stage 7A safety boundary

The first deployment may:

- install Semaphore/Ansible prerequisites;
- create the new Semaphore service/user/config/SQLite state;
- create the edge maintenance worktree and status webroot;
- run read-only version collection;
- perform isolated APT metadata refresh/simulation under temporary directories;
- inspect Docker registries/GitHub/upstream metadata;
- render local status JSON/dashboard files.

It must not:

- execute a real package upgrade;
- pull/recreate production containers;
- run `maintctl update`;
- update Git application worktrees;
- restart application services as part of version discovery;
- invoke Backrest as a universal update gate;
- expose `update.escloud.us` or `ops.escloud.us` before local framework acceptance.

## Dashboard contract

Keep the existing Home dashboard contract:

- `/status/maintenance.json`;
- `/status/actions.json`;
- 20-second status polling;
- Semaphore task API model for later actions.

For Stage 7A, action configuration is intentionally read-only. Update buttons and Master Batch must remain unavailable even if the collector reports `UPDATE_AVAILABLE`.

## Semaphore lifecycle

Install current upstream stable Semaphore through its normal native Linux distribution path rather than pinning to the older CT1000 version solely for parity. Preserve the proven Home service model:

- dedicated `semaphore` service account;
- host-native binary;
- `/etc/semaphore/config.json`;
- `/var/lib/semaphore/database.sqlite`;
- loopback-only listener;
- systemd persistence.

The Home version is evidence of the working architecture, not a pinning requirement.

## Stage 7A acceptance gates

Before Stage 7B starts:

1. Semaphore active/enabled and loopback-only.
2. zero failed systemd units attributable to the deployment.
3. version collector completes without production mutation.
4. status renderer and target refresh produce valid JSON.
5. expected edge target set is complete and duplicate-free.
6. dashboard baseline consumes the generated status locally.
7. action configuration is read-only; no update template can run.
8. existing edge services/containers pass bounded non-regression.
9. no Home credential/token material exists on edge.

Only after these gates pass do real component drivers enter Stage 7B.
