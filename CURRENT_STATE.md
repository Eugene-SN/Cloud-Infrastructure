# Cloud Infrastructure — Current State

## Snapshot status

**Project stage:** clean `edge` substrate and minimal host-level base bootstrap accepted; target-service composition / architecture work continues before service deployment.

**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

**Runtime mutation status:** provider-level clean rebuild and minimal architecture-independent host bootstrap completed and accepted. No target application/service stack has been restored or deployed yet.

## Historical baseline

The canonical as-is source for the pre-reinstall legacy VPS remains:

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`

Baseline SHA256 imported for project initialization:

`5bb56c10723c2f6e950d9d4a28bbd76989870da6e01d221429417cf806139368`

The baseline records the historical host as `nl-core-vds`. Historical names and paths in that artifact remain unchanged. It is not the desired-state architecture and no longer describes the live OS after the 2026-09-16 rebuild.

## Stage 0 preservation / recovery state

**Status:** PASS / complete.

Confirmed preservation layers:

- provider-level full VPS backup completed successfully;
- external credential-bearing migration archive downloaded and independently verified;
- archive SHA256: `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
- server-side post-copy application acceptance passed;
- `STAGE0_PRESERVATION_ACCEPTANCE=PASS`.

The sensitive archive remains outside GitHub and is the authoritative portable selective-recovery source. The provider backup remains the whole-VPS rollback path.

## Migration engineering reference

The sanitized engineering reference remains accepted at:

`migration-reference/`

Canonical acceptance record:

`MIGRATION_REFERENCE_ACCEPTANCE_2026-09-16.md`

The reference is for understanding/adapting legacy implementation logic only. It is not an authoritative restore bundle.

## Clean `edge` substrate acceptance — 2026-09-16

**Status:** PASS.

The existing GreenCloud KVM VPS was rebuilt from the provider panel as a clean Ubuntu instance and is now the live logical node `edge`.

Accepted runtime facts after controlled reboot:

- hostname/FQDN: `edge.escloud.us`;
- short hostname: `edge`;
- OS: Ubuntu 26.04.1 LTS;
- architecture: `x86_64`;
- virtualization: KVM;
- kernel: `7.0.0-31-generic`;
- vCPU: 2;
- RAM: ~15 GiB;
- swap: 4 GiB `/swap.img`;
- root filesystem: ext4 on `/dev/vda1`, ~155 GiB filesystem class;
- IPv4: `45.92.156.17/24`, default gateway `45.92.156.1`;
- IPv6: `2a0c:b847:ffff:283::a/64`, default gateway `2a0c:b847:ffff::1`;
- DNS resolution: PASS;
- NTP synchronization: PASS;
- SSH key authentication: PASS using the selected Termius ED25519 key;
- effective SSH auth: root key login allowed, password and keyboard-interactive authentication disabled;
- OpenSSH is socket-activated through `ssh.socket`;
- system state after reboot: `running`;
- failed systemd units: 0;
- current-boot error journal: empty;
- reboot-required state: absent.

### GRUB first-boot anomaly

The initial provider provisioning boot briefly produced `grub-initrd-fallback.service` failure with `invalid environment block` while GreenCloud provisioning was upgrading `grub2-common` from `2.14-2ubuntu2` to `2.14-2ubuntu2.1` in the same boot.

Root-cause evidence showed:

- package upgrade occurred during first-boot provider provisioning;
- current `grub2-common` is `2.14-2ubuntu2.1`;
- current unit ordering references `grub2-common.service` correctly;
- `/boot/grub/grubenv` is valid;
- after controlled reboot, `grub2-common.service` and `grub-initrd-fallback.service` both completed with `result=success`;
- no `invalid environment block` appeared in the accepted boot.

Therefore this was accepted as a transient first-boot provisioning race, not an active boot defect.

### Provider cloud-init warnings

GreenCloud NoCloud seed completed with `errors: []`, but schema validation reports provider-template warnings/deprecations:

- deprecated `users.0.ssh-authorized-keys` key;
- swap size encoded as a floating-point value in provider user-data;
- deprecated netplan `gateway4` / `gateway6` syntax.

These are non-blocking provider-template issues. Effective runtime state for SSH key installation, swap and IPv4/IPv6 networking is correct. Do not mutate working configuration merely to silence these warnings unless a later accepted configuration-normalization step requires it.

## Minimal base bootstrap acceptance — 2026-09-16

**Status:** PASS.

`EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`.

Architecture-independent host bootstrap was intentionally kept minimal. Accepted changes and verified state:

- package metadata refreshed successfully;
- `dpkg --audit` clean;
- no APT holds;
- Ubuntu phased updates were not forced; six phased updates remained deferred at acceptance;
- `unzip 6.0-29ubuntu1` installed as the only additional base utility;
- journald persistent-use ceiling configured via `/etc/systemd/journald.conf.d/90-edge-retention.conf` with `SystemMaxUse=500M`;
- journald active and healthy;
- timezone intentionally retained as `Europe/Moscow`; NTP synchronized;
- working provider-generated Netplan left unchanged;
- SSH configuration left unchanged; key-only root access and `ssh.socket` remain accepted;
- QEMU guest agent present and active;
- cloud-init provider warnings left unchanged as previously classified non-blocking;
- `/tmp` is tmpfs with mode `1777`;
- system state `running`, failed units 0, current-boot error journal empty after bootstrap;
- IPv4/IPv6 and SSH non-regression gates passed.

Not installed merely for convenience: `zip`, `tree`, `socat`, `pip3`. Install such tools only when a concrete consumer requires them. `pollinate` was not autoremove-cleaned solely because APT marked it unused.

## Accepted target-service direction

Accepted without further replacement search unless a concrete incompatibility emerges:

- Xray
- Hysteria2
- nginx
- n8n
- CloudCLI
- Stalwart
- Bulwark
- Authelia
- Codex CLI
- Antigravity CLI

Additional accepted directions remain:

- Backrest using Restic for future backup management;
- dedicated Cloud Infrastructure portal replacing Homepage;
- maintenance page + Semaphore replacing the legacy custom Maintenance Center.

## Open service / architecture decisions

Still unresolved and not authorized for deployment merely because the clean OS exists:

- final file/storage access implementation;
- synchronization model and Obsidian role;
- final ingress/domain composition;
- private/site-to-site connectivity;
- runtime/container topology;
- final storage layout;
- monitoring/notification scope;
- off-site DR topology;
- Codex persistent-service topology / custom runner decisions;
- remaining deferred capability decisions recorded in `DECISIONS.md`.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.

## Current deployment boundary

`EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`.

`EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`.

The clean Ubuntu substrate and minimal architecture-independent host bootstrap are accepted. Further target-service restoration/deployment remains gated by the applicable accepted service-composition, architecture and implementation decisions.