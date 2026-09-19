# Stage 05.2 — Runtime Selection Acceptance

**Date:** 2026-09-19  
**Status:** ACCEPTED  
**Scope:** runtime selection only; production Stage 05.2 deployment is not started.

## Accepted production direction

- dedicated PVE CT210 `obsidian`;
- Ignis as the server-side Obsidian-aware runtime;
- production resources: 1 vCPU, 512 MiB RAM, 256 MiB swap, 8 GiB rootfs, onboot;
- canonical vault remains on PVE at `/srv/knowledge/obsidian` and will be bind-mounted RW;
- private `obsidian.lan` only;
- normal update unit is the Ignis image and its upstream-supported Obsidian version.

## Comparative result

LinuxServer Obsidian/Selkies is not selected because its measured packaging footprint and remote-desktop stack are unnecessary for the accepted role. Native official Obsidian + Selkies 2.0.0rc0 is not selected because satisfactory adaptive browser behavior required Selkies-specific compositor/session integration beyond the desired complexity.

Ignis is selected because it provided the required browser UX while keeping the vault as ordinary filesystem data and passed the server-role acceptance on an isolated test vault.

## Verified Ignis gates

- `IGNIS_FILESYSTEM_BRIDGE=PASS`
- `IGNIS_EXTERNAL_CHANGE_VISIBILITY=PASS`
- `IGNIS_FILE_RECOVERY_BASELINE=PASS`
- `IGNIS_HEADLESS_BRIDGE=PASS`
- `IGNIS_RESTART_PERSISTENCE=PASS`
- `CANONICAL_VAULT_ISOLATION=PASS`
- `IGNIS_SERVER_ROLE_ACCEPTANCE=PASS`

The File Recovery gate verifies the enabled core-plugin baseline, not a full UI restore exercise. Syncthing and Restic/Backrest remain separate infrastructure layers and are not part of Ignis runtime acceptance.

## Experimental cleanup

The comparative CT210 was fully destroyed after testing:

- CT210 PVE registration absent;
- experimental rootfs removed;
- LinuxServer/Selkies and Ignis experimental runtime state removed with the LXC;
- canonical vault was never mounted or mutated.

Marker: `STAGE05_2_CT210_EXPERIMENT_FULL_PRUNE=PASS`.

## Production boundary

No experimental image version, container state, rootfs sizing result or test-vault content is a production baseline. Production Stage 05.2 must create CT210 fresh and use the current stable Ignis deployment path.
