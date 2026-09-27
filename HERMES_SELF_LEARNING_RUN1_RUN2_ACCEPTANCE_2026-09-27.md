# Hermes Self-Learning Run 1 → Run 2 Acceptance — 2026-09-27

## Status

**ACCEPTED**

Acceptance marker:

`HERMES_SELF_LEARNING_CROSS_SESSION_PROCEDURAL_REUSE=PASS`

## Scope

Controlled Hermes Desktop experiment against the edge node using the local Qwen runtime only. The objective was to determine whether Hermes can persist a reusable operational procedure in one session and automatically reuse it in a fresh independent Desktop session.

This acceptance covers the Run 1 → Run 2 cross-session learning result only. It does not claim that the separate Desktop `/refine` command path is working.

## Accepted evidence

### Run 1

- Desktop project workspace: `/home/core/projects/hermes-self-learning`.
- Main model/provider: `qwen3.8-27b-fp8` via `custom:ai-node-vllm`.
- Hermes created persistent skill `ops/edge-cli-ops-audit`.
- Hermes created one persistent memory entry.
- No verified Codex/Antigravity delegation or external LLM execution occurred.
- Run 1 was exploratory and required substantially more iterative probing/reasoning than the later repeat.

### Run 2

Fresh independent Desktop session:

- session id: `20260927_123427_403ed1`;
- model: `qwen3.8-27b-fp8`;
- provider: `custom`;
- workspace: `/home/core/projects/hermes-self-learning`;
- all recorded model usage remained on `http://192.168.1.30:8000/v1`;
- main audit used 4 primary Qwen API calls plus 1 title-generation call;
- real message trace recorded 9 tool calls:
  - 1 × `skill_view`;
  - 7 × read-only `terminal` probes;
  - 1 × `skill_manage`;
- the prompt did not name `edge-cli-ops-audit`, but Hermes automatically selected it;
- delegation tool calls: 0;
- external Codex/Antigravity executor use: 0;
- project workspace remained unmodified.

## Persistent learning result

The saved procedural skill survived the session boundary and was automatically reused in Run 2.

Skill SHA changed during Run 2:

- pre-Run-2: `4b6307573169fc3e45253818104f4610a2c4afb8b2b8823d8fd5612660a81ebf`;
- post-Run-2: `43fcbda520d710a31372e012da9b03c65bffb4cd87cfb16b5ae25bbb008b4a28`.

Persistent memory SHA remained unchanged:

`b93417c71385678c4bb59ea63f3bcdb827f83fe702e02a3c1c637b97124a3247`.

Hermes Journey reported `edge-cli-ops-audit` with reuse count `x2`.

## Quality result

Known Run-1 skill defects that were no longer present after Run 2:

- `hrmes-agent` typo;
- `placeholder - use show below`;
- invalid `systemd-run --user -p -- show` placeholder.

One cosmetic defect remained: duplicated top-level H1 heading.

Therefore skill self-correction is accepted as **partial**, not complete.

## Acceptance matrix

| Gate | Result |
| --- | --- |
| Cross-session skill persistence | PASS |
| Automatic skill discovery | PASS |
| Procedural reuse | PASS |
| Local Qwen-only model routing | PASS |
| Delegation absence | PASS |
| External executor absence | PASS |
| Procedural efficiency improvement | PASS |
| Skill self-update | PASS |
| Known skill-error correction | PARTIAL |
| Persistent memory survival | PASS |
| Persistent memory causal reuse | UNVERIFIED |
| Project workspace non-mutation | PASS |

## Non-blocking limitation

Desktop/gateway `/refine` currently returned `Nothing to refine yet — send a message first.` because that slash-command path requires a cached live agent. This was investigated separately and is not a blocker for the accepted foreground cross-session procedural-learning result.

## Next experiment

Proceed with a **held-out transfer/generalization test** rather than a third repetition of the same audit.

The next test should present a related but non-identical operational task so Hermes must adapt learned audit methodology rather than merely replay the saved A–E procedure. After that, perform a separate Desktop detach/reconnect survival test.
