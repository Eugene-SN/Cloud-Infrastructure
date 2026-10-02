# Explicit Hermes specialist execution

Accepted record: `EDGE_HERMES_EXPLICIT_EXECUTOR_RECONCILIATION_ACCEPTANCE_2026-10-02.md` at the repository root. This directory is the canonical deployment/recovery contract for the bounded Hermes reconciliation; the parent interaction fabric remains accepted.

Hermes uses vLLM/Qwen as its default model. Codex and Antigravity are independent specialist executors selected explicitly by the operator. Hermes does not autonomously route, fall back, fan out, cross-review, or substitute one executor for another.

n8n retains the accepted explicit AIExecution01 backend fabric. This workstream does not introduce a second routing layer.

## Operator contract

Ordinary input, without specialist selection, uses Hermes's existing `custom:ai-node-vllm` / `qwen3.8-27b-fp8`. Select a specialist with a native slash command:

```text
/codex Inspect the current repository and report findings without changing files.
/antigravity Inspect the current repository and report findings without changing files.
```

The command name fixes the backend before parsing the task. Plain task input uses `/home/core/projects/cloud-infrastructure`, HOME `/home/core`, timeout300s and `permission_mode=read-only`. For Codex this is its filesystem read-only sandbox. For AGY it is native `--mode plan --sandbox`, with no blanket permission bypass; **AGY plan is not an immutable filesystem policy**. Native AGY sandbox permits workspace writes and plan mode is read-oriented agent guidance. This contract does not claim the two permission mechanisms are equivalent.

Authorized implementation uses an explicit JSON mode and existing absolute cwd:

```text
/codex {"task":"Implement the explicitly authorized change","cwd":"/absolute/project","permission_mode":"workspace-write","timeout":600}
/antigravity {"task":"Implement the explicitly authorized change","cwd":"/absolute/project","permission_mode":"full-access","timeout":600}
```

Codex supports `read-only`, `workspace-write`, and explicit `full-access` (native `danger-full-access`). AGY supports read-oriented `plan` or explicitly selected full-access (`accept-edits` plus `--dangerously-skip-permissions`); `workspace-write` is rejected because it has no Codex-equivalent native policy. There is no automatic escalation after a sandbox/permission failure.

Optional JSON fields: `model`, `effort`, `output_mode` (`text` or `json`), `schema` (JSON object), `request_id`, `action`. Timeout is1–3600s. Provide a request ID before launch to cancel that job from another command/session, for example `/codex {"action":"cancel","request_id":"operator-job-01"}`. Cancellation uses the existing helper's PID/start-time identity check. The shared two-slot pool returns `busy` when full; it does not create a queue. CLI timeout and cancellation stop the selected process group.

Native CLI dispatch, Dashboard's native terminal chat, messaging Gateway dispatch, and Desktop/TUI `command.dispatch` resolve this command-only plugin before same-name skills. The handler returns the selected CLI result directly; it neither submits a model request nor asks Hermes to answer or review the task. Real native CLI and installed Desktop/TUI dispatcher tests are recorded in `acceptance-evidence.json`; Gateway command hotload and adapter rewiring were verified without sending a Mattermost message. Authenticated browser/Desktop user interaction was not newly tested in this workstream.

`/skill codex`, `/skill antigravity`, and natural-language skill loading are guidance, not deterministic execution. They explain the slash commands. The private `/v1/responses` endpoint remains an inference endpoint and does not implement slash-command dispatch. Do not send a specialist command through that endpoint and claim zero inference; n8n callers use the existing direct `AIExecution01` selector instead.

## Native mechanism and result

`edge-explicit-executors` is a native user plugin with two `PluginContext.register_command` callbacks, no tools, hooks, model providers, listener, daemon or source patch. The synchronous callbacks reuse `/usr/local/bin/edge-ai-exec` directly, without n8n/MCP transport. Native `build_subprocess_env` removes Hermes-owned Python/runtime environment and secrets from the child while retaining the standalone `core` CLI context. A fixed executable plus base64 JSON crosses this boundary; task input is not interpolated into shell code.

The helper runs native non-PTY `codex exec` with task stdin, `--json`, `--ephemeral`, `-C`, `--skip-git-repo-check`, final-message file and optional `--output-schema`. It runs native `agy -p` with task as an argument, JSON envelope and optional `--json-schema`. Existing independent ChatGPT/Google auth, service MCPs, web/repository tools and each specialist's own internal tool work remain intact.

Result fields include `ok`, `status`, backend, native exit code, duration, final result, bounded stderr, native envelope, child PID, cwd and HOME. The plugin adds `selected_by=operator`, `dispatch=native_plugin_command`, `hermes_inference_turns=0`. These fields describe this native command path, not arbitrary Hermes inference requests.

