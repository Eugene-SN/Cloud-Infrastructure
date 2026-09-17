# Cloud Infrastructure — Architecture State

## Status

**Stage 0:** COMPLETE / ACCEPTED.  
**Stage 1:** COMPLETE / ACCEPTED.  
**Stage 2:** COMPLETE / ACCEPTED.  
**Stage 02.5:** ACTIVE / RESEARCH-ONLY.

Current work branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

Stage 3 composition is now selected as Hermes-only, but Stage 3 production work does not begin until all Stage 02.5 research/deliverables are accepted.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them without a concrete requirement.
2. `edge` must remain independently useful without Home/PAI connectivity.
3. The canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes it.
4. VPN/DPI-bypass functionality and any future private infrastructure backbone are separate concerns.
5. Single-operator simplicity is preferred over enterprise-style complexity without demonstrated need.
6. Unresolved future products/mechanisms are selected from concrete requirements rather than precommitted globally.
7. Post-Stage-2 deployment order follows dependency direction: independent services first, connectivity before connectivity-dependent services, then lifecycle/monitoring/presentation layers over the substantially complete infrastructure.
8. User-specific n8n/agent workflows are an application layer above the finite infrastructure framework and do not block final infrastructure acceptance.
9. Presentation, backup, monitoring and maintenance tooling that depends on the final service inventory is deployed late rather than repeatedly reworked while the server composition changes.
10. Fresh verified runtime/configuration outranks historical reference when factual state differs.

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

Public listener contract includes:

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

### Public masking surface

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

### Stage 1 recovery

Local base-state recovery checkpoint:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

This checkpoint is same-VPS only and is not complete disaster recovery. Future Backrest/Restic/off-site topology remains later-stage work. Stage 0 provider backup and external migration archive remain separate recovery layers.

## Accepted Stage 2 application architecture

The production application anchors are deployed and accepted:

- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark.

These products are not reopened for replacement research without a concrete incompatibility or changed requirement.

## Accepted Cloud AI role separation

The Cloud AI plane now has explicit role boundaries:

- **n8n** — deterministic automation/orchestration plane: schedules, webhooks, mail/API triggers, stateful workflow routing and integration plumbing;
- **Hermes** — selected persistent cloud-side agent runtime for agentic reasoning, tool use, supervisory logic and delegation;
- **CloudCLI** — manual web/remote Cloud AI workspace for the user;
- **Codex CLI** — specialized OpenAI coding/agent executor, usable manually and as a Hermes delegate;
- **Antigravity CLI / `agy`** — specialized Google cloud-agent/coding executor, usable manually and as a Hermes delegate;
- **OpenClaw in Home/PAI** — local personal-agent role centered on local models and Home/PAI resources;
- **vLLM on `ai-node`** — local OpenAI-compatible inference backend, exposed to Hermes only after the cross-site connectivity foundation is accepted.

CloudCLI is not an execution proxy between Hermes and Codex/Antigravity. Hermes should invoke supported providers/executors directly.

## Stage 3 — Hermes Agent Runtime architecture

**Product:** Hermes Agent — SELECTED.

**Role:** persistent cloud agent on `edge`, running in parallel with n8n rather than replacing it.

### Placement

Preferred placement is **host-native under shared service account `core`**.

This is an accepted exception to Docker-by-default because Hermes must directly reuse the already installed host-native Codex and Antigravity executors and their user/runtime context. A container would add avoidable binary/auth/keyring/runtime bridging and therefore be more complex for this use case.

Reconsider containerization only if Stage 3 finds a concrete upstream support or compatibility requirement that makes host-native materially worse.

### Stage 3 integration boundary

Stage 3 establishes infrastructure-level integration, not user-specific automations.

Target contract:

```text
Internet / schedule / mail / webhook
                |
               n8n
                |
        deterministic steps
                |
                v
             Hermes
        agentic reasoning
          +-----+-----+
          |     |     |
          v     v     v
        Codex   AGY   vLLM
          |             ^
          v             |
       result     enabled after Stage 4
          |
          v
         n8n
          |
notification / storage / next step
```

Stage 3 should verify the local infrastructure path `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n` with a minimal acceptance workflow that contains no user-specific business logic.

The `Hermes -> vLLM` branch is part of the target architecture but is not implemented until Stage 4 provides accepted `edge ↔ ai-node` connectivity.

