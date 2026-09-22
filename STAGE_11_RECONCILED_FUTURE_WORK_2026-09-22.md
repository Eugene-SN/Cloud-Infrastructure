# Stage 11 — Reconciled Future Work and Cleanup Outcome

Date: 2026-09-22

Status: **ACCEPTED / ACTIVE CLEANUP**

## Purpose

This record closes the planning ambiguity discovered after Stage 10 by assigning every remaining identified capability a concrete disposition.

## Future implementation tasks

### Stage 12 — Nextcloud Cloud Drive & Private Workspace Access

Status: **PLANNED / ACCEPTED ENTRY CONTRACT**

Working branch:

`stage-12-nextcloud-cloud-drive`

Scope:

- `cloud.escloud.us` personal cloud-drive using Nextcloud as the primary selected candidate;
- product-independent cloud user dataset at `/srv/cloud/files`;
- Nextcloud-specific state under `/srv/nextcloud`;
- dedicated Nextcloud PostgreSQL;
- native clients, WebDAV/API, sharing, OIDC and representative n8n integration;
- private SMB access to explicitly selected ordinary POSIX project/workspace directories;
- SMB trusted/private access only; no public TCP/445;
- no automatic SMB exposure of `/srv/cloud/files`;
- backup/recovery, maintenance, monitoring and bounded non-regression integration.

### Backrest WebUI ingress

Status: **PLANNED / DEFERRED**

`backup.escloud.us` will publish the already deployed Backrest WebUI through the accepted ingress/auth architecture.

This is not a new backup product and does not redesign Stage 6.

### WenTian technical publishing

Status: **DEFERRED UNTIL CONTENT READY**

`docs.escloud.us` is reserved for a curated WenTian technical documentation publishing/library site modeled functionally on Lenovo Press.

Target content:

- selected WenTian Product Guides;
- selected WenTian Datasheets;
- English translations;
- Russian translations;
- source/revision metadata and useful document navigation/search.

Do not deploy a placeholder CMS, DMS or empty documentation site. Implementation begins only after a useful translated document corpus exists.

## Retired / historical capabilities

The following are not future deployment targets:

- legacy Filestash runtime;
- public Syncthing WebUI;
- `sync.escloud.us`;
- `go.escloud.us`;
- Homepage;
- Cockpit;
- Maintenance Center;
- legacy monitoring nginx/socket proxy;
- legacy speedtest surface;
- legacy Codex runner / automation-runner bridge;
- browser-stack / Selkies;
- legacy same-VPS Restic architecture;
- legacy `/srv/oem-docs` layout.

Current replacements remain authoritative where applicable:

- `app.escloud.us` replaces Homepage;
- Stage 7 Semaphore/`update.escloud.us` replaces Maintenance Center;
- Stage 8 `edge-monitor` replaces legacy monitoring surfaces;
- Hermes private machine interface/direct executors replace the legacy Codex runner;
- Stage 6 Backrest replaces the legacy backup architecture;
- current Syncthing remains private Knowledge replication only;
- Stage 12 Nextcloud will own end-user cloud synchronization.

## External DNS cleanup

The operator manages Cloudflare DNS manually.

Confirmed cleanup targets:

- delete stale `go.escloud.us` record;
- delete stale `sync.escloud.us` record.

Do not automate or mutate Cloudflare from Stage 11.

## Current Stage 11 closeout work

Before Stage 11 is complete:

1. remove only verified stale runtime/configuration/TLS artifacts for retired legacy names/services;
2. preserve all accepted current services;
3. verify nginx, TLS, listeners, systemd, Docker and monitoring non-regression;
4. reconcile final current-state documents;
5. leave future deployments to their dedicated tasks above.

Stage 10 remains the accepted pre-Stage-11 baseline; any cleanup verification is bounded to the affected namespace/configuration surfaces.
