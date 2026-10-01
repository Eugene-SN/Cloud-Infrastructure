# OpenProject edge decommission — 2026-10-01

Status: COMPLETE / ACCEPTED — server-side decommission and independent residue/non-regression gates PASS. External Apple Calendar subscription remains a manual client-side check.

Operator authorization: complete destructive decommission, preserve shared services and historical records, no Plane deployment. The accepted 2026-10-01 decision supersedes the stop-only sequencing in the preserved pre-decommission audit.

## Fresh delta audit and removal manifest

CONFIRMED FACT: six Compose-labelled containers under `/opt/openproject`; services web, worker, cron, cache, proxy, autoheal. One named volume `openproject_opdata`, used only by web/worker/cron. Three owned networks: frontend, backend, and the additional `openproject_default` used by autoheal. The earlier audit omitted the default network. All are OPENPROJECT_ONLY.

CONFIRMED FACT: dedicated database/role `openproject`; role dependencies are confined to that database and its global database ownership entry. Shared PostgreSQL and its two other application databases remain outside deletion scope.

OPENPROJECT_ONLY integration targets, verified live: GitHub repository webhook 689080899 (`https://projects.escloud.us/webhooks/github`, authentication query omitted); n8n workflows `OpenProjectEventIngress01`, `OpenProjectMattermost01`; credentials `OpenProjectWebhookHMAC01`, `OpenProjectAPI01`, `OpenProjectMattermostAuth01`; Mattermost bot `fc7je5jjqjfydgzjrb3nnz95gh`, private channel `5djtwy7c7jbpdkfxrgzbs9igna`, dedicated token `d8qn8xz1eibmtf4xq6hdqwdoec`; Semaphore template 19. Stalwart native JMAP subsequently confirmed dedicated Account `d`, `openproject@escloud.us`, with no aliases; that exact account was removed.

OPENPROJECT_ONLY host/current contract targets: application tree, projects nginx vhost, backup preparation sections/staging data, monitor probe/service/container list, Maintenance unit/driver/helper/playbook/template/discovery/tests, PostgreSQL provisioning variables and SQL, portal tile/icon, unused application/proxy/cache/autoheal images. Each deletion requires its live ownership/reference check.

SHARED_WITH_OTHER_SERVICES: `postgres`, `/srv/postgres`, `postgres_net`, `edge_internal`, nginx, Stalwart, Mattermost, n8n, Nextcloud, Hermes, Backrest/Restic, Edge Monitor, Maintenance/Semaphore, shared TLS lineage, canonical repository. Retain frameworks; remove only dedicated state. `projects.escloud.us` DNS/TLS namespace may remain reserved for future Plane without any backend/vhost.

HISTORICAL_REFERENCE: pre-decommission audit, rebuild contract, historical acceptance records, dated decisions, Git history and accepted Restic snapshots. Preserve them.

## Recovery evidence before irreversible mutation

Both required reference files exist in canonical Git history (including commit `d392c9476cadbe752c194605d0c1a8d98b95d587`), and current main was fast-forwarded to `997fa3da89bc0ddbbfbb3f99aafccf122dadb2d5` before work.

`HISTORICAL_DATA_RECOVERY_AVAILABLE=YES`: existing edge-state-local Restic snapshot `79ac237d` (2026-10-01 13:02:21 +03:00) contains one committed staging generation with `openproject=consolidated_postgres_pg_dump_plus_quiesced_opdata` in its manifest, a 2,424,621-byte database dump accepted by native `pg_restore -l` (2,161 TOC output lines), and attachment files of 455,768 and 442,579 bytes. This is historical recovery evidence, not a claim that later changes are included. The same snapshot contains the Mattermost dump (316,413 bytes).

Recovery path: rebuild using the adaptive contract and current supported deployment methods; when historical data is requested, restore the matched dump/opdata pair from this snapshot. No stopped stack or ad-hoc rollback copies are retained. No new pre-removal bulk backup is needed.

## Mechanism contract

Use native GitHub API, n8n lifecycle HTTP endpoints from exact installed source, Mattermost local mmctl, Stalwart JMAP, Compose down, PostgreSQL DROP DATABASE then DROP ROLE. Prefer native integration lifecycle; only the later proven orphan n8n metadata required the narrowly scoped direct cleanup documented below. n8n maintenance authorization uses a short-lived session issued with the installed native AuthService/JwtService and protected local signing state; no password/key rotation or SQL writes.

