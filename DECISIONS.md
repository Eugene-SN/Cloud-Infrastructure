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


---

## 2026-09-18T04:48:18Z — Disable unnecessary Docker live-restore on `edge`

**Status:** ACCEPTED

**Context:** Stage 3 reboot acceptance exposed an abnormal late-shutdown delay of about 90 seconds. Differential audit showed that Stage 1 had explicitly configured Docker `live-restore: true`. On the current `edge` runtime, Docker/containerd stopped while four `containerd-shim-runc-v2` processes remained in the containerd cgroup, and the next kernel boot was delayed by approximately the systemd 90-second shutdown timeout.

**Decision:**

- `/etc/docker/daemon.json` uses `"live-restore": false`;
- production containers continue to use `restart: unless-stopped` for normal reboot persistence;
- do not change systemd/containerd `KillMode`, remove `fwupd`/mdadm, or pin/downgrade Docker/containerd for this issue;
- retain current stable Docker/containerd versions unless a separate concrete incompatibility appears.

**Acceptance evidence:**

- Docker reload applied the change without restarting any production container;
- after a normal reboot, kernel + initrd + userspace completed in `13.842s`;
- previous-journal-stop to new-kernel gap fell from approximately 94 seconds to `4.203s`;
- Docker and containerd returned active;
- Authelia, Bulwark, n8n and Stalwart returned automatically under `restart=unless-stopped`;
- system state was `running` with zero failed units.

Detailed record: `EDGE_REBOOT_LIFECYCLE_FIX_ACCEPTANCE_2026-09-18.md`.

**Supersedes:** only the `live-restore: true` runtime property from the Stage 1 Docker/final acceptance state. Stage 1 historical acceptance records remain unchanged as historical evidence.


---

## 2026-09-18T04:58:00Z — Stage 3 final cross-site connectivity acceptance

**Status:** ACCEPTED

**Decision:** Stage 3 — Edge Cross-site Connectivity Foundation is complete.

Final record:

`STAGE_03_ACCEPTANCE_2026-09-18.md`

Final acceptance:

`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted current contract:

- host-native NetBird `0.78.2` on `edge`;
- `edge` overlay IPv4 `100.105.178.187/16`;
- CT300 remains the Home routing/control-plane peer at overlay `100.105.97.126/16`;
- `edge -> Home/PAI` uses the private NetBird routed path for `192.168.1.0/24`;
- `edge` consumes Home `.lan` split DNS and keeps provider-local public/default Internet;
- `edge` does not receive the Home Internet `0.0.0.0/0` resource;
- baseline Home/PAI -> Cloud access remains public VPS IPv4 / `escloud.us` service ingress;
- VM100 and MikroTik remain unchanged; LAN-wide clientless overlay routing is deferred until a concrete private-only workload requires it;
- no `edge.lan` record is created.

Final reboot evidence:

- edge boot completed in `14.881s`;
- wait-online persistence PASS;
- public IPv4-only ens3 state PASS;
- NetBird autostart/control/P2P PASS;
- Home route and split-DNS persistence PASS;
- 30/30 zero-loss traffic to CT300 overlay, PVE and `ai-node`;
- synchronized CT300 watcher measured working P2P recovery approximately `13.187s` from actual edge boot and 0% post-recovery packet loss.

The independent Docker reboot-lifecycle regression discovered during Stage 3 is resolved by the separately accepted `live-restore=false` correction.

**Roadmap effect:** Stage 4 — Edge Hermes Agent Runtime is the next production stage.

---

## 2026-09-18T08:05:00+03:00 — Stage 4 Hermes WebUI and macOS Remote Gateway contract correction

**Status:** ACCEPTED

**Context:** Stage 4 requirements review clarified that Hermes is not intended to be deployed headless. Cloud Infrastructure already uses a consistent service-ingress pattern in which application WebUIs are published on authenticated `*.escloud.us` subdomains behind the existing Xray/nginx/TLS/Authelia stack, while only the root landing page `escloud.us` is intentionally unauthenticated. The DNS record `hermes.escloud.us` has already been prepared by the operator. Upstream Hermes documentation also defines Hermes Desktop remote-backend operation against a running `hermes dashboard` service through Settings -> Gateways -> Remote gateway.

**Decision:**

1. Hermes Web Dashboard is a required part of Stage 4 production scope and the normal human UI.
2. Public user URL is `https://hermes.escloud.us`.
3. Reuse the accepted Xray/nginx/shared-TLS/Authelia ingress pattern; do not build a separate ingress stack.
4. Keep the Hermes Dashboard backend host-local/loopback by default (upstream default `127.0.0.1:9119`) and do not expose port 9119 directly to the Internet.
5. The existence of `hermes.escloud.us` does not authorize a direct public Hermes API/backend listener. n8n should use the minimum local/private machine interface.
6. Because upstream Hermes engages remote-dashboard authentication semantics for a non-loopback public URL, Stage 4 must configure the minimum supported Hermes-native auth/session mechanism that works with the existing nginx/Authelia path and verify it end-to-end rather than assuming Authelia alone substitutes for Hermes Desktop authentication.
7. The **final Stage 4 integration task** is macOS Hermes Desktop.
8. Test the simplest supported Desktop path first: **Settings -> Gateways -> Remote gateway**, with the remote Dashboard backend URL intended to be `https://hermes.escloud.us`.
9. Acceptance must prove real sign-in/auth-provider detection, backend readiness, live chat/WebSocket operation and reconnect/session persistence.
10. Only if that Remote Gateway path demonstrates a concrete incompatibility with the accepted reverse-proxy/auth topology may an alternative Desktop connection mode be evaluated.
11. User-specific Hermes/n8n workflows remain post-infrastructure scope.

