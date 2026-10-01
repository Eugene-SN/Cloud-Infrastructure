# Plane Community on edge

Current acceptance: `PLANE_PART_1_ACCEPTANCE_2026-10-01.md`. This is the operator-authorized Part 1 core deployment; Part 2 integrations are separate future work.

## Authoritative deployment inputs

Official `makeplane/plane` release v1.4.2, release ID 375236829, published 2026-08-23T14:39:21Z. `vendor-reference.json` records source URLs and SHA-256 for the unmodified release assets. This file records accepted installation identity; update discovery uses the official latest stable release API rather than this baseline version.

Runtime tree:

- `/opt/plane/setup.sh`: official release installer reference, unmodified; do not invoke its standalone start/update actions against this external database/proxy deployment.
- `/opt/plane/plane-app/docker-compose.yaml`: official unmodified release Compose.
- `/opt/plane/plane-app/docker-compose.edge.yml`: accepted site override.
- `/opt/plane/plane-app/plane.env`: root:root 0600; actual credentials stay outside Git.
- `/opt/plane/plane-app/variables.vendor.env`, `Caddyfile.vendor-ce`, `vendor-reference.json`: required upstream compatibility/update references.
- `/usr/local/sbin/plane-compose`: sole transparent Compose wrapper, fixing project name, env file and both Compose inputs.

Use `plane-compose` for lifecycle operations. A raw invocation of the vendor Compose or official installer can bypass the site override. The default graph has ten persistent services: web, api, admin, space, live, worker, beat-worker, plane-redis, plane-mq, plane-minio. Migrator is profile `migration`, run with `run --rm --no-deps` before application startup; it is not monitored as persistent. Embedded plane-db and Caddy proxy are disabled by the site profile, with their unwanted volumes/public bindings reset. Normal deployment never selects `disabled-vendor`. Native Docker Compose 5.5.1 validates/interpolates the `!override` and `!reset` merge contract; generic YAML parsing is not sufficient.

## Network and ingress contract

| Service | Host loopback | Container port | nginx route |
|---|---:|---:|---|
| web | 18110 | 3000 | `/` |
| api | 18111 | 8000 | `/api/`, `/auth/`, `/static/` |
| admin | 18112 | 3000 | `/god-mode/` |
| space | 18113 | 3000 | `/spaces/` |
| live | 18114 | 3000 | `/live/` with WebSocket Upgrade |
| plane-minio | 18115 | 9000 | `/uploads/` (effective bucket) |

All six host bindings are 127.0.0.1 only. Public HTTPS stays Xray → host nginx 127.0.0.1:8080 with proxy_protocol and the existing shared certificate. HTTP redirects to HTTPS, retaining the existing ACME route. Plane uses native email/password authentication; no Authelia gate. Forwarded proto/host/port and request path are preserved, including S3 signature-sensitive upload paths. `client_max_body_size 5m` matches the 5,242,880-byte limit. The canonical route source is `projects-escloud-us.conf`.

All ten services retain `plane_default`. Direct database consumers api, worker and beat-worker also join existing `postgres_net`; migration-time migrator joins the same database network. Only api and worker join existing `edge_internal`, with aliases `plane-api` and `plane-worker`. n8n retains alias `n8n`. `WEBHOOK_ALLOWED_HOSTS=n8n`, `WEBHOOK_ALLOWED_IPS=` propagates through the official backend environment. No actual webhook/token/workflow is created.

Dedicated database `plane`, login/owner role `plane`, shared PostgreSQL 18.6. Role is non-superuser, cannot create databases/roles. Password/DATABASE_URL live in Plane env; shared postgres container Env is unchanged. Database migrations on PostgreSQL 18 passed in this production installation.

## State and backup

Seven stable named volumes: plane_uploads, plane_redisdata, plane_rabbitmq_data, plane_logs_api, plane_logs_worker, plane_logs_beat-worker, plane_logs_migrator. The migrator log volume is reusable upstream lifecycle state. RabbitMQ has fixed hostname `plane-mq`, preserving its durable node directory through container recreation. No Plane pgdata, anonymous durable volume or proxy certificate volume exists. The official MinIO image declares `/data` but its Plane command writes `/export`; the unused `/data` is tmpfs, avoiding an empty automatic anonymous volume. Two pre-existing unreferenced PostgreSQL image volumes remain outside Plane ownership and are not deleted on speculation.