Compose external resources are preserved by upstream contract: https://docs.docker.com/reference/cli/docker/compose/down/ . PostgreSQL semantics: https://www.postgresql.org/docs/18/sql-dropdatabase.html and https://www.postgresql.org/docs/18/sql-droprole.html . Mattermost local lifecycle: https://docs.mattermost.com/administration-guide/manage/mmctl-command-line-tool . Stalwart recovery and native object deletion: https://www.stalw.art/docs/configuration/recovery-mode/ and https://www.stalw.art/docs/management/cli/delete/ . Exact installed versions/source/CLI help take precedence over mutable documentation.

Verification will include an independent extended residue sweep, shared-service gates, an actual Backrest snapshot, Maintenance Refresh/Master Health, and responsive portal rendering. External Apple Calendar state requires a separate client-side check.

## Completed execution evidence

- Native GitHub webhook deletion and empty repository webhook readback passed.
- Native n8n unpublish -> archive -> delete removed both workflows and all three dedicated credentials. Existing Hermes workflow and generic credentials remained byte-for-byte identical in their logical rows.
- Extended n8n inspection discovered orphaned `TempTestOpenProjectAPI01` state from an earlier test. Execution 10 was deleted through native `/rest/executions/delete`. The exact installed lifecycle source exposes no endpoint for orphan permission/dependency/statistics rows, completed publication-outbox rows, orphan insights metadata, or first-production onboarding links. A bounded foreign-key-enabled SQLite transaction therefore removed only these proven OpenProject rows and the specific onboarding ID field; unrelated settings/objects were preserved. Seven statistics rows, three dependency rows, one shared-workflow row, two completed publication rows and one insights metadata entry were removed. Foreign-key check passed. The subsequent all-text-column scan across all logical n8n tables returned zero matches.
- Native mmctl removed the dedicated channel, user/bot and token. A previously undiscovered administrator `prov-test` token in `/tmp/opint6_test/tok.txt` was identified by matching its secret locally to native token metadata, revoked through mmctl, and verified absent. No unrelated administrator tokens were rotated.
- Stalwart 0.16.24 native Account query proved dedicated account `d` = `openproject@escloud.us`, with no aliases. It was removed using upstream CLI 1.0.13/JMAP. Unrelated accounts `b` and `c` were identical before/after. Necessary temporary recovery-admin access used two Compose recreations on the same image ID; recovery-admin was removed and read back absent. No domain/listener or unrelated credential was altered.
- Compose down removed six containers and three owned networks. A fresh zero-consumer check preceded `openproject_opdata` removal; its mountpoint is absent. OpenProject DB/role were dropped separately; dependencies after DB drop were zero. Mattermost and Nextcloud logical DB gates passed.
- `/opt/openproject`, both projects nginx vhost entries, the canonical deployment tree, helper/playbook/template 19, and portal tile/icon were removed. Native nginx test/reload passed. Four image IDs had zero remaining consumers/references and were removed precisely: application, proxy, memcached, autoheal.
- Backup preparation retained all non-OpenProject sections and passed shell plus embedded-Python validation and runtime preflight. Real Backrest flow 345 completed SUCCESS, including preparation and D5 copy/retention hooks and indexing; snapshot `ff44d62d933d82b70207e003df2f64a0346091f17c51d122fd1ae23f81ff93b1` is present in Restic. Its staging manifest omits OpenProject.
- Final post-orphan-cleanup Backrest flow 349 and operations 350/351/352 all completed SUCCESS. Snapshot `4d2e69e062b402ccbc8027a1702ef55c9825b032a8f218396f9ebfd77c6ccb3a` is confirmed in Restic (2026-10-01 18:30:49 +03:00). Its committed staging manifest contains n8n, Authelia, PostgreSQL globals, Mattermost, mail, agent SQLite and Nextcloud, with no OpenProject stage. The staged n8n logical table scan has zero OpenProject matches. Its only three OpenProject-named paths are the preserved reference/audit/current decommission Markdown documents.
- Two additional OpenProject-only proxy build records were found in Docker Buildx history. Native removal and empty history readback passed; two exact generated local indexes were then removed after confirming `/opt/openproject/proxy` ownership. Reclaimable build data was zero.
- A stale read lock caused by the early assistant SIGPIPE verifier was positively attributed to dead PID 968181. Native `restic unlock` removed exactly that sole stale lock; production was not redesigned and no backup was blindly repeated.
- Native Maintenance local Refresh has 15 manual targets, 8 Docker units and 22 monitored components; zero unresolved/check-failed state. Contract/master tests passed after removing obsolete OpenProject assertions/counts. Master Health passed with 9 system services, 4 user services, 8 Docker units, 9 Docker services, 2 SQLite integrity checks and PostgreSQL readiness.
- Edge Monitor runtime and durable incident state contain no OpenProject; nine expected containers, EDGE_STATE=OK and OVERALL_STATE=OK. Removed obsolete standalone monitor/helper bytecode.
- Portal deployed assets were rendered in Chromium at 1440/834/390 px through local Playwright asset replay; eight tiles, no horizontal overflow, no broken images or OpenProject match. Public auth/ingress was tested separately, not bypassed in production. The badge was normalized to eight available services. Screenshots are saved as separate local visualization artifacts; new canonical portal source mirrors deployed assets.
- All twelve remaining nginx public hosts responded with valid TLS and expected public/auth/redirect behavior. Hermes gateway/dashboard are active; its existing token authenticates as `hermes` and its Mattermost channel remains accessible without sending a test message.
- Precisely removed old dedicated test/token files and stale Semaphore repository checkout after confirming zero running tasks. No blanket prune/deletion was used.

