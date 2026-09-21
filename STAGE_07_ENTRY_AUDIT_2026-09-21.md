# Stage 07 — Entry Audit & Porting Baseline — 2026-09-21

## Status

**Stage 7 — Edge Maintenance & Update: IN PROGRESS**

Entry requirements/runtime review is complete enough to begin Stage 7A implementation extraction and porting.

## Accepted source baseline

The implementation source baseline is the live accepted Home Maintenance runtime on CT1000:

- host: CT1000 `maintenance`, Debian 13;
- Semaphore `2.18.29-91719b9-1785218410`, host-native at `/usr/local/bin/semaphore`;
- service: `semaphore.service`, active/enabled, running as user/group `semaphore`;
- state DB: `/var/lib/semaphore/database.sqlite`;
- implementation worktree: `/opt/maintenance-repo`;
- Ansible `12.0.0` / ansible-core `2.19.4`;
- no Docker dependency for the maintenance controller itself.

The Home implementation is a mature orchestration framework, not a thin Semaphore wrapper. It includes:

- version/stable-state collection;
- machine-readable maintenance cache/status rendering;
- fixed target allowlists;
- APT and native per-component update drivers;
- individual manual update playbooks;
- Master Batch orchestration;
- post-update refresh and acceptance;
- reboot-required detection;
- dashboard source and action mapping.

The latest audited Home Master Batch task completed successfully before Stage 7 entry review.

## Accepted Stage 7 architecture direction

Edge Maintenance is derived from the Home Maintenance implementation rather than designed independently.

Preserve where applicable:

- Semaphore -> Ansible playbook -> native script separation;
- version/status collector and cache model;
- fixed-target dispatch;
- component-specific update adapters;
- manual update workflow;
- Master Batch pattern;
- post-update refresh and acceptance;
- dashboard/status/action contract;
- automatic real updates disabled by default.

Replace rather than copy:

- PVE/VMID inventory;
- `pct`, `qm`, QGA and Home guest control logic;
- Home-specific target definitions and component drivers;
- Home credentials, SSH keys and controller-specific state.

`update.escloud.us` begins as an adapted copy of the existing Home Maintenance dashboard implementation. Stage 7C is an adaptation/refinement task, not a greenfield frontend build.

## Edge runtime update surface confirmed at entry

Current edge classes include:

- APT/repository-managed foundation: nginx, Certbot, UFW, Docker Engine/CLI/Compose, containerd, NetBird;
- standalone/native binaries: Xray, Hysteria2, Backrest, Restic;
- package-managed Syncthing at `/usr/bin/syncthing`;
- Docker Compose applications: n8n, Authelia, Mattermost/PostgreSQL, Stalwart, Bulwark;
- user-space CLIs: CloudCLI, Codex CLI, Antigravity CLI;
- git-managed Hermes and Mattermost deployment worktree;
- existing `maintctl` updater for Xray/Hysteria2.

Existing `maintctl` already provides Xray/Hysteria2 latest-version lookup, local binary/config backup, upstream artifact installation, config validation, service restart and post-update active-state checks. Stage 7 should adapt/wrap that accepted native path rather than duplicate it.

No Stage 7 production update mutation has been executed yet.

## Backup sequencing boundary

Stage 6 precedes Stage 7 so verified backup/restore capability exists while the maintenance framework is deployed and tested.

This is a deployment/testing safety prerequisite only. It does **not** create a universal runtime Backrest gate before every production update.

Per-update backups are component-specific and are added only where the actual supported update/recovery path justifies them.

## Stage decomposition

### Stage 7A — Home Maintenance Framework Port

- extract and review the live CT1000 framework implementation;
- deploy/adapt Semaphore and the maintenance repository on edge;
- port dashboard/status/action sources;
- replace Home inventory with edge-local execution;
- reach read-only version/status acceptance before any real update mutation.

### Stage 7B — Edge Update Drivers & Recovery

- implement edge-specific collectors and update adapters;
- preserve native supported update paths;
- implement component-specific health/failure/recovery behavior;
- accept individual updates and Master Batch;
- verify one controlled update/recovery scenario.

### Stage 7C — Codex: adapt `update.escloud.us`

- begin from the copied Home dashboard;
- adapt labels, grouping, controls and presentation for Cloud/edge;
- keep `update.escloud.us` separate from `app.escloud.us`.

## Next action

Perform bounded source extraction of the live Home implementation pieces that were not fully captured by the first audit, especially:

- `scripts/maintenance-versions-collector`;
- `scripts/maintenance-status-render`;
- `scripts/maintenance-targets-refresh`;
- `scripts/manual-update`;
- `scripts/master-batch-update`;
- dashboard source and related nginx serving contract.

Then build the exact Home -> Edge porting map and begin Stage 7A deployment.
