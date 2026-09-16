# Edge Stage 1 nginx / ACME Foundation Acceptance — 2026-09-16

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_NGINX_ACME_FOUNDATION_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted runtime state

- nginx package: `1.28.3-2ubuntu1.11`;
- `nginx.service`: active/enabled;
- Ubuntu default site disabled;
- public HTTP listener: TCP/80 on IPv4 and IPv6;
- Xray fallback ingress listener: `127.0.0.1:8080 proxy_protocol`;
- Proxy Protocol real-IP trust is restricted to `127.0.0.1` through `/etc/nginx/conf.d/xray-realip.conf`;
- public webroot: `/var/www/escloud.us/public`;
- ACME webroot: `/var/www/letsencrypt`;
- Stage 1 site: `/etc/nginx/sites-available/edge-stage1.conf` enabled through `sites-enabled`;
- `/health` returns `200 ok`;
- direct public HTTP validation: PASS;
- Proxy Protocol fallback validation: PASS;
- nginx configuration syntax validation: PASS;
- nginx current-deployment error gate: PASS;
- system state remained `running`, failed units remained 0, SSH socket remained healthy.

## ACME/DNS reachability

HTTP-01 webroot reachability passed for the complete historical SAN set:

- `escloud.us`;
- `app.escloud.us`;
- `auth.escloud.us`;
- `chat.escloud.us`;
- `cloud.escloud.us`;
- `code.escloud.us`;
- `docs.escloud.us`;
- `go.escloud.us`;
- `mail.escloud.us`;
- `sync.escloud.us`.

All ten names currently resolve by A record to `45.92.156.17`. No public AAAA records are currently present for these names. No CAA restriction was observed for `escloud.us`.

## Public decoy state

The engineering reference preserves the legacy decoy role/path/routing but not the exact old HTML payload. Therefore `/var/www/escloud.us/public/index.html` is currently an explicitly temporary neutral placeholder. It must not be represented as the recovered historical page.

Before final Stage 1 acceptance, either restore the desired decoy content from the sensitive recovery archive or explicitly accept a replacement.

## Still pending

- issuance and renewal acceptance of the `escloud.us` ECDSA SAN certificate;
- Xray deployment and TCP/443 fallback integration;
- Hysteria2 deployment and UDP/443 masquerade integration;
- certificate synchronization/deploy hook for Xray/Hysteria2;
- VPN state/tooling adaptation;
- Authelia foundation;
- firewall decision;
- remaining Stage 1 layout/backup/portal boundaries.
