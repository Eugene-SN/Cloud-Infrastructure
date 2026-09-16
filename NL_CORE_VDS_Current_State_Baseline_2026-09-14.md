# NL-CORE-VDS — Current State Baseline

**Host:** `nl-core-vds`  
**Baseline date:** 2026-09-14  
**Purpose:** consolidated as-is technical baseline for future architecture review, redesign, migration, simplification and productionization of the VPS.  
**Status:** current VPS is **not yet considered fully production-adopted by the user**. Historically it was configured into a broad baseline state, but active user usage has been limited primarily to VPN connectivity. Therefore, the absence of active workload in a service **must not** be interpreted as evidence that the service is unnecessary, and the presence of a running service **must not** be interpreted as evidence that it belongs in the future architecture.

---

## 0. Baseline scope and interpretation rules

This document consolidates:

1. the original AI Workspace / Core Stack deployment guideline;
2. the later Claude-based expanded VPS audit;
3. the later runtime audit dated 2026-09-07;
4. the maintenance/Git-state notes and simplification constraints;
5. the repeated calibration audits performed on 2026-09-14:
   - `NL_CORE_VDS_CALIBRATION_AUDIT_V1`
   - `NL_CORE_VDS_CALIBRATION_FOLLOWUP_V3`
   - `NL_CORE_VDS_USAGE_AND_DRIFT_CALIBRATION_V4`

This document is intended to be a **state reconstruction**, not a target design.

### Interpretation constraints

- Do **not** infer future necessity from current runtime activity.
- Do **not** infer that a configured but inactive service is obsolete.
- Do **not** infer that a currently active service should remain in the future architecture.
- The VPS has not yet reached steady-state production use.
- Historically, VPN connectivity has been the primary actually used function.
- n8n, Syncthing, Filestash, AI tooling, Maintenance Center and related services were deployed/configured as part of the earlier architecture but were not necessarily exercised in sustained production workflows.
- Future redesign must be based on:
  1. current technical state from this baseline;
  2. new Home Infrastructure / Personal Agents Infrastructure capabilities;
  3. current user scenarios and requirements;
  4. current 2026 software/platform capabilities;
  5. explicit keep / simplify / replace / move / merge / remove decisions made later.

---

# 1. Host platform

## 1.1 Identity

| Field | Value |
|---|---|
| Hostname | `nl-core-vds` |
| FQDN | `nl-core-vds` |
| Virtualization | KVM |
| Hypervisor presentation | QEMU Standard PC i440FX + PIIX |
| Architecture | x86_64 |
| OS | Ubuntu 26.04.1 LTS |
| Codename | `resolute` |
| Kernel | `7.0.0-31-generic` |
| Time zone | `Europe/Moscow` |
| Local offset at audit | UTC+03:00 |
| NTP | active, synchronized |

### Firmware / VM presentation

- QEMU product UUID present.
- UEFI firmware via EDK2.
- RTC kept in UTC.
- Guest agent present and active.

---

## 1.2 CPU and memory

| Resource | Current state |
|---|---|
| vCPU | 2 |
| CPU model | AMD EPYC-Milan Processor |
| Threads/core | 1 |
| Sockets | 2 |
| RAM | ~15.56 GiB |
| Swap | 8 GiB `/swap.img` |

At calibration time:

- ~2.3 GiB RAM used;
- ~13 GiB available;
- swap practically unused;
- system load low.

Representative load snapshot:

- `load average: 0.26, 0.19, 0.18`
- CPU largely idle.

---

## 1.3 Storage

Primary root filesystem:

- device: `/dev/vda1`
- filesystem: ext4
- size: ~155 GiB
- used at audit: ~25 GiB
- free: ~130 GiB
- usage: ~16%

Additional partitions:

- `/boot` on `/dev/vda13`, ext4
- `/boot/efi` on `/dev/vda15`, FAT32

Docker uses the same root filesystem through `overlay2`.

No separate production data disk is present for the VPS workloads.

---

# 2. Local users and privilege boundaries

## 2.1 Users

| User | UID | Role / observed usage |
|---|---:|---|
| `root` | 0 | host administrator, system services, deployment/root-owned components |
| `core` | 1000 | AI Workspace / application service account |
| `eugene` | 1001 | human administrative account with sudo |

### `core`

Groups:

- `core`
- `adm`
- `users`

Important current boundary:

- `core` is **not** in the `docker` group.
- `core` has **no sudo rights**.
- this matches the original security boundary in the initial Core Stack guideline.

### `eugene`

- member of `sudo`;
- unrestricted `(ALL : ALL) ALL` sudo capability.

---

# 3. Network state

