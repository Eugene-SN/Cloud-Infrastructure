# Stage 04F — Stable Docker Bridge Identity Hardening Acceptance

**Date:** 2026-09-19  
**Status:** COMPLETE / ACCEPTED  
**Marker:** `STAGE4F_STABLE_DOCKER_BRIDGE_HARDENING=PASS`

## Problem

The accepted n8n → Hermes path used Docker network `n8n_default` and UFW interface `br-2bdcbc775588`. The interface name was derived from the network ID, so ordinary network recreation could change the interface name while leaving the UFW rule stale.

## Supported mechanism

Docker documents `com.docker.network.bridge.name` as the bridge-driver option for selecting the Linux bridge interface name. Docker Compose documents explicit `default` network customization through `name`, `driver_opts` and `ipam`.

References:

- <https://docs.docker.com/engine/network/drivers/bridge/>
- <https://docs.docker.com/reference/compose-file/networks/>

## Accepted target state

- Compose project: `n8n`;
- Docker network: `n8n_hermes`;
- Linux bridge interface: `n8n-hermes`;
- subnet: `172.19.0.0/16`;
- gateway / Hermes bind: `172.19.0.1`;
- n8n address after recreation: `172.19.0.2`;
- UFW allowance: `172.19.0.0/16 -> 172.19.0.1:8642/tcp` on `n8n-hermes` only;
- no public nginx route and no public TCP/8642 listener.

The stable Linux interface name is independent of Docker network ID. Subnet and gateway remain unchanged, so the Hermes bind and production workflow URL require no change.

## Recovery checkpoint

Before mutation, current compose, UFW rules, Docker network inspect and container inspect were saved under:

`/srv/backups/edge-stage4f-network/recovery-20260919T124318Z`

`SHA256SUMS` read-back passed for every saved file. The previous compose SHA256 was `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`.

Rollback is to stop the hardened compose project, restore the saved `/opt/n8n/compose.yaml` and UFW files, bring n8n up with the saved compose, and verify the original private path. No n8n database mutation was part of this change.

## Implementation evidence

- Docker Engine `29.8.1`; Docker Compose `5.5.1`.
- Native `docker compose config` validation passed before mutation and after installation.
- Old network ID: `2bdcbc775588b40ef02d46674193de96bc551e46b14dcbed220e831a8e924205`.
- New network ID: `4b49ac393d416dac4fa7d9380864ab3d4179cc2d7cfbb321c419bb4f0855036d`.
- New network inspect reports bridge option `n8n-hermes`, subnet `172.19.0.0/16`, gateway `172.19.0.1`.
- `/opt/n8n/compose.yaml` SHA256: `03f6e88c137dedf5c5ed5cb8481c097bc2ab322e612c745f636a8fcc9117dda0`.
- `/etc/ufw/user.rules` SHA256 after cleanup: `cd66c2026a7d5583fd7f85d74c4d1081aaffd24467bb107530c1ac1661c87578`.
- The old `br-2bdcbc775588` UFW rule was removed after new-path acceptance.

## Verification evidence

- `n8n` returned healthy and readiness `{"status":"ok"}` after recreation.
- Host listener remained exclusively `172.19.0.1:8642`.
- From inside the n8n container, unauthenticated Hermes detailed health returned HTTP `401` and the existing encrypted Bearer credential path returned HTTP `200`, `status=ok`, `platform=hermes-agent`.
- Production workflow `Hermes4FMachine01` / `Hermes Machine Invocation` remained active.
- `https://n8n.escloud.us/` returned expected HTTP `302` authentication redirect.
- `hermes-gateway.service` remained active with `NRestarts=0`.
- Docker, NetBird and nginx remained active.
- All other production containers remained running; health-enabled containers were healthy.

The previously accepted `vllm`, `codex` and `antigravity` E2E evidence was not repeated because the change affected only Docker network identity. Authenticated API reachability from the real n8n container and workflow persistence directly verify the changed boundary.

## Verifier notes

Two command-wrapper non-zero exits were assistant verifier defects, not runtime failures:

- the first combined post-check called a missing `sqlite3` CLI after all network/auth checks had already passed; the database check was resumed read-only through Python's SQLite library;
- the UFW deletion wrapper used `yes` under `pipefail`; `yes` received SIGPIPE after UFW had successfully deleted the rule. Immediate UFW read-back confirmed the intended final ruleset.

## Supersession

This record supersedes the operational dependency on `n8n_default` / `br-2bdcbc775588` documented in the 2026-09-18 Stage 4F acceptance. The original record remains historical evidence of the state accepted on that date.
