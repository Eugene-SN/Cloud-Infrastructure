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

---

## 2026-09-18T09:43:00+03:00 — Stage scopes are minimum acceptance contracts, not feature ceilings

**Status:** ACCEPTED

**Context:** stage names and initial scope descriptions were intentionally written as planning/acceptance anchors and did not enumerate every future use of each selected service. Treating those lists as exhaustive led to recommendations to defer normal Hermes capabilities merely because they were "not needed for the current/core Stage path", which would create artificially reduced deployments and repeated later package/runtime changes.

**Decision:**

1. A stage scope defines mandatory outcomes, sequencing and acceptance boundaries; it is **not** an exhaustive whitelist of capabilities allowed to be installed.
2. Once a service/product is accepted, deploy a **functionally complete practical upstream-supported set** appropriate to its long-lived role rather than an intentionally minimal/slim profile.
3. Standard local dependencies and broadly useful capability modules should be installed during the service's infrastructure stage when this avoids predictable later rework and carries no material downside.
4. "Not needed for the current/core Stage path" is **not a valid exclusion rationale by itself** and must not be used to justify an intentionally incomplete service deployment.
5. Do not require the user to predict and enumerate every future workflow before installing ordinary capabilities of an already selected service.
6. This does not mean enabling every optional external integration. Capabilities may remain disabled/deferred for concrete reasons: separate account/credential/subscription requirements, mutually exclusive backends, duplication, unsupported/alpha state with material operational cost, unrelated heavyweight dependencies, security/public-exposure consequences, or explicit user decision.
7. User-specific workflows may remain in later/post-infrastructure workstreams while the generic underlying service capabilities needed to support them are installed earlier.
8. This invariant applies to Stage 4 Hermes and to subsequent Cloud Infrastructure stages unless explicitly superseded.

**Supersedes:** any prior interpretation of stage-scoped/minimum deployment wording that treated the enumerated stage acceptance path as a ceiling on the normal practical feature set of an already selected service.

---

## 2026-09-18T10:11:35+03:00 — Stage 4 Hermes Qwen3.8 model-native reasoning normalization

**Status:** ACCEPTED

**Context:** the Hermes Full Setup wizard had been configured with `agent.reasoning_effort: none` following an earlier assistant recommendation. Runtime inspection established that this disables thinking rather than merely hiding it. The project functional-completeness invariant requires retaining the normal useful capabilities of the selected service/model unless there is a concrete reason to disable them.

**Decision:**

1. Remove the persistent Hermes `agent.reasoning_effort` override for the primary `qwen3.8-27b-fp8` route.
2. Set `model.reasoning_echo: true` for the custom vLLM provider so Hermes preserves/replays provider reasoning content across turns.
3. Let Qwen3.8/vLLM use its model/server-native reasoning policy instead of forcing a Hermes effort override.
4. Do not reintroduce `reasoning_effort: none` as the default Stage 4 configuration.
5. Per-run reasoning overrides remain available when explicitly useful; they do not change the accepted default policy.

**Acceptance evidence:**

- direct vLLM model-native reasoning probe: HTTP 200 with non-empty reasoning;
- Hermes runtime resolver after normalization: no persistent reasoning override;
- Hermes turn 1: completed, terminal tool side effect verified, `reasoning_tokens=45`, 2 API calls;
- Hermes turn 2 resumed the exact same session ID and completed successfully with `reasoning_tokens=34`;
- `hermes-gateway.service` remained active/enabled;
- final `config.yaml` SHA256: `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`.

`STAGE4_HERMES_QWEN38_REASONING_NORMALIZATION=PASS`

**Supersedes:** the earlier Stage 4 wizard-time choice to disable reasoning for the primary Qwen3.8 model.
---

## 2026-09-18T10:37:05+03:00 — Stage 4 Mattermost private collaboration/control substage

**Status:** ACCEPTED

**Context:** the operator explicitly expanded Stage 4 to include a lightweight private Mattermost server integrated with Hermes and other compatible services on `edge`. The previous Stage 02.5 roadmap treated a generic messaging/control frontend as optional/deferred; that no longer reflects the Mattermost requirement.

**Decision:**

1. Mattermost is a mandatory Stage 4 service/substage and must complete before server-side Stage 4 integrated acceptance.
2. Deployment is preceded by a dedicated deep-research/deployment-design gate; no Mattermost production mutation occurs until that design is explicitly accepted.
3. Mattermost is a collaboration/control/notification surface; it does not replace Hermes or n8n.
4. Hermes uses its native Mattermost adapter where compatible, with dedicated bot identity and native REST/WebSocket behavior.
5. n8n uses the official Mattermost integration for supported operations and native webhooks/slash commands for inbound flows before third-party trigger nodes/custom plugins.
6. Stalwart is the preferred existing SMTP subsystem; do not deploy a duplicate mail stack.
7. Codex and Antigravity remain reached through Hermes by default rather than parallel Mattermost bots.
8. `chat.escloud.us` is the preferred human-facing namespace because it already exists in the shared TLS/protected namespace. Final use is gated by Stage 4D validation of web/desktop/mobile behavior with Authelia.
9. Mattermost application/database backends remain private; machine integrations should use internal routes and native Mattermost credentials rather than traverse Authelia.
10. Do not add Kubernetes, HA, Elasticsearch/OpenSearch, S3/MinIO, Calls media networking, push infrastructure or custom plugins without a concrete requirement. This does not justify stripping normal Mattermost messaging/files/API/bot/webhook/slash-command capabilities.
11. macOS Hermes Desktop Remote Gateway remains the last Stage 4 integration task after Mattermost and all other server-side substages are accepted.
12. `IMPLEMENTATION_PHASES.md` now enumerates Stage 4A–4I so future responses must not present only the next immediate task as the complete remaining Stage 4 scope.

**Research record:** `STAGE_04_MATTERMOST_RESEARCH_BRIEF_2026-09-18.md`

**Supersedes:** the earlier optional/deferred classification of a generic messaging/control frontend, for Mattermost specifically.
---

## 2026-09-18T12:43:00+03:00 — Stage 4D Mattermost target deployment architecture accepted

**Status:** ACCEPTED

**Context:** extended research and operator review resolved the Mattermost deployment architecture. The operator also clarified that service-integration mechanisms must not be frozen prematurely: during deployment all current native/upstream-supported options are to be evaluated and the best maintainable supported mechanism selected per connection.

**Decision:**

1. Stage 4D research/design is complete.
2. Deploy **Mattermost Team Edition** using the current official Mattermost Docker Compose pattern.
3. Use separate Mattermost application and dedicated PostgreSQL containers; do not use the Preview all-in-one image.
4. Persist Mattermost/PostgreSQL state locally under `/srv`; exact paths/ownership are finalized during Stage 4E after the fresh runtime audit.
5. Reuse the existing Xray -> host nginx -> shared TLS ingress. Do not deploy Mattermost's optional bundled nginx.
6. Human endpoint is `https://chat.escloud.us`.
7. `chat.escloud.us` is an explicit exception to the normal service-subdomain Authelia rule: **do not place Authelia in front of Mattermost**. Use Mattermost-native authentication so official web/desktop/mobile clients and REST/WebSocket flows remain native.
8. Mattermost application and PostgreSQL backends remain private; no direct public application/database listener.
9. Enable Mattermost Test Push Notification Service (TPNS) for official mobile clients. Lack of production SLA is accepted for this private deployment.
10. Mattermost Calls is explicitly excluded from current Stage 4; do not deploy Calls media/TURN infrastructure or open Calls-specific ports.
11. Do not add Kubernetes, HA, Elasticsearch/OpenSearch, Redis, MinIO/S3, custom push proxy/mobile build or other scale-specific subsystems without a later concrete requirement.
12. Integrations with Hermes, n8n, Stalwart and other services are required where useful, but the **exact per-service mechanism is intentionally not preselected**. During Stage 4E enumerate all current native/upstream-supported mechanisms, compare reliability/simplicity/update compatibility, and choose the best supported option.
13. Research examples such as Hermes Mattermost support, n8n's official Mattermost integration page/node, Mattermost API/webhooks/slash commands and SMTP are candidates/evidence of native support, not immutable implementation choices.
14. Custom plugins, source patches, shim services, direct DB coupling or bespoke bridges require demonstrated insufficiency of practical native options and explicit operator acceptance.

**Acceptance record:** `STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`

**Supersedes:**

- the Stage 4 Mattermost decision's provisional requirement to validate Mattermost through Authelia; Mattermost now explicitly uses native authentication without Authelia;
- the Stage 4 Mattermost decision's provisional preference for specific Hermes/n8n/webhook/slash-command/SMTP integration mechanics; those exact mechanics are now intentionally selected during Stage 4E rather than frozen in advance;
- the earlier classification of Mattermost push and Calls as unresolved: TPNS is accepted, Calls is explicitly excluded.

---

## 2026-09-18T12:58:00+03:00 — Mattermost integrations are native-only in the current project

**Status:** ACCEPTED

**Context:** the operator clarified that Mattermost must integrate with other Cloud Infrastructure services only through integration mechanisms intentionally provided and supported by the relevant developers/upstream. The project must not create custom bridges merely because Mattermost exposes a generic API/webhook primitive.

**Decision:**

