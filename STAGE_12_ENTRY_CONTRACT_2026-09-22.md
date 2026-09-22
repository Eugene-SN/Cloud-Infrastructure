# Stage 12 — Nextcloud Cloud Drive Deployment & Acceptance

Date: 2026-09-22

Status: **PLANNED / ACCEPTED ENTRY CONTRACT**

Branch: `stage-12-nextcloud-cloud-drive`

## Purpose

Stage 12 deploys and accepts the previously reconciled missing `cloud.escloud.us` capability as a production personal cloud-drive on `edge`.

Stage 11 remains active for discovery/classification of other omitted infrastructure capabilities. Stage 12 is intentionally separated so Nextcloud implementation does not obscure the remaining Stage 11 inventory work.

## Carry-forward decisions

Do not reopen these accepted decisions without concrete runtime incompatibility:

1. **Primary product:** Nextcloud.
2. **Fallback only:** ownCloud Infinite Scale, only if a concrete Nextcloud incompatibility or unacceptable lifecycle/resource constraint is demonstrated.
3. **Excluded:** OpenCloud is no longer a Stage 12 candidate.
4. `cloud.escloud.us` is a level-3 personal cloud-drive, not a WebUI over the full edge filesystem.
5. Project/runtime workspaces remain separate ordinary POSIX data and may be exposed through SMB independently of the cloud-drive.
6. Normal cloud access uses native desktop/mobile clients, WebDAV/API and supported integrations; direct POSIX mutation of cloud user data is not the normal workflow.
7. Canonical product-independent user dataset:
   - `/srv/cloud/files`
8. Nextcloud-specific persistent state:
   - `/srv/nextcloud/data`
   - `/srv/nextcloud/postgres`
9. `/srv/cloud/files` must not contain Nextcloud internal runtime/application state.
10. Nextcloud must expose `/srv/cloud/files` through a supported storage integration rather than using it as the internal Nextcloud `datadirectory`.
11. Nextcloud uses a **dedicated PostgreSQL instance**, not the existing Mattermost PostgreSQL lifecycle.
12. Existing host nginx/Xray/shared TLS remain the ingress foundation.
13. Authelia is used as the OIDC identity provider through Nextcloud-native OIDC integration; ordinary nginx `auth_request` is not the target interactive/native-client model for `cloud.escloud.us`.
14. No Office suite, full-text-search stack, antivirus stack, media/photo stack or other heavyweight unrelated extension is introduced without a concrete requirement.

## Entry runtime baseline

Fresh Stage 11 read-only audits established:

- host: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- 2 vCPU;
- ~15 GiB RAM total;
- ~12 GiB RAM available at audit time;
- 4 GiB swap, effectively unused;
- root filesystem ~155 GiB total / ~133 GiB available;
- idle load approximately 0.1;
- zero failed systemd units;
- existing production Docker workloads healthy;
- `/srv/cloud`, `/srv/nextcloud`, and `/opt/nextcloud` absent;
- no existing nginx vhost for `cloud.escloud.us`;
- public DNS `cloud.escloud.us -> 45.92.156.17`;
- shared TLS certificate already contains `cloud.escloud.us`;
- Authelia OIDC discovery is live at `https://auth.escloud.us` with Authorization Code, refresh token and PKCE S256 support;
- current Mattermost PostgreSQL is isolated in `mattermost_default` and remains unrelated to the target Nextcloud DB;
- current general Backrest `edge-state` plan does not yet have a Nextcloud-specific exclusion/consistency contract.

## Target deployment shape

Production-shaped baseline:

```text
Internet / native clients
        |
        v
cloud.escloud.us
        |
Xray -> host nginx -> loopback Nextcloud HTTP backend
                         |
                         +-- Nextcloud application
                         +-- dedicated PostgreSQL
                         +-- Redis/Valkey locking/cache
                         +-- cron/background-jobs runtime
                         |
                         +-- supported storage integration
                                  |
                                  v
                           /srv/cloud/files
```

Application-specific state remains under `/srv/nextcloud`.

Use upstream-supported current stable release paths. Version/channel constraints may be used where required by Nextcloud's supported major-upgrade sequence; do not introduce unnecessary digest pinning.

