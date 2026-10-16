# Weblate on edge

`compose.yaml` is the canonical copy of `/opt/weblate/compose.yaml`.
The existing project name `weblate-edge`, service keys `weblate`/`cache`,
environment files, bind mounts, networks and image tracks are preserved.
Permanent container names are `weblate` and `weblate-valkey`.

Credentials and provider configuration remain in the protected deployment
under `/opt/weblate`; do not add their values to Git. Native Compose uses that
directory for relative `environment` and `cloud.env` paths. Operational details
remain in `/opt/weblate/OPERATIONS.md`. Recovery uses the coordinated Weblate
database/data/configuration bundle in the accepted Backrest snapshot.
