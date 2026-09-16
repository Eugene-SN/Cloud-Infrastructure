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

**Status:** ACCEPTED

**Context:** Syncthing was originally planned for Obsidian, scripts and working-directory synchronization and as a way to move file-based tasks toward cloud CLI execution.

**Decision:** Do not accept or reject Syncthing yet. Evaluate separately:

- general working-file/script synchronization;
- `edge ↔ ai-node` directory synchronization;
- Obsidian synchronization;
- cloud-AI task transport/execution interfaces.

Do not keep Syncthing merely because task execution may use files.

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

---

## 2026-09-16T15:00:00+03:00 — Functional capability scaffold before domain solution research

**Status:** ACCEPTED

**Context:** The next proposed step was a detailed `Storage / Files / Obsidian Sync` research block. That is premature while the complete preliminary functional scope of `edge` is still unknown.

**Decision:**

1. First build a comprehensive **preliminary functional capability scaffold** for Cloud Infrastructure / `edge`.
2. The scaffold describes required or potentially valuable functions/capabilities, not necessarily a selected product for every function.
3. Already accepted products may anchor the functions they already satisfy, but unresolved functions remain technology-neutral capability slots.
4. Identify overlaps with Home Infrastructure and Personal Agents Infrastructure and keep only functions for which Cloud Infrastructure provides material value.
5. Only after the functional scaffold is complete, perform focused research on implementation alternatives for unresolved domains.
6. `Storage / Files / Obsidian Sync` is explicitly deferred to that later implementation-selection stage; the previously accepted requirements for those domains remain valid.
7. After candidate services are evaluated, assemble and approve the complete service composition; only then design topology, inter-service relationships and deployment architecture.

**Supersedes:** the implied sequencing that `Storage / Files / Obsidian Sync` should be the immediate next research block.

---

## 2026-09-16T16:04:00+03:00 — First-pass capability catalog screening

**Status:** ACCEPTED

**Context:** A broad catalog of 75 common private-VPS use cases was reviewed against the existing Home Infrastructure and Personal Agents Infrastructure. The purpose was to eliminate obvious duplication before deeper research.

**Decision:**

### Accepted or already accepted for the preliminary `edge` capability scaffold

- DPI-resistant foreign Internet egress through the accepted Xray/Hysteria2 stack.
- Public web ingress/reverse proxy through nginx.
- Mail through Stalwart + Bulwark.
- Unified web authentication through Authelia.
- Dedicated private Cloud Infrastructure portal/status page, replacing Homepage; a public decoy/masquerade page for the VPN public edge is also of interest.
- Maintenance through the accepted maintenance-page + Semaphore direction.
- Backup management through the accepted Backrest direction.
- VPS working-file access from MacBook/iPhone/`ai-node` plus web file browsing/editing.
- Continuous selected-file synchronization; implementation remains unresolved.
- Obsidian synchronization/mirror role; implementation remains unresolved while canonical vault stays on `ai-node`.
- n8n as the common automation plane; do not add a separate generic cron/job automation plane merely because a task is simple.
- CloudCLI plus Codex CLI and Antigravity CLI as the accepted cloud-AI workspace/subscription execution core.
- Long-running cloud coding-agent workflows.
- Website-change monitoring/automation in n8n.
- Internet document-ingestion/orchestration toward Home/PAI processing.

### Explicitly excluded from the current `edge` functional scope

- Treating Ubuntu/SSH toolbox itself as a user-facing capability; Ubuntu is the hosting substrate.
- VPS as a replacement for the existing Home/PVE/ai-node/MikroTik infrastructure plane.
- Authoritative DNS and personal recursive/filtering DNS on `edge`; Home Infrastructure is preferred.
- Full personal cloud-drive suite on `edge`; evaluate that class of functionality for Home/PAI instead.
- Calendar/contacts DAV on `edge`.
- Git hosting/mirroring, CI/CD runner, artifact/package registry, generic sandbox/test environment, public staging environment, standalone database hosting without a consumer.
- Separate generic scheduled-script/job runner outside n8n.
- General SaaS/cloud credential gateway as a standalone capability.
- Headless browser and remote interactive browser as standalone edge services at this stage.
- Central MCP gateway and multi-provider AI API gateway/router at this stage.
- CGNAT bridge, geographical synthetic-monitoring point, TURN/STUN, MQTT/IoT broker, game/media/download/photo hosting, and general learning/lab use.
- VoIP/PBX and realtime communication servers for now; reconsider only if a future use case appears.

### Deferred for explicit evaluation before inclusion or rejection

- Central TLS/certificate handling as a distinct capability versus an implementation property of ingress.
- Public/machine API access for deployed services and the cross-device access model.
- Internet webhook reception.
- External uptime monitoring, dead-man/heartbeat monitoring and notifications.
- Public decoy/masquerade page plus private operational/status portal composition.
- Off-site backup target role relative to Home Backrest/PBS.
- Whether a separate VPS bootstrap/DR store adds value beyond GitHub/Home backup.
- Full external log/metrics collection; currently suspected to be unnecessary complexity.
- Password/2FA vault and adjacent personal information-management services.
- RSS/feed aggregation integrated with n8n/AI.
- General continuous web/data collection beyond concrete feed/change-monitoring use cases.
- Small web utilities such as paste/snippet/temporary-note/URL-shortening services.
- Hermes/personal AI-agent runtime role on `edge` and its relationship to CloudCLI, subscription CLIs and local vLLM.
- Bots as an interaction/notification channel.
- Supervised/autonomous web-research workflows.
- `edge ↔ Home/PAI` task handoff and document-ingestion integration.
- Public gateway from `edge` to Home services; evaluate separately from existing Home outbound proxy routing.
- Private/site-to-site `edge ↔ Home` connectivity mechanism.
- Limited late-stage failover/secondary-endpoint role after the primary infrastructure is complete.

**Constraints:** Do not infer a product choice from an accepted capability unless the product has already been explicitly accepted elsewhere in this log. Continue capability-level discussion before topology/product research.

**Supersedes:** the unfiltered 75-item capability catalog as a working scope.
