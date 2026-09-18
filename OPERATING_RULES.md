# Cloud Infrastructure — Operating Rules

## Project identity

- **Project name:** Cloud Infrastructure
- **Primary repository:** `Eugene-SN/Cloud-Infrastructure`
- **GitHub workflow:** ON
- **Primary VPS node:** `edge`
- **Current FQDN:** `edge.escloud.us`
- `edge` is a logical, location-agnostic node name. Do not encode provider/datacenter/country into target-state naming.

## Project scope

Cloud Infrastructure is the public/cloud-facing layer of one personal infrastructure composed of:

- **Home Infrastructure** — home compute/service plane centered on Proxmox VE and the Home LAN;
- **Personal Agents Infrastructure (PAI)** — local AI/agent/data-processing plane centered on `ai-node`;
- **Cloud Infrastructure** — external 24/7 VPS layer for public routability, foreign location, Internet-facing services, cloud AI integrations, external coordination and off-site roles.

Cloud Infrastructure should complement Home Infrastructure and PAI rather than duplicate them without a concrete requirement.

## Historical baseline invariant

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains the canonical historical/as-is snapshot of the pre-reinstall legacy VPS.

- Keep historical names such as `nl-core-vds` and legacy paths unchanged in that artifact.
- Do not reinterpret it as current runtime state after the 2026-09-16 rebuild.
- Do not treat the historical deployment as the target architecture.

## Functional scaffold versus selected implementation

`FUNCTIONAL_SCAFFOLD_DRAFT.md` is a global capability/requirements scaffold, not an independent final Architecture Contract.

Rules:

- do not infer a product choice merely because a capability exists in the scaffold;
- preserve explicitly accepted product anchors from `DECISIONS.md` unless a concrete incompatibility or changed requirement appears;
- distinguish finite infrastructure services from continuously evolving user-specific n8n/agent workflows;
- select unresolved mechanisms from actual requirements/dependencies rather than filling roadmap stages with speculative products.

## Implementation stages and work branches

