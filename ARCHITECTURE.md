# Cloud Infrastructure — Architecture State

## Status

**Stage 0:** COMPLETE / ACCEPTED.  
**Stage 1:** COMPLETE / ACCEPTED.  
**Stage 2:** COMPLETE / ACCEPTED.  
**Stage 02.5:** ACTIVE / RESEARCH-ONLY.

Current work branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

Cross-site Connectivity Foundation research is now **COMPLETE / SELECTED**. Hermes remains selected, but the deployment order is intentionally changed so connectivity is implemented first.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them without a concrete requirement.
2. `edge` must remain independently useful without Home/PAI connectivity.
3. The canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian` unless a later ACCEPTED decision changes it.
4. VPN/DPI-bypass functionality and the private infrastructure backbone are separate concerns.
5. Single-operator simplicity is preferred over enterprise-style complexity without demonstrated need.
6. Fresh verified runtime/configuration outranks historical reference when factual state differs.
7. Post-Stage-2 deployment order follows dependency direction.
8. User-specific n8n/agent workflows are an application layer above the finite infrastructure framework and do not block final infrastructure acceptance.
9. Presentation, backup, monitoring and maintenance tooling that depends on the final service inventory is deployed late rather than repeatedly reworked while the server composition changes.

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

### Public ingress

Public listener contract includes:

- TCP/22 — SSH;
- TCP/80 — nginx;
- TCP/443 — Xray;
- UDP/443 — Hysteria2;
- TCP/25 — SMTP;
- TCP/465 — SMTPS submission;
- TCP/993 — IMAPS.

Ordinary HTTPS reaches Xray TCP/443 and falls back to nginx loopback; application HTTP backends normally bind loopback and are published through nginx rather than directly exposing Docker ports.

### TLS lifecycle

- Certbot/ACME webroot remains the accepted certificate mechanism;
- ACME webroot is `/var/www/letsencrypt`;
- certificate lineage is `/etc/letsencrypt/live/escloud.us`;
- renewal uses the Certbot timer;
- deploy hooks synchronize/reload Xray, Hysteria2 and Stalwart certificate consumers.

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

## Accepted Stage 2 application architecture

Production anchors are deployed and accepted:

- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark.

These products are not reopened for replacement research without a concrete incompatibility or changed requirement.

## Accepted Cloud AI role separation

- **n8n** — deterministic automation/orchestration plane: schedules, webhooks, mail/API triggers, stateful workflow routing and integration plumbing;
- **Hermes** — selected persistent cloud-side agent runtime for agentic reasoning, tool use, supervisory logic and delegation;
- **CloudCLI** — manual web/remote Cloud AI workspace for the user;
- **Codex CLI** — specialized OpenAI coding/agent executor, usable manually and as a Hermes delegate;
- **Antigravity CLI / `agy`** — specialized Google cloud-agent/coding executor, usable manually and as a Hermes delegate;
- **OpenClaw in Home/PAI** — local personal-agent role centered on local models and Home/PAI resources;
- **vLLM on `ai-node`** — local OpenAI-compatible inference backend consumed by Hermes only after the accepted private connectivity foundation is deployed.

CloudCLI is not an execution proxy between Hermes and Codex/Antigravity. Hermes should invoke supported providers/executors directly.

# Accepted Cross-site Connectivity Architecture

Detailed acceptance record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

## Technology choice

Reuse the existing self-hosted Home NetBird as the bidirectional routed private fabric for Cloud ↔ Home/PAI.

Do not create a second parallel WireGuard/Tailscale backbone without a demonstrated failure of the accepted design.

## Audited Home baseline

Fresh read-only audit established:

- Home LAN `192.168.1.0/24`;
- CT300 `remote-access` at `192.168.1.90`;
- NetBird routing peer at `100.105.97.126/16`;
- NetBird account IPv4 overlay `100.105.0.0/16`;
- current NetBird `Networks` model is in use; legacy routes are empty;
- `Home LAN` resource is `192.168.1.0/24`;
- `Internet` resource is `0.0.0.0/0`;
- only interactive `User Devices` receive the current Internet-via-Home and Home-LAN policies;
- CT300's own default route is via MikroTik `192.168.1.1`;
- traffic arriving from NetBird `wt0` is policy-routed through table `6300`, whose default is VRRP VIP `192.168.1.254`;
- current NetBird split DNS sends only `lan` to `192.168.1.1:53` and does not make Home DNS the general resolver.

## Private routed fabric

Target topology:

```text
                         NetBird private fabric
                            100.105.0.0/16
                                   |
                 +-----------------+-----------------+
                 |                                   |
               edge                                CT300
         ordinary service peer               existing routing peer
                 |                             192.168.1.90
                 |                                   |
                 |                           Home LAN 192.168.1.0/24
                 |                           /        |        \
                 |                         PVE     ai-node    CT220...
                 |
         direct VPS Internet
         remains provider-local
