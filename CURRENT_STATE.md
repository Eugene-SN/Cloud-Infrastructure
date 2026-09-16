# Cloud Infrastructure — Current State

## Snapshot status

**Current canonical work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`  
**Current implementation stage:** **Stage 1 — Base `edge` Platform — IN PROGRESS / NOT ACCEPTED**  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

The clean provider rebuild is complete and accepted, but **Base Platform Deployment is not complete**. The project must continue Stage 1 work in branch `01` rather than proceed to a later branch.

The previously opened `02 — Edge Functional Composition & Deferred Capabilities` was premature and is not the canonical continuation point.

Canonical implementation workflow and stage sequence: `IMPLEMENTATION_PHASES.md`.

## What is actually complete

### Stage 0 — discovery / preservation / migration preparation

**Status:** COMPLETE / PASS.

Confirmed:

- legacy VPS audit and historical baseline completed;
- preliminary global functional scaffold created;
- provider-level full VPS backup completed successfully;
- external credential-bearing migration archive downloaded and independently verified;
- archive SHA256: `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
- sanitized GitHub `migration-reference/` accepted;
- clean provider-level Ubuntu rebuild selected;
- recovery paths verified.

The sensitive archive remains outside GitHub and is the authoritative portable selective-recovery source. The provider backup remains the whole-VPS rollback path.

### Migration engineering reference

The sanitized engineering reference is accepted at:

`migration-reference/`

Canonical acceptance record:

`MIGRATION_REFERENCE_ACCEPTANCE_2026-09-16.md`

It is engineering context only, not an authoritative restore bundle.

## Stage 1 current state

### Completed subphase: Edge Clean Rebuild

**Status:** PASS.

The GreenCloud KVM VPS was rebuilt from the provider panel as a clean Ubuntu instance and is now the live logical node `edge`.

Accepted runtime facts after controlled reboot:

- hostname/FQDN: `edge.escloud.us`;
- short hostname: `edge`;
- OS: Ubuntu 26.04.1 LTS;
- architecture: `x86_64`;
- virtualization: KVM;
- kernel: `7.0.0-31-generic` at substrate acceptance;
- vCPU: 2;
- RAM: ~15 GiB;
- swap: 4 GiB `/swap.img`;
- root filesystem: ext4 on `/dev/vda1`, ~155 GiB filesystem class;
- IPv4: `45.92.156.17/24`, default gateway `45.92.156.1`;
- IPv6: `2a0c:b847:ffff:283::a/64`, default gateway `2a0c:b847:ffff::1`;
- DNS resolution: PASS;
- NTP synchronization: PASS;
- SSH key authentication: PASS;
- effective SSH auth: root key login allowed, password and keyboard-interactive authentication disabled;
- OpenSSH socket activation through `ssh.socket` accepted;
- post-reboot system state: `running`;
- failed systemd units: 0;
- current-boot error journal: empty at substrate acceptance.

`EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`.

### First-boot GRUB anomaly

The initial provider provisioning boot briefly produced `grub-initrd-fallback.service` failure with `invalid environment block` while GreenCloud provisioning upgraded `grub2-common` from `2.14-2ubuntu2` to `2.14-2ubuntu2.1` in the same boot.

After controlled reboot both relevant GRUB units completed successfully and no current-boot error remained. This is accepted as a transient provider-provisioning race, not an active defect.

### Provider cloud-init warnings

GreenCloud NoCloud seed completed with `errors: []`, but provider-template schema/deprecation warnings remain for:

- deprecated `users.0.ssh-authorized-keys`;
- swap size encoded as a floating-point value;
- deprecated netplan `gateway4` / `gateway6` syntax.

These warnings are non-blocking because effective SSH, swap and IPv4/IPv6 networking are correct. Do not mutate working provider-generated configuration merely to silence them.

### Completed subphase: minimal architecture-independent bootstrap

**Status:** PASS.

`EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`.

Accepted changes/state:

- package metadata refreshed successfully;
- `dpkg --audit` clean;
- no APT holds;
- Ubuntu phased updates were not forced;
- `unzip 6.0-29ubuntu1` installed as the only additional base utility;
- journald persistent-use ceiling configured as `SystemMaxUse=500M`;
- journald active and healthy;
- timezone retained as `Europe/Moscow`; NTP synchronized;
- working provider Netplan left unchanged;
- SSH configuration left unchanged; key-only root access and `ssh.socket` remain accepted;
- QEMU guest agent present and active;
- `/tmp` is tmpfs with mode `1777`;
- IPv4/IPv6 and SSH non-regression gates passed.

Not installed merely for convenience: `zip`, `tree`, `socat`, `pip3`.

## Stage 1 is NOT complete

Only the clean-rebuild/substrate portion of branch `01` is complete. **Base Platform Deployment remains unfinished.**

### Current implementation rule

Stage work now follows an **accepted-first** order:

1. classify the current stage into already accepted/known implementation versus genuinely unresolved choices;
2. reconstruct accepted carry-forward components from the preserved legacy implementation;
3. deploy and verify dependency-ready accepted components first;
4. discuss/select only genuinely unresolved mechanisms or concrete optimizations;
5. complete the remaining stage-scoped deployment/verification;
6. accept the whole stage before any branch transition.

