# Cloud Infrastructure — Architecture State

## Status

**Stage 1 architecture:** COMPLETE / ACCEPTED.  
**Full multi-stage target architecture:** intentionally incremental; future-stage unresolved choices remain open until their stage begins.

Completed work branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

Current work branch:

`02 — Edge Core Applications`

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them without a concrete requirement.
2. `edge` must remain independently useful without Home/PAI connectivity.
3. Home/PAI integration is a later-stage layer, not a Stage 1 foundation dependency.
4. The historical `nl-core-vds` deployment is migration/reference context, not current target authority.
5. Fresh verified runtime/configuration outranks historical reference when factual state differs.
6. The canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes it.
7. VPN/DPI-bypass functionality and any future private infrastructure backbone are separate concerns.
8. Single-operator simplicity is preferred over enterprise-style complexity without demonstrated need.
9. Unresolved future products/mechanisms are selected stage-by-stage rather than precommitted globally.
10. Presentation, backup and maintenance tooling that depends on the final service inventory should be deployed late rather than repeatedly reworked while the server composition is still changing.

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

Public listener contract:

- TCP/22 — SSH;
- TCP/80 — nginx;
- TCP/443 — Xray;
- UDP/443 — Hysteria2.

Ingress relationships:

- ordinary HTTP -> nginx TCP/80;
- ordinary HTTPS -> Xray TCP/443 TLS fallback -> nginx `127.0.0.1:8080` using Proxy Protocol;
- VLESS clients -> Xray TCP/443;
- Hysteria2 clients -> UDP/443;
- future application HTTP backends should normally bind loopback and be published through nginx rather than directly exposing Docker ports.

nginx intentionally has no direct public TCP/443 listener because Xray owns TCP/443.

### TLS lifecycle

- Certbot/ACME webroot remains the accepted certificate mechanism;
- ACME webroot is `/var/www/letsencrypt`;
- certificate lineage is `/etc/letsencrypt/live/escloud.us`;
- certificate renewal uses the Certbot timer;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync` invokes `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- Xray/Hysteria2 certificate consumers are synchronized from the accepted lineage.

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

A separate temporary private Cloud portal was deliberately not introduced in Stage 1. The accepted requirement is the functioning private auth/ingress boundary; the dedicated Cloud Infrastructure portal is intentionally deferred until the final service inventory and integrations are substantially stable.

### Firewall

Accepted host firewall model:

- UFW active/enabled;
- default deny incoming;
- default allow outgoing;
- default deny routed;
- IPv6 enabled;
- public allows only TCP/22, TCP/80, TCP/443 and UDP/443 for Stage 1;
- Docker firewall integration remains enabled;
- application containers are loopback-published by default.

No additional enterprise network/auth layer is part of Stage 1.

### VPN operations

Accepted operational scripts:

- `/opt/vpn-stack/scripts/maintctl`;
- `/opt/vpn-stack/scripts/vpnctl`.

Accepted convenience entrypoints:

- `/root/maintctl`;
- `/usr/local/bin/maintctl`;
- `/usr/local/bin/vpnctl`.

The restored `maintctl` differs from its preserved source only by the two accepted current certificate-sync paths.

### Stage 1 recovery

Local base-state recovery checkpoint:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

This checkpoint is deliberately same-VPS and is not complete disaster recovery. Future Backrest/Restic/off-site topology remains later-stage work. Stage 0 provider backup and external migration archive remain separate recovery layers.

## Late-stage portal and operations lifecycle

The following sequencing is ACCEPTED because these components depend on a stable server-wide service inventory and operational contract:

1. Complete the functional service deployment and integration stages first.
2. Deploy `app.escloud.us` only near the end, once the complete service structure is known, so it can be built once as the private Cloud Infrastructure home/overview rather than repeatedly reworked.
3. Portal scope is intentionally determined at that late stage from the actual final server structure. Baseline intent is a unified service entry point plus simple useful status/monitoring. The existing `home.lan` implementation is a reference point, not a template that must be copied verbatim. A compact Home Infrastructure monitoring summary may be mirrored into a separate collapsed-by-default portal section if it proves useful and simple.
4. Do not turn the portal into another operational control plane or monitoring stack by default. Prefer simple read-only integrations and existing health/status sources; decide any richer monitoring only when portal implementation begins.
5. Deploy and configure **Backrest before Semaphore testing**. Backup repositories, policies, exclusions, retention and restore acceptance are defined against the substantially complete server state so pre-update backups can be used during maintenance/update testing.
6. Deploy **Semaphore and the maintenance page together** as one operational workstream. The maintenance page should integrate with Semaphore for visible procedure state/control while update workflows are being tested.
7. The existing PVE/Home update tool and maintenance workflow are the accepted engineering reference for the `edge` maintenance implementation. Reuse proven concepts and behavior after audit, but adapt/optimize them for `edge`; do not blindly clone PVE-specific assumptions or implementation.
8. Final integrated acceptance follows Backrest restore acceptance, Semaphore/update-procedure acceptance, maintenance-page integration acceptance and late-stage cleanup.

## Extension boundaries for later stages

Stage 1 reserves, but does not preselect the implementation of, later capabilities:

- future public/private WebUI services: loopback backend -> nginx;
- machine APIs/webhooks: define per consumer when required;
- working storage: `/srv/<service or domain>` once selected;
- monitoring: evaluate from concrete needs; avoid a full metrics stack without demonstrated value;
- Home/PAI connectivity: later-stage concern;
- full private Cloud portal/status UI: late-stage, after the service inventory is substantially complete;
- Backrest/off-site DR: final operations/lifecycle work, before Semaphore/update testing;
- Semaphore + maintenance page: final operations/lifecycle work after Backrest is usable;
- file/sync/Obsidian mechanisms: Stage 4;
- cross-site connectivity: Stage 6.

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
- dedicated `app.escloud.us` Cloud Infrastructure portal replacing Homepage, deployed near the end with final scope defined from the actual service inventory;
- Semaphore + maintenance page replacing the legacy custom Maintenance Center, deployed after Backrest and developed/tested together using the PVE/Home update workflow as the engineering reference.

## Architecture authority

For implementation work, authority order remains:

1. current user instruction;
2. latest applicable ACCEPTED decision/acceptance record;
3. `CURRENT_STATE.md` for confirmed current runtime;
4. this file for accepted architecture/invariants;
5. stage-specific planning documents;
6. `FUNCTIONAL_SCAFFOLD_DRAFT.md` for capability intent;
7. `migration-reference/` and historical baseline for legacy evidence only.

Detailed future-stage proposals are not accepted merely because they once appeared in Git history.
