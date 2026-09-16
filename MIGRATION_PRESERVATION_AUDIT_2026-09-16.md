# Cloud Infrastructure — Migration Preservation Audit — 2026-09-16

**Status:** factual runtime audit for Stage 0 preservation planning  
**Source host:** `nl-core-vds`  
**Target context:** possible clean deployment of future `edge`

This document records only non-secret preservation facts. Secret values, private keys and credential-bearing archives must not be committed to GitHub.

## Recovery context

- User initiated a provider-level VPS backup before destructive migration work.
- Runtime audit completed without mutations and all audited services remained active afterwards.
- Local migration archive is intended as a second, portable preservation layer independent of the provider backup.

## High-priority state

### Stalwart + Bulwark

Compose:

- `/srv/ai-workspace/apps/mail-stack/docker-compose.yml`
- SHA256 `890948be5dd8c6b1bf9f76b7f05979646e767936cea34466387e24eaeb1f07c9`

Stalwart mounts:

- `/srv/ai-workspace/data/mail/stalwart/etc` → `/etc/stalwart` RW
- `/srv/ai-workspace/data/mail/stalwart/certs` → `/etc/stalwart-certs` RO
- `/srv/ai-workspace/data/mail/stalwart/lib` → `/var/lib/stalwart` RW

Observed Stalwart state:

- persistent mail tree ≈107 MiB;
- `etc/config.json` is only 102 bytes;
- the substantive mail/database state is in `/srv/ai-workspace/data/mail/stalwart/lib`;
- that directory contains a live RocksDB-style store (`CURRENT`, `MANIFEST-*`, `.sst`, `.blob`, WAL/log files);
- container UID/GID ownership is numeric `2000:2000` on the host;
- current Stalwart image digest: `stalwartlabs/stalwart@sha256:93c574e52249c1ebf90061da2c4c0756a7b72abfcc1fec34506a03c2e38b5977`.

Bulwark mounts:

- `/srv/ai-workspace/data/mail/bulwark/admin`
- `/srv/ai-workspace/data/mail/bulwark/admin-state`
- `/srv/ai-workspace/data/mail/bulwark/settings`
- `/srv/ai-workspace/data/mail/bulwark/telemetry`

Bulwark includes a credential-bearing session secret at:

- `/srv/ai-workspace/data/mail/bulwark/settings/session_secret`

Current Bulwark image digest:

- `ghcr.io/bulwarkmail/webmail@sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`

Mail DNS observed:

- MX `escloud.us` → `10 mail.escloud.us.`
- `mail.escloud.us` A → `45.92.156.17`
- SPF: `v=spf1 ip4:45.92.156.17 -all`
- DMARC: `v=DMARC1; p=none; adkim=s; aspf=s`

### Xray

- binary: `/usr/local/bin/xray`
- audited version: `26.3.27`
- binary SHA256: `8255dd939c34cf966cc91517b6324dd3c8d0bcf49ffac8beca049a38c46845ed`
- service: `/etc/systemd/system/xray.service`
- config: `/etc/xray/config.json`
- TLS: `/etc/xray/tls/fullchain.pem`, `/etc/xray/tls/privkey.pem`
- public role: TCP/443 with fallback to nginx.

### Hysteria2

- binary: `/usr/local/bin/hysteria`
- audited version: `v2.12.2`
- binary SHA256: `6493dfffd55b5883f64c76c63880ecc32988f0c568c9ca9014907877b4d55f94`
- service: `/etc/systemd/system/hysteria-server.service`
- config: `/etc/hysteria/config.yaml`
- config SHA256: `e586a5df2d40b11c3ec6761e8ba17f570b62667e2a5b3441b9e50e3279ef7220`
- TLS: `/etc/hysteria/tls/fullchain.pem`, `/etc/hysteria/tls/privkey.pem`
- public role: UDP/443.

### VPN management stack

The convenience command paths are symlinks:

- `/usr/local/bin/maintctl` → `/opt/vpn-stack/scripts/maintctl`
- `/root/maintctl` → `/opt/vpn-stack/scripts/maintctl`
- `/usr/local/bin/vpnctl` → `/opt/vpn-stack/scripts/vpnctl`

Actual scripts:

- `/opt/vpn-stack/scripts/maintctl` — 39,627 bytes
- `/opt/vpn-stack/scripts/vpnctl` — 23,401 bytes

`maintctl` references state/config under the complete `/opt/vpn-stack` tree, including:

- `/opt/vpn-stack/conf/hysteria2_primary.txt`
- `/opt/vpn-stack/conf/xray_primary_uuid.txt`
- `/opt/vpn-stack/state/hysteria2/users.csv`
- `/opt/vpn-stack/state/xray/users.csv`

It also references:

- Xray/Hysteria configs and TLS copies;
- `/etc/letsencrypt` and renewal hooks;
- nginx;
- SSH configuration;
- Xray/Hysteria systemd units;
- `/usr/local/bin/xray-cert-sync.sh`;
- `/var/backups/vpn-stack/...` historical update backups.

Therefore preservation scope is the complete `/opt/vpn-stack`, not only the `maintctl` file.

## Shared ingress/TLS state

Preserve for migration/reference:

- `/etc/nginx/`
- `/etc/letsencrypt/`

Current certificate `escloud.us` covers:

