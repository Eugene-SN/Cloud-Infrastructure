# Stage 11 — Remaining Infrastructure Gap Reconciliation & Completion

Date: 2026-09-22

Status: **ACTIVE / ACCEPTED SCOPE**

## Purpose

Stage 11 performs one systematic reconciliation pass for infrastructure capabilities that were historically deployed, discussed, selected or expected before user-specific workflows but were omitted, lost or incorrectly classified during the rebuild and repository bootstrap.

Stage 10 remains COMPLETE / ACCEPTED for the clean pre-Stage-11 baseline.

## Source order

Use, in order:

1. current runtime and actual configuration;
2. current canonical repository;
3. `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` and `migration-reference/`;
4. Stage 0–10 acceptance and decision records;
5. available project conversation/history context;
6. current upstream documentation where a product/version/capability needs fresh verification.

Do not infer current state from legacy presence.

## Classification

Every discovered capability must be assigned exactly one current disposition:

- `KEEP_CURRENT` — already deployed and sufficient;
- `HISTORICAL_ONLY` — intentionally superseded/removed and not needed;
- `MISSING_REQUIRED` — should exist before user workflows;
- `OPTIONAL_DEFER` — useful only for a later concrete workflow;
- `RESEARCH_REQUIRED` — requirement appears relevant but the current product/architecture choice is unresolved.

## Workflow

1. Build a complete candidate inventory from legacy/current sources.
2. Reconcile each candidate against current runtime and accepted architecture.
3. Correct repository history/current-state drift.
4. Research only `RESEARCH_REQUIRED` items.
5. Select `MISSING_REQUIRED` capabilities.
6. Deploy and accept only selected missing capabilities.
7. Perform Stage 11 final non-regression.
8. If material infrastructure changed, revisit Stage 10 with bounded re-acceptance limited to affected integration boundaries.
9. Begin Automation & User Workflows only after the above is complete.

## Initial known gap

Legacy baseline records:

- `cloud.escloud.us` protected by Authelia;
- Filestash backend `127.0.0.1:18334`;
- `/srv/cloud -> /mnt/cloud` RW;
- Filestash state under the legacy AI workspace;
- separate `sync.escloud.us` Syncthing surface.

The clean rebuild did not restore that file-access runtime. Current need and product choice must therefore be explicitly evaluated rather than assumed from either legacy presence or current absence.

Historical OpenCloud/Filestash presence does not itself authorize redeployment.

## Boundaries

Stage 11 is infrastructure completion/reconciliation, not user workflow implementation.

Do not use Stage 11 to build:
- user-specific n8n workflows;
- user-specific Hermes/agent workflows;
- Capture Inbox flows;
- mail-triggered business logic;
- research automations;
- custom approval/orchestration flows.

Those remain in the later continuous Automation & User Workflows workstream.

## Relationship to Stage 10

`STAGE10_FINAL_ACCEPTANCE=PASS` remains valid for the pre-Stage-11 clean baseline.

If Stage 11 changes material infrastructure, Stage 10 is revisited afterward only for bounded re-acceptance of the changed integration surfaces. Unaffected destructive/recovery evidence is reused.
