# OpenProject Pre-Decommission Extended Audit — 2026-10-01

**Status:** READ-ONLY AUDIT COMPLETE  
**Runtime mutation:** NONE  
**Decommission:** NOT STARTED  
**Plane deployment:** NOT STARTED  
**Purpose:** preserve the verified pre-change OpenProject state before any stop, replacement, or cleanup work.

## Scope boundary

This file is an **audit record only**. It is not a rebuild specification, migration plan, cleanup plan, or target Plane architecture.

The operator-directed subsequent sequence is explicitly:

1. preserve this extended audit checkpoint;
2. fully stop OpenProject **without deleting it**;
3. deploy and verify Plane as the replacement;
4. only after Plane is accepted, decommission OpenProject and remove its remaining edge-specific traces.

Until step 4, OpenProject configuration, data, database state, integration state, and files are retained as rollback/reference material.

## Audit execution

The first audit attempt stopped before application inspection because Git rejected root access to the canonical repository as `dubious ownership`. No Git configuration or repository mutation was performed.

Recovery audit:

- block: `OPENPROJECT_PRE_DECOMMISSION_AUDIT_RECOVERY_V3`;
- final result: `RC=0`;
- root gate: PASS;
- canonical Git commands executed as user `core`;
- OpenProject Git inspected using command-local `safe.directory`;
- persistent Git configuration mutation: NONE;
- application/runtime mutation: NONE.

## Host checkpoint

| Property | Observed value |
|---|---|
| Host | `edge.escloud.us` |
| OS | Ubuntu 26.04.1 LTS |
| Kernel | `7.0.0-34-generic` |
| Architecture | `x86_64` |
| Virtualization | KVM / QEMU i440FX |
| Docker Engine | `29.8.1` |
| Docker Compose | `v5.5.1` |
| Canonical repo | `/home/core/projects/cloud-infrastructure` |
| Canonical HEAD | `c454133fa58615ab83d8e33d16d7f683cd4baa2e` |
| Canonical working tree | clean |

## OpenProject upstream checkout

Observed runtime checkout:

- path: `/opt/openproject`;
- owner: `root:root`;
- mode: `0755`;
- size: approximately `276K` excluding Docker-managed persistent data;
- upstream: `https://github.com/opf/openproject-docker-compose.git`;
- branch: `stable/17`;
- HEAD: `8c349d3b2a4e8ae5f5c253b5392993777148bc2f`;
- upstream tracking: `origin/stable/17`;
- tracked Git tree: clean.

Observed local runtime files include:

- `.env` with mode `0600`;
- upstream `docker-compose.yml`;
- local `docker-compose.override.yml`;
- `caddy/Caddyfile`;
- upstream `control/` and `proxy/` trees.

## Runtime ↔ canonical reconciliation

### Caddy

Runtime `/opt/openproject/caddy/Caddyfile` matches canonical
`deployments/edge/openproject/caddy/Caddyfile`.

SHA-256:

`c84ecea869a2194a73c9110436320f505afee311eb89681d594b7130dfdd920d`

**Result:** MATCH.

### Compose override

Runtime SHA-256:

`0b981b54151487e0620f3449f20f9f31bb28aadffde4fc55314c7ee95933d2e4`

Canonical SHA-256:

`ef53ce6f5590805664d9f5be3aed5f849a2315f03acaccd8db960f14b258dcf9`

**Result:** DRIFT / NO MATCH.

The live override contains newer accepted functionality not represented by the canonical copy inspected during this audit, including:

- outbound SMTP wiring;
- runtime hostname normalization for `web`;
- external `edge_internal` attachment;
- aliases `openproject` and `openproject-worker`;
- `OPENPROJECT_SSRF_PROTECTION_IP_ALLOWLIST=172.30.0.0/24` for `web` and `worker`;
- external `postgres_net`;
- embedded `db` disabled;
- `hocuspocus` disabled;
- real-time text collaboration disabled.

**Audit authority:** for this checkpoint, fresh runtime evidence is authoritative over the stale canonical OpenProject override.

## Runtime environment

Sanitized runtime configuration confirms:

- Compose project: `openproject`;
- image track: `17-slim`;
- HTTPS mode enabled;
- public hostname: `projects.escloud.us`;
- host loopback publication: `127.0.0.1:18082`;
- IMAP disabled;
- persistent app-data volume name: `opdata`;
- default language: `ru`;
- database and seed-admin credentials exist locally but are intentionally not recorded.

### Outbound SMTP

Observed live settings:

- endpoint: `mail.escloud.us:465`;
- implicit TLS: enabled;
- STARTTLS auto: disabled;
- SMTP auth: `plain`;
- peer verification: enabled;
- sender account: `openproject@escloud.us`;
- sender identity: `OpenProject <openproject@escloud.us>`;
- SMTP password retained only in local runtime configuration and omitted here.