Do not require the user to select already accepted services again from scratch. `migration-reference/`, the historical baseline and the sensitive recovery archive are the implementation starting point for accepted carry-forward services.

### Stage 1 accepted runtime/implementation anchors

- **Docker Engine + Docker Compose** are accepted as the primary runtime for suitable application services; containerization is preferred for clean deployment, lifecycle control, maintenance and updates.
- Host-native services remain allowed where they are materially simpler/better suited; such exceptions require a concrete rationale.
- **nginx**, **Xray**, **Hysteria2** and **Authelia** remain accepted products.
- Their legacy configuration/scenarios are carry-forward implementation references, not something to recreate from zero.
- The preserved TLS baseline is Certbot/ACME webroot with the `escloud.us` SAN certificate set and deploy-hook/certificate synchronization to Xray/Hysteria2.
- Historical versions are not pins; deployment uses the current supported stable release/update path unless compatibility requires otherwise.

### Legacy Stage 1 foundation reconstructed from preservation data

The old working public-edge contract included:

- nginx host-side public TCP/80 and loopback `127.0.0.1:8080 proxy_protocol`;
- Xray public TCP/443 with VLESS/TLS and fallback to nginx `127.0.0.1:8080`;
- Hysteria2 public UDP/443 with strict SNI and file-based masquerade rooted at `/var/www/escloud.us/public`;
- Certbot webroot at `/var/www/letsencrypt` with a shared ECDSA certificate named `escloud.us` covering the required `escloud.us` web names;
- Certbot renewal plus certificate-copy/deploy-hook logic for Xray and Hysteria2;
- Authelia on a loopback-published container endpoint with file/Argon2 authentication, SQLite storage, one-factor policies and `auth.escloud.us` session domain behavior;
- VPN user/state tooling under `/opt/vpn-stack` (`vpnctl`) and maintenance logic worth selectively adapting from `maintctl`.

The exact credentials and private TLS/state material remain in the sensitive recovery archive and are restored selectively where continuity is required.

### Firewall evidence

Contrary to the recollection that the legacy VPS had no firewall, the preserved runtime audit shows **UFW was active** with:

- default deny incoming;
- allow outgoing;
- deny routed;
- explicit IPv4/IPv6 rules for SSH, TCP/80, TCP/443, UDP/443 and mail ports;
- one internal Docker-bridge rule for n8n → Codex runner.

Whether to retain UFW on the new Docker host remains a Stage 1 engineering decision because Docker-published ports have special firewall semantics. Do not assume the legacy firewall was absent.

### Stage 1 functional scope still to finish

- Docker + Compose installation/acceptance;
- consumer-driven base package completion;
- normalized persistent-directory and ownership conventions;
- nginx ingress foundation;
- HTTPS/TLS/certificate lifecycle;
- Xray;
- Hysteria2;
- plausible public/decoy page;
- Authelia common web-auth foundation;
- firewall decision/minimal policy;
- initial private Cloud Infrastructure page decision/implementation boundary;
- basic backup of the new base state;
- extension points for later public/private WebUI, machine APIs, webhooks, working storage, Home/PAI connectivity and monitoring.

## Global functional scaffold status

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is the current preliminary global capability scaffold.

It defines high-level required or potentially valuable functions across the final `edge`, but it **does not select every service/program** and is **not** a final architecture or final service inventory.

Unresolved products/services are intentionally chosen in the implementation stage where they are needed. Already accepted products are deployed first where their dependencies and implementation are known.

## Accepted global product/direction anchors

Accepted without replacement research unless a concrete incompatibility or changed requirement appears:

- Xray;
- Hysteria2;
- nginx;
- n8n;
- CloudCLI;
- Stalwart;
- Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI.

Additional accepted directions:

- Backrest using Restic for future backup management;
- dedicated Cloud Infrastructure portal replacing Homepage;
- maintenance page + Semaphore replacing the legacy custom Maintenance Center.

These global anchors do not mean that all integration/runtime details are already designed.

## Important unresolved future product choices

Examples still intentionally unresolved until their corresponding stage include:

- final file/storage access implementation;
- Filestash vs alternatives;
- synchronization model and Syncthing role;
- exact `edge` role in Obsidian synchronization;
- monitoring/notification implementation;
- Hermes role;
- bots/messaging frontend;
- private/site-to-site connectivity mechanism;
- off-site DR topology;
- any adjacent implementation products not already explicitly accepted.

Canonical Obsidian vault remains on `ai-node` at:

`/srv/ai-data/knowledge/obsidian`

## Architecture state

There is **no accepted full target Architecture Contract** and no accepted preselection of all future-stage services.

`ARCHITECTURE.md` records only accepted architecture state/invariants and stage-scoped decisions. Known accepted implementation can proceed from preserved evidence without waiting for unrelated unresolved future-stage choices.

Any previous proposal that preselected future unresolved products or topology before their stage review is not current authority.

## Current branch / transition rule

Current canonical branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

Status:

**IN PROGRESS — clean rebuild complete; Base Platform Deployment incomplete.**

Do not transition to another branch until Stage 1 is fully deployed, verified and accepted.

After Stage 1 acceptance, the next branch should be:

`02 — Edge Core Applications`.
