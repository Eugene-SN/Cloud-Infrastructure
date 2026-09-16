# Cloud Infrastructure — Decision Log

Decision entries are chronological. The latest applicable `ACCEPTED` decision has priority over older conflicting entries.

---

## 2026-09-14T21:57:00+03:00 — Project taxonomy and legacy baseline

**Status:** ACCEPTED

**Context:** Cloud Infrastructure was split from the earlier legacy VPS work after Home Infrastructure and Personal Agents Infrastructure had matured.

**Decision:**

- Project name is **Cloud Infrastructure**.
- Future primary VPS node is **`edge`**, a location-agnostic logical name.
- `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` is the canonical as-is historical snapshot of the current/legacy VPS.
- Historical names such as `nl-core-vds`, legacy service names and legacy paths remain unchanged in that baseline.
- New taxonomy applies only to target-state, planning, architecture, deployment and migration materials.
- The legacy VPS is an initial resource/state to evaluate, not an architecture template.

**Constraints:** Do not infer future service necessity from legacy activity or mere installation.

**Supersedes:** none.

---

## 2026-09-14T23:04:00+03:00 — Service/function composition before topology

**Status:** ACCEPTED

**Context:** An initial research pass moved too early into NetBird/private-backbone and public-edge topology before the useful service/function set of `edge` had been defined.

**Decision:**

1. Determine what existing VPS services are worth retaining.
2. Determine what additional functions/services make `edge` maximally useful as a complement to Home/PAI.
3. Agree the complete service/function composition.
4. Only then design network, ingress, service relationships, storage/runtime layout and migration/rebuild architecture.

The `nl-core-vds` audit is context for this work, not a migration plan.

**Supersedes:** preliminary network-first/private-backbone-first research direction from the beginning of this branch.

---

## 2026-09-14T23:04:00+03:00 — Premature network-first target design

**Status:** REJECTED

**Context:** Preliminary analysis proposed a NetBird-centered `edge ↔ Home/PAI` target before the final `edge` function/service set was known.

**Decision:** Do not accept a private-backbone technology or detailed topology at this stage. Any future WireGuard/NetBird-based option must also be validated against real Russia ↔ external-VPS DPI conditions rather than assumed to work from protocol theory.

**Supersedes:** none; rejected proposal only.

---

## 2026-09-16T13:27:00+03:00 — Accepted core services for future `edge`

**Status:** ACCEPTED

**Context:** Existing legacy services were reviewed for future usefulness before adding new services.

**Decision:** Keep these product choices without further replacement search unless a concrete incompatibility or changed requirement appears:

- Xray
- Hysteria2
- n8n
- CloudCLI
- nginx
- Stalwart + Bulwark
- Authelia
- Codex CLI
- Antigravity CLI

Codex CLI + Antigravity CLI are the accepted core for cloud model use through subscription-based tooling.

Authelia is the intended unified web-login point for services under `escloud.us`. Native application authentication may be disabled for single-user convenience only where the application explicitly supports that trust model and doing so does not break API/session/security semantics.

**Supersedes:** open alternative-search status for these products.

---

## 2026-09-16T13:27:00+03:00 — Backup management direction

**Status:** ACCEPTED

**Context:** Restic on the legacy VPS works, but the current repository is on the same VPS/root filesystem and is not complete host-loss DR.

**Decision:**

- Do not reject Restic as an underlying backup engine.
- On a future clean deployment, deploy **Backrest** from scratch as the backup management/orchestration layer.
- Design the final repository/off-site DR topology later, after the complete target service set is known.

**Supersedes:** carrying the current local-only Restic arrangement forward as the final backup design.

---

## 2026-09-16T13:27:00+03:00 — VPS file-access requirements; Filestash implementation unresolved

**Status:** ACCEPTED

**Context:** Legacy Filestash was deployed mainly as a web UI for a VPS folder, but the future requirement is broader.

**Decision:** The future file layer must support, as appropriate:

- access to selected VPS working storage from MacBook;
- access from iPhone;
- access/mounting from `ai-node`;
- web browsing, upload/download and editing of selected VPS files;
- use of the same working data by automation/cloud-agent workflows where useful.

Filestash remains an implementation candidate, not an accepted final choice. Alternatives must be compared against these requirements.

**Supersedes:** treating Filestash merely as a browser UI over `/srv/cloud`.

---

## 2026-09-16T13:27:00+03:00 — Syncthing role remains under review

**Status:** PROPOSED

**Context:** Syncthing was originally planned for Obsidian, scripts and working-directory synchronization and as a way to move file-based tasks toward cloud CLI execution.

**Decision:** Do not keep Syncthing merely because task execution may use files. Evaluate separately:

- general working-file/script synchronization;
- `edge ↔ ai-node` directory synchronization;
- Obsidian synchronization;
- cloud-AI task transport/execution interfaces.

**Supersedes:** assumption that n8n-to-subscription CLI automation necessarily requires Syncthing/file-drop transport.

---

## 2026-09-16T13:27:00+03:00 — Replace Homepage

**Status:** ACCEPTED

**Decision:** Do not carry legacy Homepage forward. Create a dedicated Cloud Infrastructure page analogous in purpose to `home.lan`, including monitoring/status and useful Cloud-specific integrations.

**Supersedes:** legacy Homepage as the target portal.

---

## 2026-09-16T13:27:00+03:00 — Replace custom Maintenance Center

**Status:** ACCEPTED

**Decision:** Do not carry the legacy custom Maintenance Center forward. Target operational model is a maintenance page + Semaphore, analogous to the accepted current PVE/Home implementation.

**Supersedes:** custom updater/job/resume/rollback framework and legacy Maintenance Center implementation.

---

## 2026-09-16T14:55:00+03:00 — Obsidian canonical source and free synchronization requirement

**Status:** ACCEPTED

**Context:** Obsidian must be included explicitly in Cloud Infrastructure service/function analysis while preserving the already accepted PAI knowledge model.

**Decision:**

- Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.
- Do not make `edge` a new canonical source of truth by assumption.
- Determine the useful VPS role separately: sync endpoint, peer/mirror, remote workspace, web/file gateway, or no direct vault hosting.
- Synchronization must avoid paid Obsidian Sync and support the required Apple devices plus `ai-node`.
- Candidate mechanisms can include Self-hosted LiveSync/CouchDB, Remotely Save/WebDAV and Syncthing-compatible iOS clients, but no implementation is yet accepted.
- Do not combine multiple primary synchronization mechanisms for the same vault.

**Supersedes:** any implicit assumption that the old VPS Obsidian/data subtree should become the canonical vault.

---

## 2026-09-16T14:55:00+03:00 — Carry-forward rule for remaining legacy services

**Status:** ACCEPTED

**Decision:** Legacy services not explicitly accepted above are not carried forward automatically. Discuss and include them only if they prove a real requirement in the final Cloud Infrastructure service composition.

**Supersedes:** preserve-existing-stack-by-default approach.

---

## 2026-09-16T14:55:00+03:00 — Primary GitHub repository

**Status:** ACCEPTED

**Decision:** `Eugene-SN/Cloud-Infrastructure` is the primary GitHub repository for the Cloud Infrastructure project and the persistent cross-branch project context.

**Constraints:** Runtime infrastructure is not modified by this repository initialization. Do not commit credentials/secrets.

**Supersedes:** GitHub workflow OFF/unlinked state for this project.
