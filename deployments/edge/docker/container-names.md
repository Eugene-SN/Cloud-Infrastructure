# Edge container naming contract — 2026-10-16

The operator approved this table before implementation. Explicit
`container_name` values belong in owned Compose files/site overrides. Vendor
Compose files, project names and service keys remain unchanged. Each permanent
service has one instance; native Compose scaling beyond one instance requires
a separately chosen naming design.

| Previous name | Permanent name | Compose project / service |
|---|---|---|
| `authelia` | `authelia` (unchanged) | authelia / authelia |
| `postgres` | `postgres` (unchanged) | postgres / postgres |
| `n8n` | `n8n` (unchanged) | n8n / n8n |
| `stalwart` | `stalwart` (unchanged) | mail-stack / stalwart |
| `bulwark` | `bulwark` (unchanged) | mail-stack / bulwark |
| `github-mcp` | `github-mcp` (unchanged) | github-mcp / github-mcp |
| `mattermost-mattermost-1` | `mattermost` | mattermost / mattermost |
| `nextcloud-app-1` | `nextcloud` | nextcloud / app |
| `nextcloud-cron-1` | `nextcloud-cron` | nextcloud / cron |
| `nextcloud-redis-1` | `nextcloud-redis` | nextcloud / redis |
| `plane-web-1` | `plane-web` | plane / web |
| `plane-api-1` | `plane-api` | plane / api |
| `plane-admin-1` | `plane-admin` | plane / admin |
| `plane-space-1` | `plane-space` | plane / space |
| `plane-live-1` | `plane-live` | plane / live |
| `plane-worker-1` | `plane-worker` | plane / worker |
| `plane-beat-worker-1` | `plane-scheduler` | plane / beat-worker |
| `plane-plane-redis-1` | `plane-valkey` | plane / plane-redis |
| `plane-plane-mq-1` | `plane-rabbitmq` | plane / plane-mq |
| `plane-plane-minio-1` | `plane-minio` | plane / plane-minio |
| `weblate-edge-weblate-1` | `weblate` | weblate-edge / weblate |
| `weblate-edge-cache-1` | `weblate-valkey` | weblate-edge / cache |

| On-demand workload | Naming and lifecycle |
|---|---|
| PDF Cleanup | Persistent `pdf-cleanup`; `docker start --attach` on demand, normally `exited`; fixed mounts and retained dependencies. See `../pdf-cleanup/README.md`. |
| Plane migrator | `plane-migrator-<run-id>`, native Compose `run --rm --no-deps` in migration profile |

Service DNS aliases, network/volume names, bind paths and RabbitMQ hostname
`plane-mq` retain their existing roles. In particular, `plane-redis`,
`plane-mq`, `beat-worker`, `cache`, `app` and `cron` remain valid service keys;
they are not stale container references.

Apply with native Compose against the deployed inputs, using the existing
local images (`up -d --pull never --no-build --wait`). Compose recreates changed
containers while preserving mounted data. Coordinate with the existing backup
preparation lock and briefly pause Edge Monitor while its inventory changes.
Never use `down -v`, a daemon restart, an image upgrade or a blanket prune for
this operation.

Backup preparation uses the normalized container names. Weblate restart keeps
native Compose health waiting, with a 300-second deadline: a live backup test
exceeded the earlier 120-second deadline before the service became healthy.

Recovery: restore matching previous Compose/monitor/maintenance/backup files
from Git and rerun native Compose with the same image generation and mounted
data. Logical database/file restoration, if actually needed, follows Backrest's
coordinated application recovery bundle. Temporary protected copies are removed
after verification; historical acceptance records remain historical.

Sources: [Compose container names](https://docs.docker.com/reference/compose-file/services/#container_name),
[Compose recreation and mounted data](https://docs.docker.com/reference/cli/docker/compose/up/),
[service DNS](https://docs.docker.com/compose/how-tos/networking/).