Codex RC0 requires a nonempty final-message file. AGY RC0 also requires native `status=SUCCESS` and no `denied_actions`; WAITING/partial/error/soft-denied output is not accepted as completion. AGY's native print deadline is longer than the authoritative host deadline, preventing its partial-output timeout from being mistaken for success. Errors/timeouts return unchanged, with no retry, alternate backend or reviewer.

**Existing n8n compatibility:** helper calls omitting `permission_mode` retain their accepted full-access behavior. Hermes always sends an explicit mode, defaulting to read-only. AIExecution01's existing payload forwarding accepts an explicitly supplied mode without any workflow modification; no n8n permission-policy redesign is implied.

`Hermes4FMachine01` remains active but dormant compatibility state: the bounded audit of all nine durable workflows, retained executions and active host references found no caller. Its historical prompt-mediated specialist branches remain unchanged and are not the new specialist contract. Use `AIExecution01` for explicit n8n backends and native commands for Hermes. The audit does not establish that the legacy interface was never used historically.

## Deployment, lifecycle and recovery

| Canonical artifact | Runtime destination / role |
|---|---|
| `../edge-ai-exec` | `/usr/local/bin/edge-ai-exec`, root:root755 |
| `plugin.yaml`, `__init__.py` | `/home/core/.hermes/plugins/edge-explicit-executors/`, core-owned directory700/files600 |
| `codex-SKILL.md` | `/home/core/.hermes/skills/autonomous-ai-agents/codex/SKILL.md`, core600 |
| `antigravity-SKILL.md` | `/home/core/.hermes/skills/autonomous-ai-agents/antigravity/SKILL.md`, core600 |
| `config-fragment.yaml` | Merge only its prompt and plugin enablement into protected `/home/core/.hermes/config.yaml`; preserve unrelated settings/plugins/secrets |
| `test_contract.py` | Offline result/permission compatibility properties; no live CLI or production state |
| `acceptance-evidence.json` | Sanitized observations from real bounded tests and final audit |

Use native `hermes plugins doctor` before enabling and native `hermes plugins enable edge-explicit-executors --no-allow-tool-override` for activation. No tool override is granted. Native Gateway hotreload rewired two adapters. The protected Dashboard's native session-token activation call returned401 under its accepted OIDC boundary, so this deployment restarted only `hermes-dashboard.service` once; auth and unit configuration were unchanged. Its terminal chat launches the native CLI. Gateway remains active without a restart, and reads the global system prompt from current configuration on each turn.

Hermes local modified skills are preserved by native bundled sync; `hermes skills list-modified --json` recognizes `codex`. The new AGY skill is a normal local custom skill. Plugin command precedence avoids falling back to model-facing same-name skills. Hermes's managed upstream checkout and updater ownership remain unchanged; all three products keep their native lifecycle.

Existing Backrest `edge-state` includes `/home/core` and `/usr/local`, with no exclusion of these protected configs/skills/plugins/helper. Its current local schedule is `0 1,7,13,19 * * *`. The prior accepted matched recovery snapshot supplies the protected base/auth; Git supplies every new nonsecret artifact and the merge fragment. Restore that established protected base, deploy the matching Git artifacts, merge the fragment without replacing unrelated configuration, and perform native validation/activation. No credentials are copied into Git, additional recovery tree is created, or manual Backrest flow issued by this reconciliation.

The exact temporary fixture, verifier scripts/results, repository test bytecode and AGY cache pointer to the fixture were removed. Normal native conversation/auth history, active runtime bytecode and the helper's current slot locks retain their upstream/runtime roles. There are no remaining running request records or specialist test processes.

## Authoritative sources checked

- [Hermes native plugin commands](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/), [skills and local ownership](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
- Exact installed Hermes source `5bba024d8ddd388f56f354c1f789be825e3d8a3c`: `cli.py`, `gateway/run_inbound.py`, `gateway/run_config_loaders.py`, `tui_gateway/methods_tools.py`, `hermes_cli/plugins_activation.py`, `hermes_cli/web_server.py`, `tools/skills_sync.py`, `tools/environments/local.py`
- [Codex noninteractive mode](https://developers.openai.com/codex/noninteractive/), [official0.160.0 release](https://github.com/openai/codex/releases/tag/rust-v0.160.0), exact installed `codex exec --help` and standalone login status
- [AGY headless execution](https://antigravity.google/docs/cli/headless/), [modes](https://antigravity.google/docs/cli/modes/), [sandbox](https://antigravity.google/docs/sandbox/), [CLI reference](https://antigravity.google/docs/cli/reference/), exact installed1.2.14 help and actual authenticated responses

Source/installed help wins where website metadata lags. No product update or new version restriction was introduced.