Completed canonical stages:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — Stage 0 — COMPLETE / ACCEPTED;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — Stage 1 — COMPLETE / ACCEPTED;
- `02 — Edge Core Applications` — Stage 2 — COMPLETE / ACCEPTED;
- `02.5 — Remaining Functional Scope Reconciliation & Research` — COMPLETE / ACCEPTED / RESEARCH-ONLY;
- `03 — Edge Cross-site Connectivity Foundation` — Stage 3 — COMPLETE / ACCEPTED with `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Current canonical branch:

- `04 — Edge Hermes Agent Runtime` — IN PROGRESS / NOT YET ACCEPTED.

Remaining finite infrastructure roadmap:

- `04 — Edge Hermes Agent Runtime`;
- `05 — Edge Knowledge Replication & Data Integration`;
- `06 — Edge Backrest & Recovery`;
- `07 — Edge Maintenance & Update` — Semaphore/update workflow plus separate Codex `update.escloud.us` substage;
- `08 — Edge Monitoring, Heartbeats & Alerts`;
- `09 — Edge Cloud Portal` — separate Codex `app.escloud.us` substage;
- `10 — Edge Final Integrated Infrastructure Acceptance`.

After Stage 10, **Automation & User Workflows** is a continuous post-infrastructure workstream, not another infrastructure-completion stage.

## Functional completeness of selected services

Implementation stages are organizational and acceptance boundaries. Their short scope descriptions are **minimum requirements**, not exhaustive lists of every capability that a selected service should have installed.

Rules:

- For an accepted service/product, target a **full practical upstream-supported deployment** suitable for long-term use rather than an intentionally stripped/minimal image or profile.
- Include common local dependencies and standard capability modules when they are part of the normal useful service surface and are likely to prevent repeated future installation work.
- Never exclude a component solely because it is "not needed for the current/core Stage path". A stage's current acceptance path is not a feature ceiling.
- Do not postpone ordinary service capabilities merely to make the current stage look smaller when the postponement would require later package/runtime modification for routine use.
- Stage scope still governs ownership, sequencing, integration and acceptance. User-specific workflows can remain later work even when their supporting generic service capabilities are already present.
- This rule does **not** require enabling every optional integration. External providers/channels that require separate accounts, credentials, subscriptions, public exposure, mutually exclusive runtime choices, unsupported/alpha features with material operational cost, or unrelated heavyweight subsystems may remain disabled until there is a concrete use.
- Any omission from the normal practical feature set must have a concrete rationale (incompatibility, duplication, material resource/operational cost, unsupported state, external credential/account requirement, or explicit user decision), not merely "outside the current core path".



## Mandatory research and command-generation discipline

This rule is mandatory for all remaining stages and all agents working on this project.

### Evidence hierarchy

For any version-sensitive, externally integrated, unfamiliar or non-trivial mechanism, use this order:

1. **official documentation for the relevant/current version**;
2. **upstream source, release notes and maintainer/developer guidance** where exact behavior, syntax or compatibility matters;
3. **fresh evidence from the exact deployed version/runtime/configuration**;
4. **community/user implementation experience** as supplementary evidence only.

Do not elevate an isolated GitHub issue, forum post, Reddit thread, video or user report over the product's documented contract and the exact deployed runtime. Such reports are useful for identifying edge cases and failure modes, not for declaring an officially supported mechanism broken.

### Research before architecture and mutation

Before producing a deployment or mutation block for auth/OAuth/OIDC, reverse proxying, WebSockets, certificates, update mechanisms, backup/restore, networking, storage, service lifecycle or another integration boundary:

- complete the relevant design/recommendation research first;
- compare upstream-recommended deployment patterns and maintainer guidance;
- reconcile them with the exact versions already installed on `edge`;
- identify known practical failure modes from community experience;
- state the proposed target mechanism/architecture before implementing it;
- prefer the simplest upstream-supported design compatible with the project's single-operator trust model.

Do not jump from an incomplete audit directly into implementation merely because enough information exists to try something experimentally.

### Exact syntax and config-format verification

Before emitting commands:

- verify exact CLI flags and semantics against the relevant version's help/docs/source;
- verify config schema and file format before attempting to parse or modify it;
- account for templating, preprocessing, includes, generated files and product-specific syntax;
- prefer the product's native validator/parser/linter/dry-run/doctor over a generic external parser;
- never assume `.yml`, `.conf` or similar means generic YAML/INI that can safely be fed to PyYAML, `configparser`, `awk`, etc.;
- do not invent a custom parser for a third-party format unless its grammar/contract is confirmed;
- if uncertain, perform a minimal targeted read-only inspection to resolve the uncertainty first.

A shell block is an implementation of a verified plan, not an exploratory guessing mechanism.

### Assistant-generated block failures

If a diagnostic, verifier or implementation block fails because of assistant-authored syntax, quoting, portability, parser choice, PATH behavior, wrapper/instrumentation, test-harness logic or an unverified assumption:

- classify it explicitly as an **assistant block/verifier defect**, not a runtime/service defect;
- do not infer production failure from that result;
- retain already-proven sections and evidence;
- recover from the exact failure point only;
- do not repeat accepted or already-passed audits/tests;
- fix or replace the broken block mechanism instead of changing production to satisfy it;
- when the product has a native validation path, switch to it rather than iterating custom parsers.

The user must not be required to repeatedly debug speculative assistant-generated blocks.

### Community evidence

Community experience is valuable for:

- finding real-world interoperability problems;
- identifying version-specific bugs;
- revealing UX problems or missing documentation;
- discovering implementation patterns worth verifying.

It is not sufficient by itself to:

- reject a documented upstream mechanism;
- declare a feature unusable;
- introduce a workaround;
- choose a more complex architecture.

Any such conclusion requires corroboration from upstream/maintainer guidance and/or the exact deployed runtime.

### Stop condition before mutation

Do not mutate production while a material design assumption is still unresolved.

A stage-specific mutation may begin only when the relevant topology/mechanism is understood well enough that the command block is expected to implement a defined target rather than probe whether an idea works. For high-risk changes, retain the existing AUDIT -> PLAN -> RECOVERY PATH -> MUTATION -> VERIFY -> ACCEPTANCE workflow.

## Mandatory lifecycle for every implementation stage

Every new implementation-stage branch starts with analysis/design, not installation.

Before stage-dependent runtime mutation, perform in order:

1. **REQUIREMENTS REVIEW** — read current state, accepted decisions and relevant capability requirements.
2. **SERVICE / PRODUCT SELECTION** — research only unresolved choices; do not reopen accepted products without a concrete reason.
3. **STAGE COMPOSITION ACCEPTANCE** — explicitly record included/excluded products/mechanisms.
4. **STAGE ARCHITECTURE / DEPLOYMENT CONTRACT** — define only topology, runtime placement, paths, ingress/auth/storage relationships, dependencies and recovery path required for that stage.
5. **IMPLEMENTATION**.
6. **VERIFY** — verify properties, not merely command return codes.
7. **ACCEPTANCE** — mark complete only after the whole stage passes.
8. **PERSISTENCE** — update canonical repository state and read back critical writes.
9. **BRANCH TRANSITION** — only after acceptance may ChatGPT propose the next branch and starter prompt.

A completed subtask is not permission to leave a branch while its accepted scope remains incomplete.

## Current work checkpoint

Current facts:

1. Stage 0 preservation/recovery is complete.
2. Stage 1 clean rebuild/base platform is complete and accepted.
3. Stage 2 Core Applications is complete and accepted.
4. Stage 02.5 research reconciliation is complete and accepted.
5. Stage 3 Cross-site Connectivity Foundation is complete and accepted.
6. `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`.
7. The active production branch is `04 — Edge Hermes Agent Runtime`; Stage 4 is IN PROGRESS / NOT YET ACCEPTED.
8. Reuse the accepted Stage 3 transport; do not reopen NetBird/routing choices without a concrete incompatibility.
9. The Stage 1 Docker `live-restore=true` setting is superseded; current accepted runtime is `live-restore=false`.

# Stage 3 — Cross-site Connectivity contract

Authoritative detailed acceptance record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Stage 3 reuses the existing Home self-hosted NetBird architecture as a bidirectional routed private fabric.

Accepted final contract:

- CT300 `remote-access` remains the Home routing peer at `192.168.1.90`, overlay `100.105.97.126/16`;
- NetBird account IPv4 overlay is `100.105.0.0/16`;
- existing Home LAN resource is `192.168.1.0/24`;
- `edge` is an ordinary host-native NetBird service peer, overlay `100.105.178.187/16`;
- `edge` gets Home LAN reachability but not the Home `0.0.0.0/0` Internet resource;
- `edge` retains its direct VPS-provider default Internet route;
- reuse existing NetBird-managed Site-to-VPN masquerade; do not add duplicate manual NAT;
- reuse Home split-DNS `192.168.1.1:53` for match domain `lan`; ordinary `edge` DNS remains VPS-local;
- VM100 and MikroTik remain unchanged in the baseline;
- do not create `edge.lan`;
- Home/PAI normally reaches Cloud services through the public VPS IPv4 or accepted `escloud.us` / service-subdomain ingress;
- LAN-wide clientless Home/PAI -> `edge` overlay routing is deferred until a concrete private-only workload justifies gateway mutation;
- direct/relay behavior, process recovery, CT300 reboot recovery and edge full-reboot persistence are accepted in `STAGE_03_ACCEPTANCE_2026-09-18.md`.

Existing user-device Home Internet Exit remains separate. Do not assign its `0.0.0.0/0` resource to `edge`.

Direct WireGuard and Tailscale remain rejected as duplicate parallel backbones. AmneziaWG remains contingency only for a demonstrated NetBird transport/DPI failure.

Connectivity is transport/reachability/private naming. Application-level durable store-and-forward/retry is a later workflow concern.

# Stage 4 — Hermes contract

Stage 4 owns the production Hermes runtime **and the infrastructure integrations required for its long-lived role**: local vLLM, direct Codex/Antigravity delegation, authenticated Web Dashboard, private n8n machine interface, Mattermost collaboration/control integration and final macOS Hermes Desktop integration.

Accepted role separation:

- n8n = deterministic workflow/orchestration plane;
- Hermes = persistent cloud-side agentic reasoning/tool/delegation plane;
- Mattermost = private collaboration/control/notification surface;
- CloudCLI = manual web/remote cloud-AI workspace;
- Codex CLI and Antigravity CLI = specialist executors directly usable by the user and delegatable by Hermes;
- OpenClaw = Home/PAI local personal agent;
- vLLM on `ai-node` = local inference backend available through Stage 3.

Preferred Hermes placement is **host-native under `core`**. This is a justified exception to Docker-by-default because containerization would complicate direct reuse of host-native executor binaries and user/runtime/auth context.

Hermes installation follows the upstream-recommended path. Do not independently pin or replace it without a concrete incompatibility/regression.

Mattermost is an accepted mandatory Stage 4 surface:

- Team Edition using the official Docker Compose pattern with dedicated PostgreSQL;
- `https://chat.escloud.us` through existing Xray/nginx/shared TLS;
- Mattermost-native authentication; **no Authelia** in front of `chat.escloud.us`;
- backend/database remain private;
- Calls excluded;
- service integrations are native/upstream-supported only;
- Hermes↔Mattermost uses the built-in Hermes Mattermost gateway;
- n8n↔Mattermost uses the official n8n Mattermost integration;
- Mattermost↔Stalwart SMTP is explicitly not required / not enabled.

