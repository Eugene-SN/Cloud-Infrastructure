# Cloud Infrastructure — Operating Rules

## Project identity

- **Project name:** Cloud Infrastructure
- **Primary repository:** `Eugene-SN/Cloud-Infrastructure`
- **GitHub workflow:** direct commits to `main` by default; branches/PRs only by explicit operator request
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

## Implementation stages and repository workflow

Completed canonical stages:

- `00 — Cloud Infrastructure Architecture Discovery & Target Design` — COMPLETE / ACCEPTED;
- `01 — Edge Clean Rebuild & Base Platform Deployment` — COMPLETE / ACCEPTED;
- `02 — Edge Core Applications` — COMPLETE / ACCEPTED;
- `02.5 — Remaining Functional Scope Reconciliation & Research` — COMPLETE / ACCEPTED / RESEARCH-ONLY;
- `03 — Edge Cross-site Connectivity Foundation` — COMPLETE / ACCEPTED;
- `04 — Edge Hermes Agent Runtime` — COMPLETE / ACCEPTED;
- `05 — Knowledge Fabric Runtime Deployment` — COMPLETE / ACCEPTED, including 05.1/05.2/05.3.

Current accepted checkpoint:

- Stages 0–10 are COMPLETE / ACCEPTED;
- `STAGE10_FINAL_ACCEPTANCE=PASS`;
- final Stage 10 record: `STAGE_10_FINAL_ACCEPTANCE_2026-09-22.md`;
- Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion — is ACTIVE / ACCEPTED SCOPE.

Stage 10 is the accepted clean pre-Stage-11 baseline. Stage 11 may add only infrastructure capabilities proven missing and useful before user workflows. Historical presence alone is not sufficient justification for redeployment.

**Automation & User Workflows** begins after Stage 11 and any bounded Stage 10 re-acceptance required by material Stage 11 changes.

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

Every new implementation stage starts with analysis/design, not installation. Repository changes are committed directly to the latest `main` by default.

Before stage-dependent runtime mutation, perform in order:

1. **REQUIREMENTS REVIEW** — read current state, accepted decisions and relevant capability requirements.
2. **SERVICE / PRODUCT SELECTION** — research only unresolved choices; do not reopen accepted products without a concrete reason.
3. **STAGE COMPOSITION ACCEPTANCE** — explicitly record included/excluded products/mechanisms.
4. **STAGE ARCHITECTURE / DEPLOYMENT CONTRACT** — define only topology, runtime placement, paths, ingress/auth/storage relationships, dependencies and recovery path required for that stage.
5. **IMPLEMENTATION**.
6. **VERIFY** — verify properties, not merely command return codes.
7. **ACCEPTANCE** — mark complete only after the whole stage passes.
8. **PERSISTENCE** — update canonical repository state and read back critical writes.
9. **MAIN PERSISTENCE / NEXT STAGE** — only after acceptance may ChatGPT persist the coherent result to `main` and propose the next stage and starter prompt.

A completed subtask is not permission to leave accepted stage scope incomplete.

## Current work checkpoint

Current facts:

1. Stages 0 through 10 are complete and accepted; `STAGE10_FINAL_ACCEPTANCE=PASS`.
2. `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`, `STAGE4_FINAL_ACCEPTANCE=PASS`, `STAGE05_FINAL_ACCEPTANCE=PASS`, `STAGE06_FINAL_ACCEPTANCE=PASS`, `STAGE07_FINAL_ACCEPTANCE=PASS`, `STAGE08_FINAL_ACCEPTANCE=PASS`, `STAGE09_FINAL_ACCEPTANCE=PASS` and `STAGE10_FINAL_ACCEPTANCE=PASS` remain the accepted chain.
3. The finite Cloud Infrastructure build is complete; current work belongs to the post-infrastructure Automation & User Workflows stream unless a future infrastructure requirement explicitly opens a new stage.
4. Reuse accepted Stage 3 transport, Stage 5 Knowledge, Stage 6 recovery, Stage 7 maintenance, Stage 8 monitoring and Stage 9 portal contracts; do not reopen them without a concrete incompatibility or superseding requirement.
5. The Stage 1 Docker `live-restore=true` setting remains superseded; current accepted runtime is `live-restore=false`.

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

### Hermes WebUI / ingress — accepted contract

The accepted Hermes Dashboard endpoint is `https://hermes.escloud.us` through existing Xray/nginx/shared TLS to loopback `127.0.0.1:9119`; no public TCP/9119 exists.

Authentication is Hermes-native self-hosted OIDC with Authelia `4.39.27` as IdP, exactly one interactive provider, authorization-code PKCE/S256, native browser cookie flow and native Desktop RFC8252/PKCE flow. nginx does not use `auth_request` for Hermes. Historical forward-auth/session-token-first wording is superseded.

Certificate issuance/renewal reuses the existing Certbot webroot mechanism and shared `escloud.us` lineage. The nginx Certbot plugin is not required.

### Stage 4 acceptance

Stage 4A/B/C/D/E/F/G/H/I are COMPLETE / ACCEPTED. Final marker: `STAGE4_FINAL_ACCEPTANCE=PASS`.

