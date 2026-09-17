# Cloud Infrastructure — Architecture State

## Status

**Stage 0:** COMPLETE / ACCEPTED.  
**Stage 1:** COMPLETE / ACCEPTED.  
**Stage 2:** COMPLETE / ACCEPTED.  
**Stage 02.5:** ACTIVE / RESEARCH-ONLY.

Current work branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them without a concrete requirement.
2. `edge` must remain independently useful without Home/PAI connectivity.
3. Home/PAI integration is a later-stage layer, not a Stage 1/2 foundation dependency.
4. The historical `nl-core-vds` deployment is migration/reference context, not current target authority.
5. Fresh verified runtime/configuration outranks historical reference when factual state differs.
6. The canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes it.
7. VPN/DPI-bypass functionality and any future private infrastructure backbone are separate concerns.
8. Single-operator simplicity is preferred over enterprise-style complexity without demonstrated need.
9. Unresolved future products/mechanisms are selected from concrete requirements rather than precommitted globally.
10. Presentation, backup, monitoring and maintenance tooling that depends on the final service inventory should be deployed late rather than repeatedly reworked while the server composition is still changing.
11. Post-Stage-2 deployment order follows dependency direction: independent services first, connectivity before connectivity-dependent services, then lifecycle/monitoring/presentation layers over the substantially complete infrastructure.
12. User-specific n8n and agent workflows are an application layer above the infrastructure framework and do not block final infrastructure acceptance.

## Accepted Stage 1 platform architecture

### Host/runtime placement

- Ubuntu host provides SSH, nginx, Xray, Hysteria2, Certbot, UFW and systemd-native lifecycle where host-native placement is materially simpler.
- Docker + Compose are the default runtime for suitable application services.
- Authelia is containerized.
- Host-native Xray/Hysteria2/nginx remain accepted because they directly own/shared public ingress and preserve a simple proven operating model.

### Persistent layout

Accepted path convention:

- `/opt/<service>` — runtime definitions/scripts;
- `/srv/<service>` — persistent application state;
- `/etc/<service>` — host-native configuration;
- `/var/www/<site>` — static web roots.

Stage 1 concrete examples:

- `/opt/vpn-stack`;
- `/opt/authelia`;
- `/srv/authelia`;
- `/etc/xray`;
- `/etc/hysteria`;
- `/etc/nginx`;
- `/etc/letsencrypt`;
- `/var/www/escloud.us/public`;
- `/var/www/letsencrypt`.

The preserved `/opt/vpn-stack` operational layout is accepted and is not cosmetically migrated merely to conform to a new naming convention.

### Public ingress

Public listener contract now includes the accepted mail ports from Stage 2:

- TCP/22 — SSH;
- TCP/80 — nginx;
- TCP/443 — Xray;
- UDP/443 — Hysteria2;
- TCP/25 — SMTP;
- TCP/465 — SMTPS submission;
- TCP/993 — IMAPS.

Ingress relationships:

- ordinary HTTP -> nginx TCP/80;
- ordinary HTTPS -> Xray TCP/443 TLS fallback -> nginx `127.0.0.1:8080` using Proxy Protocol;
- VLESS clients -> Xray TCP/443;
- Hysteria2 clients -> UDP/443;
- application HTTP backends normally bind loopback and are published through nginx rather than directly exposing Docker ports.

nginx intentionally has no direct public TCP/443 listener because Xray owns TCP/443.

### TLS lifecycle

- Certbot/ACME webroot remains the accepted certificate mechanism;
- ACME webroot is `/var/www/letsencrypt`;
- certificate lineage is `/etc/letsencrypt/live/escloud.us`;
- certificate renewal uses the Certbot timer;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync` invokes `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- Xray/Hysteria2/Stalwart certificate consumers are synchronized/reloaded from the accepted lineage.

### Public masking/masquerade surface

Accepted static page:

- `/var/www/escloud.us/public/index.html`;
- title `ES Cloud — Private Workspace`;
- SHA256 `73ff3e57afa08c4f007f72902c1f2d3c8cf4e53920eabd10a86e32630106318e`.

The page is both the normal public web facade and the Hysteria2 file masquerade root. Its login/password dialog is visual-only and does not transmit or persist entered values.

### Private authentication boundary

Authelia architecture:

- Compose definition `/opt/authelia/compose.yaml`;
- state `/srv/authelia`;
- loopback backend `127.0.0.1:19091`;
- public auth path: Xray TCP/443 -> nginx loopback fallback -> Authelia;
- direct public TCP/19091 is not part of the accepted exposure contract.

The final Cloud Infrastructure portal is intentionally late-stage because it should reflect the stable final service inventory and monitoring/status sources.

### Firewall

Accepted host firewall model:

- UFW active/enabled;
- default deny incoming;
- default allow outgoing;
- default deny routed;
- IPv6 enabled;
- accepted current public ingress is TCP 22/80/443/25/465/993 and UDP 443;
- Docker firewall integration remains enabled;
- application containers are loopback-published by default.

No additional enterprise network/auth layer is part of the accepted base architecture.

### VPN operations

Accepted operational scripts:

- `/opt/vpn-stack/scripts/maintctl`;
- `/opt/vpn-stack/scripts/vpnctl`.

Accepted convenience entrypoints:

- `/root/maintctl`;
- `/usr/local/bin/maintctl`;
- `/usr/local/bin/vpnctl`.

The restored `maintctl` differs from its preserved source only by the accepted current certificate-sync paths.

### Stage 1 recovery

Local base-state recovery checkpoint:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

