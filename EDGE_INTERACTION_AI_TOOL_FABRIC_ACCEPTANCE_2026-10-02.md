# Edge interaction / AI tool fabric — 2026-10-02

Status: **COMPLETE / ACCEPTED**. One operator-authorized continuous workstream on production `edge`; no intermediate implementation commit, acceptance record or task-initiated backup flow.

Baseline: `origin/main` commit `7417aa635ad7365ffa5f7275db58acf16de7266f`, accepted Stage0–13 and Plane Part2 core. The operator explicitly authorized this full production scope and final direct-to-main persistence. Architecture, native credential ownership, input/output contracts, exact secret-free client definitions, workflow exports, recovery and authoritative source links are in [the deployment contract](deployments/edge/interaction-fabric/README.md). [Secret-free verification metadata](deployments/edge/interaction-fabric/acceptance-evidence.json) records native transport/tool counts and exact test-execution cleanup IDs.

## Deletion reconciliation and monitoring

The first deployment gate was the confirmed pagination/paired-item defect in PlaneDeletionReconcile01. Only pagination URL construction changed: preserve `$request.url` before cursor and append encoded native `next_cursor`. Native save/publish, manual execution567, real API deletion of acceptance item PERSO10, reconcile execution573 and two native Mattermost messages passed. A standalone404 is still not deletion evidence; native deleted activities remain authoritative.

Repeated genuine schedule runs passed (including580/591/602 and later745/757/769/786/797), with three scheduled critical integrations subsequently healthy. The exact PERSO10 entity/tombstone/related test rows and Mattermost posts were removed, with native reference-aware deletion and database/API readback. Test cache/inbox rows are absent.

Existing Edge Monitor now collects native active/schedule/history state for PlaneMattermost01 (30s), PlaneDeletionReconcile01 (300s), PlaneGitHubPoll01 (900s). One `n8n-workflow-health` Integration/EDGE incident supplies all three diagnostics. Three terminal failures or scheduled-success staleness beyond three cadences plus declared timeout degrade health; transient failures, manual successes and normal idle state do not create false recovery/freshness. Missing/inactive/archived workflows and cadence drift are diagnosed; n8n HTTP failure suppresses the secondary incident. Five offline property tests cover these cases and a single incident/recovery. Deployed script/config bytes equal canonical sources.

## Native MCP fabric

| Client | Plane | n8n | GitHub | Playwright | OpenAI Docs |
|---|---|---|---|---|---|
| Hermes | PASS, CE13 | PASS, native35 | PASS,44 | PASS,25 | NOT_CONFIGURED |
| Codex | PASS, CE13 | PASS, native35 | PASS,44 | PASS,25 | PASS,5 |
| Antigravity | PASS, CE13 | PASS, native35 | PASS,44 | PASS,25 | NOT_CONFIGURED |

All12 service/client transports initialized from their actual native protected client definitions; direct real service calls passed. Plane server advertises30 tools; the three native client filters select the accepted same13 CE tools. Codex and Antigravity independently created/read/updated/commented/deleted project-scoped items using separate new ordinary PATs of the existing operator; those exact items/comments/notification posts were cleaned. Hermes' pre-existing PAT/filter/project context remain. No Plane users or commercial tools were added.

n8n2.40.7's complete native instance MCP surface is enabled. Each of three clients fetched SDK guidance, validated SDK code, created a temporary native workflow, edited it, tested it and accessed native Data Tables; each separately created a table, inserted and retrieved a row. Temporary objects were archived/deleted via native mechanisms and final native DB confirms only the nine durable workflows and three durable Data Tables. The two parameterized AI/Nextcloud workflows alone are explicitly exposed; `mcp.autoExposeNewWorkflows=false`.

Native n8n key management provides one MCP key per user and rotates that user's key as a unit. The accepted existing-owner key is shared by all three clients. Current OAuth discovery advertises public editor registration/token URLs behind accepted Authelia; independent loopback OAuth would change that ingress contract. This verified native constraint was resolved without a new user/proxy/public auth exemption; no reduced builder/testing/Data Table surface was introduced.

GitHub official v1.13.0 stdio exposes exactly `repos,issues,pull_requests,actions` plus individual `get_me`. All clients authenticated as the existing operator, read canonical repository content, PRs and Actions runs. The launcher resolves existing gh credentials in memory. Final launcher recheck covered all three handshakes/44 tools/authenticated reads and no extra container after each test client closed. Active Codex/Hermes/Dashboard stdio containers are client-owned runtime, not additional custom daemons. Their stdin ownership was verified; an earlier attribution of active Codex connections as test orphans was corrected, and Codex reconnected with the final launcher.

Official Playwright v0.0.83 used existing Chromium153 with native isolated/headless flags; each client navigated the real portal, inspected the page and closed its browser. A further authenticated n8n application read returned200 and found both new durable tool workflows. The native run-code tool echoed the short-lived test JWT in its result: it was immediately revoked using native logout, replay returned401, and local test results were sanitized. The later owner acceptance session was also revoked and replay returned401. No durable PAT, MCP key, SSH private key or app password entered Git. No browser test profile remains.

