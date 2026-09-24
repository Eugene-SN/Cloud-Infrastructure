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

Current accepted checkpoint:

`Stage 13 — Backrest WebUI Ingress — COMPLETE / ACCEPTED`.

Stage 0 through Stage 13 are complete and accepted. Current markers include `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`, `STAGE4_FINAL_ACCEPTANCE=PASS`, `STAGE05_FINAL_ACCEPTANCE=PASS`, `STAGE06_FINAL_ACCEPTANCE=PASS`, `STAGE07_FINAL_ACCEPTANCE=PASS`, `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS`, `STAGE08_FINAL_ACCEPTANCE=PASS`, `STAGE09_FINAL_ACCEPTANCE=PASS`, `STAGE10_FINAL_ACCEPTANCE=PASS`, `STAGE11_FINAL_ACCEPTANCE=PASS`, `STAGE12_FINAL_ACCEPTANCE=PASS`, and `STAGE13_FINAL_ACCEPTANCE=PASS`.

Current canonical work is the post-infrastructure application and workflow layer (n8n, Hermes, Universal Capture, AI research and user-specific automations). Use `CURRENT_STATE.md` for confirmed runtime, `IMPLEMENTATION_PHASES.md` for the authoritative roadmap/substage scope, and the latest applicable ACCEPTED entries/records for supersession.

Do not duplicate mutable stage chronology in this file. `AGENTS.md` should contain durable cross-agent rules; volatile progress belongs in `CURRENT_STATE.md` and `IMPLEMENTATION_PHASES.md`.

## Repository and stage workflow invariant

The repository workflow is direct-to-`main` by default. Before work, fetch and read the latest `origin/main`. Persist a coherent accepted change as a commit directly on `main`, push it, and read back the remote commit and critical files. Create a branch or pull request only when the operator explicitly requests one.

Every implementation stage begins with design/discussion before deployment:

1. review exact requirements/baseline for that stage;
2. research only genuinely unresolved product/mechanism choices;
3. explicitly accept stage composition;
4. define the stage-scoped architecture/deployment contract and recovery path;
5. deploy;
6. verify properties, not only command RC;
7. explicitly accept and persist current state/decisions;
8. only then persist the completed scope to `main` and propose the next stage.

A completed subtask is not sufficient reason to leave accepted stage scope incomplete.

## Functional completeness invariant

Stage names, stage scopes and enumerated acceptance requirements define **minimum required outcomes and sequencing**, not an exhaustive ceiling on the capabilities of a selected service.

- When a product/service has already been selected, deploy a **functionally complete, practical upstream-supported installation** appropriate to its intended long-lived role, including common toolsets/runtime dependencies that are reasonably expected to be useful across future tasks.
- Do **not** omit a normal supported component merely because it is "not needed for the current/core Stage path". That phrase is not a valid exclusion rationale by itself.
- Avoid deliberately minimal/slim installation profiles when they would force repeated package/runtime upgrades as ordinary new use cases appear.
- Stage boundaries constrain sequencing, ownership and acceptance; they do not require artificial feature minimization inside an already selected service.
- Still avoid speculative complexity: do not automatically enable mutually exclusive backends, unrelated heavyweight subsystems, unsupported/immature features, paid services, or external integrations that require credentials/accounts and have no accepted use. Defer those for a concrete reason, and state that reason explicitly.
- Prefer installing shared local dependencies once when they support multiple standard capabilities of the selected service and carry no material downside.
- User-specific workflows may remain post-infrastructure even when the underlying service capabilities needed to support them are installed during the infrastructure stage.

## Functional scaffold invariant

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a capability/requirements map, not an independent product inventory or chronology source.

- Do not infer a product merely because a capability exists.
- Do not preselect services to fill architecture diagrams or empty stages.
- Already accepted products should not be re-compared without a concrete incompatibility, regression or changed requirement.
- Separate finite infrastructure services from continually evolving n8n/agent workflows.



## Evidence and assumption invariant

Never invent, infer silently, or present an unverified detail as factual project state.

Every material claim about runtime state, paths, names, versions, topology, ownership, configuration, behavior, capabilities, causes, or dependencies must be treated as one of:

- **CONFIRMED FACT** — directly supported by fresh runtime/config evidence, authoritative current repository state, explicit operator-provided evidence, or an authoritative upstream source applicable to the exact case;
- **INFERENCE** — logically derived from confirmed facts but not directly observed; label it explicitly as an inference and state the supporting facts;
- **ASSUMPTION** — plausible but lacking sufficient confirming evidence; label it explicitly as an assumption and state what evidence is missing;
- **UNKNOWN** — evidence is insufficient or contradictory.

Do not silently fill gaps from analogy, memory, previous deployments, naming conventions, best practices, or what would be convenient. If a proposed mutation depends materially on an inference or assumption, stop before mutation and obtain only the minimum read-only evidence needed to convert it into a confirmed fact or explicitly accepted design choice.