## 3.1 Public interfaces

Primary interface:

- `ens3`
- IPv4: `45.92.156.17/24`
- IPv6: `2a0c:b847:ffff:283::a/64`

IPv4 gateway:

- `45.92.156.1`

IPv6 gateway:

- `2a0c:b847:ffff::1`

---

## 3.2 DNS

`systemd-resolved` is active.

Configured uplink resolvers on `ens3`:

- `8.8.8.8`
- `8.8.4.4`
- `2001:4860:4860::8888`
- `2001:4860:4860::8844`

`/etc/resolv.conf` points to:

- `/run/systemd/resolve/stub-resolv.conf`

Local stub:

- `127.0.0.53`

---

## 3.3 Forwarding

Current sysctl observations:

- `net.ipv4.ip_forward = 1`
- `net.ipv6.conf.all.forwarding = 0`

---

## 3.4 NetBird

**NetBird is not installed on the VPS as of this baseline.**

Observed:

- no `netbird` binary;
- no `netbird.service`;
- no private backplane to Home Infrastructure currently exists through NetBird.

This is only an as-is statement. Future architecture decisions are out of scope for this baseline.

---

# 4. Public listening ports

## 4.1 Public

| Protocol | Port | Owner / purpose |
|---|---:|---|
| TCP | 22 | OpenSSH |
| TCP | 25 | Docker published Stalwart SMTP |
| TCP | 465 | Docker published Stalwart SMTPS / submissions |
| TCP | 993 | Docker published Stalwart IMAPS |
| TCP | 80 | nginx |
| TCP | 443 | Xray |
| UDP | 443 | Hysteria2 |

## 4.2 Loopback-only service endpoints

| Address | Purpose |
|---|---|
| `127.0.0.1:8080` | nginx fallback/backend entry from Xray |
| `127.0.0.1:9090` | Cockpit socket |
| `127.0.0.1:13000` | Homepage |
| `127.0.0.1:15678` | n8n |
| `127.0.0.1:18080` | Maintenance Center UI |
| `127.0.0.1:18081` | monitoring nginx endpoint |
| `127.0.0.1:18082` | speedtest trigger endpoint |
| `127.0.0.1:18083` | Stalwart web/admin/JMAP backend |
| `127.0.0.1:18084` | Bulwark webmail |
| `127.0.0.1:18140` | CloudCLI |
| `127.0.0.1:18334` | Filestash |
| `127.0.0.1:18384` | Syncthing GUI |
| `127.0.0.1:19091` | Authelia |

Additional private bridge service:

- `172.21.0.1:17890` — Codex runner endpoint, intended for n8n over the dedicated Docker bridge.

---

# 5. Firewall and intrusion protection

## 5.1 UFW

Status:

- active
- logging: low

Defaults:

- incoming: deny
- outgoing: allow
- routed: deny

Allowed public ports:

- `22/tcp`
- `80/tcp`
- `443/tcp`
- `443/udp`
- `25/tcp`
- `465/tcp`
- `993/tcp`

Dedicated runner rule:

- destination `172.21.0.1:17890/tcp`
- source `172.21.0.2`
- comment: `n8n to Codex runner`

IPv6 equivalents exist for the public ingress ports.

---

## 5.2 Fail2Ban

Active jails:

1. `sshd`
2. `stalwart-smtp-abuse`
3. `stalwart-submission-scan`

### SSH

Historical audit state showed thousands of failed attempts and hundreds of total bans.

### Mail jails

A concrete runtime defect exists in the current state.

The jail configuration uses:

`/var/lib/docker/containers/*/*-json.log`

However Fail2Ban resolved this wildcard at service start and still tracks old container log paths.

Current Stalwart container:

`3370562e4da003a0193a248560b16a8e6656ae5753d614e2c6572ab39be02c67`

Current Stalwart log:

`/var/lib/docker/containers/3370562e.../3370562e...-json.log`

Confirmed state:

- `CURRENT_STALWART_LOG_TRACKED_BY_SMTP_JAIL=NO`
- `CURRENT_STALWART_LOG_TRACKED_BY_SUBMISSION_JAIL=NO`

This is a **known current defect**. No corrective action is recorded in this baseline.

---

# 6. SSH

Effective configuration observed:

- port `22`
- IPv4 and IPv6 listen
- `PermitRootLogin prohibit-password`
- `PubkeyAuthentication yes`
- `PasswordAuthentication no`
- `KbdInteractiveAuthentication no`
- `AllowTcpForwarding yes`
- `X11Forwarding yes`
- `MaxAuthTries 6`

---

# 7. Public edge architecture

## 7.1 Xray

Binary:

- `/usr/local/bin/xray`

Version:

- `26.3.27`

SHA256:

`8255dd939c34cf966cc91517b6324dd3c8d0bcf49ffac8beca049a38c46845ed`

Service:

- `xray.service`
- active
- enabled
- user/group: `xray:xray`

Observed hardening:

- `PrivateTmp=yes`
- `ProtectHome=yes`
- `ProtectSystem=strict`
- `NoNewPrivileges=yes`

Network role:

- public TCP/443 endpoint
- fallback toward nginx on `127.0.0.1:8080`

TLS material:

- `/etc/xray/tls/fullchain.pem`
- `/etc/xray/tls/privkey.pem`

---

## 7.2 Hysteria2

Binary:

- `/usr/local/bin/hysteria`

Version:

- `v2.12.2`

Build:

- `2026-08-23`
- Go `1.26.6`
- commit `619a6f856b69fb7ee6a7a379e810e68b84004605`

SHA256:

`6493dfffd55b5883f64c76c63880ecc32988f0c568c9ca9014907877b4d55f94`

Service:

- `hysteria-server.service`
- active
- enabled
- user/group: `hysteria:hysteria`
- `NoNewPrivileges=yes`

Network role:

- public UDP/443

Config:

- `/etc/hysteria/config.yaml`

TLS:

- `/etc/hysteria/tls/fullchain.pem`
- `/etc/hysteria/tls/privkey.pem`

---

# 8. nginx and domain routing

nginx:

- Ubuntu package `1.28.3`
- configuration syntax passed `nginx -t`

Enabled sites:

- `mail.conf`
- `vpn-stub.conf`

Active hashes:

- `/etc/nginx/nginx.conf`: `aebe4c7c0a4be7e0582d9a8816b423bff6afcac330b882d8aff62624d44ebcd2`
- `mail.conf`: `b3c97ca6a5433c1a455974cca72a700665d4d9655c64ca342c48908b430de7e7`
- `vpn-stub.conf`: `47cc269040c4d16f63d4e7b3d7f32823d75b7c4a2590051bcf676f465fdcce90`
- `xray-realip.conf`: `621d7cc1e9139711aeb731603794e8dd8de897126faca11e2a1653089dc9a799`

nginx directly listens on:

- public TCP/80
- `127.0.0.1:8080 proxy_protocol`

Xray owns public TCP/443.

## 8.1 Domain map

| Domain | Current target / behavior |
|---|---|
| `escloud.us` | static public decoy/root |
| `auth.escloud.us` | Authelia |
| `app.escloud.us` | Homepage + admin paths |
| `go.escloud.us` | n8n |
| `cloud.escloud.us` | Filestash |
| `sync.escloud.us` | Syncthing |
| `code.escloud.us` | CloudCLI |
| `docs.escloud.us` | protected static placeholder |
| `chat.escloud.us` | protected 404/reserved |
| `mail.escloud.us` | Stalwart APIs + Bulwark |

### `app.escloud.us`

Includes:

- `/` → Homepage
- `/terminal/` → Cockpit
- `/maintenance/` → Maintenance Center
- `/maintenance/monitoring/` → monitoring
- `/speedtest/` → speedtest trigger

### `go.escloud.us`

- Authelia protected
- n8n backend `127.0.0.1:15678`

### `cloud.escloud.us`

- Authelia protected
- Filestash backend `127.0.0.1:18334`

### `sync.escloud.us`

- intentionally used for Syncthing
- Authelia protected
- backend `127.0.0.1:18384`

### `code.escloud.us`

- Authelia protected
- CloudCLI backend `127.0.0.1:18140`

### `chat.escloud.us`

- protected
- current response 404
- browser-stack removed

### `mail.escloud.us`

- HTTP→HTTPS
- Stalwart API/JMAP/admin paths → `127.0.0.1:18083`
- main webmail path → Bulwark `127.0.0.1:18084`

---

# 9. TLS

Certbot certificate:

- name: `escloud.us`
- key type: ECDSA

Covered names:

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

Audit-time expiry:

- `2026-11-10 01:15:19+00:00`

---

# 10. Docker engine

Docker Engine:

- `29.8.0`

Docker Compose:

- `5.5.1`

containerd:

- `2.3.4` at audit

runc:

- `1.5.1`

Runtime characteristics:

- rootful Docker
- overlay2
- cgroup v2
- systemd cgroup driver
- AppArmor
- seccomp
- Swarm inactive
- live restore enabled
- iptables firewall backend

Current Compose projects:

1. `core-stack`
2. `mail-stack`

Containers:

- 9 total
- 9 running
- 0 stopped