- `escloud.us`
- `app.escloud.us`
- `auth.escloud.us`
- `chat.escloud.us`
- `cloud.escloud.us`
- `code.escloud.us`
- `docs.escloud.us`
- `go.escloud.us`
- `mail.escloud.us`
- `sync.escloud.us`

The Xray, Hysteria and Stalwart certificate copies all matched the same audited certificate fingerprint.

## Other accepted-service state to preserve

### n8n

- `/srv/ai-workspace/data/n8n/`
- live SQLite state includes `database.sqlite`, `database.sqlite-wal`, `database.sqlite-shm`;
- therefore preservation should be taken while n8n is quiesced/stopped.

### Authelia

Preserve full `/srv/ai-workspace/data/authelia/`, including:

- config;
- users database;
- SQLite state;
- credential files `jwt_secret`, `session_secret`, `storage_encryption_key`.

Secret values must stay outside GitHub.

### CloudCLI

Preserve:

- `/home/core/.cloudcli/`
- credential/state database `/home/core/.cloudcli/auth.db`

Current `auth.db` SHA256:

- `7dd8e5c9cdce1261b112567bd48b713f7dd4ca940cd9b1bd34831bf7776590b0`

### Codex CLI

Preserve current `/home/core/.codex/` for migration/reference, especially:

- `auth.json`;
- `config.toml`;
- session state;
- SQLite state where useful.

The current tree is ≈484 MiB and includes transient app-server socket/lock files; transient UNIX sockets should not be treated as restore state.

Current legacy `codex-runner` implementation and token are reference-only unless explicitly reselected later.

### Antigravity CLI

No Antigravity CLI binary or state was present during this audit. It will be installed/configured fresh if retained in target implementation.

## Preservation categories

### RESTORE / MIGRATE

- complete Stalwart/Bulwark persistent mail state and credential material;
- complete Xray/Hysteria configs and TLS material;
- complete `/opt/vpn-stack` including `maintctl`/`vpnctl` and state;
- nginx/Certbot configuration required to reconstruct ingress and certificate handling;
- n8n complete persistent state;
- Authelia complete config/database/secrets;
- CloudCLI auth/state;
- Codex CLI auth/config/useful user state;
- selected SSH credential/config state as migration recovery material.

### REFERENCE

- current core-stack Compose layout;
- current systemd unit definitions;
- UFW/Fail2Ban/network/sysctl configuration;
- legacy Codex runner/app-server topology where not selected for target state;
- current package/image/version inventory.

### RECREATE

By default install current stable versions fresh rather than restoring executable binaries:

- Ubuntu/packages;
- Docker/Compose;
- Xray/Hysteria binaries;
- nginx/Certbot;
- CloudCLI/Codex binaries;
- Docker images/networks.

## Consistency requirement

Do not archive the live Stalwart RocksDB, n8n SQLite+WAL, Authelia SQLite, CloudCLI DB or Codex SQLite state as an uncontrolled live filesystem copy. For the migration archive, temporarily quiesce relevant services, copy state, restore services, verify health, then compress the staged copy.

## Migration archive creation

A consistency-preserving archive was created on `nl-core-vds` after temporarily quiescing Stalwart/Bulwark, n8n, Authelia, CloudCLI and Codex app-server/runner state. Xray, Hysteria2, nginx and SSH remained available during preservation.

Server-side archive result:

- archive: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`
- checksum file: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz.sha256`
- archive size: `233857366` bytes
- archive SHA256: `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`
- archive mode: `0600`
- internal staged-file SHA256 manifest created;
- gzip integrity test: PASS;
- tar listing/readability test: PASS;
- post-copy service resume gate: PASS;
- Xray/Hysteria2/nginx remained active.

The archive contains credentials/private keys and is sensitive recovery material. It must remain outside GitHub.

## 2026-09-16T17:11:00+03:00 — Server-side preservation acceptance

**Status:** PASS

Post-archive recovery verification confirmed:

- archive SHA256 matched the expected value;
- gzip and tar readability passed;
- all key preservation objects were present in the archive;
- Stalwart container running and healthy;
- Bulwark container running;
- n8n container running and healthy, `/healthz` returned `{"status":"ok"}`;
- Authelia container running and healthy;
- Xray, Hysteria2, nginx, CloudCLI, Codex app-server and Codex runner services active;
- TCP listeners for SMTP/HTTP/HTTPS/IMAPS and application backends present;
- Hysteria2 confirmed as the process owning UDP/443 (`MainPID=1179` at verification time);
- nginx configuration test passed and public stub returned HTTP 200;
- Stalwart SMTP returned `220 mail.escloud.us Stalwart ESMTP at your service`;
- Stalwart HTTP backend returned 302 and Bulwark HTTP backend returned 307.

`SERVER_SIDE_PRESERVATION_ACCEPTANCE=PASS`.

The earlier UDP/443 failure in `EDGE_POST_ARCHIVE_ACCEPTANCE_V1` was a diagnostic-block defect: it inspected the wrong `ss` field for the UDP local endpoint. No runtime failure was present; the corrected recovery check confirmed Hysteria2 UDP/443 ownership.

Outstanding before destructive rebuild acceptance:

1. download archive and `.sha256` to an external trusted device and independently verify the downloaded archive SHA256 equals `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
2. confirm provider-level VPS backup completed successfully.

No migration/rebuild decision is implied by this audit alone.