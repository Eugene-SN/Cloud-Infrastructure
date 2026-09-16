# Edge Stage 1 Authelia Local Runtime Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_AUTHELIA_LOCAL_RUNTIME_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Runtime

- Authelia version: `4.39.27`;
- image channel: `docker.io/authelia/authelia:latest`;
- container name: `authelia`;
- restart policy: `unless-stopped`;
- loopback publish: `127.0.0.1:19091 -> 9091`;
- public TCP/19091 exposure: none;
- health endpoint `/api/health`: HTTP 200;
- root endpoint: HTTP 200;
- Docker health: healthy.

## Preserved state at runtime

- users database visible and non-empty at `/config/users_database.yml`;
- SQLite `PRAGMA integrity_check`: `ok`;
- preserved secrets/state from the earlier restore remain in use;
- first start under Authelia 4.39.27 performed the expected SQLite schema migration from 28 to 29;
- subsequent restart reported the schema already up to date.

Schema 29 is therefore the current accepted production runtime state. The preserved migration archive remains the continuity/rollback source and is not an instruction to downgrade the live database schema.

## Restart acceptance

- container restart completed successfully;
- container PID changed as expected;
- post-restart Docker health returned healthy;
- post-restart `/api/health` returned HTTP 200;
- `RestartCount=0` after the explicit controlled restart.

## Existing edge non-regression

- Docker active;
- nginx active;
- Xray active;
- Hysteria2 active;
- existing Xray → nginx HTTPS fallback `/health`: PASS;
- failed systemd units: 0.

## Next Stage 1 work

Add only the Stage 1 `auth.escloud.us` nginx route on the existing Xray fallback ingress, proxy it to `127.0.0.1:19091`, validate nginx, and verify the Authelia login/root endpoint over public HTTPS through Xray. Do not restore unrelated future application vhosts yet.