This checkpoint is deliberately same-VPS and is not complete disaster recovery. Future Backrest/Restic/off-site topology remains later-stage work. Stage 0 provider backup and external migration archive remain separate recovery layers.

## Accepted Stage 2 application architecture

The production application anchors are now deployed and accepted:

- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark.

These products are not reopened for replacement research without a concrete incompatibility or changed requirement.

## Dependency-aware remaining architecture

### 1. Remaining Standalone Core Services

First complete any additional full services that can run and be accepted on `edge` independently from future Home/PAI connectivity and from late lifecycle/presentation layers.

Do not classify user-specific n8n workflows or agent tasks as standalone infrastructure services merely because they run on `edge`.

### 2. Cross-site Connectivity Foundation

Before deploying services whose correctness depends on Home/PAI, determine the real flows and establish the minimum required connectivity between:

- `edge`;
- `ai-node`;
- PVE/Home Infrastructure.

NetBird, direct WireGuard, authenticated HTTPS or other transports remain unresolved until evaluated against actual flows and connectivity conditions. Do not choose a private-backbone technology first and then invent uses for it.

Connectivity foundation means transport/reachability/endpoints. Application-level durable task queues, retry state machines and user workflows are separate later concerns.

### 3. Cross-site Data & Knowledge Services

Only after connectivity is accepted should the project deploy services that depend on it, including selected implementations for:

- VPS working-file access;
- MacBook/iPhone/iPad/`ai-node` access;
- web file management;
- selected-directory synchronization;
- Obsidian synchronization or relay/mirror role.

The canonical Obsidian vault remains `ai-node:/srv/ai-data/knowledge/obsidian`.

### 4. Remaining Infrastructure Services

Complete all other selected infrastructure services after their dependencies are satisfied so the service inventory becomes substantially stable before global lifecycle/monitoring layers are finalized.

### 5. Backrest & Recovery

Backrest using Restic remains the accepted backup-management direction.

Its late-stage implementation must define backup scope, repository destinations, exclusions, retention, schedules, off-site topology and verified restore procedures against the substantially complete server.

Backrest restore acceptance must precede Semaphore/update testing.

### 6. Semaphore & dedicated maintenance/update page

Semaphore remains the accepted operational execution product. It is developed/tested together with the maintenance/update surface using the existing PVE/Home updater as an engineering reference, after audit and adaptation for `edge`.

The dedicated custom page is `update.escloud.us`; it is not folded into the general `app.escloud.us` portal.

`update.escloud.us` will be implemented as a separate Codex substage only after the real Semaphore/update workflow and status/control contract is known.

### 7. Infrastructure-wide Monitoring, Heartbeats & Alerts

Production monitoring is intentionally late-stage so it can cover the actual stable inventory in one pass rather than being repeatedly revisited.

Potential scope includes:

- `edge` service availability;
- external checks;
- cross-site connectivity;
- selected Home/PVE/`ai-node` heartbeats;
- file/sync health where useful;
- Backrest job/backup health;
- Semaphore/update health/state;
- alert delivery.

The concrete monitoring implementation remains a Stage 02.5 research decision. Avoid heavy observability unless justified by the actual requirements.

### 8. Final `app.escloud.us` portal

`app.escloud.us` is built after monitoring/status sources and the final service inventory are known.

Its role is unified navigation and useful summary/status presentation. It is not another operational control plane. Detailed maintenance/update control remains on `update.escloud.us`.

The page will be implemented as a separate Codex substage against the accepted service URLs and monitoring/status interfaces.

### 9. Final integrated infrastructure acceptance

Final server-wide acceptance occurs only after:

- all selected infrastructure services;
- cross-site connectivity/integration;
- Backrest restore acceptance;
- Semaphore/update acceptance;
- `update.escloud.us` acceptance;
- monitoring/alert acceptance;
- `app.escloud.us` acceptance;
- final cleanup.

### 10. Post-infrastructure automation/workflow layer

User-specific automation belongs after infrastructure acceptance and evolves continuously rather than defining infrastructure completeness.

This later layer includes, as appropriate:

- Universal Capture Inbox — user submission of URLs/text/files/images into automation workflows;
- human-in-the-loop approvals — explicit approval/reject/choice gates;
- mail-triggered workflows;
- continuous information intake/change-detection workflows;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for real cross-site tasks;
- messaging/bot command surfaces;
- orchestration across n8n, CloudCLI, Codex, Antigravity and PAI.

Hermes is added only if research proves a concrete persistent-agent/supervisory gap not already served by the accepted stack.

## Accepted global product anchors

Do not replace without a concrete incompatibility or changed requirement:

- Xray;
- Hysteria2;
- nginx;
- n8n;
- CloudCLI;
- Stalwart + Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI.

Additional accepted directions:

- Backrest using Restic for backup management, deployed late after the functional server composition stabilizes;
- Semaphore for operational execution, tested only after working Backrest restore capability exists;
- dedicated `update.escloud.us` maintenance/update page built separately with Codex;
- infrastructure-wide monitoring deployed after the main service inventory and lifecycle services exist;
- dedicated `app.escloud.us` portal built separately with Codex after monitoring/status sources are accepted.

## Architecture authority

For implementation work, authority order remains:

1. current user instruction;
2. latest applicable ACCEPTED decision/acceptance record;
3. `CURRENT_STATE.md` for confirmed current runtime;
4. this file for accepted architecture/invariants;
5. `IMPLEMENTATION_PHASES.md` and stage-specific planning documents;
6. `FUNCTIONAL_SCAFFOLD_DRAFT.md` for capability intent;
7. `migration-reference/` and historical baseline for legacy evidence only.

Detailed historical future-stage proposals are not accepted merely because they once appeared in Git history.