---

# 11. Docker networks

| Network | Subnet | Internal |
|---|---|---:|
| `core-internal` | `172.18.0.0/16` | yes |
| `core-egress` | `172.19.0.0/16` | no |
| `core-monitoring` | `172.20.0.0/16` | yes |
| `automation-runner` | `172.21.0.0/24` | yes |
| `mail-network` | `172.22.0.0/16` | no |

`automation-runner` currently provides the dedicated n8n → Codex runner path.

---

# 12. Container inventory

## 12.1 n8n

Image:

`docker.n8n.io/n8nio/n8n:2.37.10@sha256:307d6065be25619aa24cfc63a7c2f04ca56d084a08c05c8e9f189a89f353b1ec`

Image ID:

`sha256:05f8527a0e12dff0e5c121911a5d3e69c7523b2bfc886fc8f2c67672bf070d9f`

Runtime:

- user `node`
- healthy
- restart count 0
- logging `local`
- `127.0.0.1:15678 -> 5678`

Networks:

- `automation-runner=172.21.0.2`
- `core-egress=172.19.0.6`
- `core-internal=172.18.0.7`

Mounts:

- `/srv/ai-workspace/data/n8n -> /home/node/.n8n` RW
- `/etc/codex-runner/token -> /run/secrets/codex_runner_token` RO

Database:

- `/srv/ai-workspace/data/n8n/database.sqlite`
- SQLite integrity check: `ok`

Snapshot counts:

- workflows: 2
- credentials: 1
- executions: 0
- webhooks: 0
- projects: 1
- tags: 0
- active workflows: 0

**Do not use these counts to infer future relevance. The VPS had not entered active production use.**

---

## 12.2 Filestash

Image:

`machines/filestash@sha256:0b8fc005e52e6202c626ff5e155d8c2a313c83fd2130861b19fc96cdc41b55ad`

Runtime:

- user `filestash`
- healthy
- logging `local`
- `127.0.0.1:18334 -> 8334`

Mounts:

- `/srv/cloud -> /mnt/cloud` RW
- `/srv/ai-workspace/data/filestash/state -> /app/data/state` RW

State footprint ~7.6 MiB.

`/srv/cloud` snapshot:

- 0 files
- 1 directory
- ~4 KiB

This is current pre-production state only.

---

## 12.3 Authelia

Image:

`authelia/authelia:4.39.22@sha256:936134132eaf01bfa2faf85055afbc1e0cc1cc5ca4547e9c06408fd0dd784646`

Runtime:

- healthy
- `127.0.0.1:19091 -> 9091`

Data path:

- `/srv/ai-workspace/data/authelia`

Contains:

- `configuration.yml`
- `users_database.yml`
- `db.sqlite3`
- JWT/session/storage secrets

Historical auth model:

- one-factor deployed
- two-factor deferred

---

## 12.4 Homepage

Image:

`ghcr.io/gethomepage/homepage:v2.2.0@sha256:753eeb0cc22ab7baad39ed47cbd1aae14e193dd1b264e965f193a9ea1d1e1bdd`

Runtime:

- healthy
- host port `127.0.0.1:13000`
- networks: egress, internal, monitoring

The observed `next-server` process owned by root belongs to this container.

---

## 12.5 Monitoring

Image:

`nginx:1.31.5-alpine@sha256:72ba65eb42c10344912a84ff42408db7d34f2feb642204570ab8fc5ffd29f1d3`

Runtime:

- healthy
- `127.0.0.1:18081`
- generated health/status content

---

## 12.6 Docker socket proxy

Image:

`tecnativa/docker-socket-proxy:v0.5.0@sha256:1f5038b54f06c3e18422902cf00ba21803d1c97805aae032e5e6673d532d3459`

Runtime:

- healthy
- internal monitoring network
- Docker socket mounted read-only

---

## 12.7 Syncthing

Image:

`syncthing/syncthing:2.1.3@sha256:8c8ff37ab6aa8be23b700648a90fa9412e214852e9fd6ea8477c8334792daec0`

Runtime:

- healthy
- GUI host bind `127.0.0.1:18384`
- persistent state under `/srv/ai-workspace/data/syncthing`

Snapshot:

- folders: 0
- devices: 1
- global discovery: false
- local discovery: false
- relays: false
- NAT: false
- GUI TLS: false behind external TLS termination

Do not infer future necessity from the empty folder list.

---

## 12.8 Stalwart

Image:

`stalwartlabs/stalwart@sha256:93c574e52249c1ebf90061da2c4c0756a7b72abfcc1fec34506a03c2e38b5977`

Runtime:

- user `stalwart`
- healthy
- JSON-file logging

