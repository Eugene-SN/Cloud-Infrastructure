# Weblate on edge

CONFIRMED 2026-10-23: use Weblate on Edge at https://translate.escloud.us
with the existing Authelia login. Runtime/configuration: /opt/weblate;
operations: /opt/weblate/OPERATIONS.md; persistent data: /srv/weblate.
Hermes is reached through the existing Edge-local integration. Documentation
runtime: /home/core/.hermes/profiles/documentation/pipeline on Edge.
The ai-node test Weblate, /srv/pdf-poc, port 17880 and the dedicated
weblate-hermes SSH transport/account were removed. Do not reuse their old
credentials, component IDs, paths or deployment commands. The ai-node vLLM
endpoint at 192.168.1.30:8000 remains a separate model backend.

Historical profile snapshots elsewhere in this repository must not overwrite
newer deployed settings. The earlier ai-node pilot is not an access/runbook source.

`compose.yaml` is the canonical copy of `/opt/weblate/compose.yaml`.
The existing project name `weblate-edge`, service keys `weblate`/`cache`,
environment files, bind mounts, networks and image tracks are preserved.
Permanent container names are `weblate` and `weblate-valkey`.

Credentials and provider configuration remain in the protected deployment
under `/opt/weblate`; do not add their values to Git. Native Compose uses that
directory for relative `environment` and `cloud.env` paths. Operational details
remain in `/opt/weblate/OPERATIONS.md`. Recovery uses the coordinated Weblate
database/data/configuration bundle in the accepted Backrest snapshot.