## Effective Docker topology

Effective Compose services:

- `autoheal`;
- `cache`;
- `cron`;
- `web`;
- `proxy`;
- `seeder` as a Compose service definition;
- `worker`.

Six persistent containers were running:

| Container | Role | State |
|---|---|---|
| `openproject-web-1` | web | running / healthy |
| `openproject-worker-1` | background worker | running |
| `openproject-cron-1` | scheduled jobs | running |
| `openproject-cache-1` | memcached | running |
| `openproject-proxy-1` | Caddy proxy | running |
| `openproject-autoheal-1` | health/restart helper | running / healthy |

Observed images at audit time:

- `openproject/openproject:17-slim`;
- `openproject/proxy`;
- `memcached`;
- `willfarrell/autoheal:1.2.0`.

Observed OpenProject application image digest:

`sha256:48952034215d2a8ecf07086db86be55c74819cc76aa26af61f8da9ce5f06eda2`

Image versions/digests are historical evidence only.

## Persistent storage

Exactly one OpenProject Compose-labelled Docker volume was present:

`openproject_opdata`

Observed properties:

- driver: `local`;
- mountpoint: `/var/lib/docker/volumes/openproject_opdata/_data`;
- size: approximately `908K`;
- owner: `core:core`;
- mode: `0775`;
- contains `files/attachment`;
- mounted by three OpenProject containers;
- non-OpenProject consumers: **0**.

It is mounted as OpenProject application asset/attachment storage at `/var/openproject/assets`.

## Docker networks

### OpenProject-owned networks

`openproject_frontend` members:

- `openproject-proxy-1`;
- `openproject-web-1`.

`openproject_backend` members:

- `openproject-cache-1`;
- `openproject-cron-1`;
- `openproject-web-1`;
- `openproject-worker-1`.

Both networks carry Compose ownership labels for project `openproject`.

### Shared `postgres_net`

Observed members:

- `postgres`;
- `mattermost-mattermost-1`;
- `nextcloud-app-1`;
- `nextcloud-cron-1`;
- `openproject-web-1`;
- `openproject-worker-1`;
- `openproject-cron-1`.

This is shared PostgreSQL infrastructure and is not OpenProject-owned.

### Shared `edge_internal`

Observed members:

- `n8n`;
- `mattermost-mattermost-1`;
- `openproject-web-1`;
- `openproject-worker-1`.

This is shared application-integration infrastructure and is not OpenProject-owned.

## Shared PostgreSQL — OpenProject-specific state

The shared `postgres` service was running.

Observed OpenProject-specific state:

| Property | Value |
|---|---|
| Database | `openproject` |
| Role | `openproject` |
| Database exists | true |
| Role exists | true |
| Database size | approximately `46 MB` |
| Non-system tables | `212` |
| Projects | `3` |
| Users | `6` |
| Work packages | `93` |

Extensions:

- `btree_gist`;
- `pg_trgm`;
- `plpgsql`;
- `unaccent`.

The PostgreSQL service itself is shared infrastructure. No deletion is authorized by this audit.

## Public ingress

Public hostname:

`projects.escloud.us`

Observed DNS:

`45.92.156.17`

Nginx configuration test:

**PASS**

OpenProject-specific nginx configuration exists at:

- `/etc/nginx/sites-available/projects-escloud-us.conf`;
- `/etc/nginx/sites-enabled/projects-escloud-us.conf`.

Observed topology includes:

- HTTP → HTTPS redirect;
- internal nginx listener on `127.0.0.1:8080` using proxy protocol;
- proxying to OpenProject through loopback;
- Docker publication `127.0.0.1:18082 -> openproject-proxy-1:80/tcp`;
- a `/hocuspocus` nginx location still exists although application-level real-time collaboration is disabled.

## Systemd

No OpenProject-specific systemd unit was found under:

- `/etc/systemd/system`;
- `/home/core/.config/systemd/user`.

Observed OpenProject lifecycle ownership is Docker/Compose.

## Backup integration

Host script `/usr/local/sbin/edge-state-prepare` contains explicit OpenProject handling:

- quiesce `openproject-web-1`;
- quiesce `openproject-worker-1`;
- quiesce `openproject-cron-1`;
- logical `pg_dump` of database `openproject`;
- non-empty dump validation;
- capture of `openproject_opdata`;
- restart/recovery of the stopped OpenProject containers;
- post-restart OpenProject readiness validation;
- OpenProject stage PASS marker.

The text scan did not find a direct OpenProject reference under `/var/lib/backrest`; however, OpenProject is demonstrably part of the host-side backup preparation lifecycle through `edge-state-prepare`.

## Edge Monitor integration

`/usr/local/sbin/edge-monitor` contains explicit OpenProject monitoring for:

- OpenProject service identity;
- public availability of `projects.escloud.us`;
- web;
- worker;
- cron;
- cache;
- proxy;
- autoheal.