Ports:

- `25`
- `465`
- `993`
- loopback web/admin `18083`

Persistent data:

- `/srv/ai-workspace/data/mail/stalwart/etc`
- `/srv/ai-workspace/data/mail/stalwart/certs`
- `/srv/ai-workspace/data/mail/stalwart/lib`

Snapshot footprint:

- ~104 MiB
- ~120 files

---

## 12.9 Bulwark

Image:

`ghcr.io/bulwarkmail/webmail@sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`

Runtime:

- user `nextjs`
- no Docker healthcheck
- JSON-file logging
- `127.0.0.1:18084 -> 3000`

Persistent state includes admin/settings/telemetry directories.

The second observed `next-server` process belongs to Bulwark.

---

# 13. Docker volume residue

One anonymous volume:

`122add53c440a645130bdd8f5c38021341f02e8b7e78dc5e7a9015930923bf09`

State:

- created 2026-07-10
- ~8 KiB
- attached containers: 0

No cleanup performed.

---

# 14. Systemd/custom services

Project-related services include:

- `cloudcli.service`
- `codex-app-server.service`
- `codex-runner.service`
- `maintenance-center.service`
- `speedtest-trigger.service`
- `xray.service`
- `hysteria-server.service`

No failed systemd units were observed.

---

# 15. CloudCLI

Binary:

- `/home/core/.local/bin/cloudcli`

Version:

- `1.37.2`

Service:

- user/group `core:core`
- working directory `/srv/ai-workspace`
- port `18140`
- DB `/home/core/.cloudcli/auth.db`
- `Restart=on-failure`
- `NoNewPrivileges=true`
- `PrivateTmp=true`
- `ProtectSystem=full`

State footprint:

- `/home/core/.cloudcli` ~224 KiB

Public route:

- `code.escloud.us`

---

# 16. Codex

CLI:

- `/home/core/.local/bin/codex`
- version `0.153.4`

Manifest checksum:

`56ef98ab4032d317ab26e9b5e5a175650717351edb16ed9cde0cb6d1734d62da`

User state:

- `/home/core/.codex` ~483 MiB

Major footprint portions:

- standalone package ~336 MiB
- temporary plugin data ~88 MiB
- plugins/cache ~35 MiB
- remote plugin catalog ~17 MiB

## 16.1 App server

`codex-app-server.service`

- user `core`
- `codex app-server --remote-control --listen unix://`
- `NoNewPrivileges=yes`

## 16.2 Runner

`codex-runner.service`

Executable:

- `/usr/local/libexec/codex-runner-api`
- Python
- SHA256 `e7247e70c2e2e6d5386cf40f691ba3174c87f0b4c1ed810e0a5279b60dfae1eb`

Runtime protections:

- user `core`
- `NoNewPrivileges=yes`
- `PrivateTmp=yes`
- `ProtectHome=read-only`
- `ProtectSystem=strict`
- address families: `AF_INET AF_UNIX`

Writable:

- `/srv/ai-workspace/tasks`
- `/home/core/.codex`

Read-only:

- `/srv/ai-workspace/workspaces/manual`
- `/etc/codex-runner/token`

---

# 17. AI/development CLI inventory

Under `core`:

| Tool | Version |
|---|---|
| Claude Code | `2.1.263` |
| Codex CLI | `0.153.4` |
| CloudCLI | `1.37.2` |
| task-master-ai | `0.43.1` |
| Node | `22.22.1` |
| npm | `10.9.4` |
| Python | `3.14.4` |
| Git | `2.53.0` |

Absent at audit:

- Gemini CLI
- Antigravity
- pnpm
- bun

---

# 18. Task runner state

Path:

- `/srv/ai-workspace/tasks`

Snapshot:

- four task directories
- dated 2026-07-11
- ~92 KiB total
- no open file references

Files include:

- `request.json`
- `status.json`
- stdout/stderr logs
- result files

This is historical state only.

---

# 19. Maintenance Center

Service:

- `maintenance-center.service`

Executable:

- `/usr/local/libexec/maintenance-center-ui`
- Python
- SHA256 `b90ca12e2be7473a3720cce6d3aea0a69a332ae3006131f1afd557bde25432d5`

Service user:

- `maintenance-center`

Observed protection:

- `PrivateTmp=yes`
- `PrivateDevices=yes`
- `ProtectHome=yes`
- `ProtectSystem=full`
- `NoNewPrivileges=no`
- address families: INET/INET6/UNIX

State:

- `/var/lib/maintenance-center/state`

Contains:

- `snapshot.json`
- `version-catalog.json`
- `status.json`
- `backup.json`
- `versions.json`
- `speedtest.json`