Codex-only OpenAI Docs MCP initialized5 native read tools, searched official Codex documentation and fetched the relevant current page. Context7/security plugin and existing Hermes browser tooling remain. Antigravity native global context and Codex developer instructions carry PERSO UUID and explicit workflow-tool usage.

## Explicit AI execution

AIExecution01 is active/published/exposed. Backend is required and restricted to the four explicitly requested identities; an attempted `auto` selector failed validation before a backend call. There is no quota/fallback router.

| Backend/property | Actual verification |
|---|---|
| Direct vLLM |647 text marker;654 real native JSON-schema result; current served qwen3.8-27b-fp8 |
| Direct Codex |681 native schema result;782 final noninteractive sandbox/approval argv with exact marker |
| Direct Antigravity |693 successful native structured_output/schema result |
| Hermes backend |723 actual private authenticated agent result |
| Existing Hermes4FMachine01 |774 native input fixture → real private Hermes response, exact legacy marker; original definition/update timestamp preserved |
| CLI timeout |718 timeout after1s, process-group termination, actual exit-15 |
| CLI cancellation |719 canceled with exit-15;720 cancel_requested via same native SSH path |
| CLI concurrency |735 busy/75 with both declared slots occupied; no extra CLI started |
| vLLM failure handling |730 unknown-model HTTP error;731 token_limit with bounded token budget |
| Invalid JSON / missing selector |739 native pinned backend-response test yielded invalid_json;740 explicit auto selector rejected |

The SSH private key is held by encrypted native credential; only its dedicated public key is added to existing core authorized_keys. The shared one-shot helper constructs argument arrays, carries stdin/encoded input, returns native exit/status/structured output and bounded stderr, cleans temporary files, and limits CLI concurrency to two. CLI cancellation records cannot signal a reused PID without matching start identity. There is no executor listener, Linux account, background worker or additional queue. HTTP timeout bounds the API request; cancellation addresses CLI process groups. Hermes JSON mode is prompt-plus-parse, not constrained decoding.

The existing Hermes native updater had already installed source `5bba024d8ddd388f56f354c1f789be825e3d8a3c`; this workstream did not issue an update. One configuration restart encountered native Python ImportDeadlockError; the same unchanged-contract restart recovered the API/Mattermost gateway. No source patch or inferred policy was introduced. Final gateway and Dashboard were reloaded against the current configuration and verified active.

## Nextcloud foundation

The existing OIDC operator owns native app password `n8n automation foundation` and encrypted n8n Nextcloud credential. No Nextcloud user was created. App and cron join existing edge_internal, app alias nextcloud.edge.internal; trusted domain/private local request options match the installed native contracts. Public HTTPS/OIDC and existing native Mattermost URL/token remain.

All11 operations passed against real operator storage: list658, find660, metadata657 and final native XML metadata780; mkdir680, upload683, download685 (content comparison), copy686, move687, share688, revoke689, delete690. Hermes779 and Antigravity781 also called the common exposed Nextcloud workflow successfully. The installed native node's successful empty-body DAV writes throw in its response utility; native HTTP Request with the same encrypted credential implements those writes and OCS revocation. Native list/find/download/share nodes and XML metadata remain. Final native save/publish/export readback also normalized empty-base64 input selection; no claim is made of an extra live empty-file test.

Four bundled native webhook registrations cover created/written/deleted/renamed. Source/runtime audit confirmed that userIdFilter suppresses DAV events because registration happens before authentication; the final native four-event filter is unfiltered, while payload preserves the real operator UID. Existing cron delivered eight actual file events into the authenticated native durable inbox, including all four requested classes; response204 follows insertion. Native authentication payload requires no generated event-user token. Unauthenticated calls to event/AI/Nextcloud webhooks return403. No business consumer or Mattermost notification workflow was invented.

The exact test folder/files, both temporary share links, native trash entry and eight inbox rows were removed; final rows/shares/trash/test-path readback is empty. Native Nextcloud→Mattermost NetworkService authenticated through unchanged `https://chat.escloud.us` and returned the existing eugene user. No SMTP integration was added.

## Non-regression and cleanup

Fresh evidence confirms Plane current API/project/webhook and SMTP configuration (mail.escloud.us465, implicit TLS, no STARTTLS); validated TLS1.3 EHLO250; genuine Mattermost/reconcile/GitHub polling scheduled successes; active Hermes API/Dashboard/Mattermost connection; healthy Nextcloud/native Mattermost path, Knowledge/Syncthing, Maintenance/Semaphore, Backrest and Edge Monitor. All monitor application and domain states were OK before the final backup; post-flow verification is recorded below.

Exact cleanup: three acceptance Plane entities with related records, four native Mattermost test posts, three temporary MCP-built workflows, three temporary Data Tables,68 explicitly identified n8n test executions and two stored Hermes responses removed. Native scheduled/audit/token-use/JWT-blacklist/CLI history is preserved. Acceptance payload/source/auth workspace is removed before final snapshot; snapshot readback scratch is removed afterward. Browser files/profiles and inactive execution request/temp records are absent.