1. For every service already deployed or selected in Cloud Infrastructure, first establish whether the current upstream provides a native Mattermost integration or an explicitly supported standard-protocol counterpart.
2. If a supported integration exists, it becomes the project integration path and is documented/verified in the owning stage.
3. If no supported Mattermost integration exists, the service remains **unintegrated with Mattermost in the current Cloud Infrastructure project**.
4. Missing integrations are not replaced by custom plugins, patched source, shim services, direct database access, bespoke bridges, compatibility hacks, or an n8n-mediated relay solely to connect otherwise unrelated products.
5. Such an integration may be reconsidered only as a separate future task outside the current project if upstream support or a new requirement appears.
6. Confirmed native paths at this checkpoint:
   - **Hermes ↔ Mattermost:** Hermes built-in Mattermost gateway adapter using Mattermost REST API v4 + WebSocket;
   - **n8n → Mattermost:** n8n official built-in Mattermost integration/node for the operations it supports;
   - **Mattermost → Stalwart:** Mattermost standard SMTP integration using the existing Stalwart SMTP service.
7. Additional directions, including event/command flows from Mattermost into n8n, are enabled only if the actually deployed versions expose an upstream-supported counterpart for that direction. A generic webhook primitive alone is not sufficient to justify a custom bridge.
8. Codex CLI and Antigravity CLI remain reached through Hermes in the accepted architecture; no direct Mattermost integration is added unless their upstream later provides one and a separate future task accepts it.
9. The same rule applies to CloudCLI, Bulwark, NetBird, Backrest, Semaphore and later selected monitoring/operational services: native integration present -> adopt and document; absent -> no current-project Mattermost integration.

**Supersedes:** the Stage 4D wording that merely preferred native integrations while still allowing custom bridges after native options proved insufficient. The current project now stops at the absence of upstream-supported integration and defers any custom integration outside project scope.

---

## 2026-09-18T13:20:00+03:00 — Stage 4 execution reordering: deploy Mattermost before remaining Hermes work

**Status:** ACCEPTED

**Context:** Mattermost Stage 4D design is accepted while Hermes already has a functioning gateway, vLLM inference, reasoning, terminal and browser/toolchain baseline. Deploying Mattermost now creates the real native messaging surface needed to test Hermes through its officially supported Mattermost adapter, avoiding a second round of integration testing after finishing Hermes in isolation.

**Decision:**

1. Stage 4 substage labels remain scope identifiers, but current execution order is dependency-driven rather than numeric.
2. Begin **Stage 4E Mattermost deployment now**, before completing the remaining Hermes 4A/4B/4C items.
3. After base Mattermost web/mobile/push acceptance, configure **Hermes ↔ Mattermost first** using the official Hermes guide:
   `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost`.
4. The Hermes integration uses the built-in Mattermost gateway adapter over Mattermost REST API v4 + WebSocket, a dedicated Mattermost bot, explicit operator user allowlist, and the installed Hermes gateway lifecycle.
5. After Hermes↔Mattermost acceptance, configure and verify **n8n ↔ Mattermost** using only upstream-supported integration paths.
6. Only after Hermes and n8n are complete, hold a separate usefulness/necessity review for **Mattermost ↔ Stalwart SMTP/email**. Do not enable it automatically merely because Mattermost supports SMTP.
7. Existing Stalwart email service and ordinary mail clients remain independent of Mattermost. The future SMTP review must identify concrete benefit such as Mattermost password recovery or email notifications before activation.
8. Resume the remaining Hermes capability/executor/Dashboard work after the Mattermost/Hermes/n8n sequence; macOS Hermes Desktop remains the final Stage 4 integration task.

**Supersedes:**

- the earlier interpretation that Stage 4A/4B/4C must be completed before Stage 4E;
- the 2026-09-18 native-only Mattermost integration decision only where it described Mattermost→Stalwart SMTP as already fixed for implementation. SMTP support remains a native capability, but activation is now pending explicit usefulness acceptance.



## 2026-09-18 — Mattermost ↔ Stalwart SMTP not required

**Status:** ACCEPTED

**Context:** Mattermost email/SMTP capability was reviewed separately from the native Hermes and n8n service integrations. The deployment already has a normal mail service/client path through Stalwart, while Mattermost-generated email is not required for the accepted single-operator operating model.

**Decision:** Do not configure Mattermost SMTP against Stalwart. Mattermost ↔ Stalwart email integration is out of the current target state and must not be enabled automatically.

**Constraints:** Revisit only if a concrete future requirement appears for Mattermost-generated email such as password-reset mail, email notifications, invitations, or another explicit mail-dependent workflow.

**supersedes:** prior unresolved/pending Mattermost ↔ Stalwart usefulness discussion.

---

## 2026-09-18T17:18:00+03:00 — Stage 4 core-agent acceptance priority

**Status:** ACCEPTED

**Context:** Stage 4 capability probing proved Web Search/Extract, Edge TTS and Vision functional on the deployed Hermes runtime, while Computer Use is not applicable on the intentionally headless `edge` host. Image Generation remained blocked only by separate Hermes-managed Codex image-generation authentication. The operator clarified that image generation is not a core autonomous-agent acceptance function because useful image output inherently requires human visual review, whereas correct Qwen3.8/vLLM behavior and delegation to Codex/Antigravity define the primary Hermes role.

**Decision:**

1. Stage 4 critical acceptance is centered on the main agent execution path: `Hermes -> qwen3.8-27b-fp8/vLLM`, including correct reasoning mode, tool calling, reasoning replay and multi-turn/session continuity.
2. Re-verify that the accepted Qwen3.8 normalization remains effective: no persistent `agent.reasoning_effort` override, `model.reasoning_echo=true`, model/server-native reasoning preserved, and real Hermes tool use succeeds.
3. Stage 4B direct specialist delegation is next in priority: prove Hermes -> standalone Codex CLI and Hermes -> standalone Antigravity CLI using their official Hermes skill patterns and existing CLI authentication.
4. Keep Hermes' default/main runtime on the accepted local custom vLLM/Qwen route. Do not switch the main agent to the optional Codex app-server runtime merely to integrate Codex.
5. The bundled Codex skill uses Hermes terminal -> `codex exec` in a git workspace. The official optional `antigravity-cli` skill uses Hermes terminal -> `agy --print` / `agy -p`. These are the accepted integration shapes unless runtime evidence proves incompatibility.
6. Image Generation remains an optional installed/configured capability and is **non-blocking for Stage 4 acceptance**. Do not create a separate Hermes Codex OAuth session solely to satisfy Stage 4. A future image-generation check, when actually useful, requires human visual acceptance of the result.
7. Headless Linux CUA remains `NOT_APPLICABLE_HEADLESS_EDGE`; do not add a desktop/X11/Wayland stack solely to convert that capability into a synthetic PASS.
8. Already-proven Web Search/Extract, Edge TTS and Vision are retained as accepted capability evidence and are not re-tested without a concrete regression signal.

**Supersedes:** only the prior interpretation that Image Generation or server-side CUA must independently pass before the core Hermes Stage 4A/4B path can proceed. The functional-completeness invariant remains in force for practical capabilities that do not require disproportionate infrastructure or inherently manual acceptance.

---

## 2026-09-18T18:21:00+03:00 — Stage 4B trusted full-access executor contract

**Status:** ACCEPTED

**Context:** Stage 4B deep research and the completed read-only runtime audit established that `edge` is a single-operator trusted environment; Hermes runs host-native under `core` with `terminal.backend=local`; the actual Hermes terminal child receives `HOME=/home/core`, cwd `/home/core`, and `/home/core/.local/bin` on PATH; no `OPENAI_BASE_URL`, `OPENAI_API_KEY` or `CODEX_*` environment override leaks from the local Qwen/vLLM provider into standalone executor processes. Codex CLI `0.154.0` uses its existing OAuth state and exposes the native non-interactive `codex exec` surface. Antigravity CLI `1.2.5` exposes native headless `agy -p/--print`, JSON output, timeout/model/effort and sandbox/permission controls. The operator explicitly rejects blanket filesystem/network sandboxing as unnecessary friction that would reduce the usefulness of trusted specialist agents.

**Decision:**

1. Hermes remains the main orchestrator/reasoning agent on the accepted local `qwen3.8-27b-fp8` / vLLM route. Codex and Antigravity remain specialist executors invoked directly through Hermes terminal; CloudCLI is not a proxy and Codex app-server is not the main Hermes runtime.
2. The default Stage 4B one-shot Codex path is **foreground, non-PTY `codex exec`**. PTY is reserved for genuinely interactive Codex TUI sessions; background execution is reserved for genuinely long-running or parallel jobs.
3. The default Stage 4B one-shot Antigravity path is **foreground, non-PTY `agy -p/--print` with structured JSON output where supported by the installed CLI**. Interactive PTY and background/process lifecycle are used only when the task actually requires them.
4. Codex and Antigravity are trusted to operate with the host/workspace access required by the delegated task under Unix user `core`. Do **not** impose blanket Docker/container isolation, workspace-only filesystem restriction, network denial, or sandbox-by-default policy merely for defense in depth.
5. Authorization for critical mutations belongs at the **Hermes/orchestration and agent-instruction layer**, not in an artificial executor sandbox. Before delegating a destructive, system-wide, production, network, credential/auth, data-deletion or similarly high-impact mutation, Hermes must obtain the operator's explicit approval unless that exact mutation was already explicitly authorized in the current instruction.
6. After the operator has approved the critical mutation, the executor should receive the permissions needed to complete it without an additional artificial sandbox/ACL barrier. Ordinary non-critical tasks should not incur unnecessary confirmation prompts.
7. Executor prompts/instructions must preserve the same project discipline: inspect relevant current state before mutation, avoid unrelated redesign, verify the result, and stop for operator approval at the defined critical-action boundary.
8. Existing standalone Codex OAuth and Antigravity authentication/state are reused. Do not create duplicate provider credentials merely for Hermes delegation.
9. Long-running jobs may use Hermes `terminal(background=true)` plus `process(wait/poll/log)`; this remains a supported capability and is not rejected because of third-party issue reports. It is simply not the default for short one-shot work.
10. Stage 4B acceptance must prove the selected foreground headless paths end-to-end through Hermes/Qwen while leaving the main Hermes provider/config unchanged.

