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

**Constraints:** Do not infer future service necessity from current runtime activity.

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

---

## 2026-09-16T16:10:00+03:00 — Four capability gaps added to the scaffold

**Status:** ACCEPTED

**Context:** A gap-analysis of the consolidated functional scaffold found four useful capabilities that did not require new top-level blocks but should be explicit requirements.

**Decision:** Add the following capabilities:

1. **Universal Capture Inbox** — low-friction submission of URLs, text, files, PDFs, images or commands from user devices into `edge` automation/knowledge workflows.
2. **Human-in-the-loop approvals** — selected n8n/agent workflows must be able to pause for explicit approve/reject/choice/confirmation using existing notification/WebUI/messaging surfaces.
3. **Mail as automation transport** — the accepted Stalwart + Bulwark stack may also provide inbound mail/attachment triggers and outbound system mail for n8n workflows.
4. **Durable store-and-forward between `edge` and Home/PAI** — cross-site tasks/events must survive temporary destination unavailability and support persisted state, retry/resume, observable outcome and safe re-delivery where required.

**Constraints:** These capabilities do not by themselves authorize new dedicated services. Reuse n8n, mail and existing interfaces where sufficient; do not infer a message broker, separate inbox application or approval platform.

**Supersedes:** the previous scaffold only insofar as these four capabilities were implicit or absent.

---

## 2026-09-16T16:56:26+03:00 — Migration preservation archive may include credentials

**Status:** ACCEPTED

**Context:** Stage 0 preservation is intended to support a possible clean Ubuntu rebuild while retaining expensive-to-reconstruct service state.

**Decision:** The manually downloaded migration-preservation archive may and should include the complete configuration and persistent state of services selected for the future `edge`, including credentials, authentication state, application secrets, private keys, TLS material and other sensitive files required for faithful restoration or migration.

Initial high-priority preservation audit focuses on Stalwart + Bulwark and Xray + Hysteria2, including the complete current `maintctl` script for later adaptation/optimization. The preservation scope may also include nginx, n8n, Authelia, CloudCLI, Codex CLI and other accepted services once their exact current paths and dependencies are audited.

**Constraints:**

- Sensitive archive contents are for local/manual transfer and recovery only.
- Do not commit credentials, private keys, application secrets or credential-bearing archives to GitHub.
- Do not print secret values into routine audit output when path/metadata verification is sufficient.
- Verify archive integrity before any destructive rebuild.

**Supersedes:** any narrower interpretation that the migration archive should omit credentials or secret state.

---

## 2026-09-16T19:44:00+03:00 — Two-plane migration preservation model

**Status:** ACCEPTED

**Context:** A complete credential-bearing migration archive is useful for disaster recovery, but is a poor working format for engineering review and should not be committed into Git history. The project also needs durable, directly readable migration context available to ChatGPT through the private GitHub repository during the fresh deployment.

**Decision:** Use two distinct preservation planes:

1. **Recovery plane** — the complete sensitive migration archive stays outside GitHub as authoritative recovery material. It may contain credentials, private keys, TLS material, application databases and auth state. The provider-level full VPS backup is an independent second recovery path.
2. **Engineering-context plane** — create a structured `migration-reference/` tree in `Eugene-SN/Cloud-Infrastructure` containing useful text/configuration/script/runtime-reference artifacts needed to understand and adapt the legacy implementation during fresh deployment.

The engineering-context tree should include, where useful:

- `maintctl` and `vpnctl` source scripts;
- Xray/Hysteria configuration structure and systemd units;
- nginx routing configuration;
- mail Compose/configuration structure and DNS/runtime notes;
- n8n/Authelia Compose/runtime structure;
- CloudCLI/Codex service definitions and non-secret runtime/reference configuration;
- firewall/network/systemd/package/runtime metadata needed for reconstruction.

**Constraints:**

