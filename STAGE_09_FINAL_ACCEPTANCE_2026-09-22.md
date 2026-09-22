# Stage 09 Final Acceptance — 2026-09-22

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`STAGE09_FINAL_ACCEPTANCE=PASS`

## Scope

Stage 9 — Edge Cloud Portal.

The accepted baseline portal is deployed at `https://app.escloud.us` and provides authenticated navigation plus concise infrastructure/status presentation from the accepted Stage 8 monitoring snapshot.

## Accepted production runtime

- public endpoint: `https://app.escloud.us`;
- ingress: existing Xray -> host nginx -> shared TLS;
- authentication: existing Authelia `auth_request` policy for `app.escloud.us`;
- static web root: `/var/www/app.escloud.us`;
- nginx vhost: `/etc/nginx/sites-available/app-escloud-us.conf` enabled through `/etc/nginx/sites-enabled/app-escloud-us.conf`;
- status source: Stage 8 `/run/edge-monitor/snapshot.json`;
- same-origin read-only endpoint: `/api/status`;
- frontend poll interval: 5 seconds;
- freshness semantics: LIVE, STALE after 30 seconds, UNAVAILABLE on fetch/schema failure;
- no portal backend, container, database, daemon, SSE/WebSocket, second collector or duplicated monitoring state;
- Stage 7 update execution remains exclusively on `update.escloud.us`.

Initial navigation links:

- Hermes;
- n8n;
- CloudCLI;
- Mattermost;
- Mail;
- Maintenance.

Reserved/unimplemented domains are not presented as working applications. In particular, `backup.escloud.us` is not exposed as a working Backrest UI.

## Deployment evidence

Baseline deployment passed after recovery from two assistant verifier defects:

1. the original root-context `www-data` readability probe invoked `-u` without a command; it failed before mutation and left no artifacts;
2. the freshness acceptance verifier attempted to execute JSON as Python; production UI/state were already valid and the verifier was corrected without changing runtime.

Final deployment evidence:

- dedicated `app.escloud.us` nginx vhost enabled;
- nginx syntax validation PASS;
- nginx reload PASS;
- HTTP -> HTTPS redirect PASS;
- unauthenticated HTTPS -> Authelia redirect PASS;
- unauthenticated `/api/status` -> Authelia redirect PASS;
- existing public services non-regression PASS;
- zero failed systemd units;
- Stage 8 configuration SHA256 remained `91bacef62dbf5076b405b3b08512aa85ab6bb03ca0c887b7f86521cdd78133c5`;
- `edge-monitor.service` remained active/enabled with `NRestarts=0`;
- Stage 8 EDGE, HOME_PAI, KNOWLEDGE, OPERATIONS and OVERALL states remained OK.

Accepted deployed file hashes:

- `/var/www/app.escloud.us/index.html`: `1890ae58e03bb139f185f0b073f073ffd346b9bf4d881eead452c63b4850e7ca`;
- `/var/www/app.escloud.us/app.css`: `6df0fb556a2d2242e6a3d37420a969c0d097938f012945d94dbd4d1c1db9acdc`;
- `/var/www/app.escloud.us/app.js`: `d18cc8fdb320cc8413813ca162626445d869ca4d4471af741db75dba15a1c331`;
- `/etc/nginx/sites-available/app-escloud-us.conf`: `b478be6beb15e38422473a3c73989b084507c6a0d865d8d9b502647dbef39f16`.

## Browser / freshness acceptance

Operator browser acceptance confirmed:

- Authelia login and authenticated portal rendering;
- production UI displays LIVE / OK;
- service navigation cards and infrastructure/status sections render correctly;
- current Stage 8 data is visible for infrastructure, applications, host, Home/PAI and operations.

A controlled fixture-only frontend test, without stopping `edge-monitor.service` and without modifying the production snapshot, proved:

- LIVE presentation;
- STALE presentation;
- UNAVAILABLE presentation;
- restoration to LIVE;
- production `app.js` restored byte-for-byte to SHA256 `d18cc8fdb320cc8413813ca162626445d869ca4d4471af741db75dba15a1c331`.

Final recovery verifier:

- schema version 1;
- snapshot sequence 422;
- OVERALL=OK;
- EDGE=OK;
- HOME_PAI=OK;
- KNOWLEDGE=OK;
- OPERATIONS=OK;
- `edge-monitor.service NRestarts=0`;
- nginx config valid;
- zero failed systemd units;
- `STAGE09_FRESHNESS_UI_ACCEPTANCE=PASS`;
- `STAGE09_FINAL_ACCEPTANCE_READY=YES`.

## Final acceptance

`STAGE09_FINAL_ACCEPTANCE=PASS`

Stage 9 is COMPLETE / ACCEPTED.

The portal baseline is intentionally minimal and may be enhanced later without reopening Stage 9 so long as future changes preserve the accepted responsibility boundaries: Stage 8 owns monitoring/state, Stage 7 owns update execution, and the portal remains presentation/navigation unless a future requirement explicitly supersedes that architecture.

## Roadmap effect

The next finite infrastructure stage is:

`10 — Edge Final Integrated Infrastructure Acceptance`.