## 19.1 Superseded update architecture

Historical work introduced increasingly complex updater/job/inventory architecture.

Later project constraints explicitly rejected that direction in favor of a simpler maintenance model:

- installed version
- available version
- update yes/no
- manual update
- post-update health check
- optional simple rollback

The complex updater design must be treated as historical/superseded context, not as future architecture requirement.

---

# 20. Monitoring/exporters

Timers include:

- monitoring health exporter
- backup status exporter
- version status exporter
- speedtest refresh

These generate state used by current management UI/components.

---

# 21. Speedtest

Services:

- `speedtest-trigger.service`
- `speedtest-refresh.service`

Trigger executable:

- `/usr/local/libexec/speedtest-trigger`
- SHA256 `717f94c16a514e4ba1090a830da84ff558528904a3377e74f3f98522905e947d`

Important behavior:

- HTTP GET to the trigger endpoint causes a refresh.
- It is **not** a read-only health endpoint.

This was confirmed during audit and must be remembered for future diagnostics.

---

# 22. Cockpit

Installed functional packages:

- `cockpit-bridge 360-1`
- `cockpit-system 360-1`
- `cockpit-ws 360-1`

The meta-package `cockpit` itself is absent.

Socket:

- `cockpit.socket`
- active/enabled
- bound by drop-in to `127.0.0.1:9090`

nginx route:

- `app.escloud.us/terminal/`

---

# 23. Backup

Restic:

- version `0.18.1`

Repository:

- `/var/backups/restic/repository`

Same root filesystem as production data:

- `/dev/vda1`

Retention:

- 7 daily
- 4 weekly
- 3 monthly

Timers:

- backup
- retention
- repository check
- restore test

Audit state:

- last backup success
- repository check success
- restore test success
- retention success
- monitoring overall `ok`

Repository size ~23 MiB at audit.

---

# 24. `/srv` layout

Relevant paths:

- `/srv/ai-workspace`
- `/srv/cloud`
- `/srv/oem-docs`

Historical paths absent:

- `/srv/core`
- `/srv/oem-data`
- `/srv/ai-workspace/vault`

Main `/srv/ai-workspace` structure:

- `apps`
- `backups`
- `config`
- `data`
- `logs`
- `tasks`
- `tmp`
- `workspaces`
- `_ops`

Data subtrees include:

- authelia
- code
- codex
- filestash
- homepage
- mail
- n8n
- obsidian
- syncthing

---

# 25. `/srv/cloud`

Ownership:

- `core:core`

Mode:

- `2770`

Snapshot:

- 0 files
- 1 directory
- ~4 KiB

Mounted RW into Filestash.

Current emptiness must not be used to infer future irrelevance.

---

# 26. `/srv/oem-docs`

Structure:

- `archive`
- `changelog`
- `incoming`

Snapshot:

- no files
- ~16 KiB
- no active configuration references found

Originates from older OEM-document workflow planning.

Future relevance must be considered later against the newer ai-node OCR/document/knowledge architecture.

---

# 27. Browser-stack historical state

Previously deployed browser-stack/Chromium/Selkies architecture is fully absent now.

Confirmed absent:

- browser-stack containers
- browser-stack network/image deployment
- `/srv/ai-workspace/apps/browser-stack`
- `/srv/ai-workspace/data/browser`
- `/var/www/ai-chat-launcher`
- old nginx token snippet
- old ports `18141` / `18143`

`chat.escloud.us` remains a protected 404 placeholder.

---

# 28. Git

Repository:

- `/srv/ai-workspace/workspaces/ai-workspace`

Ownership:

- `core:core`

Mode:

- `700`

State:

- branch `main`
- HEAD `e695030daac02f5b1a8b18a2159a7c92df5218de`
- clean working tree
- upstream `origin/main`
- local ahead by 1, behind by 0

Remote:

- `git@github.com:Eugene-SN/ai-workspace.git`

Recent history includes:

- `e695030 docs(runbook): close structural-recovery gaps, add rebuild runbook`
- `b1c51f2 chore(manifest): update hysteria2 and codex to latest stable`
- `8454194 sync(nginx): reconcile production routing with deployed state`
- `f6bb547 fix(ops): preserve Cockpit login authorization`
- `cd3f4d3 feat(ops): add protected Cockpit console`
- `e9c0b7f fix(maintenance): use writable Docker CLI config`
- `686b09f refactor(maintenance): simplify runtime and remove legacy app`
- `f45bf32 cleanup(maintenance): remove unused job and inventory legacy`

Historical branches:

- `feature/lightweight-updater-foundation`
- `feature/monitoring-stage6-profile`
- `fix/updater-inventory-schema`

---

# 29. Git vs deployed production drift

## 29.1 nginx

Runtime matches Git for:

- `vpn-stub.conf`
- `mail.conf`

## 29.2 systemd

Runtime matches Git for:

- Codex app-server
- Codex runner
- Maintenance Center
- Hysteria
- Xray

CloudCLI has byte-level drift but no demonstrated operational semantic drift in the audited projection.

## 29.3 Core stack Compose

Significant drift exists.

Production:

- Filestash newer digest
- nginx monitoring `1.31.5` vs Git `1.31.2`
- Authelia `4.39.22` vs Git `4.39.20`
- n8n `2.37.10` vs Git `2.29.10`
- Syncthing `2.1.3` vs Git `2.1.2`
- socket proxy `v0.5.0` vs Git `v0.4.2`
- Homepage `v2.2.0` vs Git `v1.13.2`

Git also still contains an older containerized Maintenance Center definition that is absent from current production Compose, where Maintenance Center is host-side systemd.

## 29.4 Mail Compose

Production and Git differ for:

- Stalwart image digest
- Bulwark image digest/tag generation

Therefore **Git does not currently reproduce exact deployed production state**.

---

# 30. Component manifest

File:

- `manifests/components.json`

SHA256:

`6110b7824e4191521a5905dd4df6fe3d82d422072f27f9e8164cbcd866e62d3e`

Manifest currently carries newer standalone component information such as:

- Xray `26.3.27`
- Hysteria2 `2.12.2`
- Codex `0.153.4`

It also contains historical update-policy metadata including immutable digest requirements, risk/isolation classification and rollback-classification fields.

The repository therefore contains multiple generations of desired-state information.

---

# 31. Package/update snapshot

At the audit date the package cache showed updates including:

- containerd `2.3.4 -> 2.3.5`
- Buildx `0.37.0 -> 0.37.1`
- curl/libcurl
- libc
- Python 3.14 packages
- Perl
- Vim
- mdadm
- sos
- wireless-regdb

Docker Engine itself:

- installed/candidate `29.8.0`

Compose:

- installed/candidate `5.5.1`

nginx:

- installed/candidate `1.28.3-2ubuntu1.10`

OpenSSH:

- installed/candidate `10.2p1-2ubuntu3.6`

Restic:

- installed/candidate `0.18.1-3ubuntu1`

No packages held.

This section is volatile.

---

# 32. Generic Ubuntu packages/services

Observed:

- ModemManager
- multipath-tools
- UDisks2
- fwupd
- snapd
- mdadm

Marks:

| Package | apt mark |
|---|---|
| modemmanager | auto |
| multipath-tools | manual |
| udisks2 | auto |
| fwupd | manual |
| snapd | manual |
| mdadm | manual |

No removal conclusion is made.

---

# 33. Current filesystem residues / historical state

Recorded:

- `/srv/oem-docs` ~16 KiB
- `/srv/ai-workspace/tasks` ~92 KiB
- `/srv/ai-workspace/backups` ~20 KiB
- `/srv/ai-workspace/_ops` ~84 KiB
- `/srv/cloud` ~4 KiB
- one unattached anonymous Docker volume ~8 KiB

No cleanup was performed.

---

# 34. Known current defects and inconsistencies

## 34.1 Fail2Ban mail jails stale after container recreation

Confirmed.

## 34.2 Git does not exactly reconstruct deployed production

Confirmed.

Affected primarily:

- core-stack Compose
- mail-stack Compose
- minor CloudCLI byte drift

## 34.3 Restic repository is on the same filesystem as production

Structural fact.

## 34.4 Speedtest GET endpoint performs an action

Confirmed.

---

# 35. Current as-is architecture diagram

```text
                                  INTERNET
                                     |
                    +----------------+----------------+
                    |                                 |
                 TCP/443                           UDP/443
                    |                                 |
                  Xray                            Hysteria2
                    |
              TLS / fallback
                    |
             nginx 127.0.0.1:8080
                    |
      +-------------+--------------+------------------------------+
      |             |              |                              |
 auth.escloud.us  app.escloud.us  go.escloud.us               code.escloud.us
      |             |              |                              |
  Authelia       Homepage         n8n                          CloudCLI
                    |              |
                    |              +--> automation-runner
                    |                   172.21.0.2
                    |                        |
                    +--> Cockpit             v
                    |                  host :17890
                    +--> Maintenance         |
                    |                        v
                    +--> Monitoring      Codex runner
                    |                        |
                    +--> Speedtest           v
                                          Codex CLI

 cloud.escloud.us --------------------> Filestash ----> /srv/cloud

 sync.escloud.us ---------------------> Syncthing

 docs.escloud.us ---------------------> protected static placeholder

 chat.escloud.us ---------------------> protected 404

 mail.escloud.us ----------------------> Bulwark
        |
        +-----------------------------> Stalwart web/API

 TCP/25,465,993 ----------------------> Stalwart


 HOME INFRASTRUCTURE
        |
        X  no NetBird/private VPS-home backplane at baseline
        |
   nl-core-vds
```