Accepted machine contract:

- n8n uses the upstream Hermes API Server through a private Docker-bridge listener with Bearer authentication;
- Compose explicitly fixes network `n8n_hermes`, Linux bridge `n8n-hermes`, subnet `172.19.0.0/16` and gateway `172.19.0.1`; UFW targets the stable bridge name;
- the production n8n workflow supports `vllm`, `codex` and `antigravity` selectors;
- no public Hermes machine API is permitted;
- native HTTP JSON is used instead of parsing contaminated CLI `stream-json` stdout.

Accepted lifecycle constraint: controlled Hermes SIGTERM can exit status 1 after graceful-shutdown logging; requested restart recovery succeeds. Do not patch Hermes casually or mask it with `SuccessExitStatus=1`.

Accepted Desktop contract: macOS Hermes Desktop uses `https://hermes.escloud.us` and native self-hosted OIDC/RFC8252 PKCE; no session-token workaround or public backend port.

Preserve the final Stage 4 records and do not repeat accepted E2E tests without a concrete regression signal. User-specific workflows remain outside Stage 4.

## Data/knowledge sequencing

Stage 5 is COMPLETE / ACCEPTED.

Authoritative final records:

- `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_2_FINAL_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

Accepted runtime:

- PVE owns authoritative Knowledge at `/srv/knowledge/obsidian` on the dedicated `pve/knowledge` filesystem, remains the Syncthing hub/recovery authority, and hosts the single Ignis-based server-side Obsidian runtime through CT210;
- ai-node owns the active RW PAI/application replica at `/srv/ai-data/knowledge/obsidian`;
- edge owns the active RW Cloud/agent replica at `/srv/knowledge/obsidian`;
- topology is PVE ↔ ai-node plus PVE ↔ edge; no direct edge ↔ ai-node Syncthing peer;
- edge Syncthing runs as `syncthing@core.service`, is reboot-persistent, and exposes only loopback `127.0.0.1:22000` / `127.0.0.1:8384`;
- edge n8n binds `/srv/knowledge/obsidian` at the same container path RW;
- Hermes/Codex/Antigravity use the local edge path directly;
- propagation, outage/reconnect, conflict preservation and reboot recovery are accepted;
- no public Syncthing and no edge Obsidian runtime/WebUI were added;
- OpenClaw keeps its existing PVE read-only relationship;
- future public client access through edge remains outside Stage 5 and requires a separately selected mechanism.

## Update ownership policy

For every deployed service/product, prefer the vendor/upstream-native update lifecycle over project-built update automation.

Rules:

- If the service provides a supported native automatic-update mechanism, keep and use that mechanism by default.
- Do not disable a native automatic updater merely to route the service through maintenance/Semaphore.
- If the service has no supported native automatic-update mechanism, manage its updates manually through the accepted maintenance/Semaphore workflow.
- Never create independent custom automatic-update scripts, cron jobs, systemd timers or equivalent project-specific auto-update mechanisms merely to add automation that upstream does not provide.
- Maintenance/Semaphore may still inspect, report or expose status for a service that self-updates natively, but it must not become a competing update owner.
- Override a native updater only for a concrete incompatibility, regression, migration constraint, or explicit operator decision.

For Codex specifically, its supported managed-daemon/native auto-update lifecycle remains authoritative; do not disable it merely to make Codex a manual Semaphore-managed update target.

## Backup/update sequencing

- Backrest using Restic is the accepted backup-management direction.
- Stage 6 deploys Backrest against the substantially complete service inventory.
- A usable Stage 6 backup/restore path must be accepted before Stage 7 Semaphore/update testing.
- Semaphore and maintenance/update workflow are developed/tested together.
- Existing PVE/Home update tooling is an engineering reference to audit/adapt, not copy blindly.
- `update.escloud.us` is the single Stage 7 operator origin: `/status/` serves the custom maintenance/update page and `/project/1/history` opens the full Semaphore UI for task/template inspection and live logs.
- Do not reintroduce the retired `ops.escloud.us` name into edge configuration, certificates, recovery material or automation; keep Semaphore itself loopback-only and publish both Stage 7 interfaces through the accepted `update.escloud.us` ingress.

## Monitoring sequencing

Stage 8 finalizes/deploys production monitoring only after the service inventory, connectivity, Backrest and update subsystem substantially exist.

Avoid heavyweight metrics/logging/observability stacks unless concrete requirements justify them.

## Portal sequencing

- `app.escloud.us` is the final Cloud Infrastructure navigation/status dashboard.
- It is built in Stage 9 only after Stage 8 monitoring/status sources and final service inventory are accepted.
- It is a separate Codex substage.
- Do not put detailed maintenance/update controls into `app.escloud.us`; those remain on `update.escloud.us`.

## Post-infrastructure workflow rule

After Stage 11 completion and any required bounded Stage 10 re-acceptance, user-specific automation can evolve independently: n8n workflows, Hermes/agent workflows, Capture Inbox, approvals, mail-triggered automation, continuous information intake/change detection, bounded AI research, durable application-level cross-site task handoff, messaging/bot commands and orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

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
2. Stage 1 same-VPS recovery checkpoint `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, which is not complete host-loss DR;
3. stage-specific recovery checkpoints for later production mutations, including `/srv/backups/edge-stage4f-network/recovery-20260919T124318Z`;
4. future Backrest + Restic topology, still unresolved for off-site repository placement and final retention/restore policy.