```

This is routed L3 connectivity, not an L2 bridge.

### `edge -> Home/PAI`

`edge` is enrolled as a host-native NetBird service peer in a dedicated Cloud Infrastructure service group.

It receives access to `Home LAN 192.168.1.0/24` through CT300, but **does not receive** the Home `Internet 0.0.0.0/0` resource.

Therefore:

- private Home/PAI traffic uses NetBird;
- `edge` public/default Internet remains directly through its VPS provider;
- Xray, Hysteria2, nginx, mail and cloud-AI provider egress stay provider-local.

### `Home/PAI -> edge`

Ordinary Home/PAI hosts do not need individual NetBird clients by default.

Use gateway-level routing of the NetBird account network:

```text
100.105.0.0/16 via 192.168.1.90
```

The route must exist on both VM100 and MikroTik so VRRP ownership does not change private reachability.

VM100 requires only the narrow LAN-to-NetBird-account forwarding exception needed for this route.

CT300 already exposes NetBird-managed marking/masquerade behavior consistent with Site-to-VPN traffic; implementation must first reuse and verify it rather than adding duplicate manual NAT by assumption.

Install individual NetBird peers on PVE, `ai-node`, CT220 or other Home guests only when a concrete consumer needs direct peer identity/P2P semantics that routed access cannot provide.

## VRRP relationship

The private `edge -> Home LAN` path through CT300 does not depend on the VRRP VIP because `192.168.1.0/24` is directly connected on CT300.

The existing User Devices Internet Exit deliberately does use VRRP:

```text
Remote User Device -> NetBird -> CT300 -> 192.168.1.254 -> VM100/Mihomo normally
```

If VM100 fails and the VIP moves to MikroTik, address-level exit continuity can remain while Mihomo-specific routing naturally disappears with VM100. A controlled end-to-end failover test belongs to Stage 3 deployment acceptance.

## Private DNS

Reuse the existing Home `.lan` namespace and NetBird split-DNS:

- `*.lan` from `edge` resolves through `192.168.1.1:53`;
- ordinary Internet DNS on `edge` remains VPS-local;
- no new DNS server is introduced;
- after NetBird enrollment/routing acceptance, add `edge.lan` through the existing canonical Home DNS mechanism, mapped to the stable NetBird address of `edge`.

Public `*.escloud.us` names remain a separate Internet-facing namespace.

Expected private naming model:

```text
edge -> ai-node.lan
edge -> pve.lan
Home/PAI -> edge.lan
```

## Transport fallback

Reuse the existing self-hosted NetBird management/signal/relay plane, including relay availability via TCP/443/WebSocket. Real Stage 3 acceptance must observe actual direct/relay behavior on the target path rather than assume protocol behavior.

Direct WireGuard and Tailscale are rejected as duplicate parallel backbones. AmneziaWG remains contingency only if real NetBird deployment acceptance demonstrates an unresolved transport/DPI failure.

# Planned dependency-aware remaining architecture

## Stage 3 — Cross-site Connectivity Foundation

Deploy the accepted NetBird fabric before connectivity-dependent applications.

Stage 3 owns:

- host-native NetBird enrollment on `edge`;
- Cloud service-peer grouping/policy;
- Home LAN access without Home Internet Exit;
- Home/PAI-to-`edge` route through CT300;
- VM100/MikroTik route and narrow forwarding changes;
- `.lan` split DNS and `edge.lan` private naming;
- direct/relay, reboot-persistence, non-regression and controlled VRRP acceptance.

Stage 3 does **not** own vLLM service/provider configuration beyond proving reachability to `ai-node`.

## Stage 4 — Hermes Agent Runtime

**Product:** Hermes Agent — SELECTED.

Preferred placement is host-native under shared service account `core` because Hermes must directly reuse host-native Codex/Antigravity executors and their user/runtime context.

Stage 4 establishes infrastructure-level integration, not user-specific automations.

Target contract:

```text
Internet / schedule / mail / webhook
                |
               n8n
                |
                v
             Hermes
        agentic reasoning
          +-----+-----+
          |     |     |
          v     v     v
        Codex   AGY   vLLM
          |            ^
          v            |
       result      ai-node over
          |         Stage 3 fabric
          v
         n8n
