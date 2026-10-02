# Edge Hermes explicit executor reconciliation — 2026-10-02

Status: **COMPLETE / ACCEPTED**. Bounded reconciliation of operator-selected Hermes specialists, against accepted foundation `b65ffdbc4551fdb1dcd815a5c11a11fa737231b0`. This does not reopen the interaction/AI fabric or Stage0–13. Canonical deployment contract: `deployments/edge/interaction-fabric/hermes-executors/README.md`; sanitized real observations: `acceptance-evidence.json` in that directory.

## Pre-change facts and upstream reconciliation

Fresh installed Hermes is `v0.21.5+5635.g5bba024 (2026.9.24)`, source `5bba024d8ddd388f56f354c1f789be825e3d8a3c`; Codex0.160.0 and AGY1.2.14 are independently authenticated standalone CLIs. Hermes default is `custom:ai-node-vllm`, `qwen3.8-27b-fp8`, private `http://192.168.1.30:8000/v1`. No product update was issued here. Official Codex release API reports0.160.0 as latest stable (published2026-10-01T20:19:13Z); a stale web release listing is not a reason to downgrade. Hermes's native managed rolling source/update ownership is retained.

Installed and bundled Codex guidance incorrectly required PTY, treated a Git repository as mandatory despite current `--skip-git-repo-check`, recommended full access as an automatic sandbox workaround, and encouraged autonomously chosen batches/reviews/fan-out. No installed/custom AGY skill existed. The existing shared helper unconditionally selected full access, did not distinguish AGY native RC0 WAITING/denials from success, and used a native AGY deadline that can return partial output. These are confirmed instruction/helper defects; service MCP/auth/ingress are not defects.

Current upstream and installed source provide a supported general user-plugin command API, `PluginContext.register_command`. CLI, Gateway and Desktop/TUI dispatch these commands before model-facing same-name skills. The Dashboard's terminal chat launches native CLI. `/skill` injects guidance into a model turn and is not deterministic dispatch. `/v1/responses` remains an inference endpoint, not a slash-command endpoint. No specialist model-provider plugin is needed.

Supported local modified skills are preserved by native bundled sync. Native subprocess environment sanitization prevents Hermes Python/runtime variables and secrets from leaking into standalone children. Exact current help and actual source supplied flag/schema/completion semantics; upstream Codex supports non-PTY exec, stdin, JSON/schema, cwd/sandbox, final-message files and standalone ChatGPT auth. AGY supports headless JSON/schema and standalone Google auth, with native SUCCESS/denied-actions handling and a print timeout that can yield partial output. Its plan/sandbox does not offer Codex-equivalent filesystem immutability.