- Do not commit private keys, SSH private keys, TLS private keys, application auth databases, OAuth/session tokens, raw credential files, mail databases, n8n credential databases, Authelia secret files or other credential-bearing state into GitHub.
- Do not place the complete migration archive in GitHub, Git LFS or release assets as normal project context.
- Before committing candidate text files, perform a secret-content audit and either verify that the file is safe verbatim or create a clearly marked redacted copy.
- Preserve original filenames/paths in manifests so the legacy implementation can be reconstructed accurately.
- The GitHub engineering reference is for architecture/migration work and is not itself the authoritative recovery backup.

**Supersedes:** any idea of using the complete credential-bearing archive as the primary GitHub project context.

---

## 2026-09-16T20:34:11+03:00 — Clean `edge` rebuild and substrate acceptance

**Status:** ACCEPTED

**Context:** Stage 0 preservation and both recovery planes were already accepted. The user selected and executed a GreenCloud provider rebuild of the existing VPS with Ubuntu 26.04, hostname `edge.escloud.us`, 4 GiB swap and the existing Termius ED25519 SSH key. The rebuilt host then underwent read-only first-boot audits, GRUB root-cause analysis, a controlled reboot and post-reboot acceptance.

**Decision:**

- The migration method for the legacy VPS is a **clean provider-level Ubuntu rebuild**, not an in-place migration.
- The rebuilt VPS is now the live Cloud Infrastructure node **`edge`**.
- `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`.
- Accepted substrate state includes Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`, KVM/x86_64, 2 vCPU, ~15 GiB RAM, 4 GiB swap, ~155 GiB root filesystem class, IPv4 `45.92.156.17/24`, IPv6 `2a0c:b847:ffff:283::a/64`, working DNS/NTP and SSH key access.
- OpenSSH socket activation through `ssh.socket` is accepted; do not enable `ssh.service` merely to match the previous service model.
- Root SSH access remains key-only in effective configuration (`PermitRootLogin prohibit-password`; password and keyboard-interactive authentication disabled).
- The first-boot `grub-initrd-fallback.service` failure is classified as a transient provider-provisioning race while `grub2-common` was upgraded from `2.14-2ubuntu2` to `2.14-2ubuntu2.1` during the same boot. After controlled reboot both GRUB units returned `success`, system state was `running`, failed units were 0 and no current-boot errors remained.
- GreenCloud cloud-init schema/deprecation warnings are non-blocking because effective SSH, swap and network state are correct; do not rewrite working provider-generated configuration solely to silence them.
- Historical `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains unchanged as the pre-reinstall historical snapshot and no longer describes current runtime state.

**Constraints:**

- This acceptance authorizes the clean substrate and explicitly scoped base-bootstrap work only.
- It does not implicitly authorize target-service restoration/deployment or architecture-dependent networking/storage/ingress changes.
- `migration-reference/` remains engineering context, not a restore bundle.
- Provider backup remains the whole-VPS rollback path; the external sensitive migration archive remains the selective recovery source.

**Supersedes:**

- the unresolved `in-place migration versus clean Ubuntu reinstall` status;
- the prior rule that no runtime mutation whatsoever could occur before a complete Architecture Contract, but only for the now-completed clean substrate reset and explicitly scoped base-bootstrap work.

---

## 2026-09-16T21:44:20+03:00 — Implementation chronology and branch/stage distinction

**Status:** SUPERSEDED

**Context:** This entry attempted to resolve sequencing drift by separating work-branch numbering from implementation-stage numbering and directing work through a separate functional-composition branch followed by a separate Architecture Contract branch.

**Historical decision:**

- branch `01` was treated as complete after clean substrate/minimal bootstrap even though its title still included unfinished Base Platform Deployment;
- branch `02 — Edge Functional Composition & Deferred Capabilities` was made the next work branch;
- branch `03 — Edge Architecture Contract & Topology` was planned before returning to finish Stage 1.

This sequencing was later found to conflict with the intended project workflow and is no longer current authority.

**Superseded by:** `2026-09-16T22:13:31+03:00 — Stage-aligned branch lifecycle and rollback to unfinished Stage 1`.

---

## 2026-09-16T22:13:31+03:00 — Stage-aligned branch lifecycle and rollback to unfinished Stage 1

**Status:** ACCEPTED

