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

Before additional Stage 1 runtime deployment, the project must continue in the same branch and perform the mandatory stage design cycle:

1. review exact Stage 1 functional requirements against the global scaffold;
2. identify already accepted Stage 1 products versus unresolved implementation choices;
3. research/discuss unresolved services/mechanisms for Stage 1 only;
4. accept the Stage 1 service/product composition;
5. define the Stage 1 scoped architecture/deployment contract and recovery path;
6. deploy the remaining Base Platform components;
7. verify and explicitly accept Stage 1;
8. persist accepted state to GitHub;
9. only then open the next branch.

### Stage 1 functional scope still to finish

The Stage 1 capability set currently includes, subject to the stage-specific design/selection process where details remain unresolved:

- target networking/firewall/SSH baseline beyond the already accepted provider networking/SSH state where changes are actually required;
- Docker + Compose where required by the selected Stage 1 implementation;
- normalized persistent-directory and ownership conventions;
- nginx ingress foundation;
- HTTPS/TLS/certificate mechanics;
- Xray;
- Hysteria2;
- plausible public/decoy page;
- Authelia common web-auth foundation;
- initial private Cloud Infrastructure page;
- basic backup of the new base state;
- extension points for later public/private WebUI, machine APIs, webhooks, working storage, Home/PAI connectivity and monitoring.

Products already explicitly accepted globally — including nginx, Xray, Hysteria2 and Authelia — are not reopened for replacement research without a concrete incompatibility. Their Stage 1 deployment/integration design still remains to be discussed and accepted.

## Global functional scaffold status

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is the current preliminary global capability scaffold.

It defines high-level required or potentially valuable functions across the final `edge`, but it **does not select every service/program** and is **not** a final architecture or final service inventory.

Unresolved products/services are intentionally chosen at the beginning of the implementation stage where they are needed.

This prevents premature selection of Stage 4/5/6 products before their real consumers and constraints exist.

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

`ARCHITECTURE.md` records only accepted architecture state/invariants and the current stage-design model. Stage-specific architecture is added only after that stage's requirements and service composition are accepted.

Any previous proposal that preselected future unresolved products or topology before their stage review is not current authority.

## Current branch / transition rule

Current canonical branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

Status:

**IN PROGRESS — clean rebuild complete; Base Platform Deployment incomplete.**

Do not transition to another branch until Stage 1 is fully deployed, verified and accepted.

After Stage 1 acceptance, the next branch should be:

`02 — Edge Core Applications`

and must begin with Stage 2 requirements analysis and service/product composition before Stage 2 deployment.
