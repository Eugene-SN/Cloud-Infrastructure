# Edge interaction and AI tool fabric

Accepted workstream: `EDGE_INTERACTION_AI_TOOL_FABRIC_ACCEPTANCE_2026-10-02.md`.
This foundation extends the accepted applications; operator-specific workflows remain future work.

The later bounded Hermes specialist reconciliation is accepted in `EDGE_HERMES_EXPLICIT_EXECUTOR_RECONCILIATION_ACCEPTANCE_2026-10-02.md`. Native commands, permission boundaries, updated helper completion and exact lifecycle/recovery are canonical in [hermes-executors/README.md](hermes-executors/README.md). It preserves this foundation and AIExecution01 definitions.

## Runtime and credential ownership

| Component | Native runtime / transport | Ownership |
|---|---|---|
| Plane MCP | `uvx plane-mcp-server stdio`, CE-compatible 13 tools | Existing operator; independent Hermes, Codex and Antigravity PATs |
| n8n instance MCP | `http://127.0.0.1:15678/mcp-server/http` | Existing n8n owner, native instance MCP key |
| GitHub MCP | `/usr/local/bin/edge-github-mcp`, official on-demand Docker stdio | Existing `gh auth token --hostname github.com` context |
| Playwright MCP | `npx --yes @playwright/mcp@latest`, isolated headless stdio | Existing host Chromium; no persistent test profile |
| OpenAI Docs MCP | `https://developers.openai.com/mcp` | Public read-only, Codex only |
| Direct CLI execution | Native n8n SSH node → `core@172.19.0.1:22` → `/usr/local/bin/edge-ai-exec` | Dedicated SSH key stored in encrypted n8n credential |
| Nextcloud automation | Native n8n credential → `http://nextcloud.edge.internal` | Existing OIDC operator, dedicated native app password |

Native client paths are `/home/core/.hermes/config.yaml` plus `.env`, `/home/core/.codex/config.toml`, and `/home/core/.gemini/config/mcp_config.json`. They are protected mode600. Definitions in `clients/` contain secret placeholders and must be merged into those existing files, preserving unrelated settings, Context7 and the Codex security plugin. They are not complete replacement configurations. `clients/context.md` records the added project/tool context: Codex uses native `developer_instructions`; Antigravity uses its native global `/home/core/.gemini/GEMINI.md`.

The installed Plane MCP version at acceptance is 0.3.3. Hermes uses native `tools.include`, Codex `enabled_tools`, and Antigravity `disabledTools` to present the same accepted 13-tool CE subset. Workspace is `personal`; project `personal` / `PERSO`, UUID `0be26f75-fc5b-4e15-9d69-efc4cca4e65d`. Project-scoped work-item calls require `project_id`; commercial/Pages and workspace-wide PQL tools are excluded because the installed CE API does not provide them. Existing Hermes PAT and configuration are preserved.

n8n MCP retains the complete native 35-tool core surface, including SDK reference, node discovery, workflow creation/update/validation/testing/history/publishing/execution, credentials discovery, project/tag discovery and Data Tables. Instance access is enabled; `mcp.autoExposeNewWorkflows=false`. Only `AIExecution01` and `NextcloudTools01` are explicitly exposed as durable execution tools. The event intake and previously accepted infrastructure workflows retain their existing exposure settings.

The native n8n API-key UI supports one MCP key per user; regenerating it replaces that user's key. All three clients therefore share the existing owner's MCP bearer. Native OAuth advertises the public editor registration/token URLs behind the accepted Authelia ingress; independent loopback OAuth would require changing that ingress contract. No new user, proxy, auth bypass or public MCP route was introduced. This is the confirmed native authentication contract, not a new restriction on future capabilities.

GitHub uses precisely `repos,issues,pull_requests,actions` and individual `get_me`, 44 tools at acceptance (official server v1.13.0). The launcher resolves the existing gh token in memory and passes it through environment, without copying it to client definitions. Docker `--rm` and exact `--cidfile` cleanup bind the container to the requesting stdio client, including client termination under sudo. There is no separate GitHub daemon or update target. Install the canonical launcher as root755 at `/usr/local/bin/edge-github-mcp`.

Playwright v0.0.83 uses existing Chromium153 at `/home/core/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`. Native `--isolated` avoids persisted profiles; `--no-sandbox` is required by the observed host Chromium sandbox launch failure. The MCP process/browser belongs to the invoking client. Existing Hermes browser tooling remains available.

## AIExecution01

Native workflow ID: `wQ9ZqMisMCGadGEE`. Export: `n8n/AIExecution01.json`.

