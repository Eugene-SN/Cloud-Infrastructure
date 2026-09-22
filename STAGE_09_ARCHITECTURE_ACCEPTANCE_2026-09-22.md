# Stage 09 Architecture Acceptance — 2026-09-22

## Status

**ARCHITECTURE / DEPLOYMENT CONTRACT — ACCEPTED**

Acceptance marker:

`STAGE09_ARCHITECTURE_ACCEPTANCE=PASS`

## Scope

Stage 9 — Edge Cloud Portal.

The accepted baseline deliberately starts small and remains extensible. The initial portal is a lightweight authenticated navigation/status surface, not a second maintenance UI or a new monitoring backend.

## Accepted baseline architecture

- public user endpoint: `https://app.escloud.us`;
- existing Xray -> host nginx -> shared TLS ingress;
- ordinary Authelia `auth_request` protection for the portal;
- static frontend only, served from `/var/www/app.escloud.us`;
- no Docker container, application server, systemd portal daemon, database, SSE or WebSocket;
- same-origin read-only status endpoint `/api/status`;
- `/api/status` serves the accepted Stage 8 live snapshot `/run/edge-monitor/snapshot.json`;
- Stage 8 remains the only monitoring/state producer and is not modified for Stage 9;
- response caching for status is disabled;
- frontend polls status approximately every 5 seconds;
- frontend supports explicit `LIVE`, `STALE` and `UNAVAILABLE` presentation;
- `STALE` threshold is 30 seconds from snapshot `generated_at`;
- health values `OK`, `DEGRADED` and `FAIL` are consumed from Stage 8 as-is;
- the portal does not create a replacement aggregate health engine;
- because schema v1 has no top-level `applications.state`, the portal shows individual application states instead of deriving a new aggregate;
- concise presentation includes overall state, Edge, Home/PAI, Knowledge, Operations, selected host metrics, application states, Backrest freshness and maintenance metadata;
- detailed low-level unit/probe internals and snapshot IDs are not primary UI content.

## Navigation baseline

Initial service links are limited to real operator-facing endpoints:

- Hermes — `https://hermes.escloud.us`;
- n8n — `https://n8n.escloud.us`;
- CloudCLI — `https://code.escloud.us`;
- Mattermost — `https://chat.escloud.us`;
- Mail — `https://mail.escloud.us`;
- Maintenance — `https://update.escloud.us`.

Do not add fake/placeholder application cards for reserved names.

`auth.escloud.us` is infrastructure authentication rather than an operator destination.

`backup.escloud.us` currently has DNS/TLS identity but no accepted public Backrest UI vhost, so it is not represented as a working portal destination.

## Maintenance boundary

The portal may display read-only maintenance metadata such as update count and reboot-required state and may link to `update.escloud.us`.

It must not receive or expose:

- Semaphore credentials;
- update template IDs as execution controls;
- individual update actions;
- selected-update actions;
- Master Batch actions;
- Refresh actions;
- any other mutation API.

`update.escloud.us` remains the only Stage 7 operator surface for real update execution.

## Runtime evidence used for acceptance

The bounded Stage 9 current-state audit confirmed:

- `edge-monitor.service` active/enabled with `NRestarts=0`;
- `/run/edge-monitor/snapshot.json` present as root:root mode 0644 under traversable 0755 directories;
- valid schema v1 containing `overall_state`, Edge, applications, Home/PAI, Knowledge and Operations data;
- `app.escloud.us` DNS resolves to the edge public IPv4 and is present in the shared TLS SAN set;
- no active dedicated nginx vhost exists yet for `app.escloud.us`;
- current `app.escloud.us` HTTP 200 is therefore default-vhost fallback, not a deployed portal;
- `backup.escloud.us` likewise has no active dedicated nginx vhost;
- zero failed systemd units.

## Deployment / recovery contract

Deployment sequence:

1. inspect exact current nginx and Authelia runtime files required for the new vhost;
2. create static portal assets;
3. create the inactive nginx vhost configuration;
4. validate nginx syntax;
5. enable the vhost;
6. validate nginx syntax again;
7. reload nginx without restart;
8. verify HTTP->HTTPS, Authelia protection, authenticated portal rendering and `/api/status`;
9. verify `LIVE`, `STALE` and `UNAVAILABLE` presentation using fixture/alternate-path testing without stopping `edge-monitor.service`;
10. perform bounded production non-regression.

Rollback is limited to disabling/removing the Stage 9 nginx vhost/static assets and reloading nginx. Existing Stage 8 monitoring and Stage 7 maintenance are not mutated.

## Acceptance boundary

This record accepts architecture and deployment contract only. Stage 9 runtime deployment and final integrated acceptance remain pending.

The baseline is intentionally extensible: later visual/detail improvements may be added without changing the accepted separation between portal presentation, Stage 8 monitoring and Stage 7 update execution.
