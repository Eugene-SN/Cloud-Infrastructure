# Docker logging and bounded cleanup

The logging limit is three files of 10 MB per container. Docker's native
rotation owns the files; no external logrotate/truncation job is used.
`daemon.json` supplies defaults to future containers, including GitHub MCP and
one-shot PDF Cleanup. Existing `live-restore=false` remains unchanged.

Persistent Compose services explicitly declare the same limits. Existing
`local` drivers for Authelia/Weblate and bounded `json-file` mail services remain
in place. PostgreSQL, n8n, Nextcloud, Mattermost and Plane use bounded `json-file`.
Plane's normally absent migrator also has explicit limits in its site override.
Native upstream Compose files and application image versions are preserved.

Docker defaults require a daemon restart and do not retroactively change old
containers. Apply the matching canonical Compose files and recreate the affected
services with the already installed images; pulling/building/upgrading is not
part of logging maintenance. Stop application consumers before databases and
queues, then restore dependencies before consumers. Coordinate with the existing
edge-state preparation lock. Transient stdio MCP containers end during a Docker
restart and receive the defaults when their clients start replacements.

Recovery: restore the previous canonical configuration from Git, validate with
native Compose and `dockerd --validate`, then recreate the same service graph
against its existing mounts. Application data recovery remains the accepted
Backrest flow; logging changes do not migrate data. Keep protected temporary
copies of exact deployed configurations until live verification finishes, then
remove them.

Weblate monitoring covers its HTTP health endpoint, both runtime containers and
shared PostgreSQL in one incident, with existing Docker-parent suppression and
normal failure/recovery notification handling.

Cleanup is based on exact audited volume/cache identities. Never infer that an
image with no current container is obsolete: the PDF Cleanup production image,
its build parent and Python base remain required. Retain `plane_logs_migrator`
for its declared migration lifecycle. Historical test data is examined only on
isolated temporary copies, never by starting the original volume.

Sources: [Docker logging](https://docs.docker.com/engine/logging/drivers/json-file/),
[exact build-cache filters](https://docs.docker.com/reference/cli/docker/buildx/prune/),
[PostgreSQL single-user diagnostics](https://www.postgresql.org/docs/18/app-postgres.html).
