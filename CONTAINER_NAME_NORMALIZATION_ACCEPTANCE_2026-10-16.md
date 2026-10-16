# Edge container naming normalization — 2026-10-16

Status: COMPLETE / VERIFIED. `EDGE_CONTAINER_NAMES_NORMALIZED=PASS`.

The operator approved the complete naming table and authorized deployment,
integration changes, data preservation, verification and stale-reference
cleanup. Contract: [all 22 names and both on-demand workloads](deployments/edge/docker/container-names.md).

## Deployment and retained state

- 16 permanent containers recreated through native Compose using the exact
  existing image IDs; six already normalized containers retain their IDs.
- Canonical and live Compose inputs match. Native effective configurations
  differ from baseline only in `container_name`. All four Compose projects
  converge: a subsequent native dry run schedules no replacement or pull.
- Mounted data, environment values, commands, ports, logging, restart policy,
  project/service keys and network membership match baseline. Existing service
  aliases remain, obsolete generated container aliases are absent. RabbitMQ
  keeps hostname `plane-mq` and `plane_rabbitmq_data`.
- Primary-key counts/hashes match in 11 tables across Mattermost, Nextcloud,
  Plane and Weblate. Shared PostgreSQL was not recreated. No database migration
  or application/image update was executed by this task.
- PDF CleanUp retains `pdf-cleanup-<execution_id>` and `--rm`; its published
  workflow remains available. A concurrent standalone regression container was
  observed, identified by its inspected image, mounted regression script and
  automatic removal setting, and preserved. Plane migrator now receives a
  unique `plane-migrator-<run-id>` in the existing update driver.

## Integration verification

- Master health: 9 system services, 4 user services, 12 Docker update units,
  22 persistent Compose services, 2 SQLite checks and PostgreSQL readiness PASS.
- Edge Monitor: 22 container probes and 13 HTTP probes PASS; overall state OK.
- n8n DNS/HTTP paths to Mattermost, Plane, Nextcloud, Weblate and shared GitHub
  MCP PASS (the unauthenticated MCP endpoint returns its expected 401).
- Plane native migration check, Celery ping and API/MinIO/public routes PASS;
  application TCP paths to PostgreSQL, Valkey, RabbitMQ and MinIO PASS.
- Native Redis/Valkey pings and RabbitMQ running-node diagnostics PASS.
  Nextcloud reports installed, maintenance false and no required DB upgrade.
- 21 monitor tests PASS, including failure/deduplication/recovery for renamed
  Plane scheduler and Weblate dependencies. Native Plane topology tests reject
  nine drift cases. All 19 manual update routes pass isolated dispatch tests;
  six affected update-unit preflights pass against live configuration.
- Seven published n8n workflows contain no old container references. Bounded
  current-file scans cover 14 runtime/configuration roots and find no old names.

## Backup verification and corrections

The prior actual Backrest recovery snapshot is
`35d566187fea085851fb0d9f026e148b19dede63fe22e9fc4480535276165506`.
Its four logical database dumps and deployed Compose files were verified through
the native snapshot-file API before deployment cleanup.

The first live post-change backup exposed the existing 120-second Weblate
startup deadline: operation 800 / hook 801 failed while waiting for health;
services recovered and no new snapshot was committed. The script now waits for
native Compose health for up to 300 seconds. Weblate's official Dockerfile uses
a five-minute health start period. The repeated preparation, hook 803, passes
all ten stage gates, including Weblate and staging commit.

Fresh version discovery also exposed an incomplete Weblate Docker Hub alias
path when the remote digest differs. Weblate now uses the existing registry
helper and official OCI version label. The live result correctly reports an
available image digest update for the same application version 2026.10.1;
no image update is executed. Discovery finishes with zero unresolved rows.

The successful repeated backup is operation 802, snapshot
`ced0024094be380689564ec9e5b05d8c9dec21680ca001fda838ebaaae8b8465`.
Native snapshot-file checks verify 14 expected files in 12 directories,
including all four logical database dumps, nine updated runtime files and the
coordinated staging manifest. The request and preparation finish successfully;
subsequent health checks remain OK.

## Cleanup and provenance

21 superseded setup/configuration copies under `/opt/weblate/backup/last`
were removed after verifying all 21 filenames/sizes in the actual prior
Backrest snapshot. This includes retired script copies and the old STDIO
GitHub MCP launcher copy. Weblate operational instructions now point to the
coordinated Backrest recovery bundle and canonical Compose.

Evidence: [runtime/data/backup verification](deployments/edge/docker/container-names-evidence-2026-10-16.json).
The independent PDF standalone-image change landed as `51ebf68` during this task;
its accepted runtime and committed documentation are preserved.

Dated acceptance records, Git history and required Backrest recovery state
retain their historical naming. Unrelated translation/knowledge/PDF worktree
changes are preserved and excluded from this task's commit. The task temporary
directory and protected rollback copies were removed after final evidence
extraction; no unfinished task processes or temporary containers remain.

Sources: [Compose naming](https://docs.docker.com/reference/compose-file/services/#container_name),
[Compose recreation/data preservation](https://docs.docker.com/reference/cli/docker/compose/up/),
[native health waiting](https://docs.docker.com/reference/cli/docker/compose/start/),
[Weblate labels and health start period](https://github.com/WeblateOrg/docker/blob/main/Dockerfile).