```

Stage 4 must verify:

- `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- the current `ai-node` vLLM bind/exposure state;
- the minimum required private vLLM exposure through the accepted Stage 3 fabric;
- actual `Hermes -> vLLM` inference.

No public Hermes domain/listener is assumed. User-specific Hermes/n8n workflows remain post-infrastructure work.

## Stage 5 — Cross-site Data & Knowledge Services

After Stage 3 connectivity and Stage 4 Hermes acceptance, deploy selected implementations for:

- VPS working-file access;
- MacBook/iPhone/iPad/`ai-node` access;
- web file management;
- selected-directory synchronization;
- Obsidian synchronization or relay/mirror role.

Canonical Obsidian remains `ai-node:/srv/ai-data/knowledge/obsidian`.

## Stage 6 — Remaining Infrastructure Services

Conditional slot only. Use it only if Stage 02.5 selects another full infrastructure service whose dependencies are satisfied after Stage 5 and which does not belong to backup/update/monitoring/portal layers.

Do not create an empty branch merely to preserve numbering. If empty at Stage 02.5 closure, remove it and normalize subsequent numbering before Stage 3 opens.

## Stage 7 — Backrest & Recovery

Backrest using Restic remains the accepted backup-management direction. Restore acceptance must precede Semaphore/update testing.

## Stage 8 — Semaphore & dedicated maintenance/update page

Semaphore remains the accepted operational execution product. `update.escloud.us` is a separate custom UI responsibility from `app.escloud.us` and is built in its own Codex substage only after the real backend/status/control contract exists.

## Stage 9 — Infrastructure-wide Monitoring, Heartbeats & Alerts

Production monitoring remains late-stage so it can cover the actual stable inventory in one pass. Avoid a heavyweight metrics/logging stack unless concrete requirements justify it.

## Stage 10 — `app.escloud.us` Cloud Portal

Build after monitoring/status sources and final service inventory are accepted. Its role is unified navigation and concise infrastructure/status presentation, not another operational control plane.

## Stage 11 — Final Integrated Infrastructure Acceptance

Final server-wide acceptance occurs only after all selected infrastructure services, cross-site integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.

## Post-infrastructure automation/workflow layer

User-specific automation begins after Stage 11 and evolves continuously rather than defining infrastructure completeness. It may include Capture Inbox, approvals, mail-triggered workflows, continuous information intake/change detection, bounded AI research, durable application-level cross-site task handoff, messaging/bot surfaces and orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

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
- Hermes Agent;
- existing self-hosted NetBird for Cloud ↔ Home/PAI private connectivity.

Additional accepted directions:

- Hermes host-native under `core` by default;
- Backrest using Restic for backup management;
- Semaphore for operational execution;
- dedicated `update.escloud.us` maintenance/update page;
- infrastructure-wide monitoring after main inventory/lifecycle services exist;
- dedicated `app.escloud.us` portal after monitoring/status sources are accepted.

## Architecture authority

For implementation work, authority order remains:

1. current user instruction;
2. latest applicable ACCEPTED decision/acceptance record;
3. `CURRENT_STATE.md` for confirmed current runtime;
4. this file for accepted architecture/invariants;
5. `IMPLEMENTATION_PHASES.md` and stage-specific planning documents;
6. `FUNCTIONAL_SCAFFOLD_DRAFT.md` for capability intent;
7. `migration-reference/` and historical baseline for legacy evidence only.