**Supersedes:** only the earlier Stage 02.5 wording that no public Hermes domain/listener was assumed. The selected Hermes product, host-native `core` placement, direct Codex/Antigravity delegation, n8n machine-interface requirement, Stage 3 NetBird dependency and post-infrastructure workflow boundary remain unchanged.

---

## 2026-09-18T08:48:22+03:00 — Correct Hermes Desktop auth assumptions for Stage 4

**Status:** ACCEPTED

**Context:** current Hermes Desktop UI/source explicitly states that hosted gateways may use OAuth or username/password while self-hosted gateways may use a session token. Current upstream source also contains a token-mode remote-gateway path. The previous Stage 4 correction was therefore too narrow where it implied that a public Remote Gateway should be planned around a Hermes-native OAuth provider, even though the product choice for authentication had not been tested against the actual installed build and the existing nginx/Authelia ingress.

**Decision:**

1. Keep `https://hermes.escloud.us` as the Stage 4 Web Dashboard URL behind the existing nginx + Authelia ingress.
2. Do **not** preselect Nous OAuth.
3. The preferred first macOS Hermes Desktop test remains **Settings -> Gateways -> Remote gateway**.
4. For the self-hosted backend, test the **Session token** credential mode first because it is explicitly supported by the current Desktop UI/source and is the simplest candidate for this single-operator deployment.
5. Verify actual backend readiness, live chat/WebSocket traffic and reconnect persistence; a successful status probe alone is insufficient.
6. Current upstream also has a separate gated-dashboard mode that can be engaged by non-loopback bind/public-URL semantics and supports username/password/OAuth providers. Treat that as an implementation constraint to test, not as an advance decision to use Nous OAuth.
7. If session-token Remote Gateway is incompatible with the installed Hermes version or the accepted nginx/Authelia proxy topology, test the minimum next supported credential mode (username/password or OAuth). Only after Remote Gateway itself is proven incompatible may Stage 4 evaluate SSH or another connection mode.
8. Do not change the existing public-WebUI requirement, host-native `core` placement, direct Codex/Antigravity delegation, n8n machine-interface requirement, or NetBird/vLLM dependency.

**Supersedes:** only the auth-provider assumption in the 2026-09-18 Stage 4 WebUI/macOS Remote Gateway contract correction. The rest of that decision remains ACCEPTED.