No monitoring mutation was performed.

## Maintenance / Semaphore integration

Canonical repository contains OpenProject-specific Maintenance logic in:

- `maintenance/edge/config/update-units.json`;
- `maintenance/edge/config/semaphore-templates.json`;
- `maintenance/edge/config/manual-driver-enablement.example.json`;
- `maintenance/edge/scripts/maintenance-versions-collector`;
- `maintenance/edge/scripts/manual-update`;
- `maintenance/edge/scripts/update-openproject`;
- `maintenance/edge/playbooks/updates/openproject.yml`;
- `maintenance/edge/tests/`.

The canonical Maintenance model identifies OpenProject as an `openproject_compose` unit using `/opt/openproject`.

## Shared PostgreSQL canonical provisioning

OpenProject-specific provisioning entries exist in:

- `deployments/edge/postgres/.env.example`;
- `deployments/edge/postgres/init/01-init.sh`.

They define OpenProject database/role/schema/extension provisioning alongside the shared Mattermost and Nextcloud PostgreSQL contract.

## Application-level integration inventory discovered in canonical state

These are dependencies/history discovered in canonical documentation. This audit did **not** independently rerun every application-level E2E acceptance test.

### GitHub

Canonical accepted state records:

- OpenProject project `Cloud Infrastructure`;
- native GitHub integration;
- dedicated non-admin `github-integration` actor;
- dedicated integration role;
- OpenProject API token used for repository webhook authentication;
- separate GitHub webhook signature secret;
- repository webhook on `Eugene-SN/Cloud-Infrastructure`.

Credential material is intentionally absent from this audit.

### Stalwart

A dedicated mailbox `openproject@escloud.us` is part of the accepted OpenProject mail integration.

### Apple Calendar / iCalendar

Canonical accepted state records:

- native Work Package iCalendar integration;
- private saved calendar `Cloud Infrastructure`;
- persistent Apple Calendar/iCloud subscription;
- bearer URL intentionally excluded from Git.

### Nextcloud

Canonical state records OP-INT-4 as **DEFERRED / CLEAN**:

- production `integration_openproject` absent;
- integration-specific config/migrations/background jobs absent;
- integration-related Nextcloud OAuth clients absent;
- OpenProject Nextcloud Storage / ProjectStorage links returned to zero;
- temporary integration OAuth application absent.

This extended audit did not independently rerun the full Nextcloud residue audit.

### n8n

Canonical accepted state records:

- OpenProject outgoing webhook → `http://n8n:5678/webhook/openproject-events`;
- internal path over `edge_internal`;
- HMAC signature verification;
- n8n workflow `OpenProjectEventIngress01`;
- OpenProject API credential `OpenProjectAPI01`;
- OpenProject-side SSRF allowlist for `172.30.0.0/24`.

The live Compose override independently confirms the `edge_internal` attachment and SSRF allowlist.

### Mattermost

Canonical accepted state records:

- dedicated Mattermost bot `openproject`;
- dedicated private channel `openproject`;
- dedicated n8n Mattermost credential;
- n8n sub-workflow `OpenProjectMattermost01`;
- asynchronous dispatch from `OpenProjectEventIngress01`.

## Important audit findings

1. **Runtime is healthy enough to preserve as the pre-change checkpoint.**
2. **OpenProject upstream tracked tree is clean.**
3. **Canonical OpenProject override is stale relative to runtime.**
4. **OpenProject owns its application Compose networks and `openproject_opdata`, but uses shared `postgres_net` and `edge_internal`.**
5. **OpenProject data is split between shared PostgreSQL and `openproject_opdata`.**
6. **OpenProject has dependencies outside `/opt/openproject`: nginx, Edge Monitor, backup preparation, Maintenance/Semaphore, PostgreSQL provisioning, Stalwart, n8n, Mattermost, GitHub and iCalendar state.**
7. **No OpenProject-specific systemd service was found.**
8. **No OpenProject removal or cleanup has been started.**

## Audit safety markers

```text
AUDIT_MUTATION=NO
PERSISTENT_GIT_CONFIG_MUTATION=NO
SHARED_POSTGRES_DELETE_AUTHORIZATION=NO
SHARED_POSTGRES_NET_DELETE_AUTHORIZATION=NO
EDGE_INTERNAL_DELETE_AUTHORIZATION=NO
OPENPROJECT_DECOMMISSION_MUTATION=NOT_STARTED
PLANE_DEPLOYMENT=NOT_STARTED
PRE_DECOMMISSION_AUDIT=COMPLETE
```

## Checkpoint

This document is the preserved pre-change OpenProject audit checkpoint.

The next authorized runtime action is **stop-only OpenProject**, retaining its files, database, persistent volume and integration state while Plane is deployed and evaluated.

Full OpenProject deletion is explicitly deferred until Plane has been deployed, verified and accepted.
