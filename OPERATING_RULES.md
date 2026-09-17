# Cloud Infrastructure — Operating Rules

## Project identity

- Project name: `Cloud Infrastructure`.
- Primary repository: `Eugene-SN/Cloud-Infrastructure`.
- GitHub workflow: ON.
- Primary VPS node: `edge` / `edge.escloud.us`.

## Authority order

For current work, resolve conflicts in this order:

1. current explicit user instruction;
2. latest applicable ACCEPTED decision in `DECISIONS.md` or stage acceptance record;
3. fresh runtime/configuration evidence;
4. `CURRENT_STATE.md`;
5. `ARCHITECTURE.md`;
6. `IMPLEMENTATION_PHASES.md` and current stage planning;
7. `INVENTORY.md`, `DOMAIN_NAMESPACE.md` and other current support documents;
8. `FUNCTIONAL_SCAFFOLD_DRAFT.md` as a requirements map;
9. historical baseline and `migration-reference/` as legacy evidence only.

Historical future-stage proposals are not authoritative merely because they existed earlier.

## Current project checkpoint

- Stage 0 — COMPLETE / ACCEPTED.
- Stage 1 — COMPLETE / ACCEPTED.
- Stage 2 — COMPLETE / ACCEPTED.
- `EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.
- Stage 02.5 — ACTIVE / RESEARCH-ONLY.
- Current branch: `02.5 — Remaining Functional Scope Reconciliation & Research`.

No production deployment branch after Stage 2 is opened until Stage 02.5 finishes its research matrix, normalized service/product inventory, dependency graph and final replacement stage numbering.

## Stage 02.5 research-only rule

During Stage 02.5:

- do not deploy/install/configure new production services;
- do not mutate production DNS/firewall/runtime;
- read-only audits are allowed only when a concrete unknown factual state materially blocks a design decision;
- do not reopen already accepted product anchors without a concrete incompatibility or changed requirement;
- prefer official documentation/releases/upstream, then maintainers, then community evidence for changing information;
- classify each unresolved capability as `SELECTED`, `REUSE EXISTING`, `DEFERRED`, `REJECTED` or, only when evidence is genuinely insufficient, `RESEARCH STILL REQUIRED`.

## Dependency-aware roadmap rule

Post-Stage-2 deployment follows dependency direction rather than historical thematic Stage 3–7 grouping:

1. remaining standalone core services;
2. cross-site connectivity foundation;
3. cross-site data/knowledge services;
4. remaining infrastructure services;
5. Backrest + verified restore;
6. Semaphore + dedicated `update.escloud.us` maintenance/update page;
7. infrastructure-wide monitoring/heartbeats/alerts;
8. final `app.escloud.us` portal/dashboard;
9. final integrated infrastructure acceptance;
10. user-specific automation/workflow development.

User-specific n8n/agent workflows are not infrastructure-completion blockers.

## UI responsibility separation

- `ops.escloud.us` — Semaphore operational execution UI.
- `update.escloud.us` — dedicated custom maintenance/update page; built in a separate Codex substage after the real Semaphore/update backend contract exists.
- `app.escloud.us` — final navigation/status dashboard; built in a separate Codex substage after monitoring/status sources and final service inventory are accepted.

Do not put detailed maintenance/update controls into `app.escloud.us` merely to consolidate pages.

## Backup/update sequencing

- Backrest using Restic is the accepted backup-management direction.
- Backrest is deployed late against the substantially complete service inventory.
- A usable pre-update backup/restore path must be accepted before Semaphore/update testing.
- Semaphore and the maintenance/update workflow are developed/tested together.
- The existing PVE/Home updater is an engineering reference to audit and adapt for `edge`, not a template to copy blindly.

## Connectivity sequencing

Do not deploy files/sync/Obsidian or other Home/PAI-dependent services before the required `edge ↔ ai-node ↔ PVE/Home` connectivity foundation is selected and accepted.

Connectivity technology is selected from real flows. NetBird, direct WireGuard, authenticated HTTPS or another simple mechanism may be considered; do not choose a private backbone first and then invent uses for it.

Application-level durable store-and-forward/retry for n8n/agent tasks is a later workflow concern and does not by itself define the connectivity foundation.

## Obsidian invariant

Canonical Obsidian vault remains:

`ai-node:/srv/ai-data/knowledge/obsidian`

Do not make `edge` the canonical source of truth by assumption. Any `edge` role is selected separately as sync endpoint, relay/mirror, remote workspace, web/file gateway or no direct vault role.

## Runtime and placement defaults

- Docker + Compose are the default runtime for suitable application services.
- Host-native deployment remains valid when materially simpler, especially for public ingress/host lifecycle components.
- Application WebUI backends normally bind loopback and are published through nginx.
- Reuse the accepted path convention: `/opt/<service>` runtime definitions/scripts, `/srv/<service>` persistent state, `/etc/<service>` host-native configuration, `/var/www/<site>` static web roots.

## Simplicity / security model

The environment is single-operator. Prefer correctness and simplicity over enterprise ceremony.

Do not introduce IAM/LDAP/SSO layers beyond the accepted Authelia boundary, internal mTLS, auth-proxies, complex RBAC/ACL, secret-management platforms, credential rotation, heavy observability or orchestration layers without a concrete demonstrated need.

Credentials present in working diagnostic/configuration context are not automatically considered compromised. Do not rotate without evidence of exposure. Never commit secrets/private keys/credential-bearing archives to the public repository.

## GitHub persistence

- Read current authoritative files before write actions.
- Persist explicit accepted decisions and confirmed current state; do not store brainstorming as factual state.
- Historical baselines/audits are not rewritten to match later target architecture.
- After critical writes, perform read-back.
- If returning to an earlier accepted checkpoint, normalize current docs to that checkpoint; do not rewrite Git history unless explicitly requested.

## Shell block rule

Any terminal block whose output must be returned to chat uses a subshell, `set -Eeuo pipefail`, ASCII/English `BLOCK_NAME`, and green BEGIN/END delimiters including final RC.

Do not hide failures through `|| true`, global `set +e`, or stderr suppression. Handle expected non-zero statuses explicitly.

If a block fails or the terminal/session closes, first determine the failure point and side effects with a proportionate read-only recovery audit. Do not simply shorten scope or rerun already completed work.

Use `/tmp` for temporary test/audit artifacts and remove them after the task unless they become deliberate persistent artifacts.

## Verification

`RC=0` alone is not acceptance. Verify the minimum properties relevant to the change and use PASS/FAIL for important acceptance gates.

Avoid restart/reboot unless the change actually requires one.

## Branch transition

Do not open the next production deployment branch until Stage 02.5 deliverables are explicitly accepted and canonical files have been updated/read back.

Once a later implementation stage is fully accepted and its state is persisted in the primary repository, propose a new branch/title and a concise starting prompt for the next independent task.