### Hermes WebUI / ingress — recovery design gate

The Hermes Web Dashboard remains required at `https://hermes.escloud.us`, through existing Xray/nginx/shared TLS, with the backend loopback-only and no direct public 9119.

The previous forward-auth/session-token-first contract is suspended for the 04.3 recovery workstream. Verify exact deployed source/runtime before accepting a replacement. Current candidate: Hermes-native self-hosted OIDC, Authelia as IdP, no nginx `auth_request` in front of Hermes, one interactive provider, authorization-code PKCE/S256 public client. This candidate is not deployment acceptance.

Use Authelia's native validator with the actual template filter/configuration path. Reuse the existing Certbot webroot mechanism and shared `escloud.us` certificate lineage. Do not require the nginx Certbot plugin.

### Stage 4 acceptance

Preserve accepted Stage 4A/B/D/E evidence without repeated E2E tests absent a concrete regression. Remaining requirements:

- Stage 4C: real browser/OIDC login, Dashboard Chat, authenticated WS/PTY, HTTPS and loopback-only backend;
- Stage 4F: authenticated private n8n invoke/result/status and real `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`, accounting for Tirith stdout contamination;
- Stage 4G: bounded server-side integration/non-regression and lifecycle review; do not mask the known SIGTERM exit-1 behavior with `SuccessExitStatus=1`;
- Stage 4H: final macOS Desktop Remote Gateway integration, actual remote chat/WebSocket and restart/reconnect/refresh behavior using the Stage 4C accepted auth mode;
- Stage 4I: complete-stage acceptance and canonical repository reconciliation/read-back.