**Mutation boundary invariant:** never generate or execute a mutation based on an unverified assumption about runtime state, filesystem paths, deployment layout, ownership, service identity, versions, configuration, command availability, or integration behavior. If any fact required by the next mutation is uncertain, perform the smallest sufficient read-only audit first. Do not substitute a plausible default, historical pattern, repository layout, or remembered state for that audit. Assumptions may be discussed explicitly during design, but they are not valid inputs to mutation commands until verified or explicitly chosen by the operator as a new design decision.

When sources disagree, report drift/uncertainty explicitly. Do not choose the preferred-looking value and present it as fact.

## Mandatory research-before-change discipline

For any changing, version-sensitive, unfamiliar, externally integrated, or non-trivial service/mechanism, **do not generate implementation or diagnostic mutation blocks from memory, analogy, or guesswork**.

Required evidence order:

1. official product documentation for the current/relevant version;
2. upstream source/release notes and developer-maintainer guidance where behavior or syntax matters;
3. the exact deployed version and live runtime/configuration on `edge`;
4. community/user reports and implementation patterns only as supplementary evidence.

Community issues, Reddit posts, blog posts, videos, or one user's failure are diagnostic signals, not architectural truth. Never reject or redesign an upstream-supported mechanism solely because of an isolated user report.

Before proposing a deployment/auth/reverse-proxy/update/backup/configuration mechanism:

- complete the relevant research first and state the resulting target architecture/mechanism before writing mutation commands;
- verify exact CLI flags, config schema, file format, auth flow, bind/proxy semantics and version-specific behavior against authoritative sources and/or the exact installed source;
- when a product provides its own parser, validator, linter, `config validate`, dry-run, doctor or equivalent, prefer that native mechanism over a generic external parser;
- never assume that a file is ordinary YAML/INI/JSON merely from its extension; first confirm the product's actual format, templating and preprocessing rules;
- do not invent generic parsers around a third-party config/renewal format unless the format contract is confirmed;
- if material uncertainty remains, perform only the smallest targeted read-only inspection needed to resolve it before designing the mutation;
- do not send a broad shell block merely to discover whether an unverified idea happens to work.

Command blocks must be based on a known contract. The user must not become the iterative debugger for speculative assistant-generated shell.

If an assistant-generated audit/verifier/block fails because of its own parsing, quoting, portability, PATH, wrapper, test-harness or assumption error:

- identify it explicitly as an assistant block/verifier defect, not a production/runtime failure;
- preserve already-proven output;
- resume only from the exact failed point with the minimum read-only recovery necessary;
- do not rerun accepted or already-passed sections;
- do not redesign the production system to accommodate a broken test harness.

For architecture choices involving authentication, reverse proxies, OAuth/OIDC, remote clients, WebSockets, update mechanisms, backup/restore, networking, storage or other integration boundaries, perform an **extended design audit before implementation**. Compare upstream-recommended patterns and exact deployed behavior, then use community experience to identify practical failure modes. Prefer the simplest upstream-supported design that satisfies the accepted requirements and single-operator trust model.

## Stable project rules

### Operator decision authority invariant

- The operator decides **whether and when** to update, migrate, enable, disable, adopt, defer, or retain any supported service/version/capability.
- Never invent project policy, restrictions, ceilings, holds, pins, channel/branch/major-version limits, staged-rollout requirements, compatibility gates, risk controls, security layers, or other constraints that the operator did not explicitly request or accept.
- Do not convert an upstream procedural requirement into an operator policy. Report any verified upstream sequencing or compatibility requirement as information only. Never execute an intermediate step, migration, update, workaround, restriction, or other mutation unless the operator explicitly instructs that action.
- Never hide, suppress, downgrade, or relabel an available upstream-supported stable update/capability merely because a more conservative track, alias, or operating practice exists.
- When upstream offers multiple supported choices, present the relevant facts and let the operator choose; do not make the product/architecture/operational decision on the operator's behalf. The assistant's role is to inform, verify, and execute explicitly requested actions.
- A genuine hard technical/upstream constraint may be enforced only when it is verified from authoritative evidence and must be described as a mechanism constraint, not as a user policy.


- Treat `nl-core-vds` as historical/as-is identity and `edge` as the current live logical node.
- Never rewrite historical baseline/audit artifacts to use target-state naming.
- Cloud Infrastructure complements Home Infrastructure and PAI; do not duplicate them merely because a function can run on a VPS.
- Do not infer that an installed legacy service belongs in target state.
- Do not convert proposals/candidates into accepted architecture without an explicit accepted decision.
- Preserve decision chronology and supersession semantics.
- Fresh runtime/configuration outranks historical reference for factual state.
- Single-operator simplicity, minimum components and upstream-supported mechanisms are preferred over enterprise complexity.
- `core` is the trusted shared execution identity and has accepted full non-interactive root through `sudo -n` (`NOPASSWD: ALL`). Do not assume the historical `no sudo` restriction; use sudo for required root actions while preserving the project approval boundary for critical high-impact mutations.

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

Stage 3 is complete and accepted. Final record: `STAGE_03_ACCEPTANCE_2026-09-18.md`.

Durable accepted contract:

- self-hosted Home NetBird is the Cloud ↔ Home/PAI private fabric;
- `edge` is an ordinary host-native NetBird service peer at `100.105.178.187/16`;
- `edge -> Home/PAI` uses the existing `192.168.1.0/24` Home LAN resource through CT300;
- `edge` must not receive the Home `0.0.0.0/0` Internet resource and keeps its VPS-provider default route;
- Home `.lan` split DNS is reused from `edge`;
- VM100 and MikroTik remain unchanged in the accepted baseline;
- do not create `edge.lan`;
- LAN-wide clientless Home/PAI -> `edge` overlay routing is deferred until a concrete private-only workload justifies gateway mutation;
- direct WireGuard and Tailscale remain rejected as duplicate private backbones; AmneziaWG is contingency only for a demonstrated NetBird transport failure.

Application-level durable retry/store-and-forward is not part of the connectivity layer.

## Stage 4 Hermes invariant

Stage 4 is the **Hermes Agent Runtime stage**, including the infrastructure integrations required to make Hermes practically usable: local vLLM, direct Codex/Antigravity executors, the authenticated Hermes Dashboard, the private n8n machine interface, and the accepted Mattermost collaboration/control surface.

Durable role separation:

- n8n — deterministic workflow/orchestration plane;
- Hermes — persistent cloud-side agentic reasoning/tool/delegation plane;
- Mattermost — private collaboration/control/notification surface;
- CloudCLI — manual web/remote cloud-AI workspace;
- Codex CLI and Antigravity CLI — specialist executors used directly and through Hermes;
- OpenClaw — Home/PAI-side local personal agent;
- vLLM on `ai-node` — local inference backend reached through Stage 3.

Hermes remains host-native under `core` by default so it can reuse the host-native executor/auth context.

Mattermost is a mandatory accepted Stage 4 substage. `chat.escloud.us` uses Mattermost-native authentication with no Authelia; integrations are native/upstream-supported only. Hermes↔Mattermost is an accepted native path. n8n↔Mattermost uses the official n8n Mattermost integration. Mattermost↔Stalwart SMTP is explicitly **not required / not enabled**.

The accepted Hermes Web Dashboard and macOS Remote Gateway endpoint is `https://hermes.escloud.us` through the existing Xray/nginx/TLS path. Authentication is Hermes-native self-hosted OIDC with Authelia as IdP and native browser/Desktop PKCE. Do not expose the Dashboard backend or Hermes machine API directly to the Internet.

Stage 4 is COMPLETE / ACCEPTED with `STAGE4_FINAL_ACCEPTANCE=PASS`. Preserve its accepted n8n -> Hermes -> vLLM/Codex/Antigravity paths, Dashboard/OIDC, Mattermost and macOS Desktop evidence unless a concrete regression appears.

The private n8n path uses Docker network `n8n_hermes`, stable Linux bridge `n8n-hermes`, subnet `172.19.0.0/16` and gateway/Hermes bind `172.19.0.1`; UFW must target `n8n-hermes`. Marker: `STAGE4F_STABLE_DOCKER_BRIDGE_HARDENING=PASS`.

Do not implement user-specific workflows as part of Stage 4 infrastructure acceptance.

## Knowledge/Obsidian invariant

Latest authoritative Stage 5 completion record: `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

Durable accepted contract:

- PVE is the authoritative Knowledge/recovery node and Syncthing hub; vault path `/srv/knowledge/obsidian` on the dedicated `pve/knowledge` filesystem;
- CT210 is the single full server-side Obsidian runtime/WebUI node and remains private at `obsidian.lan`;
- ai-node is an active RW replica at `/srv/ai-data/knowledge/obsidian`;
- edge is an active RW replica at `/srv/knowledge/obsidian`;
- topology is PVE ↔ ai-node plus PVE ↔ edge; no direct edge ↔ ai-node Syncthing peer is required under the current topology;
- edge Syncthing runs under `core` and is loopback-only locally; do not expose Syncthing publicly;
- edge n8n uses `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`;
- Hermes/Codex/Antigravity use the same local edge path directly;
- Stage 5 propagation, outage/reconnect, conflict preservation and edge reboot recovery are accepted;
- edge has no Obsidian runtime/WebUI in the accepted Stage 5 baseline;
- OpenClaw keeps its existing PVE read-only Knowledge relationship;
- future external client access through edge is a separate future mechanism and must not be inferred to mean public Syncthing exposure.

Stage 5 branches 05.1, 05.2 and 05.3 are all COMPLETE / ACCEPTED.

## Lifecycle ordering invariants

- Backrest restore capability must be accepted before Semaphore/update testing.
- `update.escloud.us` is a dedicated maintenance/update page, separate from `app.escloud.us`, and is built as a separate Codex substage after the real backend contract is known.
- Production monitoring is deployed after the substantially complete service inventory, cross-site connectivity, Backrest and update subsystem exist.
- `app.escloud.us` is built as a separate Codex substage after monitoring/status sources and final service inventory are accepted.
- Final infrastructure acceptance follows all selected services, connectivity/data integration, backup/restore, maintenance/update, monitoring, portal and cleanup.
