# 05.2 — Obsidian Runtime Packaging Gate Acceptance

**Date:** 2026-09-19  
**Status:** ACCEPTED  
**Project:** Cloud Infrastructure  
**Primary repository:** `Eugene-SN/Cloud-Infrastructure`

`STAGE05_2_RUNTIME_PACKAGING_GATE=PASS`

## Context

Stage 05.1 accepted the PVE placement of the single full server-side Obsidian runtime but left the deployment mechanism open between native official Obsidian + native Selkies and LinuxServer Obsidian/Selkies inside the dedicated LXC.

The Stage 05.2 targeted pre-mutation audit passed and confirmed:

- PVE manager `9.2.20`, kernel `7.0.14-16-pve`;
- approximately 15 GiB RAM total with approximately 6.5 GiB available;
- 8 GiB host swap with approximately 5.6 GiB free;
- local Debian 13 amd64 LXC template already available;
- cgroup v2, overlay and AppArmor available for Docker-in-LXC;
- canonical vault on the dedicated `pve/knowledge` ext4 LV at `/srv/knowledge/obsidian`;
- current vault ownership `root:knowledge-sync`, GID 990, mode 2775;
- PVE Syncthing runtime active under `knowledge-sync`;
- private `.lan` DNS and current Home nginx ingress are available;
- `obsidian.lan` does not yet exist.

## Accepted deployment method

**LinuxServer Obsidian/Selkies inside the dedicated PVE LXC is selected.**

Rationale:

- integrated Selkies browser/session lifecycle;
- LinuxServer-provided application packaging and process supervision;
- one container image lifecycle for Obsidian + browser streaming stack;
- normal update path is image pull + container recreation while persistent state remains outside the image;
- avoids custom native Obsidian + Selkies systemd/display/session glue;
- aligns with the project's preference for lower operational complexity and stable upstream-supported update paths.

The native Obsidian + native Selkies alternative is not selected unless a concrete incompatibility with the LinuxServer implementation is later demonstrated.

## Accepted LXC envelope

| Resource | Accepted target |
|---|---:|
| CPU | 1 vCPU |
| RAM | 1024 MiB |
| LXC swap | 512 MiB |
| rootfs | 8 GiB |
| onboot | enabled |

The earlier approximately 4 GiB rootfs planning value is superseded. The 8 GiB value provides reasonable space for Debian, Docker/containerd, the LinuxServer image/layers and persistent application state without placing the canonical vault inside rootfs.

PVE host swap remains 8 GiB and is not expanded without measured pressure.

## Data boundary

The canonical vault remains at:

`/srv/knowledge/obsidian`

It remains backed by the dedicated PVE Knowledge LV and will be mounted RW into the Obsidian LXC. Canonical Knowledge data must not be copied into or made dependent on the LXC rootfs.

## Scope boundary

This acceptance resolves only the 05.2 runtime packaging and rootfs sizing gate. It does not itself create the LXC, mutate the vault, configure `obsidian.lan`, redesign ai-node/OpenClaw, deploy edge replication, or implement external client access.

## Acceptance marker

`STAGE05_2_RUNTIME_PACKAGING_GATE=PASS`
