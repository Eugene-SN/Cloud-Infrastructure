# Stage 7 — Same-Origin Semaphore UI on update.escloud.us — 2026-09-21

## Result

**COMPLETE / ACCEPTED**

`STAGE07_SEMAPHORE_SAME_ORIGIN_UI=PASS`

## Accepted user paths

- `https://update.escloud.us/` — canonical entry; after authentication the loopback dashboard server redirects to `/status/`;
- `https://update.escloud.us/status/` — custom Maintenance Control dashboard;
- `https://update.escloud.us/project/1/history` — full Semaphore task history UI opened by the dashboard's **Semaphore** button;
- `/api/` — Semaphore API contract used by the maintenance dashboard and Semaphore SPA;
- `/api/ws` — Semaphore WebSocket used for live task state/output.

No separate `ops.escloud.us` application vhost is used.

## Runtime changes

Semaphore remains host-native and loopback-only at `127.0.0.1:3000`. Its public route setting is:

```json
"web_host": "https://update.escloud.us/"
```

The internal dashboard nginx at `127.0.0.1:18070` preserves its exact root redirect and `/status/` static route. Its `/api/` route continues to proxy the Semaphore API and now carries WebSocket upgrade headers. The remaining UI and asset paths proxy to Semaphore. Both proxy paths supply the accepted public HTTPS forwarded-host contract.

The canonical and deployed dashboard copies now use:

```html
href="/project/1/history"
```

## Recovery checkpoint

Before mutation, nginx configuration, Semaphore configuration, both dashboard copies, full `nginx -T` output and a consistent SQLite backup were saved at:

```text
/srv/backups/edge-stage7-semaphore-ingress/recovery-20260921T104418Z
```

The checkpoint has a verified SHA-256 manifest. No task was active before any Semaphore restart.

## Verification

- `nginx -t`: PASS;
- nginx and Semaphore: active/running, `NRestarts=0`;
- Semaphore listener: `127.0.0.1:3000` only;
- dashboard listener: `127.0.0.1:18070` only;
- internal `/`: HTTP 302 with `Location: /status/`;
- internal `/status/`: HTTP 200;
- internal `/project/1/history`: HTTP 200 with `<base href="https://update.escloud.us/">`;
- Semaphore application JavaScript asset: HTTP 200;
- `/api/ping`: HTTP 200;
- authenticated proxy API identity: present; project template list and task history both return HTTP 200;
- template UI route `/project/1/templates`: HTTP 200; existing Refresh template remains visible;
- `/api/ws`: HTTP 101 Switching Protocols;
- public HTTP `/project/1/history`: HTTP 301 to the same path on HTTPS;
- unauthenticated public HTTPS `/project/1/history`: HTTP 302 to Authelia with the exact same return path;
- dashboard button target: `/project/1/history` in both source and deployed copies;
- SQLite state preserved: no active task; one successful historical task; template `01. Refresh — Edge Maintenance Status` remains present;
- no new public listener or UFW rule was added.

An authenticated browser session was not available in the maintenance shell. The public Authelia return path, the complete same-origin upstream route, SPA asset loading and live WebSocket boundary were verified independently.

## Accepted boundary

The full Semaphore UI is available for task/template inspection and live logs from the same Stage 7 origin. This does not authorize autonomous update execution: the accepted manual-execution rule and prohibition on update timers, schedules and background launchers remain in force.
