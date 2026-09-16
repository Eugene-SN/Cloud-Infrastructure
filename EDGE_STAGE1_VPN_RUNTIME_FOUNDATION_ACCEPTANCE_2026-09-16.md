# Edge Stage 1 VPN Runtime Foundation Acceptance — 2026-09-16

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_VPN_RUNTIME_FOUNDATION_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted runtime state

### Xray

- stable release resolved at deployment time: `v26.3.27`;
- binary: `/usr/local/bin/xray`;
- release asset SHA256 verified against upstream metadata: `23cd9af937744d97776ee35ecad4972cf4b2109d1e0fe6be9930467608f7c8ae`;
- current CLI contract verified: config flag `-c`;
- service identity: `xray` with supplemental `ssl-cert` group;
- systemd unit: `/etc/systemd/system/xray.service`;
- unit validated by `systemd-analyze verify`;
- unit state at acceptance: loaded, disabled, inactive;
- Xray TLS copies exist at `/etc/xray/tls/` and are byte-identical to the current Let's Encrypt source certificate/key;
- actual private-key access as user `xray` verified by OpenSSL.

### Hysteria2

- stable release resolved at deployment time: `app/v2.12.3` / runtime version `v2.12.3`;
- binary: `/usr/local/bin/hysteria`;
- release asset SHA256 verified against upstream metadata: `8c7a68a906998b747a0db87586e364f995fbfddb95693ae6e2fdb68a6e920d3e`;
- current CLI contract verified: config flag `--config`;
- service identity: `hysteria`;
- systemd unit: `/etc/systemd/system/hysteria-server.service`;
- unit validated by `systemd-analyze verify`;
- unit state at acceptance: loaded, disabled, inactive;
- Hysteria2 TLS copies exist at `/etc/hysteria/tls/` and are byte-identical to the current Let's Encrypt source certificate/key;
- actual private-key access as user `hysteria` verified by OpenSSL.

## Credential continuity boundary

No new VPN credentials or service configs were generated during this foundation deployment:

- `/etc/xray/config.json`: absent;
- `/etc/hysteria/config.yaml`: absent;
- Xray UUIDs were not generated;
- Hysteria2 passwords were not generated;
- neither VPN service was started or enabled;
- TCP/443 remained free;
- UDP/443 remained free.

This deliberately preserves existing client-profile continuity until the credential-bearing VPN state is restored from the external sensitive migration archive.

## Recovery incident note

Two intermediate deployment blocks stopped before unit installation because diagnostic checks incorrectly treated CLI/help behavior or path tests as hard failures. Recovery audits proved:

- the Xray private key was actually readable and valid for the `xray` identity;
- no permissions mutation was required;
- `xray run -help` returning non-zero was a diagnostic-script issue, not a runtime incompatibility;
- current Xray CLI usage is `xray run -c <config>`;
- no unintended configs/services/listeners were created by the failed intermediate blocks.

Final recovery continuation passed all required gates.

## Non-regression

- system state: `running`;
- failed systemd units: 0;
- nginx remained active;
- SSH socket remained active;
- TCP/443 free;
- UDP/443 free.

Warnings emitted by `systemd-analyze verify` about removed `CPUAccounting=` support came from Ubuntu's unrelated XFS system units and are not defects in the Xray/Hysteria2 units.

## Next accepted-first activity

Restore the credential-bearing legacy VPN state from the sensitive migration archive without regenerating UUID/password values. Then render current Xray/Hysteria2 configs from the preserved state/contract, validate them with the current binaries, start/enable the services, and verify public TCP/443 fallback and UDP/443 masquerade behavior.