Valkey is cache/pubsub; RabbitMQ is the Celery task broker. Their normal vendor volumes persist across ordinary restart/recreate. Historical recovery rebuilds these caches/queues, while task schedules and application data come from PostgreSQL. This classification follows upstream backup guidance (database, uploaded objects, configuration) and the deployed DatabaseScheduler. Pending in-flight tasks are not guaranteed by historical rollback.

Existing `/usr/local/sbin/edge-state-prepare` stages:

1. stop only Plane api/worker/beat-worker/live/MinIO for the Plane stage;
2. native custom-format logical `pg_dump -d plane`, verified by native `pg_restore -l`;
3. copy complete `plane_uploads` storage and protected runtime/Compose/env/wrapper/nginx contract, plus exact image IDs and immutable RepoDigests for all ten services;
4. restart those Plane services, with EXIT recovery for a partial stop;
5. publish the same atomic staging generation used by the existing Backrest edge-state plan and D5 tier-copy hook.

Plane stage never stops shared PostgreSQL, Mattermost or Nextcloud. The existing independent Mattermost/mail staging steps retain their own established quiesce. Recovery files are under `/var/lib/backrest-staging/edge-state/current/plane/{postgres,uploads,runtime}` in accepted Restic snapshots; raw Docker storage remains excluded by the existing plan. API startup after a restart runs upstream management/bootstrap steps and can take about two minutes on this 2-vCPU host, producing transient availability incidents during backup. The selected consistency mechanism is retained; no additional maintenance suppression policy is introduced.

## Manual updates

Maintenance target `PLANE`, driver `plane_compose`, helper `/opt/edge-maintenance/scripts/update-plane`. Semaphore project 1, template 21, `Update Plane`, uses `maintenance/edge/playbooks/updates/plane.yml`. No scheduled Plane updater is enabled.

Discovery resolves official latest stable non-prerelease identity and backend image digest. An unresolved upstream fails closed. Preflight downloads official setup/Compose/env assets into a protected temporary directory and validates both merged and unmerged native Compose graphs. Changed public Caddy routes, service/dependency/storage graph, ports, bucket, database/integration membership, env keys or environment propagation fail closed pending explicit site reconciliation. Current vendor file must match its recorded release hash. Health includes all ten containers, endpoints, migrations and actual worker ping; recovery freshness reuses the existing Backrest monitor threshold and checks actual snapshot contents as well as native dump validity, including protected env and image identity records.

Before any real update, the helper completes a real Backrest flow (including staging and tier copy), then stops the old Plane generation, installs the official new artifacts preserving the site override and secrets, pulls images and runs the official migrator. Migration failure leaves the new application stopped. Post-update health must pass before success; unused former Plane images are removed only after checking all container references. Current installed/latest v1.4.2 was checked by preflight only; no downgrade/re-upgrade was manufactured.

## Bounded rollback/recovery

Recovery is an explicitly requested operator action, not an automatic migration-failure workaround. Use the matched pre-update snapshot for all three parts (DB, objects, runtime). Restore to a protected temporary directory with Restic, inspect the manifest and native dump TOC, and stop only Plane. Reinstall that snapshot's official vendor inputs, override, env, wrapper and nginx route. Use its `runtime/images.json` immutable RepoDigests to obtain the previous images even if a release tag was retagged; deliberately select those matching images for the recovery run. Restore only the database `plane` with its `plane` owner/login role and matching secret; never restore the shared physical cluster or Mattermost/Nextcloud databases. Replace only `plane_uploads` content while MinIO is stopped. Reconstruct Plane-owned Valkey/RabbitMQ queues if restoring historical application state. Start the matching dependency/application images, then verify migrations (without applying the failed new release), native login, object reads, API, worker, ingress and shared-service non-regression. This is a recovery contract, not a claim of an executed destructive production rollback. No ad-hoc rollback copies are retained beside production.

## References

- [Official release](https://github.com/makeplane/plane/releases/tag/v1.4.2)
- [Community external reverse proxy](https://developers.plane.so/self-hosting/govern/reverse-proxy)
- [Upgrades](https://developers.plane.so/self-hosting/manage/upgrade-plane)
- [Backup/restore](https://developers.plane.so/self-hosting/manage/backup-restore)
- [Exact public route source](https://github.com/makeplane/plane/blob/v1.4.2/apps/proxy/Caddyfile.ce)
- [Exact model deletion semantics](https://github.com/makeplane/plane/blob/v1.4.2/apps/api/plane/db/mixins.py)
- [Backrest v1.14.1 synchronous Backup RPC](https://github.com/garethgeorge/backrest/blob/v1.14.1/internal/api/backresthandler.go)