**Context:** The branch `01 — Edge Clean Rebuild & Base Platform Deployment` completed only the clean rebuild/substrate portion and a minimal architecture-independent bootstrap. The Base Platform Deployment part of that branch was not completed. Moving to a new branch at that point created false chronology. In addition, the project currently has a broad functional scaffold but has not selected every service/program for the final server. A premature proposed Architecture Contract also preselected future-stage products and topology before the corresponding stage-specific requirements discussions had occurred.

**Decision:**

1. Restore the canonical current checkpoint to **`01 — Edge Clean Rebuild & Base Platform Deployment`**.
2. Stage 1 / branch 01 remains **IN PROGRESS / NOT ACCEPTED** until the complete Base Platform scope is designed, deployed, verified and explicitly accepted.
3. `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS` and `EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS` are subset acceptances inside Stage 1; neither is Stage 1 acceptance.
4. The prematurely opened `02 — Edge Functional Composition & Deferred Capabilities` is not the canonical continuation point and must not be used to skip unfinished Stage 1 work.
5. From Stage 1 onward, each implementation stage has its own work branch:
   - `01 — Edge Clean Rebuild & Base Platform Deployment`;
   - `02 — Edge Core Applications`;
   - `03 — Edge Monitoring & Human Interaction`;
   - `04 — Edge Files, Sync & Obsidian`;
   - `05 — Edge Information & Cloud AI`;
   - `06 — Edge Home & PAI Integration`;
   - `07 — Edge Optional Capabilities`.
6. Every stage branch must begin with **stage-specific functional-requirements review and service/product/mechanism discussion** before architecture-dependent deployment.
7. Mandatory lifecycle for each implementation stage is:
   - requirements review;
   - unresolved service/product selection;
   - explicit stage-composition acceptance;
   - stage-scoped architecture/deployment contract and recovery path;
   - deployment;
   - verification;
   - explicit stage acceptance;
   - GitHub persistence/read-back;
   - only then branch transition.
8. The global `FUNCTIONAL_SCAFFOLD_DRAFT.md` is a capability scaffold, not a complete service/product inventory and not a final architecture. It intentionally leaves unresolved products for the stage where they are actually needed.
9. Already accepted global products (including Xray, Hysteria2, nginx, n8n, CloudCLI, Stalwart + Bulwark, Authelia, Codex CLI and Antigravity CLI) are not re-opened for replacement research without a concrete incompatibility or changed requirement, but their stage-specific deployment/integration details still require discussion and acceptance.
10. The previous detailed proposed `ARCHITECTURE.md` is withdrawn as current authority because it prematurely selected future-stage products/topology. In particular, SFTPGo, Self-hosted LiveSync/CouchDB, Syncthing, NetBird, the proposed complete domain map and proposed future-stage runtime topology are not accepted merely because they appeared in that proposal.
11. `ARCHITECTURE.md` now accumulates only accepted architecture facts/invariants and stage-scoped decisions after the corresponding stage composition is accepted.
12. ChatGPT must not suggest a new branch while the current branch/stage contains unfinished scope. When a stage is fully accepted, it should proactively propose the next stage-aligned branch name and a concise starter prompt.

**Current Stage 1 next step:** continue in branch `01` with Stage 1 requirements review and service/product selection for the unfinished Base Platform scope, then define its scoped deployment contract and complete deployment/acceptance.

**Constraints:**

- Do not preselect unresolved future-stage products to make a complete-looking architecture.
- Do not deploy Stage 2+ services before Stage 1 acceptance.
- Do not treat a branch title as complete when only one subtask inside it has been accepted.
- Historical Git commits are not rewritten; superseded/premature proposals remain available in history but are removed or replaced as current-tree authority.

**Supersedes:**

- `2026-09-16T21:44:20+03:00 — Implementation chronology and branch/stage distinction`;
- the current-authority status of the premature full-target `ARCHITECTURE.md` proposal;
- any guidance to continue in `02 — Edge Functional Composition & Deferred Capabilities` before Stage 1 acceptance;
- any workflow that requires selecting all final server products before proceeding stage-by-stage.
