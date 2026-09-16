# Cloud Infrastructure — `edge` Pre-Reinstall Contract — 2026-09-16

**Status:** PROPOSED — READY FOR EXPLICIT ACCEPTANCE  
**Scope:** destructive reset of the existing GreenCloud KVM VPS to a clean Ubuntu substrate only  
**Runtime service deployment:** explicitly out of scope until later architecture/deployment decisions

## 1. Purpose

This contract defines the exact destructive boundary, provider-panel reinstall choice, recovery paths, first-boot acceptance criteria and stop conditions for converting the legacy `nl-core-vds` runtime into the clean base OS for future logical node `edge`.

Acceptance of this contract authorizes only:

1. provider-level OS reinstall of the existing VPS;
2. first-boot/base-OS validation;
3. minimal administrative bootstrap required to obtain reliable SSH access and set the target hostname `edge`.

It does **not** authorize deployment or restoration of Xray, Hysteria2, nginx, Stalwart/Bulwark, n8n, Authelia, CloudCLI, Codex, Backrest, Docker application stacks or any other target service.

This is a narrow exception to the earlier project runtime-mutation gate: clean substrate reset may occur before the final Architecture Contract because Stage 0 preservation is complete and no target architecture is being instantiated by this operation. The architecture gate remains in force for service deployment and topology changes after base-OS acceptance.

## 2. Preconditions already satisfied

Stage 0 preservation/recovery:

- provider-level full VPS backup: confirmed complete;
- external credential-bearing migration archive: downloaded and independently verified;
- archive SHA256: `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
- server-side post-copy service acceptance: PASS;
- `STAGE0_PRESERVATION_ACCEPTANCE=PASS`;
- sanitized GitHub engineering reference accepted at `migration-reference/`.

The external archive remains authoritative portable recovery material. `migration-reference/` is engineering context only and must not be treated as a restore bundle.

## 3. Provider and reinstall mechanism

Provider: **GreenCloud**.  
Virtualization: **KVM**.  
Management plane documented by GreenCloud for this VPS class: **SolusVM**.

Provider-documented destructive path:

`SolusVM -> select VPS -> Reinstall -> choose OS -> Reinstall`

GreenCloud documents that Reinstall wipes the VPS disk and shows the new root password once. VNC is available from the control panel for console recovery/verification. Rescue Mode is a separate repair mechanism and is **not** the reinstall method.

## 4. Exact reinstall selection

Use the existing VPS instance. Do not create a replacement VPS and do not change plan, datacenter, allocated addresses or storage size as part of this operation.

### Required selection

- action: **Reinstall**;
- OS family: **Ubuntu Linux**;
- release: **Ubuntu 26.04 LTS**;
- preferred template label: **Ubuntu 26.04.1 LTS 64-bit / AMD64**;
- acceptable equivalent provider label: **Ubuntu 26.04 64-bit / x86_64**, provided it is the 26.04 LTS template;
- architecture: **x86_64 / AMD64**;
- installation mode: provider Linux template, not custom ISO;
- partitioning: provider-template default using the existing virtual disk; no manual partition scheme during reinstall;
- generated root password: record the one-time value for bootstrap access.

Do **not** substitute Ubuntu 24.04, an interim Ubuntu release, Debian or another OS without amending and re-accepting this contract.

Ubuntu 26.04.1 LTS is the current upstream point release of the accepted 26.04 LTS line as of 2026-09-16.

## 5. Provider/network invariants before clicking Reinstall

The following are expected identity/allocation invariants of the existing VPS and must not be intentionally changed by reinstall:

- IPv4: `45.92.156.17/24`;
- IPv4 gateway: `45.92.156.1`;
- IPv6: `2a0c:b847:ffff:283::a/64`;
- IPv6 gateway: `2a0c:b847:ffff::1`;
- expected mail PTR/rDNS: `mail.escloud.us`;
- expected virtual disk capacity: approximately `155 GiB` usable root-disk class;
- vCPU: `2`;
- RAM: approximately `15.56 GiB`.

Before the destructive click, use the GreenCloud/SolusVM VM information/network view to confirm that the operation targets the VPS holding IPv4 `45.92.156.17` and that the provider backup remains present/available in the provider account.

If the panel shows a different primary IPv4, different VPS identity, an unexpected disk-size change, or indicates that the confirmed backup is unavailable, stop before Reinstall.

Do not edit public DNS or rDNS merely for the rebuild. The intended rebuild retains the same public IP allocation.

## 6. Important network reconstruction rule

Do **not** copy the historical netplan file blindly onto the fresh system.

The engineering reference contains a legacy MAC match:

`00:17:ad:e1:d8:50`

That value is historical runtime state and may change across provider rebuilds. On fresh Ubuntu, first accept the provider-generated network configuration if it correctly provides the assigned IPv4/IPv6 and routes. Reconstruct network configuration only from the fresh runtime plus the provider allocation facts above.

Likewise, legacy Google DNS resolver settings are reference state, not a precondition for first boot. Initial acceptance requires working name resolution, not a byte-for-byte copy of the old netplan.

## 7. Expected destructive effects

Acceptance explicitly acknowledges that provider Reinstall will erase the current VPS filesystem and therefore remove the currently running legacy services and local state from the live disk.

Expected temporary outage includes at least:

- Xray/Hysteria2 VPN/proxy endpoints;
- nginx/web endpoints;
- mail services;
- n8n/Authelia;
- CloudCLI/Codex services;
- all other workloads on the legacy VPS.

No DNS failover or temporary parallel VPS is part of this contract.

## 8. First-boot/base-OS acceptance boundary

Immediately after provider reinstall, do not restore application state yet.

The fresh substrate is accepted only after verifying at minimum:

1. the VM boots normally;
2. provider VNC works as out-of-band recovery access;
3. SSH access is obtained using the provider bootstrap credential;
4. `/etc/os-release` identifies Ubuntu 26.04 LTS and the system updates cleanly to the current 26.04 point-release/update state;
5. architecture is `x86_64`;
6. hostname is set to `edge`;
7. IPv4 `45.92.156.17` is configured and externally usable;
8. IPv4 default route uses the expected provider gateway/path;
9. IPv6 `2a0c:b847:ffff:283::a/64` and IPv6 default routing are present and usable, unless a fresh provider-side allocation audit proves the provider changed the assignment;
10. DNS resolution works;
11. root filesystem capacity is consistent with the existing approximately 155 GiB virtual disk and is not accidentally left at a materially smaller template size;
12. system clock/NTP is synchronized;
13. SSH key-based administrative access is installed and verified before disabling bootstrap password access;
14. no legacy application/service state has been restored yet.

A changed SSH host key is expected after reinstall. Treat the old client `known_hosts` entry as stale only after the fresh host identity has been verified through the GreenCloud console/VNC or equivalent provider-side console evidence.

## 9. Recovery paths

### Recovery Path A — provider full VPS backup

Purpose: fastest return to the complete pre-reinstall legacy runtime if the clean rebuild is abandoned or the fresh substrate cannot be made reliable.

Action:

1. stop further mutations to the fresh VPS;
2. restore the confirmed provider-level full VPS backup using the restore action exposed for that backup in the GreenCloud account;
3. if the backup object is present but no self-service restore action is exposed, use GreenCloud Technical Support to request restore of that exact provider backup to the same VPS;
4. after restore, verify boot, network, SSH, Xray/Hysteria, nginx, mail and core application health before declaring rollback successful.

The public GreenCloud KVM documentation describes Reinstall/VNC/Rescue but does not document a universal self-service backup-restore UI, so the contract does not invent a panel button that may not exist for this product.

### Recovery Path B — fresh reinstall plus selective external-state recovery

Purpose: reconstruct the future clean deployment without returning wholesale to the legacy runtime.

Authoritative recovery source:

- external archive SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`.