Inputs: required explicit `backend` (`vllm`, `codex`, `antigravity`, `hermes`) and `task`; optional absolute existing `cwd` (default project directory), `timeout`1–3600 seconds (default300), `output_mode` (`text` or `json`), JSON `schema`, CLI `model`/`effort`/`permission_mode`, vLLM `model`/`max_tokens`, `request_id`. `action=cancel` plus `request_id` addresses a running CLI request. There is no automatic selection, quota inference or fallback. Existing payload forwarding accepts the new optional permission field without workflow modification; omitted mode retains the accepted n8n full-access behavior. Hermes's separate native command path always supplies a mode, defaulting to read-only.

MCP callers first read workflow details, then call native `execute_workflow` with `executionMode=production`, `triggerNodeName="Tool Input"`, and `inputs.webhookData={method:"POST",body:{...}}`. Native subworkflow callers use `Subworkflow Input`. The direct HTTP webhook requires the encrypted `Edge foundation tool ingress` header credential; it introduces no nginx/public ingress exemption.

- vLLM calls the existing private `192.168.1.30:8000/v1/chat/completions` directly, current served model `qwen3.8-27b-fp8`. Native JSON-schema output was tested against the real model. HTTP timeout, non-2xx/model/context errors, token-limit termination and invalid JSON produce explicit failure results.
- Hermes calls the existing authenticated private `172.19.0.1:8642/v1/responses`, using its configured agent/model. JSON mode supplies a schema prompt and parses the result; it is not a claim of native constrained decoding. The accepted `Hermes4FMachine01` definition/credential remain unchanged and were retested.
- Codex/Antigravity use native encrypted SSH credential `OsTkP0IAXod5QjbI`. Dedicated public-key comment is `n8n-core-edge-ai-execution`; there is no extra Linux user. Install `edge-ai-exec` as root755 at `/usr/local/bin/edge-ai-exec`.
- The SSH command carries base64 JSON; the helper constructs argument arrays without a shell and fixes core HOME. Codex uses `exec`, a mode-selected sandbox, `approval_policy="never"`, `--ephemeral --json`, stdin task, native final-message file and optional output schema. Antigravity uses `-p`, native JSON/schema, explicit native mode/sandbox semantics and a native print timeout longer than the authoritative host deadline. Omitted-mode n8n calls retain full access; Hermes command defaults and explicit write/full-access modes are documented in the specialist contract. RC0 requires a nonempty Codex final message or AGY native SUCCESS without denied_actions; partial/denied output is a failure. Model/effort are supplied only when requested.
- Two native flock slots bound concurrent CLI execution. A full pool returns `busy`/75; no extra queue exists. Timeout/cancellation terminate the process group, escalating after5s, and return status, real process exit code and bounded stderr (16KiB). Structured Antigravity results use native `structured_output`.
- `/home/core/.local/state/edge-ai-exec` contains current coordination slot locks and running request records only. Request records and protected `/tmp/edge-ai-*` payload/result files are removed on completion, timeout and cancellation. HTTP timeout bounds the HTTP request; the cancellation command is specifically for CLI process groups.

## Nextcloud foundation

Native Nextcloud35.0.1 operator UID is `f74f359708f72bd3011f605925e1a176a495a48c67f1ee7ddaec6a602ea14425`; no separate Nextcloud user was created. Encrypted n8n `nextCloudApi` credential `6MEdI2Cs7tEUiM7o` owns the native app password and WebDAV base `http://nextcloud.edge.internal/remote.php/webdav`.

Both Nextcloud app and cron join existing `edge_internal`; app alias is `nextcloud.edge.internal`. `trusted_domains[2]` accepts it and native `allow_local_remote_servers=true` permits native webhook delivery to the accepted private n8n endpoint. Public host/HTTPS/OIDC and the existing Nextcloud→Mattermost public path remain unchanged. Installed Compose is `/opt/nextcloud/compose.yaml`; canonical source is `../nextcloud/compose.yaml`.

`NextcloudTools01` (`G0WysKToqsel8yL2`) supports `list`, `find`, `metadata`, `upload`, `download`, `mkdir`, `move`, `copy`, `share`, `revoke_share`, `delete` through the same exposed MCP workflow in all three clients. Inputs include `path` relative to the operator files (default `/`), `query`, `content` or `content_base64` plus `mime_type`, `to_path`, and `share_id` as appropriate. Paths are normalized/encoded and reject traversal/query/fragment. Results contain `ok`, operation/path and result/error; downloads include base64, text, size and MIME; metadata uses native XML→JSON parsing.

