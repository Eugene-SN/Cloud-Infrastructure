# Plane Part 2 — Core Integrations — 2026-10-02

**COMPLETE / ACCEPTED — `PLANE_PART2_CORE_INTEGRATIONS=PASS`.** One operator-authorized workstream, one final Backrest flow and one canonical implementation/acceptance commit. Starting main: `2406412567a1b67522c98f297600e174061337a5`. Part 1, its independent audit and P2-1 SMTP remain accepted. This record supersedes the proposed separate P2-2a/P2-2b/P2-3/P2-4/P2-5 sequencing; optional workflows below do not require further numbered acceptance stages.

Material runtime claims below are CONFIRMED FACTS from current Compose, installed source, native APIs, actual workflow executions, native MCP transport and the resulting recovery snapshot. No service upgrade, replacement identity, public route, Docker network or database was introduced.

## Internal transport and authentication

- n8n `2.40.7` retains the existing `edge_internal` membership and alias `n8n`; adds `n8n.edge.internal` in `/opt/n8n/compose.yaml`. No host/public DNS mutation.
- Protected Plane `plane.env`: `WEBHOOK_ALLOWED_HOSTS=n8n.edge.internal`, `WEBHOOK_ALLOWED_IPS=`. Native Compose confirms the common backend environment belongs to api/worker/beat-worker; only these three and n8n were recreated. Other service lifecycle changes were the accepted final backup quiesce/start and the required Hermes gateway reload.
- Plane worker Docker DNS resolved the new alias, reached n8n readiness with HTTP 200, and installed `WebhookSerializer` accepted the complete `http://n8n.edge.internal:5678/webhook/plane-events` URL including its SSRF validation. n8n reached `plane-api` on the existing network.
- Original `Hermes4FMachine01` workflow and both original encrypted native credentials remained byte-equivalent in their logical SQLite rows after recreation, integration and recovery capture. The stable `n8n_hermes` bridge contract remains unchanged.
- Existing operator `es@escloud.us`, UUID `62abe1fe-0ca2-4b2d-811d-e4e50ff69dd3`, owns two independent active ordinary-user PATs: `n8n Integration` (`218354ce-4e0a-4cd5-a709-7ffb65912810`) and `Hermes MCP` (`0b5b5580-6687-474c-b601-fecce0b3a061`). No service user/mailbox/invite or invented fine-grained scope. API v1 uses `X-Api-Key`; each PAT passed project retrieval.
- n8n stores its PAT only in its encrypted native credential. Hermes stores its PAT in protected mode0600 `/home/core/.hermes/.env`, referenced by native interpolation from config. Neither PAT is in Git. Independent revoke is possible; token `last_used` is expected state.

Production context: workspace `personal`, UUID `efd9a5ab-d149-44b4-ad64-60e8d3c8e19a`; its only current project `personal`, identifier `PERSO`, UUID `0be26f75-fc5b-4e15-9d69-efc4cca4e65d`. Seven pre-existing onboarding work items were retained unchanged.

## Plane → n8n → Mattermost

One active native workspace webhook: UUID `e5b6c10c-d447-4fd0-90b9-a761998d3234`, target `http://n8n.edge.internal:5678/webhook/plane-events`, only `issue=true`; project/cycle/module/issue_comment flags false. Installed sender uses HMAC-SHA256 and headers `X-Plane-Signature`, `X-Plane-Event`, `X-Plane-Delivery`. Actual create/update actions were plural `created/updated`; ingress normalizes singular and plural create/update/delete. This is the current CE webhook/API v1 implementation, not v2.

| Native n8n object | Role |
|---|---|
| `PlaneEventIngress01` | Webhook raw bytes → native Crypto v2 HMAC → fixed-length signature comparison → workspace/webhook/project validation → native durable inbox upsert → quick 204 |
| `PlaneMattermost01` | Every 30 seconds, drain/coalesce inbox serially, compare significant state, notify with existing Mattermost node/credential, persist state and remove only the exact processed payload |
| `PlaneDeletionReconcile01` | Every 5 minutes, use native API v1 deletion activities to cover CE API/MCP deletes that do not emit workspace webhooks |
| `PlaneEventInbox01` Data Table | ID `a7XaH434xzlQVgcA`; coalesces by issue UUID + normalized action, never delivery UUID |
| `PlaneIssueState01` Data Table | ID `5gGP9oUlIe17CoRg`; project context and significant-state fingerprint; seeded with the seven current tasks |
| `PlaneAPI01` credential | ID `2ViDHEcRCHBygLnv`, type `httpHeaderAuth`, `X-Api-Key`; origin/path `http://plane-api:8000/api/v1/` |
| `PlaneWebhookHMAC01` credential | ID `FZAUjrHzuRzKQml4`, type `crypto`, native encrypted HMAC secret |

