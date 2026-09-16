# Cloud Infrastructure — `edge` Pre-Reinstall Contract — 2026-09-16

**Status:** ACCEPTED / EXECUTED  
**Scope:** destructive reset of the existing GreenCloud KVM VPS to a clean Ubuntu substrate only  
**Execution result:** `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`

## 1. Accepted scope

This contract authorized only:

1. provider-level OS reinstall of the existing VPS;
2. first-boot/base-OS validation;
3. minimal administrative bootstrap required for reliable SSH access and target hostname identity.

It did **not** authorize deployment/restoration of Xray, Hysteria2, nginx, Stalwart/Bulwark, n8n, Authelia, CloudCLI, Codex, Backrest, Docker application stacks or other target services.

This narrow substrate-reset exception superseded the earlier absolute runtime-mutation gate only for the clean rebuild and base validation. Architecture-dependent service deployment remains gated by later accepted decisions.

## 2. Recovery prerequisites

Before destructive rebuild, Stage 0 preservation was complete:

- provider-level full VPS backup confirmed complete;
- external credential-bearing migration archive downloaded and independently verified;
- archive SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
- server-side post-copy acceptance PASS;
- `STAGE0_PRESERVATION_ACCEPTANCE=PASS`;
- sanitized GitHub engineering reference accepted at `migration-reference/`.

Recovery model remains:

- whole-VPS rollback through the provider backup;
- selective recovery from the external sensitive archive;
- GreenCloud rescue/console mechanisms for repair of a fresh installation.

`migration-reference/` is engineering context only, not an authoritative restore bundle.

## 3. Reinstall selection actually used

- provider: GreenCloud;
- virtualization: KVM;
- action: provider rebuild/reinstall of the existing VPS;
- name: `edge`;
- OS: Ubuntu 26.04;
- resulting OS: Ubuntu 26.04.1 LTS;
- hostname/FQDN: `edge.escloud.us`;
- short hostname: `edge`;
- architecture: x86_64 / AMD64;
- provider-template installation, not custom ISO;
- provider/default disk layout;
- swap requested: 4 GiB;
- existing Termius ED25519 SSH key selected;
- VNC was not enabled persistently.

No plan/datacenter/IP/storage migration was intentionally performed.

## 4. Accepted live substrate state

Post-rebuild and post-controlled-reboot acceptance confirmed:

- Ubuntu 26.04.1 LTS;
- kernel `7.0.0-31-generic`;
- KVM / `x86_64`;
- 2 vCPU;
- ~15 GiB RAM;
- 4 GiB `/swap.img`;
- root filesystem ext4 on `/dev/vda1`, approximately 155 GiB filesystem class;
- IPv4 `45.92.156.17/24` with default gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64` with default gateway `2a0c:b847:ffff::1`;
- DNS resolution PASS;
- NTP synchronized;
- SSH key login PASS;
- effective SSH policy: `PermitRootLogin prohibit-password`, `PubkeyAuthentication yes`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`;
- socket activation through `ssh.socket` accepted as the normal OpenSSH runtime mode;
- system state `running`;
- failed units 0;
- current-boot error journal empty;
- `REBOOT_REQUIRED=NO` after controlled reboot.

## 5. First-boot GRUB anomaly and resolution

During the provider provisioning boot, `grub-initrd-fallback.service` temporarily failed with:

`invalid environment block`

Forensic audit established that GreenCloud provisioning ran a `dist-upgrade` in that same boot and upgraded:

- `grub-pc` `2.14-2ubuntu2` -> `2.14-2ubuntu2.1`;
- `grub-pc-bin` `2.14-2ubuntu2` -> `2.14-2ubuntu2.1`;
- `grub2-common` `2.14-2ubuntu2` -> `2.14-2ubuntu2.1`.

The replacement systemd unit files were installed while the first boot was still active. `/boot/grub/grubenv` was valid after provisioning.

A controlled reboot then proved:

- kernel `7.0.0-31-generic` loaded;
- `grub2-common.service` result `success`;
- `grub-initrd-fallback.service` result `success`;
- no `invalid environment block` in the accepted boot;
- failed units 0;
- system state `running`.

The anomaly is therefore classified as a transient first-boot provider-provisioning race, not an active GRUB defect. No manual GRUB workaround was applied.

## 6. Provider cloud-init warnings

GreenCloud NoCloud provisioning completed with `errors: []`, but schema validation showed non-blocking provider-template issues:

- deprecated `users.0.ssh-authorized-keys` syntax;
- swap size encoded in provider user-data as a floating-point value;
- deprecated netplan `gateway4` / `gateway6` syntax.

Effective runtime results are correct: SSH key installed, 4 GiB swap active, IPv4/IPv6 networking functional. These warnings are not a reason to rewrite working provider-generated configuration by default.

## 7. Network reconstruction rule

Historical netplan and other networking files in `migration-reference/` remain reference-only. Fresh runtime/configuration has priority. Do not blindly restore historical network files over the accepted provider-generated network configuration.

## 8. Post-acceptance boundary

`EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`.

The clean Ubuntu substrate is accepted and is now the current runtime baseline for `edge`.

Permitted next work is explicitly scoped base bootstrap and continued architecture/service-composition work. Target-service restoration/deployment remains separately gated and must not be inferred from this acceptance.