---

# 36. Relationship to newer Home Infrastructure / PAI

The VPS was largely designed before the newer Home Infrastructure / Personal Agents Infrastructure architecture matured.

At baseline there is no implemented private integration between VPS and the newer home stack.

The newer environment includes separate capabilities such as:

- ai-node local GPU inference;
- OpenClaw;
- local AI services;
- canonical home knowledge/Obsidian storage;
- NetBird private networking;
- local automation;
- local ASR/OCR/document processing plans.

Therefore this document must be treated as the **legacy/as-is VPS side** of a future architecture comparison.

It must **not** be assumed that the future VPS should preserve the current structure.

---

# 37. Stable reference facts for future work

Unless explicitly changed later, these can usually be treated as baseline facts:

- hostname `nl-core-vds`
- Ubuntu 26.04 generation
- public IPv4 `45.92.156.17`
- Xray TCP/443 + Hysteria UDP/443 edge
- nginx fallback `127.0.0.1:8080`
- `escloud.us` domain namespace
- Docker projects `core-stack` and `mail-stack`
- users root/core/eugene
- `core` without sudo and Docker group
- `/srv/ai-workspace` structure
- mail data path
- Git repository path
- Restic repository path
- custom service paths
- browser-stack removed
- NetBird absent at baseline
- mail Fail2Ban defect
- Git/deployment drift

---

# 38. Volatile facts to revalidate before future implementation

A future redesign should **not** require a repeat of this full audit. Normally only these should be rechecked:

- exact OS/kernel patch version
- exact Docker/container versions and digests
- package update backlog
- exact certificate expiry
- Git HEAD/branch/divergence
- current container/process IDs
- current Fail2Ban tracked paths
- Restic latest backup/check/restore timestamps
- service health
- disk/RAM pressure
- external DNS/HTTP state
- current domain routing
- newly added Home Infrastructure integrations
- whether the VPS has since entered real production use

---

# 39. Explicit non-conclusions

This baseline does **not** determine whether any of the following should remain in the target architecture:

- Authelia
- Homepage
- Maintenance Center
- Cockpit
- Filestash
- Syncthing
- n8n on VPS
- n8n at home
- CloudCLI
- Codex app-server
- Codex runner
- Stalwart/Bulwark
- Xray
- Hysteria
- current public admin UI pattern
- current Git/deployment model
- current monitoring/exporter pattern
- Docker Compose
- current backup topology
- OEM directories
- generic Ubuntu packages

Those are future redesign decisions.

---

# 40. Future analysis entry point

Future architecture work should proceed from this baseline in this order:

1. Load this as the **as-is VPS state**.
2. Load accepted Home Infrastructure and Personal Agents Infrastructure state.
3. Define desired user scenarios independently of currently installed VPS services.
4. Determine which scenarios need:
   - public Internet ingress;
   - static public IP;
   - mail reputation / SMTP;
   - private access to home;
   - persistent VPS storage;
   - local home storage;
   - GPU/local AI;
   - 24/7 cloud execution;
   - mobile access;
   - webhook reception;
   - subscription-based AI CLI access;
   - backup/DR.
5. Only then compare current services against those functions.
6. Later classify functions/services as:
   - keep;
   - simplify;
   - replace;
   - move home;
   - move VPS;
   - merge;
   - remove.
7. Perform only focused volatile-state checks before implementation.

---

# 41. Baseline completion status

As of 2026-09-14:

- host/platform audit complete;
- network and firewall audit complete;
- VPN/public-edge audit complete;
- nginx/domain routing audit complete;
- Docker engine/container/network audit complete;
- systemd/custom service audit complete;
- mail topology audit complete;
- n8n state audit complete;
- Syncthing state audit complete;
- Filestash/cloud state audit complete;
- AI CLI/service inventory complete;
- backup topology audit complete;
- filesystem/history residue audit complete;
- Git and production drift audit complete;
- major current defects documented;
- no architecture redesign applied;
- no cleanup/removal performed;
- current service activity explicitly **not used as a proxy for future relevance**.

**This file is the consolidated current-state baseline for future VPS redesign work.**