# Stage 08 — Monitoring Notification Model v2 Design — 2026-09-25

## Status

**ACCEPTED DESIGN / IMPLEMENTATION PENDING**

This record refines the Mattermost notification semantics of the already accepted Stage 8 monitoring runtime. It does not reopen the accepted collectors, probe cadences, two-failure confirmation rule, snapshot publication, or edge-only monitoring scope.

## Context

A fresh read-only runtime audit on 2026-09-25 confirmed that `edge-monitor` collects substantially richer state than the Mattermost channel currently receives. The current notification path flattens each raw check into an independent key and posts a minimal `previous -> current` transition plus a short summary. This preserves deduplication but loses operational context and can produce multiple independent-looking alerts for one underlying failure.

The accepted correction is therefore a notification/correlation refinement, not a monitoring-stack replacement.

## Channel role

The private Mattermost `Monitoring` channel is an **operational incident journal**.

It is not:
- a telemetry feed;
- a log stream;
- an update-availability feed;
- a health dashboard;
- a duplicate of agent service channels.

Normal state remains silent. Current status belongs in the existing Stage 9 portal/snapshot surfaces.

## Event lifecycle

The target behavior is:

1. healthy state: no Mattermost message;
2. incident/degradation confirmed by the existing probe semantics: one informative post;
3. unchanged incident: silence;
4. materially changed root cause/severity: at most one useful update when it changes operator interpretation;
5. recovery: one recovery post with incident duration and current recovered evidence.

No periodic reminders are introduced.

## Severity model

Only three user-visible classes are required:

- **INCIDENT** — a user-facing function or important operational capability is unavailable;
- **DEGRADED** — capability still exists but an accepted health/freshness condition is violated;
- **RECOVERED** — a previous INCIDENT/DEGRADED condition returned to normal.

Routine INFO events do not belong in `Monitoring`.

## Message contract

An incident message should contain, when the current probes provide the data:

- human-readable incident title;
- scope/location (`EDGE`, `HOME/PAI`, `KNOWLEDGE`, `OPERATIONS`);
- concise user/operational impact;
- root/primary signal;
- relevant diagnostic evidence;
- incident start time;
- probe confirmation context when useful.

A recovery message should contain:

- human-readable recovered title;
- scope;
- outage/degradation duration;
- current recovered evidence;
- recovery time.

Raw internal keys such as `app/mattermost` remain implementation identifiers, not primary user-facing titles. Raw Python/JSON object dumps are not the normal Mattermost presentation.

## Primary versus diagnostic signal model

The following table is the accepted correlation contract for the currently deployed checks.

