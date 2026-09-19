# Stage 05.2 — PVE Canonical Obsidian Runtime & WebUI — Final Acceptance

**Date:** 2026-09-19  
**Status:** COMPLETE / ACCEPTED  
**Acceptance marker:** `STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS`

## Scope

Stage 05.2 deployed the accepted server-side Obsidian-aware runtime on the PVE canonical Knowledge node without moving canonical data into the application LXC or changing the accepted PVE ↔ ai-node / future PVE ↔ edge data topology.

## Production runtime

### CT210 `obsidian`

- fresh dedicated PVE LXC;
- hostname: `obsidian`;
- 1 vCPU;
- 512 MiB RAM;
- 256 MiB swap;
- 8 GiB rootfs on `local-lvm`;
- onboot enabled;
- static IPv4 `192.168.1.15/24`;
- gateway `192.168.1.254`;
- DNS `192.168.1.1`;
- search domain `lan`;
- canonical vault bind: PVE `/srv/knowledge/obsidian` -> CT210 `/srv/knowledge/obsidian` RW.

### Application stack

- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- Ignis upstream image update path: `nobbe/ignis:latest`;
- accepted deployed Ignis release: `0.8.11`;
- supported Obsidian version: `1.12.7`;
- `obsidian-headless` `0.0.14`;
- Caddy private reverse proxy / TLS;
- Ignis backend published only on CT loopback `127.0.0.1:8080`.

## Canonical vault ownership correction

The initial direct bind of the canonical vault under Ignis `/vaults` exposed Ignis entrypoint behavior that recursively executes ownership normalization on `/vaults`. This changed the canonical root ownership from the accepted PVE contract `0:990:2775` to `999:990:2775`.

The production correction did **not** patch or fork Ignis.

Accepted topology:

- CT210 canonical target: `/srv/knowledge/obsidian`;
- host-side Ignis vault directory: `/opt/obsidian/vaults`;
- symlink: `/opt/obsidian/vaults/obsidian -> /srv/knowledge/obsidian`;
- Ignis mounts `/opt/obsidian/vaults:/vaults`;
- Ignis separately mounts `/srv/knowledge/obsidian:/srv/knowledge/obsidian`.

This follows the upstream-supported symlinked-vault model and prevents recursive `chown -R /vaults` from traversing the canonical target.

Verified after startup and explicit Ignis restart:

- canonical root: `0:990:2775`;
- descendant ownership preserved;
- Ignis still discovers vault `obsidian`;
- upstream image remains unpatched and remains the normal update unit.

Marker:

`STAGE05_2_IGNIS_CANONICAL_OWNERSHIP_CORRECTION=PASS`

## Private DNS and TLS

Accepted private endpoint:

`https://obsidian.lan`

MikroTik static DNS:

`obsidian.lan -> 192.168.1.15`

Verified:

- system resolver -> `192.168.1.15`;
- direct MikroTik DNS -> `192.168.1.15`;
- HTTP redirects to HTTPS;
- TLS SAN contains `DNS:obsidian.lan`;
- HTTPS verifies against the Caddy internal root CA.

Production Caddy root CA:

- subject/issuer: `Caddy Local Authority - 2026 ECC Root`;
- valid from 2026-09-19 through 2036-07-28;
- SHA256 fingerprint:
  `B0:C6:CC:50:4D:B2:20:AE:08:09:21:99:9C:95:D5:6D:DB:D0:D4:50:CD:4E:8D:8A:D4:D0:B6:D3:6E:44:93:4A`.

macOS System Keychain trust was installed and verified. Browser access works without a certificate warning.

## Browser/runtime functional acceptance

Accepted browser behavior:

- Ignis UI loads over `https://obsidian.lan`;
- canonical vault `obsidian` opens normally;
- note creation and editing work;
- note deletion works;
- canonical RW operations are reflected through the server API and filesystem.

Ignis compatibility requirement:

- Obsidian `Use native menus` / system context menu must remain **OFF**;
- with this option enabled, Electron-native menu codepaths prevent browser context menus from opening;
- disabling it restores right-click and `...` menu behavior.

## File Recovery

`.obsidian/core-plugins.json` confirms:

`"file-recovery": true`

Production status:

- File Recovery is enabled/configured;
- the earlier runtime-selection experiment established the File Recovery baseline;
- production final acceptance intentionally did not repeat a destructive UI restore E2E.

This is recorded as:

`FILE_RECOVERY=CONFIGURED_NOT_E2E_RESTORE_TESTED`

## Reboot and persistence acceptance

A controlled CT210 reboot passed:

- CT210 returned running;
- Docker stack autostarted;
- `obsidian-ignis` returned running;
- `obsidian-caddy` returned running;
- `obsidian.lan` DNS remained correct;
- HTTPS recovered;
- canonical root remained `0:990:2775`.

Markers:

- `REBOOT_AUTOSTART=PASS`
- `CANONICAL_OWNERSHIP_POST_REBOOT=PASS`
- `DNS_TLS_CA=PASS_REUSED`

## Resource acceptance

Post-reboot measured state:

- LXC memory: 512 MiB total, 106 MiB used, ~405 MiB available;
- LXC swap: 256 MiB total, 0 used;
- Caddy container memory: ~51.84 MiB;
- Ignis container memory: ~89.8 MiB;
- both measured at idle immediately after recovery.

No resource-envelope increase is justified by current evidence.

## Final accepted state

- PVE remains canonical Knowledge authority;
- CT210 is the single accepted server-side Obsidian-aware runtime;
- canonical vault remains ordinary PVE filesystem data outside LXC rootfs;
- Ignis remains the normal upstream update unit;
- private `obsidian.lan` WebUI is live;
- browser create/edit/delete is functional;
- File Recovery is enabled/configured;
- canonical ownership survives Ignis restart and full LXC reboot;
- Stage 05.2 performs no redesign of ai-node, CT220/OpenClaw, CT208 backup policy, edge replication or external client access.

`STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS`

## Next stage

Stage 05.3 — Edge Knowledge Replication & Data Integration.