Both Data Tables belong to existing n8n personal project `O9C85OVLEuW5PgOk` and reside in its existing SQLite database. No external idempotency store. Significant fields: name, state, priority, sorted assignees, target/due date. Same semantic state and description-only changes are suppressed; older `updated_at` payloads cannot overwrite newer cached state. Multiple field events are coalesced within the 30-second window. Conditional inbox deletion preserves a concurrently received newer payload. State is saved after a successful Mattermost post. This is practical semantic deduplication, not a distributed exactly-once guarantee across a process failure after an external post.

**Confirmed CE boundary:** API v1/MCP DELETE records `IssueActivity(verb=deleted, field=issue)` but does not call workspace `webhook_activity`. Also, queued update serialization after a very fast delete can produce an empty object without an ID; ingress ignores it. Production reconciliation reads native activities, newest-first with pagination, and enqueues only an exact project/issue `deleted` activity. It never treats HTTP 404, archiving or missing access as proof of deletion. API/MCP deletion notifications can therefore take up to five minutes plus the 30-second drain; their title is the last observed cached title. A correctly signed deletion-payload fixture separately verified the ingress delete branch and duplicate suppression; it is not presented as a naturally emitted API-delete webhook.

Private Mattermost channel `plane`, ID `adkccukmsf8gffz6uimiqewk7r`, team `es-cloud` (`r41o9167j3n9urqntshb4pct9o`), has exactly operator `eugene` (`mof5mc6w3jds8qp36b678qrzoc`) and existing n8n bot (`4ty8tfwmdir9mxkeua3n7658mc`). Reused unchanged credential `16a0a988ad514ab1`, `Mattermost API - edge internal`, type `mattermostApi`, backend `http://mattermost:8065`. No additional bot/token. Notifications contain action, PERSO identifier/title, useful changed values and direct public `/personal/projects/<project>/issues/<issue>` URL.

Evidence: missing/invalid signatures returned 401; exact raw JSON bytes, including formatting differences, returned 204. Initial signed response took 153ms; final durable-before-204 delete fixture took 206ms. Real bounded `PERSO-8` (`d3191b50-6630-452f-9444-78892d242c33`) produced create and a single multi-field name/priority update post. Two replays with new delivery UUIDs and a description-only change added zero posts. Its real native deletion produced a deletion post via reconciliation. Native MCP test `PERSO-9` (`aa0992b5-f096-4ad6-9c92-bd41737620ac`) produced observed create and deletion posts. Exactly five test notification posts were permanently removed through mmctl; native membership system posts and the production channel remain.

## GitHub → n8n → Plane

- `PlaneGitHubPoll01`: every 15 minutes, paginate all repository PRs from `Eugene-SN/Cloud-Infrastructure` through GitHub REST, including open/closed/merged. No callback/public webhook route.
- Native encrypted `githubApi` credential `akETYuAX0iaYCE6K`, `GitHub API - existing edge operator`, reuses the already authorized core `gh` OAuth credential (`repo`, `read:org`, `gist`); no new GitHub identity/PAT. Revoke/expiry of this shared authorization also affects this consumer.
- Associate only exactly one unambiguous `PERSO-N` across PR title/body/head branch, resolve the existing issue through API v1, and skip missing/non-target issues. Multiple distinct IDs are treated as ambiguous.
- `PlaneGitHubSync01`: one native comment with `external_source=github`, `external_id=Eugene-SN/Cloud-Infrastructure#<number>`; useful title, URL and open/merged/closed state. Read current comments with native pagination, create once or PATCH changed content. No task state transition.
- Real authenticated paginated polling passed. Existing PRs #1/#2 currently contain no PERSO association. Bounded sync verification used actual PR #2 metadata and an explicit temporary input association to PERSO-8; no GitHub title/body/branch/PR was modified or created. Native comment `c4f76853-8155-4686-86e5-85f7b2effea0` contained its real merged status and URL. Repeating sync retained exactly one comment with unchanged `updated_at`. The comment was cleaned through deletion of its exact temporary parent issue. Natural matched-PR arrival remains future development activity, not claimed as observed today.

## Hermes ↔ Plane MCP stdio

Official current `plane-mcp-server 0.3.3` / `plane-sdk 0.3.1`, resolved through existing managed `/home/core/.hermes/bin/uvx`, without a version pin. Native config: `mcp_servers.plane`, command uvx, args `plane-mcp-server stdio`, base origin `http://127.0.0.1:18111` (no appended `/api/v1/`), slug personal, PAT reference `${PLANE_API_KEY}`, payload logging disabled. Native agent context supplies the confirmed PERSO project UUID and project-scoped CE usage. No direct Codex/Antigravity MCP configuration.