The core Qwen/vLLM and direct executor acceptance remains valid. The existing gateway stop constraint belongs in 4G. User-specific workflows remain outside Stage 4.

### Final Stage 4 macOS integration

Hermes Desktop on macOS remains the last functional integration after Stage 4G. Research the actual Desktop build and exact server auth contract. If Stage 4C accepts self-hosted OIDC, use the upstream native RFC8252/PKCE path rather than a historical session-token-first assumption. Successful status probes alone are not acceptance.

## Data/knowledge sequencing

Stage 5 is **Edge Knowledge Replication & Data Integration** and is owned as an integration stage, not a second knowledge-platform design project.

- Home Infrastructure owns the future PVE canonical knowledge foundation.
- Personal Agents Infrastructure owns the `ai-node` active replica and local AI consumers/producers after Home cutover.
- Cloud Infrastructure owns only the `edge` active RW replica and Cloud-side consumers/producers.
- Until Home explicitly accepts PVE canonical migration, the current `ai-node:/srv/ai-data/knowledge/obsidian` remains factual runtime state.
- Stage 5 begins with a fresh cross-project read-only audit and reuses the Home-accepted server-side synchronization mechanism by default.
- MacBook/iPhone/iPad Obsidian synchronization is outside Cloud Infrastructure scope.

## Backup/update sequencing

- Backrest using Restic is the accepted backup-management direction.
- Stage 6 deploys Backrest against the substantially complete service inventory.
- A usable Stage 6 backup/restore path must be accepted before Stage 7 Semaphore/update testing.
- Semaphore and maintenance/update workflow are developed/tested together.
- Existing PVE/Home update tooling is an engineering reference to audit/adapt, not copy blindly.
- `ops.escloud.us` remains Semaphore's operational execution UI.
- `update.escloud.us` is a dedicated custom maintenance/update page built in a separate Codex substage only after the backend/status/control contract is known.

## Monitoring sequencing

Stage 8 finalizes/deploys production monitoring only after the service inventory, connectivity, Backrest and update subsystem substantially exist.

Avoid heavyweight metrics/logging/observability stacks unless concrete requirements justify them.

## Portal sequencing

- `app.escloud.us` is the final Cloud Infrastructure navigation/status dashboard.
- It is built in Stage 9 only after Stage 8 monitoring/status sources and final service inventory are accepted.
- It is a separate Codex substage.
- Do not put detailed maintenance/update controls into `app.escloud.us`; those remain on `update.escloud.us`.

## Post-infrastructure workflow rule

After Stage 10, user-specific automation can evolve independently: n8n workflows, Hermes/agent workflows, Capture Inbox, approvals, mail-triggered automation, continuous information intake/change detection, bounded AI research, durable application-level cross-site task handoff, messaging/bot commands and orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

These are not blockers for final infrastructure acceptance.

## Runtime and placement defaults