Use the archive only after the relevant target service/layout is explicitly selected. Restore state selectively, not by unpacking the old filesystem over the new OS.

High-value preserved state includes mail data/configuration, Xray/Hysteria configuration and credentials, `/opt/vpn-stack`, nginx/Certbot material, n8n state, Authelia state/secrets, CloudCLI auth/state, Codex auth/config/useful state and selected SSH material.

### Recovery Path C — GreenCloud Rescue Mode

Purpose: repair a fresh OS that exists on disk but has a boot/filesystem/network/SSH problem.

GreenCloud documents a SolusVM Rescue Mode that boots a temporary rescue image and provides temporary SSH credentials. Rescue Mode is not a rollback and does not replace Paths A or B.

## 10. Stop conditions

Stop the reinstall sequence and do not continue with application deployment if any of the following occurs:

- wrong VPS/IP is selected in SolusVM;
- Ubuntu 26.04 LTS is not available as a provider reinstall template;
- provider backup is no longer present/available before the destructive action;
- reinstall unexpectedly changes the primary IPv4 allocation;
- fresh VM cannot be reached through both normal boot and provider console/recovery mechanisms;
- root disk is materially smaller than the expected existing allocation;
- base networking cannot be made reliable without changing provider allocations;
- any recovery artifact fails integrity verification when it is first needed.

## 11. Post-acceptance execution order

After explicit acceptance of this contract:

1. persist the accepted reinstall decision in `DECISIONS.md` and update current-stage wording in `CURRENT_STATE.md` / `OPERATING_RULES.md` so the narrow substrate-reset exception is canonical;
2. perform the GreenCloud/SolusVM pre-click identity/backup check;
3. execute Reinstall with the Ubuntu 26.04 LTS x86_64 template;
4. record the one-time provider root password outside GitHub;
5. verify the fresh host through VNC/SSH;
6. run a read-only fresh-OS acceptance audit;
7. only after that audit passes, apply the minimal administrative bootstrap and verify it;
8. stop at clean `edge` substrate acceptance before any target-service deployment.

## 12. Acceptance effect

Explicit user acceptance of this document means:

- clean Ubuntu reinstall is the selected migration method for the existing VPS;
- the destructive wipe is authorized under the scope above;
- Stage 0 recovery material is accepted as sufficient protection for that wipe;
- the earlier rule requiring the complete Architecture Contract before **any** runtime mutation is superseded only for this clean substrate reset and base-access bootstrap;
- all target-service deployment remains gated by later accepted architecture/implementation decisions.