| Operational capability / incident | Primary signal(s) | Diagnostic evidence / dependent checks | Correlation rule |
| --- | --- | --- | --- |
| Edge public web ingress | `xray.service`, `nginx.service` as one ingress capability | local application HTTP probes | If either ingress service fails, emit one **Edge public web ingress** incident naming the failed component(s). Local backend HTTP success does not negate public-ingress failure. Current monitoring has no external public-URL vantage point; do not claim end-to-end Internet reachability. |
| Hysteria2 | `hysteria-server.service` | none currently | Independent service incident. |
| Docker runtime | `docker.service`; `containerd.service` as underlying runtime evidence | all Docker container states and Docker-backed application HTTP probes | When Docker runtime failure explains child failures, emit one Docker-runtime incident and suppress child fan-out. Child states remain diagnostics. |
| Mattermost | `app/mattermost` HTTP probe | `mattermost-mattermost-1`, `mattermost-postgres-1`, Docker runtime | HTTP availability is the service-level signal when Docker runtime is healthy. Container/database checks explain the cause. |
| n8n | `app/n8n` HTTP probe | `n8n` container, Docker runtime | HTTP availability is primary; container state is diagnostic unless Docker runtime is the parent failure. |
| Authelia | `app/authelia` HTTP probe | `authelia` container, Docker runtime | HTTP availability is primary. |
| Semaphore | `app/semaphore` HTTP probe | `semaphore.service` | HTTP availability is primary; systemd runtime explains failures. |
| Maintenance UI/backend | `app/maintenance` HTTP probe | ingress runtime where applicable | Availability of the maintenance backend is separate from maintenance semantic state. |
| Nextcloud | `app/nextcloud` HTTP probe | `nextcloud-app-1`, `nextcloud-cron-1`, `nextcloud-db-1`, `nextcloud-redis-1`, Docker runtime | One Nextcloud incident. Containers are diagnostic evidence; do not emit a separate user-facing incident for every dependent container when a common parent explains them. |
| Projects WebDAV | `app/webdav` HTTP probe | `projects-webdav.service` | HTTP result is primary; the user service is diagnostic. Expected authenticated-response semantics remain part of the existing probe. |
| T3 Code | `app/t3_code` HTTP probe | `t3code.service` | HTTP availability is primary; user-service state is diagnostic. |
| Stalwart mail runtime | `stalwart` container | Docker runtime | Container state remains primary because no application-level mail probe is currently deployed. Do not invent protocol availability. |
| Bulwark | `bulwark` container | Docker runtime | Container state remains primary because no higher-level probe exists. |
| Hermes gateway runtime | `hermes-gateway.service` | Hermes agent service-channel lifecycle messages | Monitoring reports persistent/unplanned runtime failure; ordinary planned lifecycle notifications remain agent-channel concerns. |
| Hermes dashboard runtime | `hermes-dashboard.service` | public ingress runtime | Independent dashboard runtime signal; no claim of public end-to-end availability beyond available probes. |
| Antigravity daemon | `antigravity-cli-daemon.service` | none currently | Independent runtime incident. |
| Home/PAI overlay path | semantic NetBird state plus `netbird.service` | PVE, ai-node, vLLM and Syncthing-PVE reachability | NetBird must become an explicit notification signal. If NetBird failure explains dependent Home/PAI failures, emit one overlay-connectivity incident and suppress dependent fan-out while preserving their states as diagnostics. |
| PVE reachability | `home-pai/pve` | NetBird parent state | Emit independently only when the NetBird parent path is healthy. |
| ai-node reachability | `home-pai/ai_node` | NetBird parent state | Emit independently only when the NetBird parent path is healthy. |
| vLLM inference availability | `home-pai/vllm` including expected model/mode | ai-node reachability, NetBird parent state | Emit as a vLLM incident only when parent connectivity is healthy; otherwise treat as dependent diagnostic evidence. |
| Knowledge replication | aggregate `knowledge/syncthing` | Syncthing API, PVE peer connectivity, folder state/pull errors, `syncthing@core.service`, NetBird parent state | Emit one Knowledge replication incident/degradation with the failing subcomponent named. If NetBird is the root cause, suppress duplicate peer-connectivity incident. |
| Backrest runtime | `backrest.service` | plan freshness | Runtime failure is one incident. Freshness remains separately meaningful after its accepted age thresholds. |
| Backup freshness: `edge-state` | plan freshness state | last successful snapshot time/age, Backrest runtime | One plan-specific degradation/incident with human-readable age. |
| Backup freshness: `edge-knowledge-local` | plan freshness state | last successful snapshot time/age, Backrest runtime | One plan-specific degradation/incident with human-readable age. |
| Maintenance semantic health | `operations.maintenance` | `CHECK_FAILED`, `REBOOT_REQUIRED`, source freshness | `CHECK_FAILED` or `REBOOT_REQUIRED` may produce DEGRADED. `UPDATE_AVAILABLE` remains informational metadata and does not create a Monitoring event. |
| Host CPU / memory / root filesystem | current FAST snapshot telemetry | current values | Dashboard/snapshot only for now. No new arbitrary alert thresholds are accepted by this decision. |

## Correlation and suppression rules

- Parent/root-cause failures suppress redundant child notifications while the parent failure plausibly explains them.
- Suppression affects Mattermost presentation only; raw child probe state remains present in `snapshot.json`.
- A child incident may be emitted when its parent is healthy or when its state remains failed after the parent recovers.
- Recovery should mirror the incident identity that was emitted, not every suppressed raw probe.
- Existing two-consecutive-failure confirmation remains unchanged for ordinary endpoint probes.
- Existing Backrest freshness thresholds remain unchanged.
- Existing notification deduplication remains conceptually retained, but durable state must track incident identity/start time rather than only raw check state where needed for duration/correlation.
- Obsolete durable keys that no longer exist in the current check inventory must be pruned safely; the observed retired `app/cloudcli` key is stale state, not an active monitor target.

## Explicit current limitations

- No independent external vantage point is added. Complete edge/public-connectivity loss can still be unreportable from edge itself.
- Current application probes use local backends. Public Internet reachability of each hostname is not proven by those local probes.
- No new protocol-level Stalwart/Bulwark checks are added by this design.
- No CPU/memory/disk thresholds are introduced without a separate requirement.
- No Prometheus, Grafana, Loki, Alertmanager, Gatus, monitoring database, or additional monitoring service is introduced.

## Implementation boundary

Implementation should preserve the current collectors, probe intervals, snapshot schema where practical, and service supervision. The intended mutation is narrowly scoped to:

- service-oriented incident mapping;
- correlation/suppression;
- richer deterministic Mattermost formatting;
- incident start/duration tracking;
- explicit NetBird notification coverage;
- safe stale durable-state reconciliation.

Implementation must be followed by a controlled transition/dedup/recovery acceptance test without intentionally disrupting production services.
