# Cloud Infrastructure — Decision Log

Decision entries are chronological. The latest applicable `ACCEPTED` decision has priority over older conflicting entries.

---

## 2026-09-14T21:57:00+03:00 — Project taxonomy and legacy baseline

**Status:** ACCEPTED

**Decision:**

- Project name is **Cloud Infrastructure**.
- Future/current VPS node is **`edge`**, a location-agnostic logical name.
- `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains the canonical historical/as-is snapshot of the pre-rebuild VPS.
- Historical names/paths stay unchanged inside historical artifacts; target-state naming applies only to future/current architecture and deployment.

**Supersedes:** older umbrella naming that mixed Home, PAI and VPS scope.

---

## 2026-09-14T23:04:00+03:00 — Service/function composition before topology

**Status:** ACCEPTED

**Decision:** define useful services/functions before committing to network/topology. Legacy runtime is context, not a target template.

**Supersedes:** preliminary network-first/private-backbone-first direction.

---

## 2026-09-14T23:04:00+03:00 — Premature network-first target design

**Status:** REJECTED

**Decision:** a NetBird/private-backbone design was not accepted at that time because real cross-site consumers were not yet known. Any future tunnel choice had to be justified by actual flows and real Russia ↔ external-VPS operating conditions.

**Supersedes:** none; rejected proposal only.

---

## 2026-09-16T13:27:00+03:00 — Accepted core services for future `edge`

**Status:** ACCEPTED

**Decision:** keep these product choices unless a concrete incompatibility or changed requirement appears:

- Xray;
- Hysteria2;
- n8n;
- CloudCLI;
- nginx;
- Stalwart + Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI.

Authelia is the intended common web-login boundary where application semantics permit it. Codex CLI + Antigravity CLI are the accepted subscription/cloud execution tools.

---

## 2026-09-16T13:27:00+03:00 — Backup management direction

**Status:** ACCEPTED

**Decision:** retain Restic as acceptable engine but deploy **Backrest** as the future backup-management/orchestration layer. Final repository/off-site topology is decided after the target service set stabilizes.

**Supersedes:** treating the old same-VPS Restic repository as final disaster recovery.

---

## 2026-09-16T13:27:00+03:00 — VPS file-access requirements; Filestash implementation unresolved

**Status:** ACCEPTED

**Decision:** future file layer must support, as appropriate, MacBook/iPhone/`ai-node` access, web browse/upload/download/edit, and automation/cloud-agent access to the same selected working data. Filestash remains a candidate rather than an accepted implementation.

---

## 2026-09-16T13:27:00+03:00 — Syncthing role remains under review

**Status:** ACCEPTED

**Decision:** evaluate Syncthing separately for general working files, `edge ↔ ai-node` sync, Obsidian and file-based workflow transport. Do not keep it merely because old task execution used files.

---

## 2026-09-16T13:27:00+03:00 — Replace Homepage

**Status:** ACCEPTED

**Decision:** do not carry legacy Homepage forward. Build a dedicated Cloud Infrastructure portal/status page later against the real final inventory.

---

## 2026-09-16T13:27:00+03:00 — Replace custom Maintenance Center

**Status:** ACCEPTED

**Decision:** do not carry the legacy custom Maintenance Center forward. Use Semaphore plus a dedicated maintenance/update page based on the accepted Home/PVE operating pattern.

---

## 2026-09-16T14:55:00+03:00 — Obsidian canonical source and free synchronization requirement

**Status:** ACCEPTED

**Decision:**

- canonical vault remains `ai-node:/srv/ai-data/knowledge/obsidian`;
- `edge` does not become canonical source of truth by assumption;
- synchronization must avoid paid Obsidian Sync and support Apple devices plus `ai-node`;
- possible mechanisms include Self-hosted LiveSync/CouchDB, Remotely Save/WebDAV, Syncthing-compatible iOS approaches or alternatives;
- do not combine multiple primary synchronization mechanisms for the same vault.

---

## 2026-09-16T14:55:00+03:00 — Carry-forward rule for remaining legacy services

**Status:** ACCEPTED

**Decision:** legacy services not explicitly accepted are not carried forward automatically.

---

## 2026-09-16T14:55:00+03:00 — Primary GitHub repository

**Status:** ACCEPTED

**Decision:** `Eugene-SN/Cloud-Infrastructure` is the primary persistent-context repository for Cloud Infrastructure.

**Constraints:** no secrets/credential-bearing recovery bundles in GitHub.

---

## 2026-09-16T15:00:00+03:00 — Functional capability scaffold before domain solution research

**Status:** ACCEPTED

**Decision:** maintain a complete capability scaffold first, then perform focused solution research for unresolved domains. The scaffold is requirements input, not automatic product selection.

---

## 2026-09-16T16:04:00+03:00 — First-pass capability catalog screening

**Status:** ACCEPTED

**Decision:** retain as current capability directions:

- DPI-resistant foreign egress through Xray/Hysteria2;
- nginx public ingress;
- Stalwart + Bulwark mail;
- Authelia web authentication;
- Cloud portal/status page;
- Semaphore maintenance direction;
- Backrest backup direction;
- VPS working-file access and selected synchronization;
- Obsidian sync/mirror role with canonical vault on `ai-node`;
- n8n common automation plane;
- CloudCLI + Codex CLI + Antigravity CLI cloud-AI workspace/execution core;
- long-running cloud coding-agent workflows;
- website-change/document-ingestion automation.

Explicitly avoid duplicating Home/PAI infrastructure merely because it could also run on a VPS. Do not introduce generic job schedulers, SaaS credential gateways, headless-browser stacks, MCP gateways, AI API routers, IoT/media/game hosting or other infrastructure without a concrete consumer.

Several capabilities remained deferred for later research, including monitoring/heartbeats/alerts, password/2FA, bots, supervised research, cross-site handoff/connectivity and limited failover.

---

## 2026-09-16T16:10:00+03:00 — Four capability gaps added to the scaffold

**Status:** ACCEPTED

**Decision:** add:

1. Universal Capture Inbox;
2. human-in-the-loop approvals;
3. mail as automation transport;
4. durable application-level store-and-forward/retry between `edge` and Home/PAI.

**Constraints:** these do not by themselves authorize dedicated services or a message broker; reuse n8n/mail/existing interfaces where sufficient.

---

## 2026-09-16T16:56:26+03:00 — Migration preservation archive may include credentials

**Status:** ACCEPTED

**Decision:** the manually retained migration-preservation archive may contain complete sensitive service state required for faithful recovery/migration, including credentials/private keys/auth state, but must remain outside GitHub.

---

## 2026-09-16T19:44:00+03:00 — Two-plane migration preservation model

**Status:** ACCEPTED

**Decision:** use:

1. **Recovery plane** — full sensitive archive outside GitHub plus provider backup;
2. **Engineering-context plane** — sanitized/redacted `migration-reference/` material in the private GitHub repo.

Never commit private keys, OAuth/session tokens, credential databases or raw secret-bearing recovery state.

---

## 2026-09-16T20:34:11+03:00 — Clean `edge` rebuild and substrate acceptance

**Status:** ACCEPTED

**Decision:** clean provider-level Ubuntu rebuild is the migration method. `edge` is now live on Ubuntu 26.04.1 LTS with accepted SSH/network/swap/substrate behavior. `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`.

Historical baseline remains immutable and no longer describes live runtime.

---

## 2026-09-16T21:44:20+03:00 — Implementation chronology and branch/stage distinction

**Status:** SUPERSEDED

**Historical decision:** attempted to treat branch 01 as complete too early and introduce separate functional-composition/architecture branches.

**Superseded by:** `2026-09-16T22:13:31+03:00 — Stage-aligned branch lifecycle and rollback to unfinished Stage 1`.

---

## 2026-09-16T22:13:31+03:00 — Stage-aligned branch lifecycle and rollback to unfinished Stage 1

**Status:** ACCEPTED

**Decision:** every implementation stage has its own branch and must complete requirements → selection → stage composition → deployment contract → deployment → verification → acceptance → GitHub persistence before transition. Do not preselect unresolved future products merely to complete a diagram.

The then-current historical Stage 3–7 grouping was accepted for that checkpoint but was later superseded by Stage 02.5 dependency-aware planning.

---

## 2026-09-16T22:33:00+03:00 — Accepted-first deployment order and legacy implementation continuity

**Status:** ACCEPTED

**Decision:**

- separate accepted baseline from genuinely unresolved choices;
- deploy dependency-ready accepted components without re-running unrelated product research;
- preserved legacy implementation is the engineering starting point for accepted carry-forward services;
- Docker + Compose is default for suitable application services;
- host-native is allowed where materially simpler/better aligned with runtime integration;
- historical versions are evidence, not target pins;
- actual runtime/configuration outranks recollection.

---

## 2026-09-17T20:00:00+03:00 — Defer portal and operations lifecycle until service composition stabilizes

**Status:** ACCEPTED

**Decision:**

- move Backrest, Semaphore, maintenance/update UI and `app.escloud.us` out of Stage 2;
- deploy Backrest against a substantially complete server and prove restore before Semaphore/update testing;
- use PVE/Home update tooling as an engineering reference, not a blind copy;
- build maintenance/update page against the real Semaphore/update contract;
- build the final portal late against the actual inventory/status sources.

**Constraints:** Backrest-before-Semaphore is mandatory.

---

## 2026-09-17T20:43:00+03:00 — Stage 02.5 full remaining-scope reconciliation

**Status:** ACCEPTED

**Decision:** introduce `02.5 — Remaining Functional Scope Reconciliation & Research` as a research-only checkpoint after accepted Stage 2 and before further production deployment.

**Constraints:** no production mutation in Stage 02.5; read-only runtime inspection is permitted when factual state is required for a decision.

---

## 2026-09-17T21:05:00+03:00 — Dependency-aware post-Stage-2 roadmap and infrastructure/workflow separation

**Status:** ACCEPTED

**Decision:** remaining work follows dependency direction:

- standalone core services and connectivity before dependent data/knowledge services;
- Backrest before update testing;
- monitoring after stable inventory/connectivity/lifecycle layers;
- portal after monitoring/status sources;
- final integrated infrastructure acceptance before ongoing user-specific automation/workflows.

User-specific Capture Inbox, approvals, mail-triggered automation, research jobs, durable task handoff and messaging commands belong to a continuous post-infrastructure workstream.

---

## 2026-09-17T21:52:00+03:00 — Hermes selected and initial numbered dependency-aware roadmap

**Status:** ACCEPTED, with sequencing portion later superseded

**Context:** Stage 02.5 established that Hermes has a distinct persistent-agent role separate from n8n and the manual CloudCLI/Codex/Antigravity workspace.

**Decision:**

1. **Hermes Agent is SELECTED** as the only additional standalone core service.
2. Role separation:
   - n8n = deterministic automation/orchestration;
   - Hermes = persistent agentic reasoning/tool use/supervision/delegation;
   - CloudCLI = manual cloud-AI workspace;
   - Codex CLI and Antigravity CLI = specialized executors usable manually and delegatable by Hermes;
   - OpenClaw = Home/PAI local personal agent;
   - vLLM on `ai-node` = local inference backend for Hermes after private connectivity exists.
3. Hermes invokes supported Codex/Antigravity executors directly; CloudCLI is not a proxy.
4. Preferred Hermes placement is **host-native under `core`** because containerization would complicate reuse of host-native binaries/auth/runtime context.
5. Hermes does not receive a public domain/listener by assumption.
6. User-specific Hermes/n8n workflows remain post-infrastructure work.

**Historical sequencing portion:** this entry initially placed Hermes in Stage 3 and connectivity in Stage 4, with `Hermes -> vLLM` deferred.

**Superseded by:** `2026-09-17T23:00:00+03:00 — NetBird private fabric selected; connectivity moves before Hermes` for stage numbering/dependency order only. Hermes product/role/placement decisions remain ACCEPTED.

---

## 2026-09-17T23:00:00+03:00 — NetBird private fabric selected; connectivity moves before Hermes

**Status:** ACCEPTED

**Context:** Stage 02.5 cross-site connectivity research was completed after a fresh read-only audit of Home Infrastructure networking, VM100, CT300 and the self-hosted NetBird control plane. The audit proved the existing Home NetBird architecture is already designed for both Home-LAN access and optional Home Internet Exit for user devices, with separate routing behavior. The user also requires Home/PAI services to initiate private connections toward `edge`, not only `edge -> Home` access.

Detailed acceptance record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

**Audited factual baseline:**

- Home LAN is `192.168.1.0/24`.
- CT300 `remote-access` is `192.168.1.90/24`.
- NetBird routing peer is `100.105.97.126/16`.
- NetBird account IPv4 overlay is `100.105.0.0/16`.
- Current NetBird uses the `Networks` model; legacy routes are empty.
- Existing `Home Network` resources are `Home LAN 192.168.1.0/24` and `Internet 0.0.0.0/0`.
- `Routing Peers` contains only `netbird-router`.
- `User Devices` contains interactive remote devices and is the source of current Home-LAN and Home-Internet policies.
- Existing NetBird DNS sends match domain `lan` to `192.168.1.1:53`, with search-domain behavior enabled and no NetBird primary-DNS override.
- CT300's own default route is via MikroTik `192.168.1.1`.
- NetBird traffic arriving through `wt0` uses policy table `6300`, whose default route is via VRRP VIP `192.168.1.254`.
- Existing relay `rels://netbird.encores.ru:443` is available via WebSocket/TCP 443 and STUN is available on UDP 3478.