Native Nextcloud nodes implement list/find/download/share. The exact installed node's write utility throws on successful empty WebDAV response bodies; writes therefore use the supported native HTTP Request node with the same encrypted `nextCloudApi` credential. WebDAV implements MKCOL/PUT/COPY/MOVE/DELETE/PROPFIND; native OCS handles share revocation. No custom application or source patch was introduced. Delete follows the normal Nextcloud trash lifecycle.

Bundled enabled `webhook_listeners`2.0.0-dev.0 has four native registrations (IDs1–4), for `OCP\\Files\\Events\\Node\\NodeCreatedEvent`, `NodeWrittenEvent`, `NodeDeletedEvent`, `NodeRenamedEvent`. Authenticated destination is `http://n8n.edge.internal:5678/webhook/nextcloud-events`, native header auth matched to encrypted n8n credential `dju3iGLC4SWK191K`. Registration user filter is empty: the installed app resolves configured events before DAV user-session authentication, so an operator filter suppresses DAV events. This source/runtime behavior was verified before selecting the native unfiltered four-event mechanism.

Native background jobs deliver through the existing cron. `NextcloudEventIngress01` (`bxsXXufaaXuubA3Z`) validates the four classes and inserts into native `NextcloudEventInbox01` (`pZDk2S89xgYGSXEO`) before returning204. Columns are event_class/path/user_id/payload. The durable inbox supports future workflows; this foundation creates no notification/business consumer. Wrong/missing webhook auth returns403 before dispatch.

## Monitoring, recovery and lifecycle

Deletion reconciliation pagination preserves the original native activity URL and appends the server's next cursor from `$request.url`. It no longer depends on paired-item linkage after pagination. The canonical Plane export contains the verified final definition.

Existing Edge Monitor reads native SQLite workflow state and scheduled execution history. One generic `n8n-workflow-health` Integration/EDGE incident reports all three critical workflows, suppresses itself when n8n HTTP is unavailable, ignores manual executions and recovers through the existing incident model. Three consecutive terminal failures or absence of a scheduled success for three cadences plus execution timeout trigger health degradation. Current stale thresholds: Mattermost115s, deletion1020s, GitHub3000s. Inactive/archived/missing workflows or schedule drift fail the declared contract.

Existing Backrest `edge-state` captures protected client configs/context, SSH authorized_keys, both helpers and Compose/system config; its native consistent staging captures n8n SQLite/config/encrypted credentials and logical Plane/Nextcloud PostgreSQL data. No second backup mechanism exists. Restore the matching snapshot and staging through the established service recovery procedure; raw live SQLite and shared physical PostgreSQL are not substituted for those staged copies.

Temporary test workflows/Data Tables, Plane entities/posts, Nextcloud test files/shares/trash, n8n test executions, stored test Hermes responses, browser profiles and temporary auth/payload/source files are removed precisely. Native token use/audit/JWT blacklist history stays. Backrest's `oplog.sqlite-*.backup` is its upstream-managed database-backup lifecycle (keep3, weekly/schema-aware); it is retained for that concrete native role. An unreferenced old manual `config.json.bak` was removed.

## Authoritative mechanism references

- [n8n instance MCP](https://docs.n8n.io/connect/connect-to-n8n-mcp-server/) and [native tool reference](https://docs.n8n.io/connect/connect-to-n8n-mcp-server/mcp-server-tools-reference/)
- [Plane MCP](https://developers.plane.so/dev-tools/mcp-server)
- [Official GitHub MCP](https://github.com/github/github-mcp-server), [Docker cidfile lifecycle](https://docs.docker.com/reference/cli/docker/container/run/)
- [Official Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp), [Codex noninteractive execution](https://developers.openai.com/codex/noninteractive)
- [Antigravity CLI reference](https://antigravity.google/docs/cli/reference/), [native context/config paths](https://antigravity.google/docs/cli/gcli-migration/)
- [Nextcloud native webhook listeners](https://docs.nextcloud.com/server/stable/admin_manual/webhook_listeners/index.html), [n8n Nextcloud node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.nextcloud/)
- [Backrest1.14.1 native backup RPC](https://github.com/garethgeorge/backrest/blob/v1.14.1/internal/api/backresthandler.go), [native oplog backup lifecycle](https://github.com/garethgeorge/backrest/blob/v1.14.1/internal/oplog/sqlitestore/sqlitestore.go)

Exact installed sources, native validators, real transport calls and fresh runtime evidence supplement these upstream contracts; acceptance does not rely on community-only claims.
