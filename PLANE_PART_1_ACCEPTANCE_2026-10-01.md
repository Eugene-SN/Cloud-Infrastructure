# Plane Community Part 1 production acceptance — 2026-10-01

Status: COMPLETE / ACCEPTED. Operator-authorized core deployment on production edge following the accepted OpenProject decommission. Final marker: `PLANE_PART1_CORE_DEPLOYMENT=PASS`. Part 2 integrations are separately deferred; this is not their acceptance.

## Authorization and evidence basis

The operator's supplied Part 1 requirements accepted exact service composition, external PostgreSQL/nginx, private n8n readiness and the operational integrations, and explicitly requested autonomous deployment through production acceptance. Administrator email/password were separately supplied by the operator. Repository baseline was fetched/read on main at `79529150e1169ad04664755d1483973bbe4cd2f2`; origin/main was fetched again before persistence and matched. No branch/PR, replacement product selection, optional integration, major-version policy, autonomous Plane updater or extra auth layer was introduced.

CONFIRMED FACTS below come from live native Compose/Docker/PostgreSQL/API/browser/Backrest/Semaphore/monitor evidence and the exact release source. No claims about actual Part 2 integrations are inferred from network connectivity.

Authoritative sources and mechanisms: official [v1.4.2 release](https://github.com/makeplane/plane/releases/tag/v1.4.2), [external reverse proxy guidance](https://developers.plane.so/self-hosting/govern/reverse-proxy), [upgrade guidance](https://developers.plane.so/self-hosting/manage/upgrade-plane), [backup/restore](https://developers.plane.so/self-hosting/manage/backup-restore), exact tagged source for routes/CSRF/cookies/assets/webhook allowlists/deletion/task scheduler, native installed Compose 5.5.1, PostgreSQL 18.6, RabbitMQ 3.13.6 and Backrest 1.14.1. The deployment/recovery contract and complete file layout are in `deployments/plane/README.md`.

## Release, service graph and durable ownership

Official latest stable at acceptance: **v1.4.2**, release ID **375236829**, non-prerelease/non-draft, published **2026-08-23T14:39:21Z**. Release setup/Compose/variables were obtained from official assets and matched their recorded SHA-256; vendor files remain unmodified. Sanitized identity/hashes are in `deployments/plane/vendor-reference.json`. Current backend installed/remote digest is `sha256:90032ce088708889b60c00d491897916f4deb882facda27db59fd10fb68729ef`.

Default persistent services: **web, api, admin, space, live, worker, beat-worker, plane-redis, plane-mq, plane-minio** (ten). Backend api/worker/beat-worker/migrator use makeplane/plane-backend:v1.4.2; frontends/live use their matching official v1.4.2 images. Official dependencies: valkey/valkey:7.2.11-alpine, rabbitmq:3.13.6-management-alpine, pgsty/minio:RELEASE.2026-08-04T00-00-00Z, as selected by release assets.

Official migrator ran successfully, RC0, with a temporary one-shot container removed afterward. Default startup excludes migrator; profile `migration` enables it intentionally. Embedded **plane-db** and bundled **proxy** are disabled; no corresponding container/Plane pgdata/proxy certificate volume exists. Vendor dependency resets remove plane-db from all four DB consumers. Each persistent service has restart unless-stopped and one replica.

Seven stable named volumes: **plane_uploads, plane_redisdata, plane_rabbitmq_data, plane_logs_api, plane_logs_worker, plane_logs_beat-worker, plane_logs_migrator**. Rabbit node is `rabbit@plane-mq`, fixed hostname plane-mq; its old initial random-name directory was removed after verified zero task state. MinIO writes `/export` on plane_uploads. Its image's unused `/data` VOLUME is covered by tmpfs; an initial inherited empty anonymous volume was precisely removed after reference checks. Fresh MinIO creation has only the named uploads volume and tmpfs. No Plane-owned anonymous durable volume remains. Two pre-existing unreferenced PostgreSQL image volumes are outside proven Plane ownership; no speculative deletion was performed.

Valkey cache/pubsub and RabbitMQ Celery queue state persist through normal restart/recreate, using vendor volumes. Upstream historical backup guidance establishes database/objects/configuration as the recovery set; task schedules use Django DatabaseScheduler in PostgreSQL. Historical recovery reconstructs cache/queues rather than promising old in-flight task delivery. Log volumes support current native lifecycle, including the repeatable migrator; they are not ad-hoc rollback copies.

## Ingress and networks

All six host publications bind **127.0.0.1**; no direct Plane public 80/443 or helper exposure:

| Loopback port | Service → container port | nginx paths |
|---:|---|---|
| 18110 | web → 3000 | `/` |
| 18111 | api → 8000 | `/api/`, `/auth/`, `/static/` |
| 18112 | admin → 3000 | `/god-mode/` |
| 18113 | space → 3000 | `/spaces/` |
| 18114 | live → 3000 | `/live/` and WebSocket |
| 18115 | plane-minio → 9000 | `/uploads/` |

Existing Xray → nginx 127.0.0.1:8080 proxy_protocol and shared escloud.us certificate lineage serve `https://projects.escloud.us`. HTTP redirect and ACME route are preserved. No Authelia gate; native Plane authentication is used. Paths and HTTPS host/proto/port, real client address and WebSocket Upgrade are forwarded. Body limit 5m matches FILE_SIZE_LIMIT=5242880. Nginx configuration validation/reload passed. Native S3 presigned upload and application download both passed through public HTTPS, proving the signature-sensitive object route.

All ten services join plane_default. `postgres_net` retains **postgres, mattermost-mattermost-1, nextcloud-app-1, nextcloud-cron-1** and adds **plane-api-1, plane-worker-1, plane-beat-worker-1**. Migrator additionally joins only while running. No frontend/live/cache/queue/object service joins the database network.

`edge_internal` retains **n8n, mattermost-mattermost-1**, and adds only **plane-api-1** (plane-api) and **plane-worker-1** (plane-worker). Gateway/subnet/bridge remain 172.30.0.1/172.30.0.0/24/edge-internal. Native worker resolves n8n and GET http://n8n:5678/healthz returns 200. n8n resolves plane-api and reaches its native API with expected unauthenticated 401. WEBHOOK_ALLOWED_HOSTS is exactly n8n, WEBHOOK_ALLOWED_IPS empty, through official backend env propagation. No webhook, token, workflow or notification object was created for this test.

## Database and application acceptance

Shared PostgreSQL **18.6**: database plane, owner/login plane; role non-superuser, no CREATEDB/CREATEROLE. Public schema owner pg_database_owner, all 110 public tables owned by plane. 164 applied migration rows; native `manage.py migrate --check` RC0, no pending migration. Plane has no CREATE privilege on postgres/Mattermost/Nextcloud DBs and no dedicated grants outside its own database.

Existing postgres container ID `00050b457ab427713fa3349bce18251b8120e05daa11c6e7208d44169eab8024` and image `sha256:5a5a84b19854a9ffaa54082c166ff4ec27473a361e496e5ea167f298f2da9722` are unchanged. No Plane application secret was added to its immutable Env; no shared PostgreSQL restart/recreation was performed.

Native setup/admin API and app login passed. First administrator **es@escloud.us** uses the operator-supplied password. Public browser email/password form independently authenticated and reached the create-workspace page. God Mode and spaces frontend rendered; API/static assets were served. Protected native sessions were temporary and removed by exact user/User-Agent scope after tests.

Bounded workspace UUID `3c3eb2ad-b5dd-437c-a550-0be16d3b117e` / slug plane-acceptance-3dff18ea:

- work item created/read/updated, parent/sub-work-item relationship confirmed;
- comment and label created/applied; cycle, module and Page created/read;
- native presigned PNG uploaded via public MinIO route and downloaded via application asset route; payload SHA-256 `4b31064703e76fd1daddd0135d6432e6784f593fb1ae3e69426d2c40e4db086d` matched;
- native Celery worker ping/pong passed; at least twelve real issue activity rows established background processing; Beat uses DatabaseScheduler and loaded its schedule;
- all ten persistent Plane containers were force-recreated with the same release and existing named volumes; DB entities/Page/cycle/module/subtask and exact uploaded bytes persisted; shared postgres identity remained unchanged;
- public wss://projects.escloud.us/live/collaboration/ returned an open WebSocket; live health and actual frontend rendered project/issues succeeded; over 500 JS/CSS loads had no 5xx;
- bounded child/main work items were natively DELETEd, then read returned 404; workspace native DELETE passed. Upstream soft deletion retains rows, so exact retired workspace was physically deleted through the supported ORM hard-delete method after identity checks. 122 related records were removed; a scoped all-model audit confirmed zero records referencing that workspace;
- exactly one test object was deleted with the same S3v4 API/credentials contract used upstream, after confirming its key/prefix; no test object remains. The workspace-specific seed bot was subsequently identified by the exact upstream username/email convention and deleted only after every User foreign-key reference was audited empty;
- operator-created **personal** workspace appeared independently from an external Safari session during final verification. It and its distinct upstream seed bot are retained. Cleanup was bounded by the acceptance UUID and test User-Agent, not by global entity counts.

Browser screenshots were captured outside production temp state. Recoverable upstream React hydration errors **#418/#423** were observed during initial rendered frontend testing; usable rendered project UI, native CRUD and static/API responses passed. No product source patch was made and no stronger claim of a completely warning-free browser console is made.

## Backrest, updates, monitoring and portal

Existing edge-state plan now stages a quiesced logical plane dump, matched uploads, protected runtime including secrets/Compose/wrapper/nginx and immutable image identities. Shared physical PostgreSQL is not the rollback unit. Plane staging stops only api/worker/beat-worker/live/MinIO and has EXIT recovery for a partial stop. Existing Mattermost/mail staging retains its own established independent quiesce; Nextcloud/PostgreSQL stay running for the Plane stage.

Real first Backrest flow **361**, operations **361/362/363/364**, all SUCCESS, snapshot **3008b124f6a3a30a99282383d76a8d4654833935abf5ff843ccf14ef635f1ffd**. Actual Restic contents include valid 679,827-byte logical dump, expected PNG object storage and protected env. Dump was downloaded from snapshot to temporary disk and parsed with native pg_restore -l; no truncated pipe verification. Both existing staging and D5 tier-copy succeeded.

After cleanup, flow **365** captured snapshot **7034edb6feb7ee6974f85ccb677cb693f3deed43b7613f77a948b9f3551f897d**. The normalized runtime with immutable image identities was captured by flow **369**, operations **369/370/371/372** all SUCCESS, snapshot **db6431a46e6b1329e9ce49e1abc014918d94e3fe5077347c46a36eb1eac48dcf**. Actual snapshot contains 675,324-byte dump, 1,700-byte env and 2,911-byte images.json, mode0600; native pg_restore -l passed. Test workspace/upload are absent from that generation; the proven unreferenced test seed bot was removed afterward. A final post-cleanup checkpoint is recorded below. Historical snapshots remain in the accepted backup lifecycle.

Plane updater preflight passed against actual snapshot contents and current vendor/route/variable contract. Installed/latest v1.4.2 CURRENT; no newer stable release, so no manufactured downgrade/re-upgrade. Manual release updater preserves site override, rejects native merged/unmerged topology/route/env drift, requires completed pre-update Backrest flow, runs migrator fail-closed, checks health and retires only old unused Plane images. Offline native Compose checks rejected eight relevant topology drift cases without production failure injection.

Maintenance read-only Refresh: **23 monitored components, 16 manual targets, 9 Docker targets, 4 real available updates elsewhere, zero unresolved/check-failed**. Both existing contract suites PASS. Master Health PASS: 9 system services, 4 user services, 9 Docker units/19 services, 2 SQLite checks, shared PostgreSQL readiness. Native Semaphore **Update Plane template 21**, project1, expected Git playbook read back; no scheduled Plane update. Post-push native Refresh evidence is recorded below.

Monitor: 19 expected persistent containers; public Plane/API/local live probes. Migrator excluded. One Plane service incident aggregates the ten-container/three-probe graph, with Docker parent suppression. Read-only synthetic snapshot checks confirmed worker failure correlation without helper fan-out; no production synthetic failures were injected. Edge/overall OK after backup/bootstrap recovery. Upstream app bootstrap after stop/start can take roughly two minutes on this host, causing real transient availability incidents during quiesced backups; no unrequested incident-suppression policy was introduced.

Portal: ninth tile **Plane → https://projects.escloud.us**, native official icon, existing design/CSS, status sourced from the three actual probes. Responsive replay of exact deployed static assets plus real monitor snapshot passed at widths **1440/834/390**, nine tiles, no horizontal overflow/broken images/JS errors. This layout replay does not bypass the real portal Authelia gate; public gated ingress was independently checked.

## Non-regression and cleanliness

All nine pre-existing containers remain running/native healthy where a native check exists. Mattermost ping, n8n health, Nextcloud status and Authelia health return200. Mattermost active user count6 and Nextcloud user count1 remain unchanged. Native Nextcloud status: installed=true, maintenance=false, needsDbUpgrade=false. Master Health verifies Hermes gateway/dashboard, Antigravity daemon, WebDAV and all shared system units. Twelve public endpoints passed expected HTTPS/authentication behavior; go.escloud.us returns its expected401. nginx -t passed.

Canonical/live byte matching verified deployment override/wrapper/nginx, backup hook, monitor config/agent, portal files and changed Maintenance inputs/helper. Vendor setup/Compose/template hashes match release references. Temporary source/download/browser/verifier/dump/auth state is removed at completion. Six obsolete unreferenced Maintenance bytecode files were removed. No .bak/.old/retired trees/stale Plane container/image/network or OpenProject active deployment/integration reference was retained. Required historical OpenProject recovery/audit documents are unchanged.

Assistant block/verifier defects were handled at their failed points without production redesign: omitted User-Agent on initial account setup caused an atomic rollback; rotated CSRF/API status/field expectations were corrected; local deployment path assumption failed closed before copying a nonexistent playbook path (Semaphore correctly uses Git); 30-second Backup RPC timeout was replaced after exact Backrest source showed synchronous completion; initial portal replay captured genuine backup warm-up and was checked after healthy recovery; generic S3Storage.exists was invalid for Plane's custom adapter and was replaced with the upstream S3v4 contract before deletion; native login submit label was read from rendered UI; an SQL member-column assumption was abandoned for native model reference audit. Compose retained old anonymous volume metadata on first recreation despite tmpfs, so a fresh MinIO container was created and only the verified empty released volume was removed. Already-passed application/persistence checks were preserved.

## Explicit Part 2 deferrals

No SMTP configuration, n8n workflow/API credential/webhook, GitHub integration, dedicated Mattermost bot/channel/token, Hermes credential, Nextcloud connector, Knowledge workflow, MCP service, calendar/intake email or AI/OpenSearch subsystem was created.

Future independently accepted work: Stalwart outbound SMTP; Plane Webhooks v2→n8n; n8n→Plane API v2; Plane→n8n→Mattermost; actual Community-native GitHub capability where applicable or n8n/API; Hermes REST API and/or MCP stdio; Knowledge/Obsidian automation; useful Nextcloud/calendar workflows; optional intake email only after an architecture review. The accepted edge_internal/hostname allowlist foundation supports this future work.

## Verified final gates

```text
PLANE_CURRENT_STABLE=PASS
PLANE_VENDOR_CONFIG_CLEAN=PASS
PLANE_SITE_OVERRIDE=PASS
PLANE_EMBEDDED_POSTGRES=ABSENT
PLANE_LOCAL_PGDATA=ABSENT
PLANE_SHARED_POSTGRES_DB=PASS
PLANE_SHARED_POSTGRES_ROLE=PASS
PLANE_POSTGRES18_MIGRATION=PASS
PLANE_PENDING_MIGRATIONS=0
PLANE_BUNDLED_PROXY=ABSENT
PLANE_PUBLIC_CONTAINER_PORT_80=ABSENT
PLANE_PUBLIC_CONTAINER_PORT_443=ABSENT
PLANE_LOOPBACK_ROUTES=PASS
PLANE_WEB=PASS
PLANE_API=PASS
PLANE_ADMIN=PASS
PLANE_SPACE=PASS
PLANE_LIVE_WEBSOCKET=PASS
PLANE_UPLOAD_STORAGE=PASS
PLANE_BACKGROUND_WORKER=PASS
PLANE_BEAT_WORKER=PASS
PLANE_RESTART_PERSISTENCE=PASS
PLANE_POSTGRES_NET_MEMBERSHIP=PASS
PLANE_EDGE_INTERNAL_API_FOUNDATION=PASS
PLANE_EDGE_INTERNAL_WORKER_FOUNDATION=PASS
PLANE_WEBHOOK_ALLOWED_HOSTS=PASS
PLANE_WEBHOOK_ALLOWED_IPS_EMPTY=PASS
PLANE_BACKREST=PASS
PLANE_EDGE_MONITOR=PASS
PLANE_MAINTENANCE=PASS
PLANE_SEMAPHORE=PASS
PLANE_PORTAL=PASS
SHARED_POSTGRES=PASS
MATTERMOST_DB=PASS
NEXTCLOUD_DB=PASS
POSTGRES_NET=PASS
EDGE_INTERNAL=PASS
NEXTCLOUD=PASS
MATTERMOST=PASS
N8N=PASS
STALWART=PASS
HERMES=PASS
NGINX=PASS
BACKREST=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
OPENPROJECT_ACTIVE_RESIDUE=0
PLANE_SMTP_CONFIGURED=NO
PLANE_GITHUB_INTEGRATION_CREATED=NO
PLANE_N8N_WORKFLOWS_CREATED=0
PLANE_MATTERMOST_OBJECTS_CREATED=0
PLANE_HERMES_CREDENTIAL_CREATED=NO
PLANE_NEXTCLOUD_INTEGRATION_CREATED=NO
PLANE_MCP_SERVICE_CREATED=NO
PLANE_PART1_CORE_DEPLOYMENT=PASS
```


## Final normalized checkpoint

Final post-cleanup Backrest flow **373**, operations **373/374/375/376**, all SUCCESS. Recovery snapshot **9c54b3479f4995f84eab29cfd0853bcc75ed702118a21b54031e3bf143b7aab6** includes the protected runtime/image identity contract after MinIO normalization and removal of the exact retired test-workspace seed bot. Current DB audit confirms zero test workspace, test seed bot and acceptance User-Agent sessions; operator personal workspace/Safari session are retained. API token, webhook and workspace integration counts are zero at final audit. Runtime has ten Plane persistent containers, seven named Plane volumes, no Plane-owned anonymous volume, and no migrator/embedded database/proxy container. Final all-running assertion is performed after the authorized backup quiesce/startup recovery; a read taken during quiesce is not classified as a production defect.


Final snapshot readback: 675,183-byte Plane dump, 1,700-byte protected env and 2,911-byte immutable image record all present with mode0600; actual snapshot dump passed native pg_restore -l and no test PNG path remains. Final layout and scheduled obsolete-artifact absence gates PASS. Current critical runtime source hashes: edge-monitor `588dbf073a9ab696ef67625283b46a3607111b81285669e74ba40802b64b5e48`, backup preparation `870fbc268edb4a36e16b8355f18d676399766d81b1e285a735fdb6e83ccaaf91`, Plane update helper `261aaeb8899fb628a2fed578d06dfb6f937a1c1eb65f214ba5d47553deca3089`. Canonical sources match deployed bytes. Vendor metadata matches all three official release assets. Secret scan passed; historical OpenProject records are unchanged.


## Canonical persistence and native Semaphore Refresh

Implementation/acceptance commit **be732b404d9ce2e95e700ff4e0a4a5b14cf674d0** was pushed directly to main. Remote Git ref/commit readback matched, and all **33** changed critical files were read from fetched origin/main and byte-matched. Exact staged secret scan passed before commit.

Native Semaphore Refresh task **58**, template1, completed **success** after fetching that commit into its normal project1/template1 Git checkout. Output contains `READ_ONLY_REFRESH=PASS` and Ansible recap `ok=2 changed=0 unreachable=0 failed=0`. Checkout owner is semaphore; hash/file readback is performed under that identity (the initial root Git ownership-guard rejection was a readback-client defect, not a task/runtime failure). Native template21 readback and absence of a schedule passed. Post-task cache confirms 16 actionable/9 Docker targets/23 monitored components and zero check-failed. Final Edge/overall state remains OK. The canonical wrapper executable bit is normalized to match its already-correct production mode; five obsolete ignored repository bytecode files were removed in addition to six production bytecode files.


Completion cleanup readback: the exact protected temporary deployment directory, operator/session files, downloaded source/assets, temporary browser venv, restored dumps and all verifier files are absent. Native uv cache cleanup removed only the three task-created browser dependency packages (playwright/greenlet/pyee), after their exact single cache versions and creation times were verified. Existing shared Chromium/tool runtime is retained. Final monitor readback is EDGE_STATE=OK / OVERALL_STATE=OK; Maintenance readback confirms PLANE=CURRENT, 16 targets and zero check-failed. Accepted screenshots remain intentional evidence artifacts outside production temporary state. The final follow-up commit records readback/cleanup and normalizes the source wrapper executable bit; it does not change the tested production implementation.