Native Hermes registers 13 standard CE resource tools: project, workitem, workitem_comment/link/relation/activity/attachment, state, label, member, cycle, module, project_estimate, plus four standard MCP resource/prompt utilities. No `page` tool or commercial-only tool group. `workitem` must receive project context for CE list operations; unsupported workspace-wide/PQL routes are not acceptance paths.

Actual MCP handshake used protocol `2025-11-25`; native project list/retrieve, project-scoped workitem list, temporary create/retrieve/update/comment/delete all passed. Exact deleted object returned native API 404. Hermes' own MCP discovery reported connected and its real gateway invoked `mcp__plane__project` through the unchanged n8n machine workflow and retrieved PERSO. Codex returned `PLANE_PART2_CODEX_OK`, actual CLI v0.160.0 exit0; Antigravity `agy` returned native JSON SUCCESS and `PLANE_PART2_ANTIGRAVITY_OK`. The earlier failed `ag` attempt was corrected by Hermes to the existing accepted `agy`; no executor installation/auth change.

Only Hermes gateway was restarted for config/environment reload; Dashboard stayed running. Before reload, the old gateway returned an unexpected `on_contended` argument error. Confirmed facts: it started 2026-09-30; API source on disk changed 2026-10-01; current lease implementation accepts the argument; reload resolved the failure. **INFERENCE:** the old process retained incompatible loaded modules. No Hermes source patch or upgrade was performed.

`PART2_PERSISTENT_MCP_SERVER=ABSENT` means no independent hosted MCP daemon/service/HTTP listener; native Hermes-managed stdio children follow its normal lifecycle.

## One final recovery checkpoint

Existing Backrest `edge-state` flow **384**, operations **384/385/386/387**, all `STATUS_SUCCESS`; existing prepare and D5 tier-copy hooks passed. RPC completed in 142.8 seconds. Snapshot:

`3977cc69b645d86cbaf35dcdd3be6cc00b8af70d0c431dfa96ed7167bb414906`

Snapshot timestamp: **2026-10-02 00:26:42.963 UTC / 03:26:42.963 +03:00**. Committed generation manifest: `created_at=2026-10-02T03:26:40+03:00`.

Actual Restic snapshot files were read back, not inferred from mutable staging:

- Plane custom dump 698,155 bytes, native pg_restore TOC 1,471 lines. Selected native COPY data verified both exact PAT IDs/values/active operator ownership, one active issue webhook/secret and encrypted SMTP password row without printing secrets.
- n8n SQLite 3,457,024 bytes: integrity `ok`, six active workflows (five new + original Hermes), five encrypted credentials (three new + two unchanged originals); original workflow/credential logical rows matched exactly.
- Protected Hermes config 6,251 bytes and env 27,501 bytes matched current runtime byte-for-byte. Protected Plane env 1,714 bytes matched current runtime.
- Mattermost dump 321,619 bytes, native pg_restore TOC 532 lines; actual snapshot channel row is private/active and its membership is exactly the two accepted users.
- Accepted mail recovery tree contains 151 files / 46,076,652 bytes. Existing manifest confirms quiesced full mail state, consistent n8n/agent SQLite overlays, logical shared PostgreSQL consumers and Plane DB/uploads/runtime. No additional recovery database/system or per-integration snapshot.

## Cleanup and final non-regression

Exact PERSO-8/PERSO-9 removed with native lifecycle; test notification posts removed; both test cache/inbox rows removed; inbox empty and seven legitimate task contexts retained. Exact acceptance n8n executions removed through native API. Four exact Hermes API sessions and stored responses removed through native endpoints; the empty Codex scratch Git directory removed after reference/process checks. Temporary container credential-input files, compile artifact and maintenance Plane app session removed. Temporary n8n maintenance JWT invalidated through native logout; an explicit replay of that exact JWT was rejected with HTTP 401. Task-private source copies, rollback bytes, downloaded recovery files and secrets under `/tmp` are removed at workstream completion. No `.bak`/retired tree is retained beside production.

Upstream-managed issue deletion/activity/API-access/webhook-delivery audit history and PAT `last_used` remain normal lifecycle state. No user/token/counter history is artificially reset.

Service non-regression: all 19 persistent containers running; native healthchecks healthy; Plane/API/live, n8n, Mattermost and other accepted applications reported OK. PostgreSQL databases remain mattermost/nextcloud/plane/postgres, no OpenProject role/database/container/workflow/credential or active tree. Hermes gateway/dashboard active, zero failed system/user units. nginx native `-t` passed and Plane ingress bytes match unchanged canonical source. Fresh SMTP_SSL certificate-verified TLS1.3/EHLO250/AUTH235 passed without sending another message; actual snapshot retains encrypted accepted settings. Final monitor evidence **2026-10-02T00:32:25.705902+00:00**: EDGE/OVERALL OK. Original n8n Hermes workflow and both original encrypted credentials remain exactly unchanged.

