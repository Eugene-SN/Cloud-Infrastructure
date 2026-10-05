# n8n workflow cleanup — 2026-10-05

Status: **COMPLETE / ACCEPTED**, `N8N_WORKFLOW_CLEANUP=PASS`.
The operator explicitly authorized deletion of Documentation AI Oracle Pilot 01
and Hermes Machine Invocation after reviewing their purposes. This supersedes
the 2026-10-02 decision to retain Hermes4FMachine01 as dormant compatibility state.
Historical Stage 4 and executor acceptance records remain unchanged.

## Changes and recovery

Installed n8n is 2.40.7. Fresh read-only SQLite audit found twelve workflows,
zero archived workflows and no nonterminal executions. No remaining workflow
definition/settings referenced either selected ID. Scoped active host-reference
inspection found no callers.

The authenticated native editor REST interface performed POST archive followed
by DELETE for exactly StnDJjC7klAtEE73 and Hermes4FMachine01. The installed
workflow service and official [n8n deletion instructions](https://support.n8n.io/article/how-to-delete-a-workflow)
established the contract before mutation. Both workflows and their native
execution/history/shared-workflow records are absent, rather than merely archived.
Temporary trusted-owner sessions used the installed native encryption/JWT
implementations; native logout and HTTP401 replay verified revocation.
An initial node-e loading defect in the assistant's audit helper was corrected
by supplying a verified native entrypoint path; it caused no production mutation.

The Oracle-only Compose override had added a read-only pilot mount and file
allowlist. n8n alone was recreated from unchanged /opt/n8n/compose.yaml using
`--no-deps --force-recreate --pull never --wait`. Current image stayed
`sha256:ffeb52485f78b1b06c9a832205853cf75da72a07a514c9a27724df85979d6c34`;
both existing network IDs and the n8n/Knowledge mounts were preserved.
The pilot mount/allowlist and obsolete
/srv/benchmark/pilot-v1/runtime/n8n-oracle.override.yaml are absent.

The 2,084 other pilot files under /srv/benchmark/pilot-v1 are preserved
byte-for-byte as research evidence, source material and reproducibility artifacts;
they have no remaining n8n mount. No vendor PDF or research result was deleted.
Current encrypted credentials remain required by retained workflows and unchanged.

Existing scheduled Backrest edge-state snapshot
`cd6f692cc864c0f813225834f52a01ce960bae1252366e19c455d47fd1511cc6`
was read back: its consistent staged n8n SQLite contains both deleted workflow
IDs; its pilot export and result paths also exist. Recovery uses the established
matched n8n recovery contract/native exports. No new backup mechanism or manual
backup flow was introduced.

## Remaining inventory

Confirmed by both native MCP search and fresh live SQLite: **10 workflows,
9 published/active, 1 unpublished; zero archived**.

| Name | ID | State / trigger | Purpose |
| --- | --- | --- | --- |
| AIExecution01 | wQ9ZqMisMCGadGEE | Active; authenticated webhook or subworkflow | Explicit vLLM, Codex, Antigravity or Hermes execution; direct native paths and structured results. |
| GitHub PR → Plane Item | PlaneGitHubSync01 | Active; subworkflow | Associate an explicitly identified PR with a PERSO item and create/update its idempotent PR comment without changing issue state. |
| GitHub → Plane Polling | PlaneGitHubPoll01 | Active; every 15 minutes | Read repository PRs, find an unambiguous PERSO identifier and call PlaneGitHubSync01. |
| LenovoPdfCleanup | ENo9jFkwcE4PFOyL | Unpublished; manual/subworkflow candidate | Download one original PDF, process through edge CLI, upload cleaned output and remove its temporary job; operator acceptance remains pending. |
| NextcloudEventIngress01 | bxsXXufaaXuubA3Z | Active; authenticated webhook | Persist four native file-event classes in the durable Nextcloud Data Table inbox before acknowledgment. |
| NextcloudTools01 | G0WysKToqsel8yL2 | Active; authenticated webhook or subworkflow | Eleven reusable file/folder/share operations through the existing Nextcloud identity. |
| Plane API deletion reconciliation | PlaneDeletionReconcile01 | Active; every 5 minutes | Confirm issue deletions from native Plane activity records and enqueue them for notification. |
| Plane Event Ingress | PlaneEventIngress01 | Active; signed webhook | Verify raw-body HMAC, filter/normalize Plane events and persist them for asynchronous processing. |
| Plane → Mattermost | PlaneMattermost01 | Active; every 30 seconds | Process the Plane inbox, notify meaningful creates/changes/deletes and persist comparison state. |
| TechnicalDocumentationSync | QouVaVNhAqSiYq5D | Active; daily 07:00 Europe/Minsk; manual trigger | Monitor nine Lenovo model collections through ASP/Press, download updated originals, remove superseded filenames and update INDEX.html. |

## Verification and limits

All ten retained definitions (nodes/connections/settings/name/description/pins/meta/
node groups), draft/publication version IDs and active/archive flags match the
pre-change baseline. Credential IDs/names/types/encrypted data, Data Table schema
and all four webhook registrations are unchanged. AIExecution01 retains its
previous accepted nodes/connections/settings hash
`f63f0e5c8d6a667518694932e87b02cf1f5edf074eef0c3fb1237abeacb633e6`.
No remaining definition references either removed ID.

n8n readiness returned HTTP200 and Docker health is healthy. Fresh monitoring
shows n8n and all three critical Plane scheduled workflows OK with zero
consecutive failures; other application probes are OK. Container image, networks,
base Compose and retained workflow publication remain unchanged. Exact obsolete
override and own Playwright/temp audit artifacts are removed.

The overall monitor was already FAIL before this work: ai-node/vLLM probes have
been failing since their last success on 2026-10-04. Edge, Knowledge, operations
and the relevant n8n integrations are OK. This cleanup does not establish current
inference availability or repair that separate existing issue; no AI execution
or notification test was issued.

```text
N8N_SELECTED_WORKFLOWS_DELETED=PASS
N8N_REMAINING_WORKFLOW_COUNT=10
N8N_REMAINING_DEFINITIONS_AND_PUBLICATION=UNCHANGED
N8N_CREDENTIALS_AND_WEBHOOKS=UNCHANGED
N8N_PILOT_RUNTIME_RESIDUE=ABSENT
N8N_PILOT_RESEARCH_ARTIFACTS=UNCHANGED
N8N_READINESS_AND_CRITICAL_WORKFLOWS=PASS
N8N_RECOVERY_SNAPSHOT_READBACK=PASS
N8N_WORKFLOW_CLEANUP=PASS
```

## Subsequent operator instruction — complete testing residue deletion

The operator rejected retention of old test materials. This supersedes the
preserved-pilot-files statements and UNCHANGED marker at the earlier checkpoint
above. The current live state is:

- Entire /srv/benchmark absent: 2,086 regular files / 165,408,682 bytes removed,
  including five test-input PDFs and all pilot environments/cache, prepared data,
  reports, raw exports/results and scripts. No active process/container/workflow
  dependency was found before deletion; symlinks were removed without following
  their external targets.
- Exactly 24 AIExecution01 child runs are absent, with execution payloads removed
  through native POST /rest/executions/delete. Installed native flatted parsing
  confirmed all belong to removed pilot parents 2268/2350. IDs:
  2270, 2273, 2278, 2282, 2286, 2290, 2295, 2299, 2302, 2306, 2309, 2311,
  2351, 2360, 2368, 2374, 2398, 2411, 2414, 2421, 2426, 2430, 2432, 2434.
- Eight exact unused temporary files removed after hash/reference/open-FD checks:
  /tmp/legacy-dir-refs.Krfm3I, /tmp/test_maintenance.json, /tmp/test_status.json,
  /tmp/mm_swagger.yaml, /tmp/mm_swagger.json,
  /tmp/hermes-git-config.pre-departialize.nfQCgy,
  /tmp/installed-skill-names.txt and /tmp/maint_frozen_iris.html.
- All ten remaining workflow definitions/settings/publication and credentials
  match the pre-change baseline. All 80 files in the current cloud Lenovo
  documentation tree are byte-unchanged. Retired workflow/child storage paths
  are absent. n8n readiness HTTP200 and critical-workflow monitoring OK.
- No retained test copy/export/archive or new backup flow was created. This
  cleanup leaves the ordinary accepted backup/audit/service lifecycle intact.

Current marker: N8N_PILOT_RESEARCH_ARTIFACTS=ABSENT;
N8N_RETIRED_TEST_EXECUTIONS=ABSENT; N8N_RETIRED_TEST_RESIDUE_CLEANUP=PASS.

## Subsequent operator decision — three value-audit candidates removed

Status: **COMPLETE / ACCEPTED**, N8N_WORKFLOW_VALUE_CLEANUP=PASS.
The operator explicitly authorized removal after the extended value audit.
This supersedes retention of these three at the earlier ten-workflow checkpoint.

### Exact removal and normalization

- Native archive + permanent delete: PlaneGitHubPoll01, PlaneGitHubSync01,
  bxsXXufaaXuubA3Z (operator-renamed NextcloudEventIngress). Workflow/history/
  shared-workflow/webhook/execution records are absent; zero archived retention.
- 610 retained executions before deletion: polling295, sync0, Nextcloud315.
  Native deletion removed their payloads; zero orphan execution_data rows remain.
- Native Nextcloud OCS removed exactly registrations1–4 after URI/event/ID audit.
  All targeted nextcloud-events registrations and pending WebhookCall jobs are absent.
- Native n8n DELETE removed NextcloudEventInbox01/pZDk2S89xgYGSXEO, 343 rows,
  four column metadata records and its physical user table.
- Two proven-exclusive credentials deleted: akETYuAX0iaYCE6K and dju3iGLC4SWK191K;
  shared records absent. No gh authorization revoke: gh api user succeeds.
- Live/canonical monitor now covers only PlaneMattermost01 and
  PlaneDeletionReconcile01; only the monitoring agent was restarted.
- Canonical retired exports removed: PlaneGitHubPoll01.json, PlaneGitHubSync01.json,
  NextcloudEventIngress01.json and its dedicated data-tables.json.
- Event-only allow_local_remote_servers override deleted through native occ.
  Retained Nextcloud Mattermost URL is public HTTPS; native channels GET200 works
  after restoring the upstream false default.
- Cron's event-only edge_internal membership removed from Docker and Compose;
  default/postgres_net endpoints remain. Native Compose parser verified that
  only this membership changed. App retains its required file-tool alias/network.
  No Nextcloud/n8n container recreation, image update or shared network deletion.

### Current seven-workflow inventory

| Display name | Stable ID | Role |
|---|---|---|
| AIExecution | wQ9ZqMisMCGadGEE | Explicit AI backend tool |
| NextcloudTools | G0WysKToqsel8yL2 | Eleven file/share operations |
| LenovoPdfCleanup | ENo9jFkwcE4PFOyL | Sequential PDF cleanup child |
| TechnicalDocumentationSync | QouVaVNhAqSiYq5D | Daily07:00 Minsk source sync and cleanup caller |
| Plane Event Ingress | PlaneEventIngress01 | Signed Plane intake |
| Plane → Mattermost | PlaneMattermost01 | Significant changes every30s |
| Plane API deletion reconciliation | PlaneDeletionReconcile01 | Confirmed deletion activities every5min |

SQLite and native MCP both report seven active/published workflows, four MCP-exposed.
Before mutation the operator renamed AIExecution01/NextcloudTools01. Canonical
exports now reflect the current labels; stable IDs and webhook paths did not change.
At the post-cleanup13:04UTC hash checkpoint, retained graph/settings/description/
pins/meta/node-groups/publication, seven credentials and both Plane tables matched
baseline. All82 library files (78 originals, two cleaned PDFs, INDEX.html and INDEX.md)
matched the pre-cleanup aggregate path/content hash at that checkpoint.
Subsequent parallel operator-authorized catalogue-date work, commit9148be1,
republished TechnicalDocumentationSync as758bcab2-aa27-4c55-b158-932b74d1a4ac
and updated the index. It is preserved and belongs to that separate accepted scope;
this cleanup does not restore earlier graphs or file content.

Nextcloud app/cron native status:35.0.1, maintenancefalse, needsDbUpgradefalse.
App-password WebDAV PROPFIND207; native Mattermost channel GET200. n8n readiness200/
Dockerhealthy; both retained scheduled workflows have fresh successful runs and
monitorOK, including post-cleanup deletion reconciliation at13:00UTC.
Retired references are absent from active graphs/settings/current monitor/tool
config. Historical decisions, accepted evidence and native backup/audit/token
lifecycles remain required and preserved. No backup, test data or export copy added.

A read-only table audit initially used unsupported item GET and received editor HTML:
assistant verifier defect, no runtime failure/mutation. Installed controller
established collection GET and exact item DELETE, which passed. A standalone PHP
bootstrap verifier did not reliably emit output and was discarded; installed native
authenticated HTTP channels GET supplied actual verification. A Markdown helper
syntax error was rejected before execution and caused no file/runtime mutation.
Exact final mutation shell/Python/JavaScript passed separate syntax preflight.
Temporary trusted-owner sessions were logged out; HTTP401 replay proved revocation.

N8N_VALUE_CLEANUP_WORKFLOWS=7
N8N_VALUE_CLEANUP_CREDENTIALS=7
N8N_VALUE_CLEANUP_DATATABLES=2
N8N_RETIRED_VALUE_ARTIFACTS=ABSENT
N8N_RETAINED_BUSINESS_STATE=UNCHANGED
N8N_WORKFLOW_VALUE_CLEANUP=PASS
