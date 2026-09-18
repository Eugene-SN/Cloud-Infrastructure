# Cloud Infrastructure — Decision Log

Decision entries are chronological. The latest applicable `ACCEPTED` decision has priority over older conflicting entries. This file retains durable project decisions, not chat transcripts.

---

## 2026-09-14T21:57:00+03:00 — Project taxonomy and historical baseline

**Status:** ACCEPTED

**Decision:**

- project name: **Cloud Infrastructure**;
- future/current VPS node: **`edge`**;
- `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains the historical/as-is snapshot of the pre-rebuild VPS and is not retroactively renamed.

---

## 2026-09-16T13:27:00+03:00 — Accepted core product anchors

**Status:** ACCEPTED

**Decision:** retain unless a concrete incompatibility or changed requirement appears:

- Xray;
- Hysteria2;
- nginx;
- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart + Bulwark.

---

## 2026-09-16T13:27:00+03:00 — Backup management direction

**Status:** ACCEPTED

**Decision:** use Backrest as the backup-management/orchestration layer with Restic as the engine family. Exact repository/off-site topology is decided against the final service/data inventory.

**Supersedes:** treating old same-VPS Restic storage as complete disaster recovery.

---

## 2026-09-16T13:27:00+03:00 — Replace legacy presentation/maintenance surfaces

**Status:** ACCEPTED

**Decision:**

- do not carry legacy Homepage forward; build dedicated `app.escloud.us` late against real inventory/status sources;
- do not carry legacy custom Maintenance Center forward; use Semaphore plus dedicated `update.escloud.us` against the real update backend.

---

## 2026-09-16T14:55:00+03:00 — Historical ai-node canonical / Apple sync assumption

**Status:** SUPERSEDED

**Historical decision:**

- `ai-node:/srv/ai-data/knowledge/obsidian` was treated as the permanent canonical vault;
- Cloud research also included Apple-device Obsidian synchronization and possible LiveSync/WebDAV/iOS-Syncthing mechanisms.

**Superseded by:** `2026-09-18T00:07:00+03:00 — PVE canonical knowledge ownership and Stage 5 integration boundary`.

The old entry remains relevant only as historical/current-runtime context until Home Infrastructure completes its PVE migration.

---

## 2026-09-16T14:55:00+03:00 — Primary GitHub repository

**Status:** ACCEPTED

**Decision:** `Eugene-SN/Cloud-Infrastructure` is the primary persistent-context repository for Cloud Infrastructure. Sensitive recovery/auth material remains outside GitHub.

---

## 2026-09-16T15:00:00+03:00 — Capability scaffold before unresolved product selection

**Status:** ACCEPTED

**Decision:** maintain a capability scaffold first, then research only genuinely unresolved mechanisms. The scaffold is requirements input, not automatic product selection.

---

## 2026-09-16T16:10:00+03:00 — Four application-level capability gaps

**Status:** ACCEPTED

**Decision:** preserve as later workflow requirements:

1. Universal Capture Inbox;
2. human-in-the-loop approvals;
3. mail as automation transport;
4. durable application-level store-and-forward/retry between `edge` and Home/PAI.

These do not authorize a dedicated broker/service by themselves.

---

## 2026-09-16T19:44:00+03:00 — Two-plane migration preservation

**Status:** ACCEPTED

**Decision:**

1. sensitive recovery archive/provider backup outside GitHub;
2. sanitized engineering/migration reference material in GitHub.

Never commit private keys, OAuth/session tokens, credential databases or raw secret-bearing recovery state.

---

## 2026-09-16T20:34:11+03:00 — Clean `edge` rebuild

**Status:** ACCEPTED

**Decision:** clean provider-level Ubuntu rebuild is the migration method. Historical baseline remains immutable and no longer describes live runtime after rebuild.

---

## 2026-09-16T22:13:31+03:00 — Stage-aligned branch lifecycle

**Status:** ACCEPTED

**Decision:** every implementation stage gets its own branch and follows requirements/baseline → selection/reconstruction → deployment contract/recovery path → deployment → verification → acceptance → GitHub persistence/read-back before transition.

---

## 2026-09-16T22:33:00+03:00 — Accepted-first deployment and legacy continuity

**Status:** ACCEPTED

**Decision:**

- accepted product choices are not re-researched without concrete incompatibility;
- preserved legacy implementation is the engineering starting point for accepted carry-forward services;
- Docker + Compose is default for suitable applications;
- host-native placement is allowed where materially simpler or required for host executor/runtime integration;
- actual runtime/configuration outranks recollection/history.

---

## 2026-09-17T20:00:00+03:00 — Lifecycle/presentation deferred until service composition stabilizes

**Status:** ACCEPTED

**Decision:**

- Backrest/restore before Semaphore/update testing;
- Semaphore/update page after substantially complete service inventory;
- monitoring after connectivity/data/backup/update layers substantially exist;
- final portal after monitoring/status sources exist.

---

## 2026-09-17T20:43:00+03:00 — Stage 02.5 remaining-scope reconciliation

**Status:** ACCEPTED

**Decision:** introduce `02.5 — Remaining Functional Scope Reconciliation & Research` as a research-only checkpoint after Stage 2 and before new production deployment.

**Constraint:** no production mutation in Stage 02.5; read-only audits are permitted when factual state is required.

---

## 2026-09-17T21:52:00+03:00 — Hermes selected

**Status:** ACCEPTED, sequencing portion superseded later

**Decision:**

- Hermes Agent is the selected persistent cloud-side agent runtime;
- n8n remains deterministic orchestration;
- CloudCLI remains manual cloud-AI workspace;
- Codex CLI and Antigravity CLI are specialized executors usable manually and delegatable by Hermes;
- OpenClaw remains the Home/PAI local agent;
- Hermes invokes Codex/Antigravity directly rather than through CloudCLI;
- preferred placement is host-native under `core`;
- no public Hermes domain/listener by assumption;
- user-specific workflows remain post-infrastructure.

**Sequencing superseded by:** the NetBird connectivity decision below, which moves connectivity before Hermes so real `Hermes -> vLLM` can be accepted in one stage.

---

## 2026-09-17T23:00:00+03:00 — NetBird private fabric selected; connectivity before Hermes

**Status:** ACCEPTED

Detailed record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

**Decision:**

- reuse existing self-hosted Home NetBird as the bidirectional routed Cloud ↔ Home/PAI private fabric;
- `edge` becomes an ordinary host-native NetBird service peer;
- CT300 remains the Home routing peer;
- `edge` gets Home LAN reachability but not Home Internet `0.0.0.0/0` exit;
- `edge` keeps provider-local public/default Internet;
- Home/PAI clientless hosts reach `edge` via gateway-level routing of `100.105.0.0/16` through CT300 `192.168.1.90`;
- VM100 and MikroTik both receive the route so VRRP ownership does not change private reachability;
- reuse `.lan` split DNS and existing NetBird-managed masquerade before considering duplicate NAT;
- do not deploy direct WireGuard/Tailscale as parallel backbones;
- AmneziaWG is contingency only if real NetBird deployment acceptance proves an unresolved transport/DPI failure.

**Roadmap effect:** Stage 3 = connectivity; Stage 4 = Hermes.

---

## 2026-09-18T00:07:00+03:00 — PVE canonical knowledge ownership and Stage 5 integration boundary

**Status:** ACCEPTED

**Context:** fresh Home data-plane audit and subsequent architecture review established that PVE is the 24/7 Home infrastructure hub, already hosts CT300 NetBird and Home-side file/backup services, while `ai-node` may be intentionally offline. Home and Cloud automation domains will both actively produce knowledge.

Detailed final Stage 02.5 record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

**Decision:**

1. The future canonical Obsidian/knowledge foundation belongs to **Home Infrastructure on PVE**, not Cloud Infrastructure and not permanently to `ai-node`.
2. This planning decision does **not** claim the migration is already live. Until Home Infrastructure explicitly accepts its PVE migration, the existing `ai-node:/srv/ai-data/knowledge/obsidian` remains factual current runtime state.
3. After Home cutover:
   - PVE = canonical live knowledge host / always-on synchronization hub;
   - `ai-node` = active RW synchronized replica and local AI producer/consumer;
   - `edge` = active RW synchronized replica and 24/7 cloud producer/consumer.
4. Home Infrastructure owns PVE storage layout, PVE-side synchronization service, Home file access and Home-side knowledge backup/restore.
5. Personal Agents Infrastructure owns the `ai-node` replica, local paths/permissions and n8n/OpenClaw/vLLM/OCR/RAG integration.
6. Cloud Infrastructure owns only the `edge` replica and n8n/Hermes/cloud-AI integration.
7. Cloud Stage 5 is renamed **`Edge Knowledge Replication & Data Integration`** and is an integration stage, not a second knowledge-platform design project.
8. Stage 5 must begin with an **expanded read-only cross-project audit** of the accepted Home/PVE canonical state, Home-selected sync mechanism, PVE ↔ `ai-node` health, Backrest/restore state, PAI replica state, NetBird non-regression and `edge` storage/consumer requirements.
9. If PVE canonical migration is not accepted when Stage 5 begins, Stage 5 stops before mutation and reconciles the prerequisite rather than creating a parallel canonical/sync architecture.
10. Reuse the Home-accepted server-side synchronization mechanism by default. A second primary sync engine for the same knowledge tree requires concrete incompatibility and explicit superseding acceptance.
11. MacBook/iPhone/iPad Obsidian synchronization is **completely removed from Cloud Infrastructure research/deployment scope** and belongs to a separate late Home Infrastructure user-integration branch.
12. Filestash, SFTPGo, Syncthing or other Cloud-side file/sync products are not selected by assumption; add only when the Stage 5 audit proves a concrete requirement not already met by the Home architecture.

**Supersedes:**

- the permanent `ai-node canonical` portion of the 2026-09-16 Obsidian decision;
- Apple-device synchronization as a Cloud capability/research requirement;
- the old broad Stage 5 data/knowledge scope that mixed server replication with user-device integration.

---

## 2026-09-18T00:07:00+03:00 — Stage 02.5 final closure and roadmap normalization

**Status:** ACCEPTED

**Decision:** Stage 02.5 is complete.

`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`

Final remaining finite infrastructure roadmap:

1. Stage 3 — Edge Cross-site Connectivity Foundation;
2. Stage 4 — Edge Hermes Agent Runtime;
3. Stage 5 — Edge Knowledge Replication & Data Integration;
4. Stage 6 — Edge Backrest & Recovery;
5. Stage 7 — Edge Maintenance & Update;
6. Stage 8 — Edge Monitoring, Heartbeats & Alerts;
7. Stage 9 — Edge Cloud Portal;
8. Stage 10 — Edge Final Integrated Infrastructure Acceptance.

The old conditional `Remaining Infrastructure Services` slot is removed because no additional standalone infrastructure service was selected by Stage 02.5.

Post-infrastructure user-specific n8n/Hermes/agent automation remains a continuous workstream. Apple-device/Obsidian integration belongs to Home Infrastructure rather than that Cloud workstream.

**Intentionally stage-specific / not Stage 02.5 blockers:**

- exact Stage 5 Home-selected sync implementation details, because Home Infrastructure owns and is currently implementing that foundation;
- Cloud Backrest repository/retention details until Stage 6;
- monitoring product/topology until Stage 8;
- exact user automation/workflow implementations until after Stage 10.


---

## 2026-09-18T01:41:36Z — Stage 3 scope normalization: no LAN-wide clientless route to edge

**Status:** ACCEPTED

**Context:** Stage 3 runtime acceptance proved that host-native NetBird on `edge` provides the required `edge -> Home/PAI` private reachability while preserving provider-local Internet egress. The reverse direction does not currently require transparent private routing for arbitrary Home LAN hosts: Cloud services on `edge` are already reachable from Home/PAI through the VPS public IP and the accepted `escloud.us` / service-subdomain ingress. Implementing LAN-wide clientless routing would require production changes to VM100 and MikroTik gateway state without a concrete current workload that benefits from them.

**Decision:**

- keep `edge` as a host-native NetBird service peer with private `edge -> Home/PAI` access through CT300;
- do **not** add `100.105.0.0/16 via 192.168.1.90` to VM100 or MikroTik as part of the baseline Stage 3 implementation;
- do **not** add the corresponding VM100 nftables forwarding rule;
- do **not** create `edge.lan`; Home/PAI access to Cloud services uses the existing public VPS IP or accepted `escloud.us` / service-subdomain names;
- ordinary Home/PAI hosts without NetBird do not receive transparent access to the NetBird overlay by default;
- existing/future hosts that are themselves NetBird peers may use normal peer-to-peer NetBird reachability where useful;
- LAN-wide clientless Home/PAI -> `edge` routing is deferred as an on-demand capability and may be introduced only for a concrete private-only workload where public ingress is unsuitable and adding NetBird to the specific initiating host is less appropriate than gateway-level routing;
- no VM100/MikroTik/VRRP mutation is justified for the current Cloud workload.

**Supersedes:** only the mandatory clientless Home/PAI -> `edge` gateway-routing, VM100/MikroTik route-persistence, and `edge.lan` portions of the 2026-09-17 NetBird connectivity decision. The NetBird product selection, CT300 routing-peer role, `edge -> Home/PAI` private connectivity, and provider-local `edge` Internet egress remain ACCEPTED.