Maintenance's native Compose topology validator was normalized to the accepted FQDN in canonical and deployed `update-plane`; validation passed. Official vendor Compose, ingress, accepted services and supported update track remain unchanged. Canonical exports contain only native definitions, object IDs and secret references. Temporary verifier defects (execution context/field names/response envelope/native output and recursive-list flags) were corrected at their failed points; they were not represented as production failures or used to redesign production.

## Optional workflow disposition

Plane = execution/task state; Obsidian = durable knowledge/decisions. Knowledge is ready through accepted n8n/API capabilities but has no selected trigger/note schema and is `DEFERRED_PENDING_CONCRETE_USE_CASE`. No bulk vault mirror. Nextcloud, external calendar and intake email remain deferred. This does not block core acceptance.

## Final gates

```text
PLANE_INTERNAL_WEBHOOK_FQDN=PASS
PLANE_WEBHOOK_URL_VALIDATION=PASS
PLANE_WEBHOOK_HMAC_SHA256=PASS
PLANE_N8N_E2E=PASS
PLANE_API_V1_N8N=PASS
PLANE_MATTERMOST=PASS
PLANE_GITHUB_N8N=PASS
PLANE_HERMES_MCP_STDIO=PASS
PLANE_SMTP=PASS
PLANE_BACKUP=PASS
N8N=PASS
MATTERMOST=PASS
HERMES=PASS
STALWART=PASS
POSTGRES=PASS
NGINX=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
PART2_ADDITIONAL_PUBLIC_ENDPOINTS=0
PART2_ADDITIONAL_DOCKER_NETWORKS=0
PART2_ADDITIONAL_DATABASES=0
PART2_SILO=ABSENT
PART2_PERSISTENT_MCP_SERVER=ABSENT
KNOWLEDGE_WORKFLOW=DEFERRED_PENDING_CONCRETE_USE_CASE
NEXTCLOUD_WORKFLOW=DEFERRED
EXTERNAL_CALENDAR=DEFERRED
INTAKE_EMAIL=DEFERRED
PLANE_PART2_CORE_INTEGRATIONS=PASS
```

Mechanism references: official [Plane API v1](https://developers.plane.so/api-reference/introduction), [Plane MCP](https://developers.plane.so/dev-tools/mcp-server), [n8n Webhook/raw body](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook), [native Crypto](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.crypto), [native Data Tables](https://docs.n8n.io/build/work-with-data/data-tables), [GitHub PR REST](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests), [Backrest native API](https://garethgeorge.github.io/backrest/docs/api), and exact installed Plane v1.4.2/n8n2.40.7/Hermes source plus Backrest v1.14.1 protocol/source. Runtime exports: `deployments/plane/integrations/`; no secrets.


## Post-acceptance Mattermost sidebar correction — 2026-10-02

Operator observation: the retired OpenProject still appeared in Direct Messages, while Plane existed only as a notification channel. Fresh native Mattermost evidence at 2026-10-02T04:14:32+03:00: mmctl v11.11.1; five current bots (Calls/System/Hermes/n8n/OpenClaw), no Plane/OpenProject bot; native lookup of OpenProject username returned not found. Operator `eugene` had `direct_channel_show`, name `fc7je5jjqjfydgzjrb3nnz95gh`, value `true`: a missed sidebar preference from the retired integration. The previous active-object checks did not cover this preference.

Supported native `mmctl user preference set` changed only that preference to `false`; readback passed and all four other direct-message visibility preferences remained unchanged. This records a closed conversation; no messages were deleted or sent, no identity was reactivated, and no integration credential/workflow/service changed. Existing gateway and dashboard are active. The browser/mobile rendering after its preference update has not been directly observed; a client refresh may be needed.

Plane channel `adkccukmsf8gffz6uimiqewk7r` is confirmed private/active and serves notifications through the existing n8n bot. The accepted interactive agent surface is the existing Hermes Agent DM (`STAGE_04E_HERMES_MATTERMOST_INTEGRATION_ACCEPTANCE_2026-09-18.md`); Plane MCP is connected to that agent. There is no separately implemented Plane DM command handler. Adding a dedicated Plane control bot would change the preceding batch's explicit no-additional-bot instruction and requires the operator's interface choice; it is not represented as already deployed or verified.

This narrow correction does not create another Part 2 acceptance stage or replace flow384/snapshot3977cc69. Those remain the recorded pre-correction recovery checkpoint; no additional Backrest flow was run for a sidebar preference. Official mechanism: [mmctl user preferences](https://docs.mattermost.com/administration-guide/manage/mmctl-command-line-tool#mmctl-user-preference); exact v11.11.1 CLI help and native readback were used. `OPENPROJECT_MATTERMOST_DM_VISIBILITY=HIDDEN`.
