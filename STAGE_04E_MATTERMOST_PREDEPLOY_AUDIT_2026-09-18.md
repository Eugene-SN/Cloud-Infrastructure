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
