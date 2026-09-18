# Stage 4B — Direct Codex and Antigravity Executor Integration — Final Acceptance

Date: 2026-09-18

Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS`

## Accepted architecture

- Hermes remains the main orchestrator on the accepted local `qwen3.8-27b-fp8` / vLLM route.
- Codex CLI and Antigravity CLI remain direct specialist executors invoked through Hermes terminal.
- CloudCLI is not used as an executor proxy.
- Codex app-server is not used as the main Hermes runtime.
- The trusted single-operator executor contract is in force: no blanket sandbox/container/workspace-only/network restriction is imposed merely for defense in depth.
- Critical high-impact mutations are gated by Hermes/orchestration instructions and explicit operator approval when not already authorized in the current instruction.

## Read-only audit acceptance

`STAGE4B_EXECUTOR_READONLY_AUDIT=PASS`

Confirmed runtime:

- Hermes `0.21.3 (2026.9.14)`, exact commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, clean worktree;
- Codex CLI `0.154.0`;
- Antigravity CLI `1.2.5`;
- Hermes terminal backend `local`;
- effective terminal child cwd `/home/core`;
- child `HOME=/home/core`, `HERMES_HOME=/home/core/.hermes`;
- `/home/core/.local/bin` available to terminal children;
- no `OPENAI_BASE_URL`, `OPENAI_API_KEY` or `CODEX_*` provider override contaminating executor child environment;
- standalone Codex OAuth state reused;
- standalone Antigravity auth/state reused;
- official Antigravity Hermes skill installed;
- audited Hermes/Codex/Antigravity config/auth/settings hashes unchanged.

## Codex E2E acceptance

Final accepted marker:

`STAGE4B_CODEX_E2E=PASS`

Accepted evidence:

- Hermes/Qwen invoked the real standalone Codex CLI through terminal;
- actual command path: foreground non-PTY `codex exec`;
- invocation used `--sandbox danger-full-access --ephemeral`;
- Codex exited `0`;
- Codex read a random repository fact that was not disclosed to the Hermes prompt;
- Codex returned the correct fact;
- Hermes received and reasoned from the real Codex result;
- temporary test artifacts were removed;
- post-abort recovery proved no lingering test processes;
- main Hermes config SHA remained `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`;
- `hermes-gateway.service` remained active with `NRestarts=0`.

The earlier receipt wrapper failure was an acceptance-harness defect, not a Codex integration failure: Hermes terminal PATH resolution selected the real `/home/core/.local/bin/codex` ahead of the temporary wrapper, so the wrapper receipt could never be generated. The real Codex invocation itself had already completed successfully and returned the correct random repository fact.

## Antigravity E2E acceptance

Final accepted markers:

- `STAGE4B_ANTIGRAVITY_E2E=PASS`
- `HERMES_TO_ANTIGRAVITY_FOREGROUND_NON_PTY_E2E=PASS`

Accepted evidence:

- exactly one real Antigravity terminal invocation;
- foreground execution;
- non-PTY execution;
- command used native headless `agy -p`;
- structured `--output-format json`;
- `--mode accept-edits`;
- `--dangerously-skip-permissions`;
- no Antigravity sandbox flag;
- Antigravity returned `status=SUCCESS`;
- terminal exit code `0`;
- Antigravity read a random 40-character fact that was not disclosed to the Hermes prompt;
- structured response contained exactly the expected fact;
- Hermes final result matched the executor result exactly;
- test input remained unchanged;
- temporary workspace was not converted into a Git repository;
- main Hermes config SHA remained unchanged;
- gateway remained active with `NRestarts=0`;
- temporary artifacts were removed.

Observed structured Antigravity result contained:

- `conversation_id`;
- `status`;
- `response`;
- `duration_seconds`;
- `num_turns`;
- `usage`.

## Default executor invocation contract

### Codex

Default bounded one-shot:

`Hermes/Qwen -> terminal -> foreground non-PTY codex exec -> Codex result -> Hermes`

Use background process management only for genuinely long-running or parallel Codex jobs. Use PTY only for genuinely interactive Codex TUI sessions.

For trusted autonomous mutation tasks, the accepted direction is full executor access after operator/orchestration approval; do not introduce a second generic sandbox barrier merely for defense in depth.

### Antigravity

Default bounded one-shot:

`Hermes/Qwen -> terminal -> foreground non-PTY agy -p --output-format json -> Antigravity result -> Hermes`

Use background process management only for genuinely long-running or parallel jobs. Use PTY only for genuinely interactive Antigravity sessions.

## Known non-blocking Hermes machine-output defect

During both Codex/Antigravity structured observation, Hermes `--format stream-json` emitted one non-JSON diagnostic line to stdout:

`tirith security scanner enabled but not available — command scanning will use pattern matching only`

This violates the otherwise machine-readable JSONL expectation and is carried forward as a Stage 4F machine-interface constraint. It does **not** invalidate the direct executor E2E evidence and does not block Stage 4B acceptance.

## Non-regression

- `STAGE4A_CORE_QWEN_VLLM_REGRESSION=PASS` reused without rerun;
- main Hermes provider remains the accepted custom Qwen3.8/vLLM path;
- Hermes config SHA unchanged;
- gateway active;
- gateway `NRestarts=0`;
- no executor auth/config normalization was required;
- no production service restart was required;
- temporary test artifacts cleaned.

## Final acceptance

`STAGE4B_DIRECT_EXECUTOR_INTEGRATION=PASS`

Stage 4B is **COMPLETE / ACCEPTED**.

Next Stage 4 substage on the critical path: **Stage 4C — Hermes Web Dashboard, ingress and auth**.