**Decision:**

1. Reuse the existing self-hosted Home NetBird as the **bidirectional routed private fabric** between Cloud Infrastructure and Home/PAI.
2. `edge` becomes an ordinary **host-native NetBird service peer**. CT300 remains the Home routing peer.
3. `edge` receives access to the existing `Home LAN 192.168.1.0/24` resource but **must not receive** the existing Home `Internet 0.0.0.0/0` resource.
4. `edge` therefore retains direct provider-local Internet/default routing for public services, mail, cloud providers, Xray/Hysteria2 and normal outbound traffic.
5. Home/PAI clientless hosts reach `edge` through gateway-level routing of `100.105.0.0/16` via CT300 `192.168.1.90`.
6. That route must be implemented on both VM100 and MikroTik so VRRP ownership does not change private reachability.
7. VM100 should receive only the narrow forwarding allowance required for LAN → NetBird-account traffic.
8. CT300 already exposes NetBird-managed marking/masquerade behavior compatible with Site-to-VPN traffic. Reuse and verify it first; do not add a duplicate manual NAT rule unless implementation evidence proves it necessary.
9. NetBird clients on PVE, `ai-node`, CT220 or other Home guests are **not** baseline requirements. Add an individual peer only when a concrete consumer needs direct peer identity/P2P semantics that routed access cannot provide.
10. Reuse the existing Home `.lan` namespace through NetBird split DNS. `edge` uses `192.168.1.1:53` only for match domain `lan`; general Internet DNS stays on the VPS's normal resolver path.
11. After Stage 3 enrollment/routing acceptance, add `edge.lan` through the existing canonical Home DNS mechanism, mapped to the stable NetBird address of `edge`.
12. Existing `*.escloud.us` names remain the public/service namespace; `.lan` is the private infrastructure namespace.
13. Direct WireGuard and Tailscale are rejected as duplicate parallel backbones. AmneziaWG remains contingency only if real NetBird deployment acceptance demonstrates an unresolved transport/DPI failure.
14. The existing remote-user Home Internet Exit remains separate from `edge`: CT300 policy-routes NetBird `wt0` Internet traffic through VRRP VIP `192.168.1.254`, normally reaching VM100/Mihomo; `edge` is not placed in the policy that owns that `0.0.0.0/0` resource.
15. A controlled real VRRP failover test remains a Stage 3 implementation acceptance item. Research does not claim E2E failover PASS merely from routing-table inspection.

