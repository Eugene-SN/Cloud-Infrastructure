# Edge Stage 1 Authelia Public Ingress Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_AUTHELIA_PUBLIC_INGRESS_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted ingress path

`auth.escloud.us` is now integrated into the existing public edge path:

`client -> Xray TCP/443 TLS -> nginx 127.0.0.1:8080 proxy_protocol -> Authelia 127.0.0.1:19091`

No direct public Authelia port was introduced.

## nginx state

- dedicated Stage 1 vhost: `/etc/nginx/sites-available/auth-escloud-us.conf`;
- enabled via `/etc/nginx/sites-enabled/auth-escloud-us.conf`;
- HTTP/80 for `auth.escloud.us` redirects to HTTPS;
- ACME challenge path remains served from `/var/www/letsencrypt/.well-known/acme-challenge/`;
- HTTPS fallback vhost listens on `127.0.0.1:8080 proxy_protocol`;
- upstream backend: `http://127.0.0.1:19091`;
- proxy headers preserve host, TLS scheme/port, and Proxy Protocol client address;
- websocket upgrade map added at `/etc/nginx/conf.d/websocket-map.conf`;
- `nginx -t`: PASS;
- reload: PASS.

## Functional acceptance

- HTTP `auth.escloud.us` -> HTTPS redirect: PASS (`301`);
- HTTPS root through Xray fallback: HTTP 200;
- public `/api/health` through Xray/nginx: HTTP 200;
- TLS certificate presented for `auth.escloud.us`: Let’s Encrypt `escloud.us` certificate, verification PASS;
- Authelia backend remained running/healthy with `RestartCount=0`;
- direct public TCP/19091 exposure remains absent;
- primary `escloud.us` Xray->nginx fallback `/health` remained functional.

## Non-regression

- nginx active;
- Xray active;
- Hysteria2 active;
- failed systemd units: 0.

## Scope boundary

Only `auth.escloud.us` was restored for Stage 1. Unrelated legacy/future vhosts such as `go`, `app`, `docs`, `cloud`, `sync`, `code`, and `chat` were intentionally not restored because their backend applications belong to later stages.

## Next Stage 1 work

Audit and decide the minimal firewall/public-exposure policy for the rebuilt Docker host using actual current listeners and Docker nftables/iptables chains before any firewall mutation. Then continue the remaining Stage 1 base-platform scope.