The obsolete unreferenced manual Backrest config.json.bak was removed after reference audit. Backrest's native oplog.sqlite-*.backup remains specifically because v1.14.1 owns weekly/schema-aware database backup and keep3 lifecycle. Only current staging remains; native atomic preparation removes its transient previous generation after successful commit. No blanket Docker prune or unrelated native-history deletion was used.

Validation: five monitor property tests; native workflow save/publish/test/execution and real integrations; Python AST and Bash syntax checks; JSON/TOML parsing; canonical/deployed helper/monitor/Compose equality; Git whitespace and protected-credential/private-key scan.

## Final real Backrest flow

Exactly one task-initiated real final `edge-state` flow: **395**, native RPC HTTP200; operations**395–398** all `STATUS_SUCCESS` (backup, preparation hook, D5 copy/retention hook, snapshot indexing). Actual local snapshot **`78d8c27cfe06be6ad31e3e7b0ec441832ea8e5c6aadefc7727ba8df084bb3007`**. Native staging/snapshot and all hooks completed at2026-10-02T05:18:52Z. The pre-existing automatic04:00UTC schedule independently ran flow382 during this long workstream; it was not requested as an intermediate task checkpoint, and no existing backup schedule was changed.

Actual Restic ls/dump readback covered16 changed/configuration/recovery files. Thirteen static configs/helpers/staged encryption-key files byte-match final sources. The snapshot's n8n SQLite passes integrity_check and contains the final native workflow definitions, MCP enabled/autoexposure-off settings, owner's native MCP key, four encrypted new credentials and the empty durable Nextcloud inbox. The installed native n8n Cipher successfully decrypts those snapshot credentials using the snapshot encryption key; the restored SSH private key also validates through native crypto. Plane api_tokens, Nextcloud oc_authtoken and oc_webhook_listeners were read from the actual logical dump data and contain the new native PAT/app-password/four webhook state.

D5 was independently read via Restic: copied snapshot **`8e3b3c07bbe19661120d1d3af3c1799e8baa408db471929c03326434849c39ab`** identifies the local snapshot through native `original`. [Secret-free recovery evidence](deployments/edge/interaction-fabric/recovery-evidence.json) lists exact captured paths and properties. No recovery proof relies only on a successful command RC.

Post-flow monitor at2026-10-02T05:23:59Z reports edge/home_pai/knowledge/operations/overall and all application probes OK; all three critical scheduled workflows are OK with zero consecutive failures. No failed system/user units or stopped containers remain. Snapshot readback scratch is removed after recording this evidence. No second final flow is initiated.

## Final markers

```text
PLANE_DELETION_RECONCILIATION=PASS
N8N_CRITICAL_WORKFLOW_MONITORING=PASS
HERMES_PLANE_MCP=PASS
CODEX_PLANE_MCP=PASS
ANTIGRAVITY_PLANE_MCP=PASS
HERMES_N8N_MCP=PASS
CODEX_N8N_MCP=PASS
ANTIGRAVITY_N8N_MCP=PASS
HERMES_GITHUB_MCP=PASS
CODEX_GITHUB_MCP=PASS
ANTIGRAVITY_GITHUB_MCP=PASS
HERMES_PLAYWRIGHT_MCP=PASS
CODEX_PLAYWRIGHT_MCP=PASS
ANTIGRAVITY_PLAYWRIGHT_MCP=PASS
CODEX_OPENAI_DOCS_MCP=PASS
HERMES_OPENAI_DOCS_MCP=NOT_CONFIGURED
ANTIGRAVITY_OPENAI_DOCS_MCP=NOT_CONFIGURED
N8N_MCP_ENABLED=PASS
N8N_DIRECT_VLLM=PASS
N8N_DIRECT_CODEX=PASS
N8N_DIRECT_ANTIGRAVITY=PASS
N8N_HERMES_BACKEND=PASS
AI_EXECUTION_EXPLICIT_BACKEND_SELECTOR=PASS
AI_AUTOMATIC_QUOTA_ROUTER=ABSENT
NEXTCLOUD_N8N_CREDENTIAL=PASS
NEXTCLOUD_N8N_FILE_OPERATIONS=PASS
NEXTCLOUD_EVENT_INGRESS=PASS
NEXTCLOUD_N8N_AUTOMATION_FOUNDATION=PASS
NEXTCLOUD_AGENT_TOOL_FOUNDATION=PASS
EDGE_MCP_TOOL_FABRIC=PASS
EDGE_AI_EXECUTION_FABRIC=PASS
NEXTCLOUD_AUTOMATION_FOUNDATION=PASS
PART2_ADDITIONAL_CUSTOM_DAEMONS=0
PART2_ADDITIONAL_DOCKER_NETWORKS=0
BACKREST_FINAL_SNAPSHOT=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
EDGE_INTERACTION_AI_TOOL_FABRIC=PASS
```

Persistence: one final coherent implementation/acceptance commit directly on main; push and remote critical-file byte readback/worktree cleanliness are final checks. Historical acceptance records remain unchanged.