Authoritative sources: [Hermes plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/), [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/), [Codex noninteractive](https://developers.openai.com/codex/noninteractive/), [Codex0.160.0 release](https://github.com/openai/codex/releases/tag/rust-v0.160.0), [AGY headless](https://antigravity.google/docs/cli/headless/), [AGY modes](https://antigravity.google/docs/cli/modes/), [AGY sandbox](https://antigravity.google/docs/sandbox/). Exact installed Hermes source files and CLI help references are enumerated in the deployment contract. No architecture choice rests on an isolated community report.

`Hermes4FMachine01`: active, unchanged dormant compatibility interface. All nine durable workflow definitions, retained legacy execution history (zero rows) and scoped active host references were audited; no current caller/dependency was found. Its old specialist branches still prompt Hermes to invoke a CLI and are not the new contract. No deletion or speculative compatibility mapping was performed; absence of retained rows does not prove historical non-use.

## Accepted design and changes

Before mutation the target and recovery coverage were established, with `TARGET_ARCHITECTURE_MATCH=PASS`: default Qwen remains; explicit native command fixes Codex or AGY; one existing helper launches that standalone CLI; no model selection, fallback, reviewer, inter-executor dependency or new daemon/provider/fabric.

Hermes uses vLLM/Qwen as its default model. Codex and Antigravity are independent specialist executors selected explicitly by the operator. Hermes does not autonomously route, fall back, fan out, cross-review, or substitute one executor for another.

n8n retains the accepted explicit AIExecution01 backend fabric. This workstream does not introduce a second routing layer.

Changed runtime artifacts:

- `/usr/local/bin/edge-ai-exec`: optional explicit permission modes, correct core HOME, reliable native final-output/SUCCESS/denial checks, host deadline preceding AGY partial-output timeout, process metadata. Argument arrays, two-slot concurrency, cancellation identity, bounded stderr and exact cleanup remain. Omitted permission mode retains accepted n8n full access; Hermes always supplies read-only unless the operator explicitly selects write/full access.
- `/home/core/.hermes/plugins/edge-explicit-executors/{plugin.yaml,__init__.py}`: two synchronous native commands `/codex` and `/antigravity`, fixed backend before parsing, direct helper subprocess with native sanitized environment. No tools, hooks, provider registration or source patch.
- `/home/core/.hermes/config.yaml`: only `agent.system_prompt` and plugin enablement change. Existing Plane context is preserved; model/providers/MCP/terminal/delegation/auth and other configuration stay unchanged. Guidance forbids model-generated terminal/MCP/delegate_task specialist launching and explains the command boundary.
- Installed local `codex/SKILL.md` replaced; local `antigravity/SKILL.md` added under `/home/core/.hermes/skills/autonomous-ai-agents/`. Native modified-skill detection identifies Codex; managed source remains clean.
- Native Gateway hotreload rewired two adapters without restart. Dashboard native session-token activation returned401 under its existing OIDC boundary; one Dashboard service restart loaded current runtime. Unit/auth configuration remained unchanged. Dashboard active/expected401 and public OIDC login reachability were read back; Gateway running and Mattermost connected.
- Git versions the helper, plugin, both skills, nonsecret config merge fragment, deployment README, meaningful offline contract tests and sanitized evidence. Current State/Architecture/Decisions/Implementation Phases and parent deployment README record the bounded supersession. Historical acceptance files remain untouched.

## Final contract

| Caller | Operator selection | Effective backend/path |
|---|---|---|
| Hermes | none/default | Hermes → existing private vLLM/Qwen |
| Hermes | `/codex` | Native command → helper → standalone `codex exec` |
| Hermes | `/antigravity` | Native command → helper → standalone `agy -p` |
| n8n | `backend=vllm` | Existing direct private vLLM |
| n8n | `backend=codex` | Existing SSH/helper → standalone Codex |
| n8n | `backend=antigravity` | Existing SSH/helper → standalone AGY |
| n8n | `backend=hermes` | Existing authenticated Hermes inference API |

Native specialist commands make **zero Hermes inference requests**: the installed dispatcher invokes a plain command callback and returns the CLI output. This claim applies to that command path only. There is no control-model task answering, routing or review. CLI/MCP capabilities inside each independently selected specialist remain its own accepted tool work.

Codex defaults to read-only; `workspace-write` or `full-access` requires explicit JSON input. AGY defaults to native plan+sandbox without blanket bypass; its native sandbox can allow workspace writes, so plan is not advertised as immutable read-only. AGY full access is explicit; unsupported workspace-write is rejected. Plain task input uses current project cwd/HOME and300s; absolute existing cwd,1–3600s timeout, model/effort/schema and request ID cancellation are supported. No enterprise approval mechanism is added.

## Real bounded verification

| Gate | Observed evidence | Result |
|---|---|---|
| Default | Real private response marker `HERMES_DEFAULT_QWEN_20261002`; native session `7e01c1de-441a-49e8-a2de-d4efb4850b34` records Qwen, custom billing URL192.168.1.30,1 API call,0 tools; no new Codex/AGY PIDs | PASS |
| Codex explicit | Installed native Desktop/TUI `command.dispatch`; standalone0.160.0 PID2571729, correct fixture cwd/HOME, non-PTY, read-only, RC0, structured file-read marker; only Codex observed, inference0 | PASS |
| AGY explicit | Same native dispatcher; standalone1.2.14 PID2572403, correct cwd/HOME, non-PTY, plan+sandbox, RC0 plus native SUCCESS and structured file-read marker; only AGY observed, inference0 | PASS |
| Native CLI | Real interactive Hermes `/codex` command, PID2581934, result `HERMES_NATIVE_CODEX_COMMAND_20261002`, project cwd, read-only, inference0; native CLI exits cleanly | PASS |
| Codex failure/timeout | Unknown model RC1/error6.029s; host deadline1s gives RC-15/timeout1.132s; no AGY or fallback | PASS |
| AGY failure/timeout | Unknown model RC1/native ERROR4.527s; host deadline1s gives RC-15/timeout1.108s; no Codex or fallback | PASS |
| Boundary properties | Offline tests reject native RC0 WAITING/denials, verify explicit Codex sandbox mapping and retained n8n omitted-mode behavior; one process and cleaned request record | PASS |
| Native validation | Plugin doctor `--ci`; native config check; modified-skill detection; current source clean; runtime/canonical helper/plugin/skill bytes equal | PASS |
| MCP non-regression | Real Plane project read (raw30 advertised, CE13 filter unchanged), n8n workflow read35tools, GitHub get_me44, isolated Playwright navigate/close25, Codex-only OpenAI Docs5 | PASS |
| n8n | AIExecution01 active and exact definition hash unchanged; no reason to rerun all four costly accepted backends | PASS |
| Runtime | Gateway and Dashboard active, Mattermost connected, protected env/Codex MCP/AGY MCP byte-unchanged; default/model/providers unchanged; monitor Edge/overall/applications OK | PASS |

AIExecution01 hash: `f63f0e5c8d6a667518694932e87b02cf1f5edf074eef0c3fb1237abeacb633e6`, SHA256 of compact JSON serialization of the three raw SQLite `nodes`, `connections`, `settings` strings. A final verifier initially used spaced JSON and failed its comparison; repeating only that failed comparison with the original serialization proved equality. Managed-Python bootstrap/import and native CLI input-driver defects encountered during test preparation were also verifier defects, corrected without altering production to accommodate them. Already-passed gates were preserved. AGY/Codex runtime failure tests are intentional failures, not production regressions.

No Mattermost message, authenticated browser session or macOS Desktop UI roundtrip was sent/created for specialist testing; installed native dispatcher/source, CLI process evidence and existing surface/service health establish this bounded acceptance. SDK server-version metadata is not relabeled as an installed product/package version.

## Recovery, cleanup and limitations

Fresh Backrest edge-state paths/exclusions confirm coverage of protected `.hermes` config/env/skills/plugins and `/usr/local/bin/edge-ai-exec`; current local schedule `0 1,7,13,19 * * *`. Prior accepted matched snapshot recovery plus all new nonsecret Git artifacts and a merge-only fragment recover this change. No new secret/store/schema requires a separate snapshot; no manual Backrest flow was issued.

The exact task fixture/verifier directory `/tmp/hermes-executors.c0pfQ4E5`, its AGY last-conversation cache pointer and repository test bytecode were removed. No request records or specialist test processes remain. Native conversation/auth history, active plugin runtime cache and current coordination locks retain concrete lifecycle roles. No stale container/image/network removal is inferred from a normal active stdio client.

Real native limitations: AGY plan is not a filesystem-immutable policy; `/v1/responses` does not execute native commands; `/skill` alone remains model-facing guidance; legacy dormant prompt branches remain available as retained compatibility state. The trusted core identity and accepted service MCP tools are retained, not replaced with an OS isolation/approval layer. The new plugin has no automatic inter-executor orchestration; it is not a claim that a trusted operator or arbitrary CLI code cannot manually execute another program.

Final coherent commit goes directly to `main`, followed by push, remote commit/critical-file byte readback and a clean worktree. Git itself records the resulting SHA without embedding a circular self-hash in this acceptance file.

```text
TARGET_ARCHITECTURE_MATCH=PASS
HERMES_DEFAULT_VLLM=PASS
HERMES_EXPLICIT_CODEX=PASS
HERMES_EXPLICIT_ANTIGRAVITY=PASS
HERMES_EXECUTOR_SKILLS_CURRENT=PASS
HERMES_AUTOMATIC_ROUTING=ABSENT
HERMES_AUTOMATIC_FALLBACK=ABSENT
HERMES_CROSS_MODEL_REVIEW=ABSENT
HERMES_INTER_EXECUTOR_DEPENDENCY=ABSENT
N8N_AI_EXECUTION_FABRIC_NON_REGRESSION=PASS
EDGE_MCP_TOOL_FABRIC_NON_REGRESSION=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
EDGE_HERMES_EXPLICIT_EXECUTOR_RECONCILIATION=PASS
```
