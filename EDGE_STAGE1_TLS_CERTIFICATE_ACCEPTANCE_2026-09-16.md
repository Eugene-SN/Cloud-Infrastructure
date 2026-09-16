# Edge Stage 1 TLS Certificate Acceptance — 2026-09-16

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_TLS_CERTIFICATE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted certificate state

- Certbot version: `4.0.0`;
- certificate name: `escloud.us`;
- authenticator: `webroot`;
- ACME webroot: `/var/www/letsencrypt`;
- private key type: ECDSA P-256 / `secp256r1`;
- certificate path: `/etc/letsencrypt/live/escloud.us/fullchain.pem`;
- private key path: `/etc/letsencrypt/live/escloud.us/privkey.pem`;
- issuer observed at acceptance: Let's Encrypt `YE2`;
- validity observed: `2026-09-16 19:27:04 UTC` through `2026-12-15 19:27:03 UTC`;
- Certbot renewal configuration exists at `/etc/letsencrypt/renewal/escloud.us.conf`;
- `certbot.timer`: enabled and active;
- `certbot renew --dry-run`: PASS;
- certificate validity >30 days gate: PASS;
- nginx and SSH non-regression: PASS;
- system state: `running`, failed units: 0;
- TCP/443 remained free and reserved for Xray at acceptance.

## Accepted SAN set

The issued certificate covers the complete historical ten-name set:

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

All ten names passed DNS A-record validation to `45.92.156.17` and HTTP-01 webroot reachability before issuance. No CAA restriction was observed.

## Still pending

- Xray deployment on TCP/443 and integration with nginx fallback `127.0.0.1:8080 proxy_protocol`;
- Hysteria2 deployment on UDP/443 and public masquerade integration;
- certificate synchronization copies for Xray/Hysteria2;
- Certbot deploy hook that refreshes those copies and safely restarts/reloads the services after renewal;
- preserved VPN credential/state restoration and `vpnctl` adaptation;
- Authelia foundation;
- firewall decision;
- remaining Stage 1 layout/backup/portal boundaries.

Historical versions are not pins. Xray/Hysteria2 deployment must resolve current supported stable releases at deployment time while preserving the accepted legacy external contract unless a concrete incompatibility appears.