## Explicitly authorized immutable-container cleanup

The first residue audit identified three OpenProject entries in immutable shared PostgreSQL container Env despite clean `/opt/postgres/.env` and provisioning. The operator explicitly authorized one normal container recreation to remove them. Native Compose validation and dry-run passed; only service `postgres` was recreated with `--no-deps --pull never --force-recreate --wait`. Fresh readback confirmed exactly the same image `sha256:5a5a84b19854a9ffaa54082c166ff4ec27473a361e496e5ea167f298f2da9722`, identical mounts (`/srv/postgres` and read-only init directory), network and all non-OpenProject Env values. New container `00050b457ab427713fa3349bce18251b8120e05daa11c6e7208d44169eab8024` is healthy. OpenProject Env entries are absent. Mattermost user count remains 6, Nextcloud user count remains 1, and both database/role absence checks pass. The existing cluster was retained; provisioning was not rerun.

## External state

`GITHUB_OPENPROJECT_WEBHOOK=DELETED` (hook 689080899; readback has zero repository hooks).

`APPLE_CALENDAR_OPENPROJECT_SUBSCRIPTION=EXTERNAL_MANUAL_CHECK_REQUIRED` — native server-side feed/token state disappeared with the database; no evidence permits claiming removal of the Apple Calendar/iCloud client subscription.

`PROJECTS_DNS=RETAINED_FOR_FUTURE_PLANE` — fresh IPv4 resolution is 45.92.156.17; the shared TLS certificate/renewal namespace is retained, with no OpenProject vhost/backend or placeholder.

`PLANE_DEPLOYMENT=NOT_STARTED`.

## Independent extended residue audit

Read-only sweep after runtime/integration cleanup: Docker inspect/list, logical PostgreSQL databases/roles/dependencies, all logical n8n table text fields, Mattermost native bot list and dedicated-object checks, Semaphore native template list, current monitor snapshot/durable state, `/etc`, `/opt`, `/usr/local`, `/var/www`, current `/home/core/.config`, broader `/home/core` and `/root`, current canonical deployments/Maintenance/backup/monitor/portal sources, and exact known temporary/retired paths.

- ACTIVE_RESIDUE: zero. After the authorized PostgreSQL recreation, complete Docker inspect JSON for every remaining container/image/volume/network contains zero OpenProject/hostname matches. Current env file, future init contract, logical n8n state and current filesystem/configuration sweeps are clean.
- FUTURE_GENERIC_NAMESPACE: `/etc/letsencrypt/renewal/escloud.us.conf` retains `projects.escloud.us` in shared certificate renewal mapping; DNS remains reserved. No active nginx/backend handling exists.
- HISTORICAL_REFERENCE: preserved recovery/acceptance documents, dated decisions/state sections, Git history, agent conversation/log/session records and shell history. These are evidence, not current service configuration.
- NOT_OPENPROJECT: upstream MATLAB lexer builtin `openProject`, Hermes Desktop `openProject` function identifiers and bundled T3 UI code. These lexical matches do not reference this product/deployment.
- Newly identified production/test residues (orphan n8n metadata, dedicated test administrator token, monitor bytecode, obsolete Semaphore checkout and Buildx records) were removed and read back absent.
- Two existing anonymous Docker volumes are empty and have no consumers or OpenProject labels/content. Their ownership is UNKNOWN; they are not deleted on speculation or counted as OpenProject volumes.

### Verified enumerated gates

Fresh post-mutation observations, with backup quiesce completed and shared network members restored:

```text
OPENPROJECT_CONTAINERS=0
OPENPROJECT_VOLUMES=0
OPENPROJECT_OWNED_NETWORKS=0
OPENPROJECT_IMAGES=0
OPENPROJECT_DATABASE=ABSENT
OPENPROJECT_DATABASE_ROLE=ABSENT
OPENPROJECT_WORKDIR=ABSENT
OPENPROJECT_NGINX_ACTIVE_CONFIG=0
OPENPROJECT_BACKUP_ACTIVE_REFERENCES=0
OPENPROJECT_MONITOR_ACTIVE_REFERENCES=0
OPENPROJECT_MAINTENANCE_ACTIVE_REFERENCES=0
OPENPROJECT_SEMAPHORE_ACTIVE_REFERENCES=0
OPENPROJECT_N8N_ACTIVE_OBJECTS=0
OPENPROJECT_MATTERMOST_ACTIVE_OBJECTS=0
OPENPROJECT_STALWART_ACTIVE_OBJECTS=0
OPENPROJECT_PORTAL_ACTIVE_REFERENCES=0
SHARED_POSTGRES=PASS
MATTERMOST_DB_GATE=PASS
NEXTCLOUD_DB_GATE=PASS
POSTGRES_NET=PASS
EDGE_INTERNAL=PASS
NEXTCLOUD=PASS
MATTERMOST=PASS
N8N=PASS
STALWART=PASS
HERMES=PASS
NGINX=PASS
BACKREST=PASS
EDGE_MONITOR=PASS
MAINTENANCE=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
PLANE_DEPLOYMENT=NOT_STARTED
OPENPROJECT_CURRENT_STATE_RESIDUE=PASS
OPENPROJECT_EDGE_DECOMMISSION=PASS
```

Canonical changes are prepared in the working tree: architecture/current state/inventory, deployment README and PostgreSQL provisioning, Maintenance manifests/scripts/tests, new exact current backup/monitor/portal sources, removal of current OpenProject deployment/helper/playbook. Required recovery documents remain byte-for-byte unchanged. Final ACCEPTED decision is appended after all server-side gates passed. The coherent change is persisted directly to main, followed by remote commit/critical-file readback.

## Final post-recreation evidence — 2026-10-01

- Real Backrest flow 353 and operations 354/355/356 all SUCCESS; snapshot `723f16c99fc22e223de500dacf8d3bdabc53e0e254a651f96cc153229df7aeb0` is present (2026-10-01 18:47:35 +03:00). Snapshot manifest has no OpenProject stage. Mattermost dump 317,490 bytes and Nextcloud dump 1,293,410 bytes both pass native `pg_restore -l` after complete capture (no streaming SIGPIPE).
- After quiesce hooks finished, exact network membership is restored: `postgres_net` = postgres/Mattermost/Nextcloud app/cron; `edge_internal` = n8n/Mattermost. All production services remain healthy; native Nextcloud status is installed, maintenance=false, needsDbUpgrade=false.
- Remaining twelve public sites pass expected HTTP status with TLS verify=0. Native n8n health uses the inspected host binding `127.0.0.1:15678`, HTTP 200. Stalwart native SMTP client with valid FQDN EHLO passes; removed mailbox RCPT returns 550. Hermes token still authenticates as hermes.
- Read-only Refresh passes with 22 components, 15 actionable targets, 8 Docker targets, 4 real available updates and zero unresolved/check-failed state. Contract and Master contract tests PASS; Master Health PASS with 9 system services, 4 user services, 8 Docker units, 9 services, 2 SQLite checks and PostgreSQL readiness.
- Assistant verifier defects were corrected without production changes: a guessed n8n host port, a guessed contract-cache filename, and an SMTP response loop that waited only for 250 after invalid EHLO. Proven earlier results were preserved; only failed checks were resumed against inspected paths/native SMTP behavior.
- Required recovery documents remain byte-for-byte identical to their committed versions. Temporary test/authentication files and browser session artifacts were removed. No Plane runtime/configuration or premature portal tile was created.

## Canonical persistence and Semaphore readback

Implementation/acceptance commit `bbcc00411d529502107445d67fc0002a28cd38d7` was pushed directly to main. GitHub commit readback matched the local commit, and contents API readback matched critical architecture/current state/inventory/decisions, both unchanged recovery documents, PostgreSQL provisioning, Maintenance unit contract, backup/monitor source and portal source.

Native Semaphore Refresh task **57** completed **success** after pulling that commit into its normal repository checkout. Checkout readback confirmed the accepted commit and absence of the deleted deployment/helper. Actual task output includes `READ_ONLY_REFRESH=PASS`, `ACTIONABLE_TARGET_COUNT=15`, `DOCKER_TARGET_COUNT=8`, `CHECK_FAILED_COUNT=0`. Current Edge Monitor remains EDGE_STATE=OK / OVERALL_STATE=OK. Final task/schema/baseline temporary files are removed.
