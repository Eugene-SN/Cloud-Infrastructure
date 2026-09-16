# Edge Stage 1 Cert Sync Lifecycle Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_CERT_SYNC_LIFECYCLE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted certificate synchronization state

- synchronization script installed at `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- Certbot deploy hook installed at `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- hook target resolves to `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- active Let’s Encrypt lineage remains `/etc/letsencrypt/live/escloud.us`;
- Xray receives certificate/key copies under `/etc/xray/tls`;
- Hysteria2 receives certificate/key copies under `/etc/hysteria/tls`;
- Xray certificate/key copy integrity matched the active Let’s Encrypt lineage;
- Hysteria2 certificate/key copy integrity matched the active Let’s Encrypt lineage;
- accepted permissions: Xray fullchain `root:root 0644`, Xray private key `root:ssl-cert 0640`, Hysteria fullchain `root:hysteria 0644`, Hysteria private key `root:hysteria 0640`.

## Hook behavior

The preserved lifecycle was retained but corrected so service refresh failures are not suppressed.

Direct hook execution:

- copied current certificate/key material successfully;
- restarted Xray successfully;
- restarted Hysteria2 successfully;
- both services remained active.

Certbot integration test:

- `certbot renew --cert-name escloud.us --dry-run --run-deploy-hooks`: PASS;
- Certbot executed the deploy hook successfully;
- both VPN service PIDs changed, proving hook execution/restart;
- production active certificate remained unchanged by the staging dry-run;
- post-dry-run certificate copies still matched the active production lineage.

## Functional post-hook verification

After direct and Certbot-triggered hook execution:

- Xray TLS verification: PASS;
- Xray HTTPS fallback through nginx: PASS;
- Hysteria2 authenticated handshake using preserved credentials: PASS;
- HTTPS through Hysteria2 proxy path returned HTTP 200;
- temporary client artifacts were removed.

## Service / renewal state

- Xray: active, enabled, `NRestarts=0`;
- Hysteria2: active, enabled, `NRestarts=0`;
- Certbot timer: active and enabled;
- nginx: active;
- SSH socket: active;
- system state: `running`;
- failed systemd units: 0.

## Next Stage 1 work

The nginx/TLS/Xray/Hysteria2 public-edge foundation and certificate-renewal lifecycle are accepted. Remaining Stage 1 work still includes the plausible public/decoy page decision, Authelia web-auth foundation, firewall/minimal public policy decision, normalized persistent layout/ownership where still unresolved, initial private Cloud Infrastructure page boundary, basic backup of the rebuilt base state, and final Stage 1 composition/non-regression acceptance.