**Read-only audit evidence:**

- `STAGE4B_EXECUTOR_READONLY_AUDIT=PASS`;
- Hermes child cwd `/home/core`, `HOME=/home/core`, `HERMES_HOME=/home/core/.hermes`;
- no OpenAI/Codex provider environment contamination in the Hermes terminal child;
- Codex CLI `0.154.0`: `--json`, `--ephemeral`, `--sandbox`, `--skip-git-repo-check`, `--output-last-message` and `--model` present;
- Antigravity CLI `1.2.5` raw help confirms `--print`, `--output-format`, `--print-timeout`, `--model`, `--effort`, `--sandbox`, `--dangerously-skip-permissions`, `--continue` and `--conversation`;
- Hermes config/auth/skill state remained byte-identical through the audit.

**Supersedes:** only the Stage 4B executor-invocation and permission portions of the 2026-09-18T17:18:00+03:00 Stage 4 core-agent priority decision where they relied on the current Hermes Codex skill's PTY-oriented example as the default one-shot shape. The product selections, Qwen/vLLM main-agent role, direct delegation architecture, and non-blocking Image Generation/CUA decisions remain ACCEPTED.



---

## 2026-09-18T20:10:54+03:00 — Core full non-interactive root privilege

**Status:** ACCEPTED

**Context:** `edge` is a single-operator trusted environment and `core` is the shared host-native execution identity for Hermes, Codex, Antigravity and related Cloud Infrastructure work. The earlier rebuild baseline intentionally left `core` without sudo. Continued service deployment now requires the trusted agent/tooling context to perform system administration without switching to a separate interactive root session or introducing per-service privilege workarounds.

**Decision:**

1. Keep `core` as UID/GID `1000:1000` with its password locked.
2. Grant full non-interactive sudo using `core ALL=(ALL:ALL) NOPASSWD: ALL` in `/etc/sudoers.d/90-core-root`.
3. Use `sudo -n` from `core` for root-required host operations; do not change `core` to UID 0.
4. Do not add `core` to the `docker` group merely for Docker administration because full sudo already provides the required capability.
5. Preserve the existing trusted-executor safety contract: critical destructive/system-wide/production/network/credential/data mutations still require operator authorization at the orchestration/instruction layer unless already explicitly authorized.

**Acceptance evidence:** `CORE_FULL_ROOT_SUDO_ACCEPTANCE_2026-09-18.md`; `visudo -c` PASS; `sudo -n` root UID/GID/user verification PASS; arbitrary run-as verification PASS; rule SHA256 `545bf1fb2ab8c68f09c45e711100bea1db2b14341db1bdec986b315d4f04fc30`.

**Supersedes:** the prior current-state restriction that `core` has no sudo access. Historical stage records retain their original factual state and are not rewritten.

---

## 2026-09-18 — Stage 04.3 recovery scope and evidence reconciliation

**Status:** ACCEPTED — operator-directed recovery workflow, not Stage 4C architecture/deployment acceptance.

**Decision:**

1. Continue Stage 4 in `04.3 — Edge Hermes Stage 4 Recovery, Completion & Final Acceptance`; Git branch `04.3-edge-hermes-recovery-completion` starts from `32cd97b7da9a62250f30c2f8240fcbe06f48186b`.
2. Preserve Stage 4A core/capability, Stage 4B executor, Stage 4D design and Stage 4E implementation acceptance. Do not repeat these E2E tests without a concrete regression signal. Track the already-known gateway SIGTERM exit-1 constraint in 4G.
3. Stage 4C is NOT ACCEPTED. Suspend earlier mandatory nginx forward-auth/session-token-first assumptions pending exact-source and live-runtime design verification. Required endpoint, loopback backend, existing ingress and prohibition on a public machine API remain unchanged.
4. Correct current-document duplication/stale summaries without retroactively rewriting historical acceptance records. Earlier records listing a then-future 4B are chronology, not evidence that 4B needs repeating.
5. GitHub reconciliation identifies the duplicate next-step list introduced by `5597ff7b`; the nine requested commits modify only documentation. The accepted 4B evidence record distinguishes actual executor success from a failed receipt wrapper. No reviewed commit accepts Stage 4C or deploys OIDC.
6. Direct local read-only evidence on edge confirms the accepted Hermes source/config hash, healthy user gateway, no Dashboard listener/unit/frontend/config section, Certbot 4.0.0 with existing webroot renewal and DNS 45.92.156.17. This is bounded recovery evidence, not a new 4A/B acceptance run.
7. The previous failed deployment's pre-mutation stop is operator-reported and consistent with readable runtime; the full previous-session transcript and root-only recovery inspection are still unavailable. Do not label that full recovery gate PASS yet.
8. Complete the Stage 4C source/runtime/recovery contract and explicitly record its architecture decision before mutation. Browser/OIDC Chat/WS acceptance precedes 4F; 4G precedes macOS 4H; Stage 5 stays closed until 4I is persisted.

**Supersedes:** the operational force of the 2026-09-18 08:05 and 08:48 Stage 4 auth decisions only where they mandate forward-auth/session-token-first. The replacement OIDC architecture below remains PROPOSED pending the recovery design gate.

## 2026-09-18 — Stage 4C self-hosted OIDC candidate and verified source contract

**Status:** PROPOSED / SOURCE-VERIFIED / ROOT RUNTIME RECONCILIATION PENDING.

This entry is not Stage 4C acceptance and does not claim deployment.

**Candidate:**

- Browser/future Desktop -> `https://hermes.escloud.us` -> existing Xray TLS and nginx fallback -> `127.0.0.1:9119`.
- Hermes native self-hosted OIDC with issuer `https://auth.escloud.us`; exactly one interactive provider, `self-hosted`.
- No nginx `auth_request` in front of Hermes, no Basic/Nous provider by default, no public 9119.
- Hermes public URL set explicitly; upstream-supported frontend build and persistent user-systemd Dashboard under `core`.
- Authelia public client: `public: true`, no client secret, `token_endpoint_auth_method: none`, `require_pkce: true`, `pkce_challenge_method: S256`, authorization-code flow, callback `https://hermes.escloud.us/auth/callback`. Final refresh/scopes/policy settings must preserve upstream refresh semantics and the actual operator authentication policy.
- Authelia provider requires a separate HMAC secret and issuer JWK; RS256 RSA private signing key is supported. Secrets stay outside Git. Existing template filter is confirmed in the live Compose definition; use native config validation, not PyYAML.
- Reuse `escloud.us` certificate lineage with the existing `webroot` authenticator and `/var/www/letsencrypt`. Preserve the complete current SAN set and deploy-hook behavior when adding `hermes.escloud.us`; no nginx Certbot plugin is required.

**Verified version-specific evidence:**

