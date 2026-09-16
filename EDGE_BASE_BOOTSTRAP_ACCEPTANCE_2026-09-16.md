# Cloud Infrastructure — `edge` Minimal Base Bootstrap Acceptance — 2026-09-16

**Status:** ACCEPTED  
**Acceptance:** `EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`

## Scope

Architecture-independent host bootstrap only. No Docker, firewall policy, ingress, VPN/proxy, mail, application runtime, private backbone or target-service deployment was included.

## Accepted changes

- Refreshed Ubuntu APT metadata.
- Installed `unzip 6.0-29ubuntu1` as the only additional base utility.
- Added `/etc/systemd/journald.conf.d/90-edge-retention.conf`:

```ini
[Journal]
SystemMaxUse=500M
```

- Restarted `systemd-journald` to apply the retention ceiling.

## Verified unchanged / retained state

- timezone: `Europe/Moscow`;
- NTP synchronized;
- provider-generated Netplan unchanged;
- IPv4 `45.92.156.17/24` retained;
- IPv6 `2a0c:b847:ffff:283::a/64` retained;
- SSH configuration unchanged;
- `ssh.socket` active;
- root SSH remains key-only (`PermitRootLogin prohibit-password`, password and keyboard-interactive authentication disabled);
- GreenCloud cloud-init warnings remain untouched and non-blocking;
- QEMU guest agent remains present and active.

## Package/update state

- `dpkg --audit`: clean;
- APT holds: none;
- six Ubuntu updates remained deferred by normal phased-update policy;
- phasing was not bypassed or forced;
- `pollinate` was reported auto-removable but was deliberately not removed solely for cleanup;
- `zip`, `tree`, `socat`, and `pip3` were not installed without a concrete consumer.

## Acceptance verification

After mutation:

- `systemctl is-system-running`: `running`;
- failed units: `0`;
- current-boot error journal: empty;
- journald active;
- journald disk use ~8 MiB;
- effective `SystemMaxUse=500M` confirmed;
- `unzip` installed and executable;
- IPv4 gate: PASS;
- IPv6 gate: PASS;
- SSH socket gate: PASS.

## Deployment boundary

This completes the clean-host bootstrap stage. It does not authorize target-service deployment. The project returns to unresolved functional/service-composition work and, only after that is accepted, topology / Architecture Contract design.