No public Hermes domain/listener is assumed. Ingress/API exposure, if required, must be justified by the Stage 3 deployment contract and should remain private/loopback where possible.

## Planned dependency-aware remaining architecture

### Stage 4 — Cross-site Connectivity Foundation

Before deploying services whose correctness depends on Home/PAI, determine the real flows and establish the minimum required connectivity among:

- `edge`;
- `ai-node`;
- PVE/Home Infrastructure.

NetBird, direct WireGuard, authenticated HTTPS or another transport remain unresolved until evaluated against actual flows and real Russia ↔ external-VPS operating conditions.

Connectivity foundation means transport/reachability/endpoints. Application-level durable queues/retry state machines are separate later workflow concerns.

Stage 4 also activates the previously deferred Hermes -> local vLLM path after connectivity acceptance.

### Stage 5 — Cross-site Data & Knowledge Services

Only after Stage 4 acceptance should the project deploy selected implementations for:

- VPS working-file access;
- MacBook/iPhone/iPad/`ai-node` access;
- web file management;
- selected-directory synchronization;
- Obsidian synchronization or relay/mirror role.

Canonical Obsidian remains `ai-node:/srv/ai-data/knowledge/obsidian`.

### Stage 6 — Remaining Infrastructure Services

This is a conditional slot only. Use it if Stage 02.5 selects another full infrastructure service whose dependencies are satisfied after Stage 5 and which does not belong to backup/update/monitoring/portal layers.

Do not create an empty deployment branch merely to preserve numbering. If this slot is empty at Stage 02.5 closure, remove it and normalize subsequent numbering before Stage 3 opens.

### Stage 7 — Backrest & Recovery

Backrest using Restic remains the accepted backup-management direction.

Its implementation must define backup scope, repository destinations, exclusions, retention, schedules, off-site topology and verified restore procedures against the substantially complete server.

Backrest restore acceptance must precede Semaphore/update testing.

### Stage 8 — Semaphore & dedicated maintenance/update page

Semaphore remains the accepted operational execution product. It is developed/tested with the maintenance/update workflow using the existing PVE/Home updater as an engineering reference, after audit and adaptation for `edge`.

`update.escloud.us` is a separate custom UI responsibility from `app.escloud.us`.

A dedicated Codex substage builds `update.escloud.us` only after the real Semaphore/update backend, status model and control contract are known.

### Stage 9 — Infrastructure-wide Monitoring, Heartbeats & Alerts

Production monitoring is late-stage so it can cover the actual stable inventory in one pass rather than being repeatedly revisited.

Potential scope includes:

- `edge` service availability;
- external checks;
- cross-site connectivity;
- selected Home/PVE/`ai-node` heartbeats;
- file/sync health where useful;
- Backrest job/backup health;
- Semaphore/update health/state;
- alert delivery.

Avoid a heavyweight metrics/logging stack unless concrete requirements justify it.

### Stage 10 — `app.escloud.us` Cloud Portal

Build after monitoring/status sources and final service inventory are accepted.

Its role is unified navigation and concise infrastructure/status presentation, not another operational control plane. Detailed update controls remain on `update.escloud.us`.

A dedicated Codex substage builds `app.escloud.us` against accepted service URLs and status interfaces.

### Stage 11 — Final Integrated Infrastructure Acceptance

Final server-wide acceptance occurs only after:

- all selected infrastructure services;
- cross-site connectivity and data/knowledge integration;
- Backrest restore acceptance;
- Semaphore/update acceptance;
- `update.escloud.us` acceptance;
- monitoring/alert acceptance;
- `app.escloud.us` acceptance;
- final cleanup.

Stage 11 closes the finite infrastructure build.

## Post-infrastructure automation/workflow layer

User-specific automation begins after Stage 11 and evolves continuously rather than defining infrastructure completeness.

This workstream may include:

- Universal Capture Inbox — user submission of URLs/text/files/images into workflows;
- human-in-the-loop approvals;
- mail-triggered workflows;
- continuous information intake/change detection;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for real cross-site tasks;
- messaging/bot command surfaces;
- orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

The infrastructure stages provide stable execution/transport/storage primitives but do not prebuild these user workflows.

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
- Antigravity CLI;
- Hermes Agent.

Additional accepted directions:

- Hermes host-native under `core` by default;
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