**Roadmap change:**

- **Stage 3 becomes `03 — Edge Cross-site Connectivity Foundation`.**
- **Stage 4 becomes `04 — Edge Hermes Agent Runtime`.**
- Stage 5 and later retain their existing relative order, subject to the already accepted conditional Stage 6 removal/renumbering rule.

**Reason for swap:** connectivity is now a known prerequisite. Deploying it first allows Stage 4 Hermes to close the complete infrastructure contract in one stage, including both cloud executors and local vLLM, instead of deliberately leaving `Hermes -> vLLM` unfinished.

**Stage boundary:**

- Stage 3 owns NetBird enrollment, policies/routes, private DNS, reachability, real direct/relay behavior, reboot persistence, non-regression and controlled VRRP acceptance.
- Stage 3 does not own consumer-specific vLLM bind/provider configuration beyond proving `ai-node` reachability.
- Stage 4 owns Hermes deployment plus `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`, inspection/minimal private exposure of the real `ai-node` vLLM endpoint, and verified `Hermes -> vLLM` inference over the Stage 3 fabric.

**Constraints:**

- Stage 02.5 remains ACTIVE / RESEARCH-ONLY; this decision authorizes no production networking/DNS/firewall/runtime mutation yet.
- No Stage 3 deployment branch opens until complete Stage 02.5 deliverables are accepted and canonical project files are read back.
- Backrest-before-Semaphore remains mandatory.
- Production monitoring remains late-stage.
- `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

**Supersedes:**

- only the Stage 3/Stage 4 sequencing and deferred-local-vLLM portions of `2026-09-17T21:52:00+03:00 — Hermes selected and initial numbered dependency-aware roadmap`;
- the unresolved connectivity-mechanism status from earlier Stage 02.5 planning;
- any current-plan interpretation that private Cloud ↔ Home/PAI access should be asymmetric or should require a second overlay stack.