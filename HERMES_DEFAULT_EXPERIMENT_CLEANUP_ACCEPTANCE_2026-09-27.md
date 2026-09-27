# Hermes Default-Profile Experiment Cleanup Acceptance — 2026-09-27

## Status

**ACCEPTED**

Acceptance marker:

`HERMES_DEFAULT_EXPERIMENT_CLEANUP=PASS`

## Objective

Remove the early Hermes self-learning experiment artifacts that were created in the production/default Hermes profile before storage isolation was introduced, while preserving useful evidence inside the disposable self-learning project.

## Preserved evidence

Preservation root:

`/home/core/projects/hermes-self-learning/results/default-profile-cleanup`

Preserved before deletion:

- exported Run 1 session;
- exported Run 2 session;
- exported T3 transfer session;
- default-profile memory candidate;
- 13 `edge-cli-ops-audit` curator ledger entries;
- `edge-cli-ops-audit` usage metadata;
- 12 curator backup blobs covering the experiment skill evolution;
- default-profile project registration metadata;
- legacy experiment baselines were already preserved under `baselines/from-default-profile`.

## Removed from production/default Hermes

### Sessions and model-usage state

Deleted session IDs:

- `20260927_113148_fbe6cc` — Run 1
- `20260927_123427_403ed1` — Run 2
- `20260927_192304_cbe9bf` — T3 transfer

Post-delete verification confirmed zero residual rows for all three IDs in:

- `sessions`;
- `messages`;
- `session_model_usage`.

`state.db` passed `PRAGMA quick_check`.

### Experiment knowledge

Removed:

- `/home/core/.hermes/skills/ops/edge-cli-ops-audit`
- `/home/core/.hermes/memories/MEMORY.md`
- `/home/core/.hermes/experiment-state/self-learning-local-qwen`

The current learned skill remains preserved project-locally at:

`/home/core/projects/hermes-self-learning/.hermes/skills/ops/edge-cli-ops-audit/SKILL.md`

SHA-256 at cleanup acceptance:

`71524c830d0fe8d27b2d2fb02cddf61341e59115f9bb3613ecc4c7f33f52b3f1`

### Curator metadata

Removed from the default profile:

- all 13 curator ledger entries for `edge-cli-ops-audit`;
- the `edge-cli-ops-audit` usage entry;
- all 12 identified curator backup blobs associated with the experiment skill.

Post-cleanup verification:

- ledger target count: 0;
- usage target absent;
- target curator blob count: 0.

The default curator was paused for the mutation and resumed successfully afterward.

### Default project registration

Removed from `/home/core/.hermes/projects.db`:

- project row for `p_c4afb88b`;
- its `project_folders` row;
- `project_meta.active_id` pointing to that project.

Preserved:

- `project_meta.repo_discovery_policy`.

`projects.db` passed `PRAGMA quick_check`.

After cleanup, `hermes -p default project list` reports no projects.

## Disposable self-learning environment

The isolated training environment remained intact:

- project-local `edge-cli-ops-audit` SHA unchanged;
- `selflearning` memory marker still present;
- `selflearning/projects.db` passed `PRAGMA quick_check`;
- exactly one self-learning project row and one project-folder row remain.

## Accepted current state

Production/default Hermes no longer contains the early self-learning experiment's:

- global skill;
- memory;
- sessions;
- project registration;
- active-project pointer;
- legacy experiment-state directory;
- curator metadata.

The disposable training environment remains the sole active location for continued Hermes self-learning.

## Non-blocking observation

The Markdown export command reported 60 exported messages for Run 1, whereas an earlier raw database audit counted 77 `messages` rows for that session. The cleanup verification itself is unaffected: all session/message/model-usage rows for the target IDs are now absent, and the higher-level experiment evidence required for the workstream remains preserved in the disposable project. The difference in exporter vs raw-row counting has not been independently characterized and is not treated as a blocker for this cleanup stage.

## Next stage

Continue Hermes self-learning/generalization only through:

- profile: `selflearning`
- project: `/home/core/projects/hermes-self-learning`

The remaining lifecycle is:

`sandbox → learn → evaluate → distill → promote → production-verify → cleanup`
