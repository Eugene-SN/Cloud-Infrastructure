# AGENTS.md — Cloud Infrastructure

These are durable project-specific rules for any agent working in this repository.

## Required context before work

Read, in this order when relevant:

1. `OPERATING_RULES.md`
2. `DECISIONS.md`
3. `CURRENT_STATE.md`
4. `IMPLEMENTATION_PHASES.md`
5. `FUNCTIONAL_SCAFFOLD_DRAFT.md`
6. `ARCHITECTURE.md`
7. `INVENTORY.md`
8. stage-specific acceptance records relevant to the current task
9. `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` only when legacy/as-is VPS facts are needed.

## Current checkpoint invariant

Current canonical work is:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Stage 0, Stage 1 and Stage 2 are complete and accepted. `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Stage 02.5 is **research-only**. Do not deploy/install/configure a new production service, mutate production DNS/firewall/runtime, or open the next production branch until all Stage 02.5 deliverables are explicitly accepted and canonical files are updated/read back.

Completed Stage 02.5 research blocks:

- Remaining Standalone Core Services — Hermes Agent selected;
- Cross-site Connectivity Foundation — existing self-hosted NetBird selected/reused with bidirectional routed Cloud ↔ Home/PAI fabric and existing `.lan` split DNS.

Current next research block is **Cross-site Data & Knowledge Services**.

## Current planned stage order

- Stage 3 — `03 — Edge Cross-site Connectivity Foundation`
- Stage 4 — `04 — Edge Hermes Agent Runtime`
- Stage 5 — `05 — Edge Cross-site Data & Knowledge Services`
- Stage 6 — `06 — Edge Remaining Infrastructure Services` — conditional; remove/renumber if empty at Stage 02.5 closure
- Stage 7 — `07 — Edge Backrest & Recovery`
- Stage 8 — `08 — Edge Maintenance & Update`
- Stage 9 — `09 — Edge Monitoring, Heartbeats & Alerts`
- Stage 10 — `10 — Edge Cloud Portal`
- Stage 11 — `11 — Edge Final Integrated Infrastructure Acceptance`

After Stage 11, Automation & User Workflows is a continuous post-infrastructure workstream, not an infrastructure-completion stage.

The former `Hermes Stage 3 / Connectivity Stage 4` ordering is historical and superseded.

## Stage workflow invariant

Each implementation stage has its own work branch. Every stage branch begins with design/discussion before deployment:

1. review exact requirements/baseline for that stage;
2. research only genuinely unresolved product/mechanism choices;
3. explicitly accept stage composition;
4. define the stage-scoped architecture/deployment contract and recovery path;
5. deploy;
6. verify properties, not only command RC;
7. explicitly accept and persist current state/decisions;
8. only then propose the next work branch.

A completed subtask is not sufficient reason to leave a branch while accepted scope remains incomplete.

## Functional scaffold invariant

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a capability/requirements map, not an independent product inventory or chronology source.

- Do not infer a product merely because a capability exists.
- Do not preselect services to fill architecture diagrams or empty stages.
- Already accepted products should not be re-compared without a concrete incompatibility, regression or changed requirement.
- Separate finite infrastructure services from continually evolving n8n/agent workflows.

## Stable project rules

- Treat `nl-core-vds` as historical/as-is identity and `edge` as the current live logical node.
- Never rewrite historical baseline/audit artifacts to use target-state naming.
- Cloud Infrastructure complements Home Infrastructure and PAI; do not duplicate them merely because a function can run on a VPS.
- Do not infer that an installed legacy service belongs in target state.
- Do not convert proposals/candidates into accepted architecture without an explicit accepted decision.
- Preserve decision chronology and supersession semantics.
- Fresh runtime/configuration outranks historical reference for factual state.
- Single-operator simplicity, minimum components and upstream-supported mechanisms are preferred over enterprise complexity.

## Accepted product anchors

Unless a later accepted decision supersedes them, do not search for replacements for:

- Xray
- Hysteria2
- nginx
- Authelia
- n8n
- CloudCLI
- Codex CLI
- Antigravity CLI
- Stalwart + Bulwark
- Hermes Agent
- existing self-hosted NetBird for Cloud ↔ Home/PAI private connectivity

Backrest + Restic is the accepted backup-management direction. Semaphore is the accepted operational execution product.

## Stage 3 connectivity invariant

Detailed accepted architecture:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Stage 3 reuses the existing Home self-hosted NetBird architecture as a bidirectional routed private fabric.

Accepted facts/direction:

- Home LAN `192.168.1.0/24`;
- CT300 `remote-access` `192.168.1.90` remains the Home routing peer;
- NetBird account IPv4 overlay `100.105.0.0/16`;
- `edge` becomes an ordinary **host-native** NetBird service peer;
- `edge` receives the Home LAN resource but must **not** receive Home `0.0.0.0/0` Internet Exit;
- `edge` keeps its VPS-provider default Internet route;
- Home/PAI clientless hosts reach `edge` through gateway-level `100.105.0.0/16 via 192.168.1.90` routing on both VM100 and MikroTik;
- VM100 receives only the narrow forwarding allowance required for LAN → NetBird-account traffic;
- reuse and verify NetBird-managed Site-to-VPN masquerade before adding any manual NAT;
- individual NetBird peers on PVE/`ai-node`/CT220 are not baseline requirements;
- reuse existing `.lan` split DNS: `192.168.1.1:53` only for match domain `lan`; ordinary `edge` DNS remains VPS-local;
- add `edge.lan` through the existing Home DNS mechanism after enrollment/routing acceptance;
- verify real direct/relay behavior and controlled VRRP failover during Stage 3 acceptance.

Existing remote-user Internet Exit remains a separate capability of `User Devices`: CT300 policy-routes traffic from `wt0` through VRRP VIP `192.168.1.254`, normally reaching VM100/Mihomo. Do not assign this resource to `edge`.

Direct WireGuard and Tailscale are rejected as duplicate parallel backbones. AmneziaWG is contingency only if real NetBird acceptance demonstrates an unresolved transport/DPI failure.

Connectivity means transport/reachability/private naming. Durable application-level task retry/store-and-forward is a later workflow concern.

## Stage 4 Hermes invariant

Stage 4 is **Hermes-only** plus the minimum consumer-side integration needed to use already accepted executors and local vLLM over Stage 3 connectivity.

Role separation:

- n8n — deterministic workflow/orchestration plane;
- Hermes — persistent cloud-side agentic reasoning/tool/delegation plane;
- CloudCLI — manual web/remote cloud-AI workspace;
- Codex CLI and Antigravity CLI — specialized executors usable manually and delegatable by Hermes;
- OpenClaw — Home/PAI-side local personal agent;
- vLLM on `ai-node` — local inference backend reached through the accepted Stage 3 private fabric.

Preferred Hermes deployment is **host-native under `core`**. Docker is not preferred because it would complicate direct reuse of existing host-native Codex/Antigravity binaries and user/runtime/auth context. Reconsider only for a concrete upstream/runtime incompatibility.

Stage 4 should verify:

`n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`

and also real:

`Hermes -> vLLM on ai-node`

Stage 4 must inspect the actual vLLM bind/exposure state and make only the minimum change needed for private access through Stage 3. Do not implement user-specific n8n/Hermes workflows in Stage 4. Do not assume a public Hermes domain/listener.

## Knowledge/Obsidian invariant

Canonical Obsidian vault remains:

`ai-node:/srv/ai-data/knowledge/obsidian`

Do not make `edge` the canonical source of truth by assumption. File/sync/Obsidian implementations are selected for Stage 5 only after Stage 3 connectivity is accepted. Avoid paid Obsidian Sync and do not combine multiple primary synchronization mechanisms for one vault.

## Files and synchronization

Filestash, SFTPGo, Syncthing, Self-hosted LiveSync/CouchDB and other file/sync implementations remain candidates until explicitly accepted.

Stage 5 requirements include as appropriate:

- VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web browsing/editing of selected VPS files;
- cloud-agent access to the same working data;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror.

Do not conflate application task transport with general file synchronization.

## Lifecycle ordering invariants

- Backrest restore capability must be accepted before Semaphore/update testing.
- `update.escloud.us` is a dedicated maintenance/update page, separate from `app.escloud.us`, and is built as a separate Codex substage after the real backend contract is known.
- Production monitoring is deployed after the substantially complete service inventory, cross-site connectivity, Backrest and update subsystem exist.
- `app.escloud.us` is built as a separate Codex substage after monitoring/status sources and final service inventory are accepted.
- Final infrastructure acceptance follows all selected services, connectivity/data integration, backup/restore, maintenance/update, monitoring, portal and cleanup.