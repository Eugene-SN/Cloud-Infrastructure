# Edge Stage 1 VPN Public Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_VPN_PUBLIC_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Xray acceptance

- service: active and enabled;
- version: `26.3.27`;
- listener: TCP/443;
- VLESS/TLS config validated before start;
- current Let's Encrypt `escloud.us` certificate presented successfully;
- certificate verification: PASS;
- HTTPS fallback through Xray to nginx `127.0.0.1:8080` with Proxy Protocol: PASS via `/health`;
- `NRestarts=0` at acceptance;
- preserved Xray credentials functionally retained.

## Hysteria2 acceptance

- service: active and enabled;
- version: `2.12.3`;
- listener: UDP/443;
- preserved auth user count from CSV state: 2;
- real local Hysteria2 client handshake using preserved primary credential: PASS;
- TLS verification with SNI `escloud.us`: PASS;
- temporary SOCKS5 client listener: PASS;
- HTTPS request through the Hysteria2 tunnel returned HTTP 200;
- temporary client process and test artifacts were cleaned;
- `NRestarts=0` at acceptance;
- preserved Hysteria2 credentials functionally retained.

## Listener state at acceptance

Public/edge listeners include:

- SSH TCP/22;
- nginx TCP/80;
- Xray TCP/443;
- Hysteria2 UDP/443;
- nginx fallback listener `127.0.0.1:8080` with Proxy Protocol.

## Non-regression

- system state: `running`;
- failed systemd units: 0;
- nginx active;
- SSH socket active;
- Xray active/enabled with zero restarts;
- Hysteria2 active/enabled with zero restarts.

## Next accepted-first activity

Restore/adapt the preserved certificate synchronization lifecycle and Certbot deploy hook so renewed `escloud.us` certificate/key material is copied with the required ownership/modes into `/etc/xray/tls` and `/etc/hysteria/tls`, then safely refresh the running VPN services and verify post-hook TLS/fallback/Hysteria functionality.
