# Hermes Self-Learning Isolation Acceptance — 2026-09-27

## Status

**ACCEPTED**

Acceptance marker:

`HERMES_SELF_LEARNING_ISOLATION=PASS`

## Objective

Establish a disposable Hermes self-learning environment that can be used to improve production Hermes without polluting the default profile during experimentation.

## Accepted architecture

### Production profile

`/home/core/.hermes`

Production/default Hermes remains the long-term knowledge target. Experiment runs must not write disposable learning artifacts into this profile.

### Disposable learning profile

`/home/core/.hermes/profiles/selflearning`

Owns experiment-scoped Hermes state that is inherently profile-scoped, including session history, model usage, built-in memory, curator/runtime bookkeeping and profile configuration.

### Disposable project

`/home/core/projects/hermes-self-learning`

This is a Git project and trusted Hermes project root. It owns experiment-visible artifacts:

- `.hermes/skills/` — project-local experimental skills;
- `baselines/` — experiment baselines;
- `results/` — experiment results;
- `notes/` — experiment notes;
- `AGENTS.md` — experiment persistence and promotion rules.

The profile setting `skills.create_dir` points to:

`/home/core/projects/hermes-self-learning/.hermes/skills`

Project-local skills take precedence inside the project.

## Desktop routing acceptance

A fresh Hermes Desktop session was created through the remote gateway using profile `selflearning` and project `/home/core/projects/hermes-self-learning`.

Confirmed:

- exactly one new Desktop session was created in the `selflearning` profile;
- no new default-profile session was created;
- model remained `qwen3.8-27b-fp8`;
- provider remained `custom`;
- all recorded model usage remained on the local ai-node vLLM endpoint;
- no delegation was used.

## Storage isolation acceptance

Controlled marker: `SELFLEARNING_PROFILE_ISOLATION_V1`.

Verified destinations:

- built-in memory marker:
  `/home/core/.hermes/profiles/selflearning/memories/MEMORY.md`
- disposable project-local skill:
  `/home/core/projects/hermes-self-learning/.hermes/skills/experiment-storage-isolation-probe/SKILL.md`
- project result artifact:
  `/home/core/projects/hermes-self-learning/results/profile-routing-probe.md`

Verified absence:

- marker absent from production `/home/core/.hermes/memories/MEMORY.md`;
- disposable probe skill absent from production `/home/core/.hermes/skills`;
- disposable probe skill absent from the `selflearning` profile-local skills directory;
- production `edge-cli-ops-audit` remained byte-identical during the isolation test;
- project-local `edge-cli-ops-audit` also remained byte-identical.

## Ownership recovery

The disposable project was initially created partly as root. This caused a project-local `skill_manage create` write to fail until `.hermes/skills` ownership was corrected.

Final accepted ownership:

- `/home/core/projects/hermes-self-learning/.hermes` → `core:core`
- `/home/core/projects/hermes-self-learning/.hermes/skills` → `core:core`
- `/home/core/projects/hermes-self-learning/.hermes/skills/ops` → `core:core`
- all paths under project-local skills → `core:core`
- writeability as `core` → PASS

## Learning lifecycle

The accepted workflow for the remainder of this workstream is:

`sandbox → learn → evaluate → distill → promote → production-verify → cleanup`

Experiment-specific knowledge remains disposable. Only durable, production-useful procedures and facts are promoted to the default Hermes profile after final curation.

## Outstanding cleanup

The early Run 1 / Run 2 / transfer tests were executed before isolation and left experiment artifacts in the default profile. These have not yet been deleted.

The next task is a dedicated default-profile experiment-artifact cleanup:

1. audit the exact cleanup set;
2. preserve any still-needed evidence in the disposable project;
3. remove only experiment-specific default-profile artifacts;
4. verify production Hermes remains healthy and the disposable training environment remains intact.
