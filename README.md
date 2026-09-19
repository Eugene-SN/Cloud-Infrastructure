# Cloud Infrastructure

Public/cloud-facing infrastructure for the `edge.escloud.us` VPS, integrated with Home Infrastructure and Personal Agents Infrastructure.

## Current checkpoint

- Stages 0, 1, 2, 02.5, 3 and 4 are COMPLETE / ACCEPTED.
- Final Hermes marker: `STAGE4_FINAL_ACCEPTANCE=PASS`.
- Stage 4F Docker-network identity hardening is accepted; n8n reaches Hermes through stable bridge `n8n-hermes`.
- Stage 5 — Edge Knowledge Replication & Data Integration — is the next finite infrastructure stage and has not started.
- Stages 6–10 cover recovery, maintenance/update, monitoring/alerts, the Cloud portal and final integrated acceptance.

See [CURRENT_STATE.md](CURRENT_STATE.md) for accepted runtime facts and [IMPLEMENTATION_PHASES.md](IMPLEMENTATION_PHASES.md) for the dependency-ordered roadmap.

## Repository map

- [OPERATING_RULES.md](OPERATING_RULES.md) — project workflow, evidence and safety rules.
- [AGENTS.md](AGENTS.md) — durable instructions for agents working in this repository.
- [CURRENT_STATE.md](CURRENT_STATE.md) — canonical accepted runtime checkpoint.
- [ARCHITECTURE.md](ARCHITECTURE.md) — accepted architecture and ownership boundaries.
- [IMPLEMENTATION_PHASES.md](IMPLEMENTATION_PHASES.md) — completed stages and remaining acceptance plan.
- [INVENTORY.md](INVENTORY.md) — deployed components, versions and unresolved later-stage choices.
- [DECISIONS.md](DECISIONS.md) — chronological decisions with supersession semantics.
- [DOMAIN_NAMESPACE.md](DOMAIN_NAMESPACE.md) — `escloud.us` naming and ingress allocation.
- [FUNCTIONAL_SCAFFOLD_DRAFT.md](FUNCTIONAL_SCAFFOLD_DRAFT.md) — capability map; not a chronology authority.
- [STAGE_04_FINAL_ACCEPTANCE_2026-09-18.md](STAGE_04_FINAL_ACCEPTANCE_2026-09-18.md) — final Stage 4 acceptance.
- [STAGE_04F_NETWORK_IDENTITY_HARDENING_ACCEPTANCE_2026-09-19.md](STAGE_04F_NETWORK_IDENTITY_HARDENING_ACCEPTANCE_2026-09-19.md) — accepted stable Docker bridge/UFW follow-up.

Historical acceptance records preserve the state and evidence available at their creation time. Later canonical documents and explicitly superseding decisions take priority for current intent. Fresh runtime inspection takes priority for live facts.

## Secrets and recovery data

Do not commit credentials, private keys, session tokens or sensitive recovery archives. The historical temporary migration-preservation archive is absent and no longer required; do not recreate it. `migration-reference/` contains the retained sanitized engineering context and is not an authoritative restore bundle. New sensitive recovery state belongs in deliberate persistent/off-host storage with separately verified access and restore procedures.
