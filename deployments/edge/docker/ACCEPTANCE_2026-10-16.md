# Weblate monitoring, Docker logging and historical test cleanup

Status: DEPLOYED / VERIFIED. Operator explicitly requested all three changes
and conditional deletion of proven obsolete test volumes. Stage 13 remains the
accepted infrastructure checkpoint; no new stage or product is introduced.

## Runtime changes

Edge Monitor now covers 21 persistent containers, adding Weblate application
and Valkey. Local `/healthz/` is checked through port 18090. One Weblate incident
combines that HTTP result, both containers and shared PostgreSQL. Existing
two-probe confirmation, Docker-parent suppression and recovery notifications
are retained. Three new offline tests reproduce the previously missing incident,
then check dependency/HTTP failure propagation, suppression, deduplication and
recovery without sending live test messages. All 13 monitor tests pass.

Native Docker logging defaults are `json-file`, `max-size=10m`, `max-file=3`.
The existing `live-restore=false` is preserved. The 16 previously unbounded
permanent services were recreated using their existing image IDs, mounts,
environment values, commands, identities, port bindings and network membership.
No images were pulled/built/upgraded by this change. Existing bounded local/mail
drivers remain. Plane's one-shot migrator also receives explicit logging limits.
Native Compose proved the merged runtime configuration changed only in logging.
The previously stale canonical Mattermost override was reconciled to its already
deployed `edge_internal` alias; this added no runtime networking change.

Application consumers and then dependencies were stopped in order under the
existing edge-state preparation lock. Docker was restarted once; dependencies
were restored before consumers. Transient MCP clients restarted their containers;
an authenticated GitHub MCP read succeeded afterward. Every running container,
including replacement MCP instances, has bounded logging.

A disposable container using the already installed Python image inherited the
daemon defaults without explicit logging flags. It emitted 41,472,000 bytes.
Docker retained three log files and `docker logs --tail 1` returned the expected
end marker. The container had no volumes/network and was removed afterward.

## Exact historical-volume classification and deletion

Original volumes were never started. Isolated temporary copies ran PostgreSQL
18.6 with no network or published ports, read-only root filesystem and read-only
SQL transactions. Single-user diagnostics identified the nonstandard bootstrap
role before normal socket-only inspection.

| Original volume | Installation time, UTC+3 | Content |
| --- | --- | --- |
| `83d048b5893ab010bd33007f75e8540d570d9b69aefcf797c7d501a5ad1c446b` | 2026-09-30 05:06:04 | `nc_test`; roles `nc_test`/`oc_admin`; 139 Nextcloud tables; user `admin`; 76 initial file-cache entries; integration_openproject 3.2.0 enabled |
| `846b84d898b3e0a1d69c04122f1dff263ed939936ae03ffe5057f2a5792873d9` | 2026-09-30 05:00:48 | Same test graph; separate instance ID; integration_openproject 3.2.0 disabled |

Names, initial content and installation times identify the retired September 30
Nextcloud/OpenProject compatibility tests, independently of the unknown original
container names. Neither volume has container consumers or references in the
audited current configuration. Production PostgreSQL uses `/srv/postgres`, has
neither test role, and retains its four application databases. Both exact volume
names were removed with native Docker volume removal. Their combined displayed
size was approximately 148.6 MB. Earlier historical descriptions of these volumes
as empty/unknown are superseded by this direct inspection; dated records remain
unchanged.

## Build cache, recovery and cleanliness

Thirteen exact audited cache IDs were selected with a native Buildx ID filter.
The first prune removed four private records (214.3 kB). A second exact-ID prune
with `--all` removed the nine remaining shared cache records (541.8 MB accounting
size); their image-owned layers remain. Build cache is zero. All 22 original
image IDs are preserved, including the PDF Cleanup production/build-parent/base
images. No image, container, network or volume blanket prune was used.

`plane_logs_migrator` remains as required by the native migration profile. Final
volume count is seven: six attached Plane volumes and that migration log volume.
Configuration recovery copies and old-cluster clones were temporary only and
were removed after live verification. Recovery for active application data
remains the existing Backrest system; no test-data archive is retained.

Assistant verifier defects were confined to their failed points: an initial
assumption about the clone's `postgres` role, a service-name text matcher, ordered
environment-list comparison and an unnecessary Buildx boolean filter were
corrected without repeating deployment or changing production to satisfy tests.

## Verification

- Native daemon validation and all affected Compose parsing/semantic comparisons pass.
- Master Health: 9 system services, 4 user services, 11 Docker units / 21 services,
  2 SQLite integrity checks and PostgreSQL readiness pass.
- Maintenance Master contract and 13 monitor tests pass.
- Fresh monitor snapshot: 21 containers, Weblate HTTP/incident OK, Edge/overall OK.
- n8n reaches Mattermost, Nextcloud, Plane, Weblate and Hermes with HTTP 200.
- Nextcloud status/SQL read/Redis ping pass; Plane queues have active consumers
  and no ready/unacknowledged backlog; application health endpoints return 200.
- No stopped permanent service, unbounded running container, removed-volume
  reference or targeted build-cache record remains.

Sanitized machine evidence: [evidence-2026-10-16.json](evidence-2026-10-16.json).
Marker: `EDGE_DOCKER_MONITOR_LOGGING_CLEANUP=PASS`.
