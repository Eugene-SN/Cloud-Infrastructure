# Edge Stage 1 Authelia State Restore Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_AUTHELIA_STATE_RESTORE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Preserved state continuity

The legacy Authelia state was selectively restored from the verified sensitive migration archive into the normalized current paths without regenerating authentication state or secrets.

Accepted persistent paths:

- `/srv/authelia/config/configuration.yml`;
- `/srv/authelia/config/users_database.yml`;
- `/srv/authelia/secrets/session_secret`;
- `/srv/authelia/secrets/storage_encryption_key`;
- `/srv/authelia/secrets/jwt_secret`;
- `/srv/authelia/data/db.sqlite3`;
- `/srv/authelia/data/notification.txt`.

Runtime definition path:

- `/opt/authelia/compose.yaml`.

## Current runtime candidate

- image channel: `docker.io/authelia/authelia:latest`;
- resolved runtime version at restore time: `v4.39.27`;
- resolved image/repository digest: `sha256:40005803cd4e2eaeea4418517e9e9c7f515b55b31071a02829341ca2e50ca7c0`;
- Docker Engine: `29.8.1`;
- Docker Compose: `5.5.1`.

The historical Authelia version was not retained as a pin; the current upstream stable channel was used.

## Compatibility and integrity verification

- preserved configuration parsed and validated successfully with current Authelia `4.39.27`;
- production-path configuration validated successfully with the same current image;
- preserved users database contains Argon2 password state and passed structural validation;
- SQLite `PRAGMA integrity_check` result: `ok`;
- all three preserved Authelia secrets matched the archive source by SHA256 after restore;
- `configuration.yml`, `users_database.yml`, SQLite state, and notifier file matched the staged archive source by SHA256 after restore;
- `notification.txt` is an intentionally valid empty file (0 bytes), preserved exactly from the archive.

## Accepted file state

- `configuration.yml`: `root:root`, mode `0640`;
- `users_database.yml`: `root:root`, mode `0660`;
- secret files: `root:root`, mode `0600`;
- `db.sqlite3`: `root:root`, mode `0660`;
- `notification.txt`: `root:root`, mode `0660`;
- `/opt/authelia/compose.yaml`: `root:root`, mode `0644`.

## Service boundary at acceptance

This subphase intentionally did not start Authelia:

- Authelia container: not created;
- loopback TCP/19091: free;
- Docker remained active;
- nginx remained active;
- Xray remained active;
- Hysteria2 remained active;
- failed systemd units: 0.

## Next Stage 1 work

Create/start the Authelia container from `/opt/authelia/compose.yaml`, verify health and the loopback-only `127.0.0.1:19091` listener, verify preserved SQLite/users state is usable at runtime, then add the `auth.escloud.us` nginx route only after local runtime acceptance.