The historical temporary migration-preservation archive is absent and no longer required. Do not recreate it. `migration-reference/` is the retained sanitized engineering context only and must not be used as an authoritative restore bundle.

## Source-of-truth and persistence rules

### Evidence classification rule

Never invent or silently assume project facts. For any material statement about runtime state, paths, versions, names, topology, ownership, configuration, behavior, capabilities, causes, or dependencies:

- state it as a **confirmed fact** only when supported by applicable evidence;
- label a logical but unobserved conclusion explicitly as **INFERENCE**;
- label a plausible but unconfirmed statement explicitly as **ASSUMPTION** and identify the missing evidence;
- use **UNKNOWN** when evidence is insufficient or contradictory.

Do not fill factual gaps from analogy, memory, prior deployments, naming conventions, or best-practice expectations. A mutation that materially depends on an inference or assumption must wait for the minimum required read-only verification or an explicit operator decision accepting that design choice.

For project intent, use latest applicable ACCEPTED decisions and canonical current documents. For factual runtime state, priority is:

1. fresh runtime audit;
2. actual live configuration;
3. current repository state;
4. historical docs/reference.

A discrepancy is drift and must be resolved explicitly rather than guessed.

Before modifying project files:

1. fetch and read the latest `origin/main`;
2. avoid duplicate documents/facts;
3. update canonical existing documents for current state/architecture;
4. preserve historical acceptance/audit artifacts rather than rewriting them retroactively;
5. commit and push directly to `main` unless the operator explicitly requested a branch/PR;
6. read back the remote commit and critical writes.

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

- Direct-to-`main` is the default repository workflow for ChatGPT/Codex work in this project.
- Do not create a branch or pull request unless the operator explicitly asks for one.
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

## Trusted `core` privilege model

- `core` is the shared trusted host service/operator account for Cloud Infrastructure.
- Current accepted policy grants `core` full non-interactive root through `sudo`: `core ALL=(ALL:ALL) NOPASSWD: ALL` in `/etc/sudoers.d/90-core-root`.
- Keep the Unix identity as `core`; use `sudo -n` for commands that require root rather than changing UID/GID or maintaining a separate root execution path.
- Do not add `core` to the `docker` group solely for Docker administration; `sudo -n docker ...` already satisfies that requirement.
- Full sudo capability does not remove the existing approval boundary for destructive, system-wide, production, network, credential/auth, data-deletion or similarly high-impact mutations. Authorization remains at the operator/orchestration instruction layer.
- Acceptance record: `CORE_FULL_ROOT_SUDO_ACCEPTANCE_2026-09-18.md`.

## Shell block rule

Any terminal block whose output must be returned to chat uses a subshell, `set -Eeuo pipefail`, ASCII/English `BLOCK_NAME`, and green BEGIN/END delimiters including final RC.

Do not hide failures through `|| true`, global `set +e`, or stderr suppression. Handle expected non-zero statuses explicitly.

If a block fails or the terminal/session closes, determine the failure point and side effects with a proportionate read-only recovery audit before retrying.

Use `/tmp` for temporary test/audit artifacts and remove them after the task unless they become deliberate persistent artifacts.

## Verification

`RC=0` alone is not acceptance. Verify the minimum properties relevant to the change and use PASS/FAIL for important acceptance gates.

Avoid restart/reboot unless actually required.

## Stage 7 update ownership and execution

- Use a native-first ownership model: supported upstream/vendor automatic update lifecycle remains authoritative unless a concrete incompatibility, regression, migration constraint or explicit accepted decision requires otherwise.
- Maintenance/Semaphore owns only manual targets that do not have an accepted native automatic owner. Those real manual updates and Master Batch executions are operator-initiated from `update.escloud.us`.
- Native-owned components may be monitored by Maintenance but must be non-actionable there; do not create a competing Semaphore template/driver for them.
- Current native owners are Codex managed-daemon auto-update, Hermes native cron + conditional settlement, and Ubuntu security updates through package-owned `apt-daily*` / `unattended-upgrades`.
- Normal and third-party APT updates remain manual through `APT_EDGE`; automatic reboot remains disabled.
- Do not create project-specific automatic cron/systemd/scheduled update mechanisms for products that lack a supported native automatic updater.
- Semaphore remains the backend executor/orchestrator for manual targets only; it must not independently schedule or launch them.
- Read-only status/version refresh may be invoked as needed and must never chain into a manual update.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without demonstrated use.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are separate from the private infrastructure backbone.
- Home/PAI connectivity must not become a foundation requirement for independently useful `edge` capabilities, but it must exist before services whose correctness depends on Home/PAI.
- Do not carry legacy configuration forward blindly; use `migration-reference/` only as sanitized engineering context.
- Do not begin the next implementation stage until the current stage is accepted and canonical files have been committed to `main` and read back.