- Docker + Compose are default for suitable application services.
- Host-native deployment is valid where materially simpler or better aligned with the upstream/runtime integration contract.
- Application WebUI backends normally bind loopback and are published through nginx.
- Use accepted path convention: `/opt/<service>` runtime definitions/scripts, `/srv/<service>` persistent state, `/etc/<service>` host-native configuration, `/var/www/<site>` static web roots.
- Preserve upstream-required internal container UID/GID where necessary rather than cosmetically remapping it.

## Current substrate contract

Accepted live substrate facts include:

- Ubuntu 26.04.1 LTS, x86_64, KVM;
- hostname/FQDN `edge.escloud.us`, short hostname `edge`;
- kernel `7.0.0-31-generic` at current accepted state;
- 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- no public/global IPv6 on `ens3`; IPv6 remains enabled for link-local and NetBird overlay use;
- SSH public-key access works; root password authentication is disabled;
- OpenSSH is socket-activated through `ssh.socket`;
- persistent journald-use ceiling is `500M`;
- `/etc/netplan/50-cloud-init.yaml` is the current authoritative IPv4-only public network config; cloud-init network regeneration is disabled by `/etc/cloud/cloud.cfg.d/99-edge-disable-network-config.cfg`;
- Docker/Compose, nginx, Xray, Hysteria2, Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark are accepted current runtime components as documented in `CURRENT_STATE.md`;
- Docker `live-restore=false` is the accepted current lifecycle state; application containers use `restart=unless-stopped` for reboot persistence.

Fresh runtime/configuration has priority over historical reference.

## Recovery model

Current recovery layers include:

1. provider-level whole-VPS backup / rollback path from Stage 0 where applicable;
2. external sensitive migration archive with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf` retained for selective legacy reference/recovery;
3. Stage 1 same-VPS recovery checkpoint `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, which is not complete host-loss DR;
4. future Backrest + Restic topology, still unresolved for off-site repository placement and final retention/restore policy.

`migration-reference/` is engineering context only and must not be used as an authoritative restore bundle.

## Source-of-truth and persistence rules

For project intent, use latest applicable ACCEPTED decisions and canonical current documents. For factual runtime state, priority is:

1. fresh runtime audit;
2. actual live configuration;
3. current repository state;
4. historical docs/reference.

A discrepancy is drift and must be resolved explicitly rather than guessed.

Before modifying project files:

1. read current repository state;
2. avoid duplicate documents/facts;
3. update canonical existing documents for current state/architecture;
4. preserve historical acceptance/audit artifacts rather than rewriting them retroactively;
5. read back critical writes.

Store structured state and decisions, not chat transcripts.

## Decision semantics

Decision statuses:

- `PROPOSED`
- `ACCEPTED`
- `SUPERSEDED`
- `REJECTED`
- `DEPRECATED`

Latest applicable `ACCEPTED` decision has priority. `SUPERSEDED`, `REJECTED`, and `DEPRECATED` entries are historical only.

## Git and secrets

- Do not commit credentials or secrets to GitHub.
- Persistent non-secret configuration/design/runbooks may be stored in Git.
- Sensitive recovery state remains outside GitHub.
- Credentials present in working chat/configuration/diagnostic context are not automatically considered compromised; rotate only with evidence of exposure.

## Service account and ownership default

- Use shared host service account `core` by default for Cloud Infrastructure application services and host-native service execution.
- Do not create one Unix account per service merely for isolation.
- Use a service-specific account only where upstream/runtime requirements make it necessary.
- For containers, preserve upstream-required internal users/UID/GID.
- Verify numeric ownership before mutations rather than assuming it.

## Shell block rule

Any terminal block whose output must be returned to chat uses a subshell, `set -Eeuo pipefail`, ASCII/English `BLOCK_NAME`, and green BEGIN/END delimiters including final RC.

Do not hide failures through `|| true`, global `set +e`, or stderr suppression. Handle expected non-zero statuses explicitly.

If a block fails or the terminal/session closes, determine the failure point and side effects with a proportionate read-only recovery audit before retrying.

Use `/tmp` for temporary test/audit artifacts and remove them after the task unless they become deliberate persistent artifacts.

## Verification

`RC=0` alone is not acceptance. Verify the minimum properties relevant to the change and use PASS/FAIL for important acceptance gates.

Avoid restart/reboot unless actually required.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without demonstrated use.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are separate from the private infrastructure backbone.
- Home/PAI connectivity must not become a foundation requirement for independently useful `edge` capabilities, but it must exist before services whose correctness depends on Home/PAI.
- Do not carry legacy configuration forward blindly; use `migration-reference/` for engineering context and the external archive only where exact state/credentials are actually required.
- Do not open a new production branch until the current stage is accepted and canonical files have been updated/read back.