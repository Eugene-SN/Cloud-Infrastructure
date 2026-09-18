# Stage 04E — Mattermost Pre-deployment Audit — 2026-09-18

**Status:** PASS / READY FOR DEPLOYMENT MUTATION

## Runtime evidence

Fresh read-only audit on `edge`:

- Ubuntu 26.04.1 LTS, kernel 7.0.0-31-generic;
- Docker 29.8.1, Compose 5.5.1;
- ~15 GiB RAM total, ~13 GiB available at audit time, 4 GiB swap unused;
- root/`/srv` filesystem: ext4, 155 GiB total, ~138 GiB free;
- existing application containers healthy/running: Stalwart, Bulwark, n8n, Authelia;
- existing Docker networks are separate per-stack bridges; no Mattermost network/state exists;
- ports 18065, 8065, 8443 and 5432 were free;
- no existing Mattermost state found under `/opt`, `/srv` or nginx;
- existing public ingress pattern uses Xray TCP/443 -> nginx loopback proxy-protocol listener;
- no nginx vhost yet exists for `chat.escloud.us`;
- shared TLS certificate already contains `DNS:chat.escloud.us`;
- DNS `chat.escloud.us -> 45.92.156.17` resolves;
- public HTTPS currently reaches the default/fallback site with HTTP 200 because no Mattermost vhost exists yet;
- UFW already permits public TCP/443 through the accepted Xray ingress; no Mattermost-specific public firewall port is needed;
- Hermes pre-integration non-regression passed:
  - `Hermes Agent v0.21.3 (2026.9.14) · upstream d177b119`;
  - gateway active/enabled;
  - config SHA256 remains `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`.

## Deployment implications

- use `127.0.0.1:18065 -> Mattermost:8065` as the host backend mapping;
- do not publish PostgreSQL;
- do not expose 8065 or Calls 8443 publicly;
- no UFW mutation is required;
- deploy under `/opt/mattermost` with persistent application/database state under `/srv/mattermost`;
- create a new dedicated Compose network for the Mattermost stack;
- reuse existing host nginx/Xray/shared TLS for `chat.escloud.us`;
- Calls remains disabled;
- TPNS remains accepted;
- Hermes baseline is clean enough to proceed with Mattermost before the remaining Hermes capability work.

`STAGE4E_MATTERMOST_PREDEPLOY_AUDIT=PASS`


## Recovery continuation after initial deployment-script probes

The first deployment attempt stopped before filesystem/runtime mutation because the current Mattermost Team image is distroless and has no `sh`. A follow-up metadata probe also stopped on an optional Docker inspect key that was absent. Neither failure created `/opt/mattermost`, `/srv/mattermost`, or Mattermost/PostgreSQL containers; only image pulls occurred.

Final recovery audit established:

- Mattermost image ID: `sha256:335db2833330323d9a9f43313429f4b16b497067644660acfdfc2424ab04d2de`;
- runtime image user: `mattermost`;
- image command: `/mattermost/bin/mattermost`;
- image is distroless (no shell);
- Mattermost version: **11.11.0**, Team build (`Build Enterprise Ready: false`);
- PostgreSQL image ID: `sha256:6c538e7206ea40ff740ef27883529390a690b6ead6ba96b44c67a9f7c638e8fd`;
- PostgreSQL runtime UID/GID from the current image: `70:70`;
- ports 18065/8065/8443/5432 remained free;
- deployment continuation point is filesystem layout + Compose creation.

Current Mattermost upstream source/runtime contract uses UID/GID `2000:2000` for the `mattermost` account; the corrected deployment block uses that documented bind-mount ownership rather than attempting to invoke a shell in the distroless image.

`STAGE4E_MATTERMOST_CORE_DEPLOY_RECOVERY_AUDIT_V3=PASS`


## Recovery audit V4 validity correction

A later recovery script printed a final PASS marker despite an arithmetic syntax error caused by a malformed container-count command substitution that produced `0\n0`. Therefore that script's final PASS marker is **INVALID** and must not be used as acceptance evidence.

The useful read-only facts from that output remain valid:

- `/opt/mattermost` exists as an otherwise empty root-owned directory;
- `/srv/mattermost` exists as an otherwise empty root-owned directory;
- all Mattermost application subdirectories are absent;
- `/opt/mattermost/.env` and `compose.yaml` are absent;
- no Mattermost/PostgreSQL containers were created;
- host UID/GID 2000 have no name entries, which is irrelevant because upstream instructs numeric `chown 2000:2000`.

No runtime deployment occurred.

The subsequent deployment procedure is reset to the exact official `mattermost/docker` workflow documented in Stage 4D, with only the accepted loopback/no-Calls Compose override.

`STAGE4E_MATTERMOST_RECOVERY_V4_FINAL_MARKER=INVALID_DUE_SCRIPT_ERROR`

## Official Docker deployment runtime reached; verification V2 false-negative

The official Docker deployment itself completed successfully from upstream `mattermost/docker` commit `497414659ee7127677d2b91b44bb4f3ea9d14695`.

Confirmed before the verifier stopped:

- upstream worktree clean and merged Compose config valid;
- `mattermost-mattermost-1` running healthy with `restart=unless-stopped`;
- `mattermost-postgres-1` running with `restart=unless-stopped`;
- PostgreSQL accepts connections;
- Mattermost API `/api/v4/system/ping` returns `status=OK`;
- Mattermost runtime is `11.11.0`, Team build (`Build Enterprise Ready: false`);
- Compose reports only `127.0.0.1:18065->8065/tcp` as the Mattermost host publication; PostgreSQL shows internal `5432/tcp` only;
- the host listener output explicitly shows `127.0.0.1:18065`.

The later `LOOPBACK_BACKEND_GATE=FAIL` is a verifier false-negative caused by combining `set -o pipefail` with a `... | grep -q ...` pipeline: after `grep -q` exits on the first match, an upstream process can receive SIGPIPE, making the pipeline non-zero despite a successful match.

Do not repeat already-passed database/API/version/runtime checks. Final core acceptance requires only the missing listener/publication and Hermes post-deployment non-regression checks.

`STAGE4E_MATTERMOST_DEPLOY_RUNTIME=RUNNING_ACCEPTANCE_PENDING_FINAL_MISSING_GATES`

## Verification V3 validity correction

The subsequent `STAGE4E_MATTERMOST_CORE_RUNTIME_FINAL_VERIFY_V3` script is **INVALID** as acceptance evidence. Its embedded Python was passed through a shell single-quoted `python3 -c '...'` string while the Python body itself contained single-quoted dictionary keys inside an f-string expression. Shell quote removal transformed expressions such as `state.get('Status')` into `state.get(Status)`, causing a Python `NameError` before any verification could complete.

This was a script-construction error, not a Mattermost runtime failure. No mutation occurred in that verifier.

For the next verifier:
- embedded Python is removed entirely;
- container state uses direct `docker inspect -f` fields;
- listener checks use `ss` string capture rather than pipelines;
- no `grep -q` is used;
- Hermes checksum parsing avoids pipelines;
- the exact shell block was locally syntax-checked with `bash -n` and static-scanned for the previous anti-patterns before being sent.

`STAGE4E_MATTERMOST_CORE_RUNTIME_FINAL_VERIFY_V3=INVALID_SCRIPT`