## Functional target

Stage 12 must establish and verify:

- working WebUI at `https://cloud.escloud.us`;
- Nextcloud-native authentication through Authelia OIDC;
- macOS native client with File Provider / Files-on-Demand behavior where supported by the deployed current client;
- Windows native client with virtual-files / Files-on-Demand behavior;
- iOS/iPadOS native client where practical;
- selective/offline access;
- upload/download/create/move/delete;
- filename search;
- public share links;
- `/srv/cloud/files` visible and writable through the supported Nextcloud storage layer;
- native/supported n8n integration for representative file operations;
- supported WebDAV/API access path suitable for Codex/Hermes/Antigravity when later workflows need it;
- no exposure of project/runtime workspaces through the cloud-drive.

## Resource policy

Do not pre-allocate arbitrary large limits merely because memory is available.

Deploy first, measure actual idle and representative burst usage, and only add resource limits if evidence justifies them.

The current 2-vCPU / ~15-GiB edge baseline passed the Stage 11 capacity gate; resource pressure is not currently a deployment blocker.

## Backup and recovery gate

Stage 12 is not accepted until Nextcloud backup/recovery is integrated with the accepted Stage 6 model.

Required distinction:

- portable user dataset: `/srv/cloud/files`;
- Nextcloud-specific state: `/srv/nextcloud/*`;
- PostgreSQL: application-consistent dump/state;
- Nextcloud config/app state: preserved consistently with the DB;
- avoid accidental duplication of a potentially large cloud dataset in the generic `edge-state` chain.

The final backup topology is chosen from actual post-deployment data/runtime behavior rather than guessed in advance.

A real isolated restore/usability test is required before Stage 12 final acceptance.

## Deployment workflow

Use dependency-aware CHECK -> CHANGE -> VERIFY units:

1. pre-mutation exact deployment preflight;
2. create storage/application paths with verified ownership/modes;
3. deploy dedicated PostgreSQL + Redis/Valkey + Nextcloud + cron;
4. verify local application/database/cache/background-job health and measure resource use;
5. configure loopback backend and host nginx ingress for `cloud.escloud.us`;
6. configure Nextcloud-native OIDC against existing Authelia;
7. create/attach the accepted `/srv/cloud/files` storage boundary;
8. perform WebUI/basic Files acceptance;
9. perform macOS native-client/File-Provider E2E;
10. perform Windows native-client/VFS E2E;
11. perform iOS/iPadOS client acceptance where practical;
12. verify public sharing and filename search;
13. verify representative n8n integration plus WebDAV/API machine access;
14. integrate Stage 6 backup/recovery and perform isolated restore;
15. add Stage 7 maintenance/update handling for the new components;
16. add Stage 8 monitoring/status coverage and Stage 9 portal navigation if justified;
17. bounded full non-regression of affected Stage 10 integration boundaries;
18. persist final accepted state to canonical repository.

## Acceptance boundaries

Do not declare Stage 12 complete merely because containers are running.

Final acceptance requires:

- healthy runtime and reboot/lifecycle persistence where required;
- native-client E2E on the actual user platforms;
- OIDC/native-client compatibility;
- portable dataset boundary verified;
- public sharing verified;
- backup + isolated restore proven;
- maintenance/update path integrated;
- monitoring/portal current state reconciled;
- no regression of existing mail, Mattermost, n8n, Hermes, Knowledge, NetBird, maintenance, monitoring or ingress boundaries.

## Non-goals

Stage 12 does not implement:

- user-specific Capture Inbox workflow;
- document OCR/translation business workflow;
- user-specific Hermes/Codex automation logic;
- Office collaboration suite;
- full-text search stack;
- photo-management platform;
- project workspace exposure through `cloud.escloud.us`;
- SMB redesign for project/workspace access.

Those remain separate workflow or later-requirement concerns.

## Relationship to Stage 11

Stage 11 remains the active reconciliation stage in the current conversation/project work.

Stage 12 branch is prepared for a later dedicated deployment thread. No runtime mutation has been performed by creating this branch or contract.
