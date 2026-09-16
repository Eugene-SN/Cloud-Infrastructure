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

This accepts only the **minimal architecture-independent bootstrap subset** inside Stage 1 / branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

It does **not** complete Base Platform Deployment and it does **not** complete Stage 1.

Canonical chronology clarification (superseding any earlier interpretation of this acceptance as a branch-transition point):

- remain in branch `01`;
- perform Stage 1 requirements review;
- discuss/select unresolved Stage 1 services/mechanisms;
- accept the Stage 1 composition and scoped deployment contract;
- deploy/verify the remaining Base Platform scope;
- explicitly accept Stage 1;
- only then open `02 — Edge Core Applications`.

See `DECISIONS.md`, `IMPLEMENTATION_PHASES.md` and `CURRENT_STATE.md` for the current authoritative workflow.