- [Hermes Dashboard guide at deployed commit](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/website/docs/user-guide/features/web-dashboard.md): self-hosted OIDC is supported for Internet exposure; config uses `dashboard.oauth.self_hosted.{issuer,client_id,scopes}` or equivalent `HERMES_DASHBOARD_OIDC_*` environment settings.
- [Actual self-hosted provider](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/plugins/dashboard_auth/self_hosted/__init__.py): discovery, S256 authorization, ID-token verification against issuer/audience/JWKS and refresh are implemented. The source additionally supports confidential clients despite a stale documentation sentence denying them; public PKCE works without relying on that discrepancy.
- [Server auth gate](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/hermes_cli/web_server.py): a non-loopback `public_url` engages auth on a loopback bind and declares the accepted public Host/Origin; no configured provider means fail-closed. Forwarded headers are trusted only from bounded configured proxies/loopback.
- [Auth routes](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/hermes_cli/dashboard_auth/routes.py) and [WS tickets](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/hermes_cli/dashboard_auth/ws_tickets.py): browser callback is `/auth/callback`; authenticated `POST /api/auth/ws-ticket` mints a single-use 30-second ticket for WS upgrade. Native endpoints broker Desktop sign-in rather than requiring a separate Desktop callback in Authelia.
- [Native Desktop sign-in](https://github.com/NousResearch/hermes-agent/blob/d177b119e9c56c9ddc0b7379ffce52341ec06584/website/docs/guides/desktop-native-signin.md): RFC8252/PKCE flow, system browser, token exchange/refresh and capability detection. This establishes source support, not observed macOS acceptance.
- [Authelia v4.39.27 provider](https://github.com/authelia/authelia/blob/v4.39.27/docs/content/configuration/identity-providers/openid-connect/provider.md), [clients](https://github.com/authelia/authelia/blob/v4.39.27/docs/content/configuration/identity-providers/openid-connect/clients.md) and [schema](https://github.com/authelia/authelia/blob/v4.39.27/internal/configuration/schema/identity_providers.go): HMAC/JWK/public-client/PKCE syntax confirmed. OIDC client authorization policy is distinct from ordinary access_control rules; an nginx auth_request bypass/access-control rule is not required for an OIDC-only relying party.
- Stage 1 TLS record and directly read live renewal configuration agree on webroot. Live Certbot version is 4.0.0.

**Still unknown before mutation:** root-only Authelia configuration/secret inventory, current certificate SANs and deploy hooks, final validated staged config and concrete recovery commands. No upstream code patch or lifecycle masking is authorized by this candidate.

**Acceptance boundary:** actual browser login, Dashboard Chat, authenticated `/api/ws` and `/api/pty`, loopback exposure and main-provider/gateway non-regression are mandatory before any Stage 4C PASS.


---

## 2026-09-18T17:15:00Z — Stage 4C native self-hosted OIDC deployment design

**Status:** ACCEPTED — DESIGN ONLY; Stage 4C functional acceptance remains pending.

Root recovery now confirms Authelia v4.39.27, no OIDC-related config keys or generated OIDC secrets, native config validation PASS, and the existing 12-SAN certificate without Hermes. The operator provided non-interactive sudo to the local core session. Earlier lack of sudo is historical and no longer a blocker.

**Accepted implementation:**

1. Reuse the current Xray TLS -> nginx `127.0.0.1:8080 proxy_protocol` ingress. Publish Hermes only at `https://hermes.escloud.us`; proxy to `127.0.0.1:9119`, preserve public Host, trusted forwarded HTTPS/client metadata and WebSocket upgrades. No nginx auth_request for Hermes.
2. Run upstream `hermes dashboard --host 127.0.0.1 --port 9119 --no-open` in a persistent core user-systemd service. Use service-local supported `HERMES_DASHBOARD_PUBLIC_URL` and `HERMES_DASHBOARD_OIDC_*` settings so the main Qwen/vLLM config need not change. Build via Hermes' upstream automatic frontend mechanism.
3. Register exactly one interactive Hermes provider, self-hosted, issuer `https://auth.escloud.us`, client `hermes-dashboard`, scopes `openid profile email offline_access`. No Basic/Nous provider or session-token bypass.
4. Authelia public client: `public: true`, token endpoint auth `none`, authorization-code plus refresh-token grants, response type `code`, PKCE required/S256, exact callback `https://hermes.escloud.us/auth/callback`, explicit consent. Use `one_factor` to preserve the existing service-login policy instead of silently introducing a different operator-login requirement. Ordinary access_control remains unchanged.
5. Add isolated OIDC HMAC and RS256 RSA signing key through the existing template secret-file mechanism. Native-validate the staged complete configuration before replacing/restarting Authelia. Do not parse templated configuration with PyYAML.
6. Extend the existing `escloud.us` certificate to preserve all current 12 SANs and add `hermes.escloud.us`, using Certbot 4.0.0 `certonly --webroot -w /var/www/letsencrypt --cert-name escloud.us --expand`. Reuse the existing account/renewal state and deploy hook. The hook copies TLS state and restarts Xray, Hysteria2 and Stalwart; this necessary disruption is explicit.
7. Save root-only recovery copies before mutation: Authelia config, Certbot state, TLS consumer copies and nginx configuration. Keep the main Hermes config hash unchanged. Rollback application activation by disabling Dashboard, removing only the new vhost, restoring the previous Authelia config and native-validating before restart. A successfully expanded shared certificate can remain valid on application rollback; do not revoke/reissue it unnecessarily.
8. Verify runtime/status/provider/redirect/TLS/listeners and gateway/hash properties. Browser/OIDC login, Chat and WS/PTY require actual interactive evidence before Stage 4C can pass. Desktop remains 4H after 4G.

**Why this matches the deployed versions:** the immediately preceding source-verified candidate cites exact Hermes source and Authelia v4.39.27 docs/schema; local CLI help, actual Compose template filter, current webroot renewal state, ACME nginx route and deploy-hook source were additionally inspected. The root configuration passed Authelia's own validator before any change.

**Supersedes:** the preceding PROPOSED candidate status and the older mandatory forward-auth/session-token-first design. This does not supersede any Stage 4A/B/D/E acceptance or claim Stage 4C deployment success.

---

## 2026-09-18T21:25:00+03:00 — Stage 4C Dashboard and Desktop authentication contract

**Status:** ACCEPTED

**Decision:**

1. `https://hermes.escloud.us` is the canonical browser and macOS Desktop Remote Gateway endpoint.
2. Hermes-native self-hosted OIDC with Authelia `4.39.27` as IdP is the accepted authentication contract. The only interactive provider is `self-hosted`.
3. Browser authorization uses the public authorization-code client and PKCE/S256 callback `https://hermes.escloud.us/auth/callback`. Desktop uses the upstream native RFC8252/PKCE broker endpoints.
4. nginx terminates the existing Xray-provided TLS path and proxies to loopback `127.0.0.1:9119` with WebSocket forwarding. nginx does not use `auth_request` for Hermes.
5. No Basic/Nous fallback and no public TCP/9119 are part of the accepted runtime.
6. The shared `escloud.us` certificate lineage and its established Certbot webroot mechanism include `hermes.escloud.us`.
7. Browser callback/session/Chat traffic, WebSocket HTTP 101 and operator functional confirmation complete Stage 4C. Native Desktop authorize/token exchanges, two WebSocket connections and operator confirmation complete Stage 4H.

**Supersedes:** all earlier current-state forward-auth/session-token-first requirements and the DESIGN ONLY/pending-acceptance status of the preceding Stage 4C decision. Historical audit records remain unchanged.

---

## 2026-09-18T21:26:00+03:00 — Stage 4F native Hermes API Server for n8n

**Status:** ACCEPTED

**Decision:**

1. n8n invokes Hermes through the upstream-native Hermes API Server `/v1/responses` interface.
2. The API binds only `172.19.0.1:8642` on the n8n Docker bridge, requires a strong Bearer key and is limited by a narrow UFW rule to the n8n subnet. It has no nginx/public route.
3. n8n uses its built-in HTTP Request node and encrypted `httpBearerAuth` credential. No custom adapter, CLI wrapper, MCP-to-HTTP shim or public webhook is introduced.
4. The production reusable workflow `Hermes Machine Invocation` accepts `task` plus selector `vllm`, `codex` or `antigravity`.
5. `vllm` returns a direct result from the configured Hermes model without executor tool calls. `codex` and `antigravity` require the corresponding real foreground non-PTY CLI and return its usable result.
6. The known Tirith CLI stdout warning is irrelevant to this path because n8n consumes native HTTP JSON rather than CLI `stream-json`.
7. Exact-value E2E passed for all three selectors; only the reusable workflow remains in production.

**Supersedes:** the unresolved Stage 4F mechanism and any assumption that a custom service is required for n8n to invoke Hermes.

---

## 2026-09-18T21:27:00+03:00 — Final Stage 4 runtime and lifecycle acceptance

**Status:** ACCEPTED

**Decision:**

1. Stage 4A/B/C/D/E/F/G/H/I are COMPLETE / ACCEPTED. Final marker: `STAGE4_FINAL_ACCEPTANCE=PASS`.
2. Hermes remains on `qwen3.8-27b-fp8` through the custom vLLM endpoint `http://192.168.1.30:8000/v1`. A Dashboard-driven switch to `openai-codex` found during 4G was a real regression and was corrected with native Hermes commands before final acceptance.
3. Current Antigravity CLI `1.2.6` supersedes the inventory value `1.2.5`; the version change passed a bounded real n8n/Hermes/Antigravity E2E. Codex remains `0.154.0`.
4. Controlled Hermes SIGTERM exit status 1 after graceful-shutdown logging is an accepted upstream constraint because requested restart recovery and service persistence pass. Do not patch source or add `SuccessExitStatus=1` merely to hide it.
5. Current Hermes config SHA256 is `fe2f0fead4781ed28d0c4bf61720bdc52a6b31a41040a477afe6351b5df2f824`; accepted model semantics are restored and user Dashboard theme `rose` is preserved.
6. Stage 5 may begin only from the persisted final Stage 4 checkpoint and its own mandatory entry audit.

**Supersedes:** all remaining current-state descriptions of Stage 4C/F/G/H/I as pending. It does not rewrite the historical state recorded by earlier acceptance/audit artifacts.

---

## 2026-09-19 — Read-only checkpoint and cross-project documentation reconciliation

**Status:** EVIDENCE RECONCILIATION ONLY; no new architecture decision or runtime deployment.

- Stage 4 closure is preserved: `STAGE4_FINAL_ACCEPTANCE=PASS`, recorded on 2026-09-18 in `04.3-edge-hermes-recovery-completion`. The open draft PR #1 and stale main checkpoint do not reopen the completed stage.
- Read-only edge inspection on 2026-09-19 confirmed active/enabled Gateway and Dashboard with `NRestarts=0`, the accepted Hermes commit/config hash, loopback Dashboard, private bridge API and one active production Hermes n8n workflow with two credential records. It did not repeat E2E or reboot acceptance.
- [Home Infrastructure CURRENT_STATE.md](https://github.com/Eugene-SN/Home-Infrastructure/blob/main/CURRENT_STATE.md) (content blob `7c70ae1069568c2538f3b14d518765e8861b6fe3`) records accepted PVE canonical cutover, Syncthing 2.1.5, CT220 cutover/legacy cleanup and CT208 backup/restore plus production policy.
- [PAI CURRENT_STATE.md](https://github.com/Eugene-SN/Personal-Agents-Infrastructure/blob/main/CURRENT_STATE.md) (content blob `41a827a5338d976caf2cace92e1f1853a45cb1c9`) records ai-node as non-canonical and its accepted dedicated local Knowledge backup.
- These later Home/PAI records supersede Cloud current-state wording that describes Home cutover as still pending. Historical acceptance records and earlier decision chronology remain unchanged.
- Cloud Stage 5 remains undeployed/unaccepted. Its fresh Home/PAI/Cloud entry audit is still mandatory. PVE's documented completion is not a fresh remote runtime measurement.
- Remaining stages are 5 through 10; the existing lifecycle ordering and product anchors remain unchanged. Detailed additions to the roadmap are planning/acceptance checklists, not implementation authorization.
- The Stage 0 migration-preservation archive identity and SHA256 remain historical evidence, but the 2026-09-19 read-only edge audit found its `/tmp` path absent. Current documents must not present it as available recovery state.
- The Stage 4F private n8n path currently depends on the concrete `n8n_default` bridge/subnet identity. This is accepted current runtime, not a portable invariant; Docker network recreation requires coordinated bind/workflow/UFW reconciliation.

---

## 2026-09-19T15:45:20+03:00 — Direct-to-main workflow and migration-archive retirement

**Status:** ACCEPTED

**Decision:**

1. ChatGPT/Codex writes to the latest `main` by default for this repository. It fetches/reads `origin/main`, produces one coherent accepted commit, pushes directly to `main`, and reads back the remote commit and critical files.
2. A branch or pull request is created only when the operator explicitly requests one. Stage boundaries and acceptance gates remain unchanged.
3. PR #1 is merged into `main` as `c4d402175ea1a049f20a93ab77daa0b068071277`; Stage 4 has no pending GitHub persistence work.
4. The historical temporary migration-preservation archive is absent and no longer required. Its identity/hash remain chronology only; do not recreate it.
5. Sanitized `migration-reference/` remains the engineering reference. New recovery artifacts are created only for a concrete current recovery requirement.

**Supersedes:** the 2026-09-16 stage-aligned branch lifecycle as a repository-branch requirement; the accepted-first stage lifecycle remains in force. Also supersedes any current requirement to retain or recreate the historical migration-preservation archive.

---

## 2026-09-19T15:45:20+03:00 — Stable n8n Docker bridge identity for Hermes

**Status:** ACCEPTED

**Decision:**

1. Preserve the accepted private `172.19.0.1:8642` Hermes API, Bearer authentication, n8n subnet and absence of public ingress.
2. Define the Compose default network explicitly as Docker network `n8n_hermes`, bridge driver, Linux bridge `n8n-hermes`, subnet `172.19.0.0/16`, gateway `172.19.0.1`.
3. Bind the narrow UFW allowance to stable interface `n8n-hermes`; remove the obsolete network-ID-derived `br-2bdcbc775588` rule only after authenticated n8n-container reachability passes.
4. Keep the production workflow URL and Hermes bind unchanged because the gateway address remains `172.19.0.1`.
5. Preserve recovery checkpoint `/srv/backups/edge-stage4f-network/recovery-20260919T124318Z` and acceptance record `STAGE_04F_NETWORK_IDENTITY_HARDENING_ACCEPTANCE_2026-09-19.md`.

**Acceptance evidence:** `docker compose config` PASS; n8n healthy/readiness PASS; unauthenticated container request HTTP 401; authenticated container request HTTP 200 with Hermes `status=ok`; production workflow active; gateway/Docker/NetBird/nginx and other containers non-regressed. Marker: `STAGE4F_STABLE_DOCKER_BRIDGE_HARDENING=PASS`.

**Supersedes:** the operational `n8n_default` / `br-2bdcbc775588` dependency recorded on 2026-09-18 and in the earlier 2026-09-19 read-only reconciliation. The original entries remain historical evidence.


---

## 2026-09-19T15:57:00+03:00 — Stage 4 post-acceptance runtime reconciliation

**Status:** ACCEPTED

**Decision:**

1. Preserve `STAGE4_FINAL_ACCEPTANCE=PASS`; Stage 4 remains COMPLETE / ACCEPTED and is not reopened.
2. Record current Antigravity CLI runtime as `1.2.7`. Historical acceptance remains unchanged: Stage 4B accepted `1.2.5`, and Stage 4G accepted `1.2.6` with bounded real E2E.
3. Fresh read-only reconciliation confirms current Stage 4 server boundaries: Hermes Gateway/Dashboard active/enabled; Dashboard self-hosted OIDC and PKCE/S256; loopback `127.0.0.1:9119`; private Hermes API `172.19.0.1:8642`; Docker network `n8n_hermes` with stable Linux bridge `n8n-hermes`; one active Hermes n8n workflow and two accepted credentials; stable UFW rule; Mattermost and foundation non-regression.
4. The attempted Antigravity `1.2.7` smoke verifiers that stalled are classified as assistant test-harness defects (root-owned temporary-directory traversal and job-control/timeout behavior), not production failures. No production mutation or service restart occurred.
5. Current repo/runtime drift is reconciled. Stage 5 entry is eligible.

**Acceptance evidence:** `STAGE4_FINAL_BOUNDARY_RECONCILIATION=PASS`; `STAGE4_FINAL_ACCEPTANCE_STATUS=SUPPORTED`.

**Supersedes:** only current-state references that described Antigravity `1.2.6` as the live runtime. It does not supersede or rewrite historical Stage 4B/4G acceptance evidence.
---

## 2026-09-19T18:01:00+03:00 — Three-node Knowledge Fabric roles and edge-only Stage 5 mutation scope

**Status:** ACCEPTED

Detailed record:

`STAGE_05_KNOWLEDGE_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`

**Context:** the fresh Stage 5 entry audit confirmed the accepted PVE canonical vault, healthy PVE ↔ ai-node Syncthing fabric, ai-node local n8n consumption, edge private reachability to Home/PAI, edge resource/account model, and absence of an existing edge Syncthing/Knowledge tree.

**Decision:**

1. PVE remains the canonical administrative/recovery Knowledge authority and Syncthing hub at `/srv/knowledge/obsidian`.
2. ai-node remains an active RW non-canonical replica at `/srv/ai-data/knowledge/obsidian` and the local Knowledge/application layer for PAI workloads; n8n is a confirmed current RW consumer.
3. edge becomes an active RW non-canonical replica at `/srv/knowledge/obsidian` and the Cloud Knowledge source for Hermes, n8n, Codex and Antigravity.
4. Replication topology remains PVE-centered: PVE ↔ ai-node plus PVE ↔ edge. Do not add direct edge ↔ ai-node Syncthing merely to create a nominal full mesh because the edge -> Home path itself depends on CT300 on PVE.
5. `canonical` does not make PVE an online master. Secondary nodes continue local RW application operation during disconnection; only convergence pauses.
6. edge ownership target is `/srv/knowledge core:core 0755` and `/srv/knowledge/obsidian core:core 2775`; Syncthing runs under `core`.
7. No Obsidian runtime/WebUI is required on edge. ai-node is the preferred future private Obsidian/WebUI host (`obsidian.lan` direction); PVE runtime remains optional/not established.
8. edge is the accepted future Internet-reachable data-access node for iOS/other external client applications. Exact client/protocol/access service remains unresolved and must not be substituted with public Syncthing exposure.
9. Cloud Stage 5 runtime mutation scope is **edge only**. PVE/ai-node target roles are recorded for future reconfiguration and for non-regression checks.
10. PVE currently lacks the edge Device ID/folder relationship; that remote authorization is a cross-project prerequisite to be performed under Home Infrastructure or after explicit later scope exception. Cloud Stage 5 must not silently mutate PVE.
11. OpenClaw keeps the current PVE canonical RO path. Direct ai-node Knowledge fallback is not required; n8n may pass locally sourced context to OpenClaw for n8n-driven tasks.

**Supersedes in part:** prior blanket statements that MacBook/iPhone/iPad Obsidian integration is completely outside Cloud Infrastructure. Future public/mobile data access through edge is now an accepted Cloud role, while exact implementation remains deferred.
---

## 2026-09-19 — Stage 05.1 scope correction and 05.2 implementation boundary

**Status:** ACCEPTED

Authoritative record:

`STAGE_05_1_KNOWLEDGE_RECONCILIATION_TARGET_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`

**Decision:**

1. Stage 5 is split into exactly two Cloud Infrastructure work branches:
   - `05.1 — Cross-project Knowledge Reconciliation & Target Architecture`;
   - `05.2 — Edge Knowledge Replication & Data Integration`.
2. 05.1 is research/architecture only and is COMPLETE / ACCEPTED.
3. 05.2 owns all Stage 5 runtime implementation and final acceptance.
4. 05.2 is centered on edge deployment but may inspect and modify PVE where required for edge↔PVE Syncthing integration, topology correctness and verification.
5. ai-node is not redesigned in Stage 5; do not deploy the future Obsidian WebUI or otherwise restructure PAI application architecture in 05.2.
6. OpenClaw behavior/current PVE Knowledge relationship is not redesigned in Stage 5.
7. Future external iOS/macOS/Windows client data access through edge remains part of the documented target architecture but is **not implemented in Stage 5**.
8. Existing PVE↔ai-node runtime is preserved and verified for non-regression; edge→PVE→ai-node propagation is an acceptance requirement.

**Supersedes:** only clauses 9–10 of the immediately preceding accepted decision `Three-node Knowledge Fabric roles and edge-only Stage 5 mutation scope` insofar as they restricted Stage 5 mutations to edge and treated PVE peer authorization as an external prerequisite. All non-conflicting topology, role, path and future-access decisions remain accepted.
---

## 2026-09-19 — Final Knowledge runtime placement and three-branch Stage 5 structure

**Status:** ACCEPTED

Authoritative record:

`STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`

**Context:** fresh PVE resource readiness confirmed an Intel Core i3-N305 with 8 cores, ~15 GiB RAM, ~6.5 GiB available memory, existing 8 GiB host swap with ~5.6 GiB free, and the canonical vault already isolated on the dedicated `pve/knowledge` 32 GiB ext4 LV. The operator selected a PVE-centered full Obsidian runtime model and split Stage 5 further to isolate PVE application deployment from edge deployment.

**Decision:**

1. PVE remains canonical RW Knowledge authority, Syncthing hub and primary durable Knowledge recovery authority.
2. A new dedicated lightweight PVE LXC becomes the single full server-side Obsidian application node for the canonical vault.
3. Initial LXC envelope: 1 vCPU, 1024 MiB RAM, 512 MiB swap, approximately 4 GiB rootfs, onboot enabled.
4. The vault remains on `/srv/knowledge/obsidian` backed by the dedicated `pve/knowledge` LV and is RW bind-mounted into the LXC; it must not be copied into or depend on the LXC rootfs.
5. The PVE Obsidian runtime provides File Recovery, index/metadata, CLI/core-plugin capability and private `obsidian.lan` browser UI.
6. `obsidian.lan` is private Home LAN / NetBird-routed access only.
7. ai-node remains a secondary RW PAI/application replica with n8n/OCR/RAG/AI consumers and no server-side Obsidian runtime/WebUI by default.
8. edge remains a secondary RW Cloud/agent replica. No edge Obsidian WebUI/runtime is deployed in Stage 5.
9. Future iOS/macOS/Windows/Android client access terminates on edge through a separately selected client-facing mechanism. That implementation is not part of Stage 5. A future edge Obsidian runtime is conditional only if the later client-access design or another explicitly accepted edge-local Obsidian requirement needs it.
10. Existing 8 GiB PVE host swap remains unchanged. Do not expand swap merely because disk space is available; revisit only if post-deployment measurements show actual pressure.
11. LXC runtime packaging is not pre-committed to native or Docker. Stage 05.2 compares official native Obsidian + native Selkies against LinuxServer Obsidian/Selkies and selects the simpler, better-supported stable implementation. Native is a preference, not a requirement.
12. Stage 5 is split into three branches:
    - `05.1 — Cross-project Knowledge Reconciliation & Target Architecture` — COMPLETE / ACCEPTED;
    - `05.2 — PVE Canonical Obsidian Runtime & WebUI` — NEXT;
    - `05.3 — Edge Knowledge Replication & Data Integration` — PLANNED.
13. 05.2 owns PVE Obsidian LXC/runtime/WebUI deployment and non-regression acceptance.
14. 05.3 owns edge replica/Syncthing/consumer deployment and final Stage 5 integration acceptance.
15. OpenClaw keeps its current PVE canonical RO Knowledge relationship; Stage 5 does not redesign it.

**Supersedes:** the prior Stage 05.1 decisions that (a) placed the future private Obsidian WebUI on ai-node, (b) treated PVE Obsidian runtime as optional/not required, and (c) split Stage 5 into only 05.1 + 05.2 with edge deployment as 05.2. Non-conflicting topology, paths and audit evidence remain accepted.

---

## 2026-09-19 — Stage 05.2 Obsidian runtime packaging and rootfs sizing

**Status:** SUPERSEDED

**Decision:**

1. Stage 05.2 uses **LinuxServer Obsidian/Selkies inside the dedicated PVE LXC**.
2. The native official Obsidian + native Selkies alternative is not selected for this deployment because the LinuxServer image provides a more integrated display/session/WebUI lifecycle and a simpler upstream-supported container update path.
3. The LXC resource envelope is 1 vCPU, 1024 MiB RAM, 512 MiB swap and **8 GiB rootfs**, with onboot enabled.
4. The increase from the earlier approximately 4 GiB planning value to 8 GiB is accepted because the LinuxServer image, Docker/containerd layers and persistent application state make 4 GiB unnecessarily tight.
5. The canonical vault remains outside the LXC rootfs at `/srv/knowledge/obsidian` and is mounted RW into the application LXC. This decision does not move or duplicate canonical Knowledge data.
6. PVE host swap remains unchanged at 8 GiB unless later measurements show real memory pressure.
7. Stage 05.2 implementation remains private Home LAN / NetBird only and does not add edge replication or external client access.

**Acceptance marker:** `STAGE05_2_RUNTIME_PACKAGING_GATE=PASS`

**Supersedes:** only the unresolved packaging gate and the approximately 4 GiB rootfs planning value in the 2026-09-19 final Stage 05.1 runtime-placement decision. All other Stage 05.1 architecture remains accepted.
---

## 2026-09-19 — Stage 05.2 CT210 rootfs resize after measured LSIO footprint

**Status:** SUPERSEDED

**Context:** the LinuxServer Obsidian/Selkies smoke deployment on CT210 measured approximately 6.4 GiB used on the originally accepted 8 GiB rootfs, leaving only about 997 MiB free (87% used). The active LSIO image measured approximately 5.179 GB and the container writable layer approximately 362 MB, leaving insufficient practical headroom for normal pull/recreate updates.

**Decision:**

1. CT210 rootfs is increased from 8 GiB to **16 GiB**.
2. The resize is performed in place on `local-lvm`; the canonical vault remains outside the rootfs and is not involved.
3. Post-resize filesystem use is approximately 44% with about 8.5 GiB free.
4. Docker and Obsidian/Selkies restart persistence passed after CT stop/start; HTTPS recovered immediately and the container retained `RestartCount=0`.
5. The earlier 8 GiB rootfs target is superseded by measured production packaging requirements.

**Acceptance marker:** `STAGE05_2_CT210_ROOTFS_RESIZE=PASS`



---

## 2026-09-19 — Stage 05.2 Ignis runtime selection and clean production reset

**Status:** ACCEPTED

**Context:** Stage 05.2 performed a bounded comparative experiment without mounting the canonical vault. LinuxServer Obsidian/Selkies proved unnecessarily heavy for the role. Native official Obsidian + Selkies 2.0.0rc0 preserved the Electron runtime but failed the required adaptive browser UX without Selkies-specific compositor/session plumbing. Ignis provided the required browser UX and then passed the server-role acceptance on an isolated test vault. After selection, the entire experimental CT210 was stopped and destroyed; its rootfs and PVE registration are absent and the canonical vault was never mounted or mutated by the experiment.

**Decision:**

1. Stage 05.2 production runtime is **Ignis inside a dedicated PVE LXC**.
2. The dedicated LXC remains justified as an independent lifecycle boundary for the RW canonical-vault application runtime; do not merge Ignis into unrelated existing LXCs or install Docker directly on the PVE host merely to save a small amount of RAM.
3. Production CT210 starts fresh with **1 vCPU, 512 MiB RAM, 256 MiB swap, 8 GiB rootfs and onboot enabled**.
4. The canonical vault remains ordinary filesystem data on PVE at `/srv/knowledge/obsidian` and is bind-mounted RW into CT210. Ignis must not become a separate source of truth.
5. Ignis supplies the private Obsidian WebUI plus the Obsidian-aware capabilities required by the PVE role: File Recovery baseline, filesystem/external-change bridge, and the headless bridge (`ob` / Headless Sync). Full native Electron parity is not a requirement unless a concrete workflow later proves it necessary.
6. Syncthing replication and Restic/Backrest recovery remain independent infrastructure layers and are not acceptance responsibilities of Ignis itself.
7. The normal maintenance/update unit is the **Ignis image**. Use the Obsidian version supported by the installed Ignis release; do not independently auto-update or advance Obsidian ahead of Ignis without a concrete compatibility reason.
8. `obsidian.lan` remains private to Home LAN and NetBird-routed Home clients.
9. Experimental versions, images and the temporary 16 GiB CT210 rootfs are historical test evidence only and are not production baselines.
10. Production Stage 05.2 implementation is still **not started** after this decision; a new clean 05.2 production branch creates CT210 from scratch and performs the canonical-vault deployment.

**Acceptance evidence:**

- `IGNIS_FILESYSTEM_BRIDGE=PASS`
- `IGNIS_EXTERNAL_CHANGE_VISIBILITY=PASS`
- `IGNIS_FILE_RECOVERY_BASELINE=PASS`
- `IGNIS_HEADLESS_BRIDGE=PASS`
- `IGNIS_RESTART_PERSISTENCE=PASS`
- `CANONICAL_VAULT_ISOLATION=PASS`
- `IGNIS_SERVER_ROLE_ACCEPTANCE=PASS`
- `STAGE05_2_CT210_EXPERIMENT_FULL_PRUNE=PASS`

**Supersedes:** the 2026-09-19 Stage 05.2 LinuxServer Obsidian/Selkies packaging decision and the subsequent 16 GiB LSIO rootfs resize decision. It also resolves the runtime-packaging comparison gate in the Stage 05.1 architecture. Non-conflicting Stage 05.1 topology and data-role decisions remain accepted.

---

## 2026-09-19 — Stage 05.2 production deployment and final acceptance

**Status:** ACCEPTED

**Context:** The clean production CT210 deployment completed after the Ignis runtime-selection experiment. Initial direct mounting of the canonical vault under Ignis `/vaults` exposed an upstream entrypoint behavior that recursively `chown -R`s `/vaults` on startup and changed the canonical PVE root ownership. The production integration was corrected without patching the Ignis image by using the upstream-supported symlinked-vault pattern and mounting the canonical target at the same absolute path inside the container.

**Decision:**

1. CT210 `obsidian` is the accepted production PVE Obsidian runtime: 1 vCPU, 512 MiB RAM, 256 MiB swap, 8 GiB rootfs, onboot, static `192.168.1.15/24`.
2. PVE `/srv/knowledge/obsidian` remains the sole canonical vault and is mounted RW into CT210; canonical root ownership remains `0:990:2775`.
3. Ignis runs unpatched from the upstream image update path. Inside Ignis, `/vaults/obsidian` is a symlink to `/srv/knowledge/obsidian`; the canonical path is separately bind-mounted at that same absolute location. This prevents Ignis startup recursive ownership changes from traversing the canonical tree while preserving normal upstream updates.
4. Ignis writes as `PUID=999`, `PGID=990`. Current accepted application stack is Ignis 0.8.11 / Obsidian 1.12.7 with Caddy private HTTPS.
5. `obsidian.lan -> 192.168.1.15` is the accepted private DNS identity through MikroTik. Caddy internal CA is the accepted TLS mechanism for Home LAN / NetBird clients; the CA private key remains inside CT210 and only the root certificate is distributed to clients.
6. Obsidian `Use native menus` / system context menu must remain disabled in Ignis because Electron-native menu codepaths do not work in the browser. With it disabled, create/edit/delete UI operations are accepted.
7. File Recovery is enabled/configured. Production acceptance does not require a repeated destructive restore E2E because the runtime-selection gate already established the File Recovery baseline and the final production audit confirms the core plugin is enabled.
8. Final LXC reboot/autostart, DNS/HTTPS recovery, canonical ownership persistence and measured resource envelope all pass. No resource increase is justified by current evidence.
9. Stage 05.2 is COMPLETE / ACCEPTED. Stage 05.3 becomes the next Cloud Infrastructure stage.

**Acceptance marker:** `STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS`

**Supersedes:** only the previous current-state wording that production Stage 05.2 had not started. It does not rewrite the historical runtime-selection experiment or its cleanup evidence.

---

## 2026-09-20T00:47:25+03:00 — Stage 05.3 deployment and final Stage 5 acceptance

**Status:** ACCEPTED

**Context:** Stage 05.3 deployed and exercised the edge Knowledge replica against the already accepted PVE hub. Fresh runtime evidence confirmed the standard edge path, Syncthing peer behavior, n8n container identity/path compatibility, bidirectional propagation, controlled outage/conflict handling and full edge reboot recovery. Earlier planning text that used the container alias `/home/node/knowledge-canonical` was not implemented.

**Decision:**

1. edge is an active RW non-authoritative Knowledge replica at `/srv/knowledge/obsidian`; `/srv/knowledge` is `core:core 0755` and the vault root is `core:core 2775`.
2. edge uses Syncthing `2.1.5` under `core` via `syncthing@core.service`, enabled at boot.
3. edge initiates the PVE peer connection to `tcp://192.168.1.3:22000`; PVE remains the Syncthing hub and retains its existing ai-node peer.
4. edge Syncthing GUI/API and listener remain loopback-only at `127.0.0.1:8384` and `127.0.0.1:22000`; global/local discovery, relays and NAT traversal are disabled.
5. Hermes, Codex and Antigravity use `/srv/knowledge/obsidian` directly on the host.
6. edge n8n uses the same path on both sides of the bind: `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`. The older planned alias `/home/node/knowledge-canonical` is superseded.
7. Accepted topology remains PVE ↔ ai-node plus PVE ↔ edge; no direct edge ↔ ai-node peer is added.
8. PVE → edge, edge → PVE and edge → PVE → ai-node live propagation passed.
9. Controlled edge Syncthing outage/reconnect and divergent-edit conflict preservation passed without silent data loss. Whether the conflict copy itself reached ai-node before cleanup was not directly captured; normal edge → PVE → ai-node propagation was independently verified.
10. Controlled edge reboot acceptance passed: Syncthing auto-started, recovered the PVE connection, Knowledge converged with no pending items/pull errors, n8n returned healthy with its Knowledge bind, and Stage 4 user services remained active.
11. No edge Obsidian runtime/WebUI or public Syncthing exposure is part of the accepted baseline.
12. Stage 05.3 is COMPLETE / ACCEPTED and Stage 5 as a whole is COMPLETE / ACCEPTED. Stage 6 — Edge Backrest & Recovery is next.

**Acceptance markers:**

- `STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS`
- `STAGE05_FINAL_ACCEPTANCE=PASS`

**Supersedes:** the prior planned/not-started status for 05.3 and the earlier planned edge n8n alias `/home/node/knowledge-canonical`. It does not rewrite historical Stage 05.1/05.2 acceptance evidence.

## 2026-09-20T19:20:00+03:00 — Stage 6 edge backup scope simplified to one general DR chain

**Status:** ACCEPTED

**Context:** Edge is a single personal VPS where the highest-value recovery need is current user/application state plus rollback after failed service/system updates. Splitting general protection into separate broad system and broad data plans adds operational complexity without a demonstrated recovery benefit.

**Decision:**

- use one general Backrest/Restic backup plan for the edge VPS, covering the root filesystem broadly rather than maintaining separate system/data plans;
- include persistent application/user state under `/srv` in that same general plan; exact exclusions remain limited to non-recoverable/runtime/transient content and the local Restic repository itself;
- use a short local retention tier on edge and replicate successful general snapshots to CT208/D5 through the accepted append-only rest-server path;
- D5 general-backup history must not exceed approximately six months; exact daily/weekly/monthly bucket counts are finalized in the retention substage;
- local edge history must be materially shorter than D5 and exists primarily for fast rollback / temporary Home-D5 unavailability;
- do not create a periodic Restic full/bare-metal backup chain for edge;
- after final edge infrastructure acceptance, the operator will create one manual provider-panel golden backup/snapshot outside Backrest as the clean post-build baseline;
- keep Knowledge as the sole separate backup chain: whole `/srv/knowledge`, local-only on edge, no D5 tier-copy, using the already accepted 2-hour stagger relative to ai-node (`04:00/10:00/16:00/22:00` local while ai-node uses `02:00/08:00/14:00/20:00`);
- Knowledge remains independent because it has a distinct high-frequency history/recovery purpose.

**Constraints:** Do not duplicate general edge data in separate system/data Restic plans. Do not introduce a VPS full-image/full-Restic chain unless a new concrete recovery requirement appears. Application-consistent handling for live databases is still required inside the single general plan and is designed separately.

**Supersedes:** proposals to split edge general protection into separate `edge-system` and `edge-data` plans, and proposals for a recurring edge full/bare-metal Restic chain.

---

## 2026-09-21T09:09:00+03:00 — Stage 6 deployment contract and D5 retention normalization

**Status:** ACCEPTED

**Context:** Expanded read-only audits of edge and ai-node confirmed the final persistent-state inventory, live database classes, current Backrest/Restic topology and the unnecessary cost of backing up reproducible container layers. The operator rejected a rolling 180-day D5 archive for edge because hundreds of equal-granularity restore points are operationally hard to navigate and requested the same day/week/month model already used for ai-node State.

**Decision:**

- edge dedicated Knowledge is deployed and accepted at `/srv/knowledge`, schedule `04/10/16/22`, rolling local `14d`, no D5;
- edge general backup uses one plan `edge-state`, broad persistent roots, schedule `01/07/13/19`, local rolling `7d`, grouping `host,tags`;
- successful edge-state snapshots are copied to CT208/D5 over the existing append-only rest-server path;
- CT208 owns D5 forget/prune with State-class retention: daily30, weekly8, monthly6, yearly0, grouped by `host,tags`;
- exclude backup/self-reference, dedicated Knowledge, Docker/containerd layers and selected rebuildable caches; keep `/srv/backups`;
- use application-consistent staging for n8n, Authelia, Mattermost/PostgreSQL, Stalwart/Bulwark and known agent SQLite stores;
- no recurring edge full/bare-metal Restic chain; one provider-panel golden VPS snapshot is created only after final infrastructure acceptance;
- apply the accepted ai-node corrections documented in `STAGE_06_6_DEPLOYMENT_CONTRACT_2026-09-21.md` without redesigning its established D5 bucket policies.

**Detailed contract:** `STAGE_06_6_DEPLOYMENT_CONTRACT_2026-09-21.md`.

**Supersedes:** only the unresolved Stage 6 retention/consistency details and the rejected rolling-180d D5 edge proposal. The previously accepted one-general-plan edge topology remains in force.

## 2026-09-21T10:45:00+03:00 — Stage 06.7 production backup deployment accepted

**Status:** ACCEPTED

**Context:** Stage 06.6 defined the exact deployment contract. Stage 06.7 then deployed and verified the production edge general plan, CT208/D5 append-only copy path, consistency staging, and the previously accepted bounded ai-node corrections. Two verifier defects were encountered during acceptance (source/destination Restic snapshot IDs differ after `restic copy`; and a premature Backrest restart interrupted an ai-node success hook). Both were reconciled without redesigning the accepted architecture.

**Decision:**

- accept `edge-state` production backup runtime at schedule `01/07/13/19`, local rolling `7d`, grouping `host,tags`, with application-consistent staging and successful append-only D5 copy;
- accept D5 State retention daily30/weekly8/monthly6/yearly0 under CT208 maintenance;
- accept ai-node tier-copy grouping `host,tags`;
- accept self-contained n8n SQLite staging with `journal_mode=delete` and no WAL/SHM dependency;
- accept full-system Docker/containerd exclusions;
- accept local full `keep-last 2` only after successful D5 copy, grouped by `host,tags`;
- accept reconciled full-restore external mount directories;
- keep dedicated Knowledge policies unchanged;
- Stage 06.7 is COMPLETE / ACCEPTED with `STAGE06_7_FINAL_ACCEPTANCE=PASS`;
- Stage 06.8 isolated restore/application usability remains mandatory before final Stage 6 acceptance.

**Evidence:** `STAGE_06_7_FINAL_ACCEPTANCE_2026-09-21.md`.

**Supersedes:** no accepted topology. This closes the implementation status left open by the Stage 06.6 deployment contract.

## 2026-09-21T11:10:00+03:00 — Stage 06.8 isolated restore and application recovery accepted

**Status:** ACCEPTED

**Context:** Stage 06.8 exercised real D5 restore paths for the accepted Stage 6 backup design in isolated temporary environments without overwriting production.

**Decision:**

- accept the edge D5 filesystem restore and restored transactional/application state as usable;
- accept Mattermost PostgreSQL dump restore and restored application boot against the recovered database;
- accept restored n8n, Authelia, Stalwart and Bulwark application boot/usability on edge;
- accept integrity of the 24 staged agent SQLite overlays;
- accept ai-node n8n D5 restore, self-contained SQLite state and isolated application boot;
- classify the PostgreSQL 18 temporary mount failure encountered during testing as a test-harness defect, not a backup/restore defect;
- Stage 06.8 is COMPLETE / ACCEPTED with `STAGE06_8_FINAL_ACCEPTANCE=PASS`;
- proceed to Stage 06.9 final Stage 6 non-regression/persistence/cleanup acceptance.

**Evidence:** `STAGE_06_8_FINAL_ACCEPTANCE_2026-09-21.md`.

**Supersedes:** no accepted topology or retention decision.

## 2026-09-21T11:15:00+03:00 — Stage 06 final acceptance

**Status:** ACCEPTED

**Context:** Stage 06.7 deployed and verified the production backup chains; Stage 06.8 proved real isolated D5 restores and application usability; Stage 06.9 completed final cleanup and non-regression. The pre-existing CloudCLI CHDIR drift was also reconciled before final acceptance.

**Decision:**

- Stage 6 — Edge Backrest & Recovery is COMPLETE / ACCEPTED;
- final marker: `STAGE06_FINAL_ACCEPTANCE=PASS`;
- retain the accepted edge Knowledge, edge-state, CT208/D5, and bounded ai-node backup contracts;
- accept the tested restore paths as the Stage 6 recovery baseline;
- retain the existing CloudCLI systemd unit contract and restored `/srv/ai-workspace` root;
- no Stage 6 reboot acceptance is required;
- proceed to Stage 7 — Edge Maintenance & Update.

**Evidence:** `STAGE_06_FINAL_ACCEPTANCE_2026-09-21.md`.

**Supersedes:** the Stage 6 IN PROGRESS state only; no accepted topology is superseded.

## 2026-09-21 — Stage 7 backup sequencing clarification

**Status:** ACCEPTED

**Context:** Stage 6 was intentionally completed before Stage 7 so a verified backup/restore capability would already exist while Semaphore and the maintenance/update workflow are being deployed, modified and tested.

**Decision:**
- Stage 6 -> Stage 7 ordering is a deployment/testing safety dependency.
- Do not interpret this ordering as a requirement to invoke Backrest before every routine production update.
- A per-update backup step is component-specific and is added only when the concrete supported update/recovery path justifies it.
- Stage 7 still requires component-specific update paths, health checks, failure reporting and recovery/rollback handling, but not a universal runtime backup gate.

**Supersedes:** any Stage 7 wording that described a universal mandatory pre-update Backrest gate.

## 2026-09-21 — Stage 7 Home Maintenance framework reuse and dashboard port

**Status:** ACCEPTED

**Context:** The Stage 7 runtime/contract audit of Home CT1000 proved that Home Maintenance is already a mature, modular implementation rather than a thin Semaphore wrapper. It contains a reusable version/status collector and cache, fixed-target dispatch, per-component update drivers, Master Batch orchestration, post-update refresh/acceptance and an operational dashboard. Reimplementing those mechanisms independently on edge would add duplication and regression risk without a demonstrated benefit.

**Decision:**
- derive Edge Maintenance from the accepted live Home Maintenance implementation at CT1000 `/opt/maintenance-repo`;
- preserve its architecture, Semaphore workflow, status/cache model, fixed-target dispatch, per-component driver pattern, post-update refresh/acceptance flow and dashboard wherever applicable;
- replace Home/PVE-specific inventory, VMID/PCT/QGA logic, target definitions, collectors and update drivers with edge-specific equivalents;
- do not copy Home credentials, SSH keys or controller-specific runtime state;
- retain automatic real updates disabled by default unless a later explicit decision changes that policy;
- begin `update.escloud.us` as an adapted copy of the existing Home Maintenance dashboard implementation and status/action contract instead of building a new frontend from scratch;
- Stage 7C is therefore an adaptation/refinement substage for the copied dashboard, not a greenfield UI build;
- do not introduce a second independent maintenance framework or dashboard without a demonstrated incompatibility with the accepted Home-derived design.

**Stage decomposition:**
- Stage 7A — Home Maintenance Framework Port: Semaphore + framework + read-only edge version/status model + copied dashboard baseline;
- Stage 7B — Edge Update Drivers & Recovery: edge-specific update adapters, health/failure/recovery handling, individual manual updates and Master Batch acceptance;
- Stage 7C — Codex: adapt/refine the copied dashboard for `update.escloud.us`.

**Constraints:** The separate accepted Stage 7 backup-sequencing decision remains in force: Stage 6 exists as deployment/testing recovery protection, not as a universal mandatory pre-update Backrest gate.

**Supersedes:** prior Stage 7 wording that implied an independent new maintenance framework or a greenfield `update.escloud.us` frontend.

## 2026-09-21 — Stage 7A read-only framework final acceptance

**Status:** ACCEPTED

**Context:** The Home-derived maintenance framework has completed deployment, recovery and full read-only E2E testing on edge.

**Decision:**
- Stage 7A — Home Maintenance Framework Port is COMPLETE / ACCEPTED.
- Retain Semaphore as a host-native loopback service with project `Edge Maintenance`.
- Semaphore repository uses the canonical `Eugene-SN/Cloud-Infrastructure` repository on branch `main`.
- The accepted Refresh template is ID `1` and executes `maintenance/edge/playbooks/semaphore-refresh.yml`.
- The adapted Home dashboard remains loopback-only at the Stage 7A boundary; public `update.escloud.us` ingress remains deferred.
- The action surface remains read-only: Refresh is allowed; component update templates, Master Batch and automatic updates remain disabled until Stage 7B explicitly accepts them.
- Hysteria2 upstream tag namespace `app/` is normalized before version comparison.
- The Stage 7A E2E path dashboard -> Semaphore -> canonical GitHub playbook -> local collectors/cache -> dashboard is accepted.
- Stage 7A executed no real component update and passed production non-regression.

**Acceptance marker:** `STAGE07A_READONLY_DASHBOARD_SEMAPHORE_E2E=PASS`.

**Next:** Stage 7B — Edge Update Drivers & Recovery.

**Supersedes:** Stage 7A deployment-checkpoint state that kept the substage IN PROGRESS pending dashboard/Semaphore E2E.

## 2026-09-21 — Stage 7 manual update execution through update.escloud.us only

**Status:** ACCEPTED

**Context:** The operator requires direct manual review and initiation of every real update through the deployed maintenance page. Automatic or background update execution would prevent that verification workflow.

**Decision:**
- `update.escloud.us` is the only operator surface permitted to initiate a real Stage 7 update;
- Semaphore remains the backend execution/orchestration engine only;
- do not create or enable update timers, cron jobs, systemd update services, background update daemons, unattended updates, scheduled update jobs, or equivalent autonomous launch mechanisms;
- the rule applies to individual component updates, Master Batch, and Stage 7B acceptance tests;
- each new driver is first exposed in `update.escloud.us`; the operator inspects the presented state/version and manually starts the test update from the page;
- read-only version/status refresh is allowed as part of the page workflow but must not automatically chain into a real update.

**Constraint:** No Stage 7B implementation step may execute a production update on behalf of the operator outside the maintenance page.

**Supersedes:** any wording that treated `auto_update=false` merely as a default that could still allow scheduled/background/manual-outside-UI update execution during Stage 7B.

## 2026-09-21 — update.escloud.us public ingress and origin-relative redirects

**Status:** ACCEPTED

**Context:** Public HTTPS ingress for `update.escloud.us` was activated after the Stage 7A loopback-only acceptance boundary. The internal dashboard nginx listens on `127.0.0.1:18070`, while the public nginx proxies authenticated traffic to it. Its root handler returned `302 /status/`; with nginx `absolute_redirect` enabled by default, the internal server serialized that relative target as `http://update.escloud.us:18070/status/`. The public proxy passed the `Location` header through, exposing a private loopback port in the browser and producing an unreachable URL.

**Decision:**
- the canonical operator URL is `https://update.escloud.us/`;
- retain the existing public Xray -> host nginx -> Authelia -> loopback dashboard route;
- retain `127.0.0.1:18070` as a private backend only, with no TCP/18070 UFW opening;
- configure the internal root handler with location-scoped `absolute_redirect off` and return `302 /status/`;
- require origin-relative redirects from this backend so its internal scheme and port cannot appear in public browser URLs;
- keep the Stage 7B manual-update execution boundary unchanged.

**Verification:** The internal root response now contains exactly `Location: /status/`; `/status/` returns HTTP 200; public HTTP redirects to HTTPS; public HTTPS redirects unauthenticated clients to Authelia; TCP/18070 remains bound only to loopback and unreachable publicly; nginx configuration validation and service-health checks pass.

**Acceptance marker:** `STAGE07_UPDATE_ROOT_REDIRECT_FIX=PASS`.

**Evidence:** `STAGE_07_UPDATE_INGRESS_REDIRECT_FIX_2026-09-21.md`.

**Supersedes:** only the current-runtime implication that public `update.escloud.us` ingress remained deferred after the Stage 7A boundary. The Stage 7A acceptance record remains historically accurate.
