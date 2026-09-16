# Edge Stage 1 VPN State Restore / Render Acceptance — 2026-09-16

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_VPN_STATE_RENDER_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Preserved state restored

Selective credential-bearing VPN state was restored from the verified migration archive into `/opt/vpn-stack` without regenerating client credentials.

Restored production state includes:

- `/opt/vpn-stack/state/services.env`;
- `/opt/vpn-stack/state/xray/users.csv`;
- `/opt/vpn-stack/state/hysteria2/users.csv`;
- `/opt/vpn-stack/conf/xray_primary_uuid.txt`;
- `/opt/vpn-stack/conf/hysteria2_primary.txt`;
- `/opt/vpn-stack/state/web-domains.txt`;
- `/opt/vpn-stack/scripts/vpnctl`.

Credential continuity was revalidated after restore:

- preserved Xray primary UUID still matches Xray CSV state;
- preserved Hysteria2 primary password still matches Hysteria2 CSV state;
- no UUID/password values were regenerated.

## Node identity adaptation

Only node identity metadata was intentionally adapted from the legacy node to the new node:

- `DOMAIN=escloud.us` preserved;
- `NODE_CODE=edge`;
- `NODE_DISPLAY=Edge`;
- `XRAY_PORT=443` preserved;
- `HY2_PORT=443` preserved.

## Rendered Xray contract

Current Xray config at `/etc/xray/config.json` was rendered from preserved state using the legacy `vpnctl` contract and validated by current Xray `26.3.27` both as root and as the `xray` service identity.

Verified non-secret contract:

- tag: `vless-tls-edge`;
- listen: `0.0.0.0`;
- port: `443/tcp`;
- protocol: VLESS;
- preserved client count: 2;
- TLS enabled;
- SNI: `escloud.us`;
- ALPN: `http/1.1`;
- fallback: `127.0.0.1:8080`;
- fallback Proxy Protocol version: `xver=1`.

## Rendered Hysteria2 contract

Current Hysteria2 config at `/etc/hysteria/config.yaml` was rendered from preserved state using the legacy `vpnctl` contract.

Verified non-secret contract:

- listen: `:443/udp`;
- TLS certificate/key copies under `/etc/hysteria/tls`;
- `sniGuard: strict`;
- authentication type: `userpass`;
- masquerade type: file;
- masquerade webroot: `/var/www/escloud.us/public`;
- `rewriteLocation: true`.

The intermediate printed value `HYSTERIA_USER_COUNT=4` came from an over-broad textual YAML counter and is not authoritative for the actual auth user count. Credential continuity was already proven against the preserved CSV state before rendering. Future acceptance must use a section-aware/parsed count rather than that diagnostic value.

## File ownership / permissions

Accepted state:

- credential-bearing VPN state files: root-owned, mode `0600`;
- preserved `vpnctl`: root-owned, executable mode `0755`;
- `/etc/xray/config.json`: `root:xray`, mode `0640`;
- `/etc/hysteria/config.yaml`: `root:hysteria`, mode `0640`.

## Service boundary at acceptance

- Xray service: disabled, inactive;
- Hysteria2 service: disabled, inactive;
- TCP/443: free;
- UDP/443: free.

No public VPN listener was activated by this subphase.

## Next accepted-first activity

Start and enable Xray/Hysteria2, verify listener ownership and service stability, verify public TLS/HTTPS fallback through Xray, perform a local Hysteria2 client handshake using preserved credentials without printing them, then add and test the Certbot deploy-hook/certificate-sync lifecycle.
