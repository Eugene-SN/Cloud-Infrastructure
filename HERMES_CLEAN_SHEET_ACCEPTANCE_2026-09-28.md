# Hermes Clean-Sheet Acceptance — 2026-09-28

## Status

COMPLETE / ACCEPTED

## Purpose

Retire the Hermes self-learning experiment completely and establish a default-only production baseline that can accurately be described as a clean sheet.

The experiment is retained only as a historical capability evaluation. No experiment-generated skill, memory, session state, or task artifact is promoted into production.

## Final runtime

- Hermes Agent: `v0.21.5+4396.gad2d482 (2026.9.24)`
- upstream commit: `ad2d4822e18a43e6f6a5faa2ec1117182f753abf`
- install method: git
- install directory: `/home/core/.hermes/hermes-agent`
- Python: `3.14.7`
- OpenAI SDK: `2.24.0`
- config schema: `49`

## Experiment retirement

Verified final state:

- `/home/core/.hermes/profiles/selflearning`: absent
- `/home/core/projects/hermes-self-learning-runtime`: absent
- experiment sessions/history: removed
- experiment memory: not promoted
- experiment skills: not promoted
- stale experiment leases: `0`

## Default clean-sheet state

Verified:

- profiles: default only
- sessions: `0`
- messages: `0`
- durable memory: empty/absent
- learned/custom skills: `0`
- bundled skills: `58`
- bundled skill tree aligned with current installed checkout
- learned-skill curator ledger: absent
- old local history: `0`
- old cache/log/update-backup/state-snapshot footprint: removed before fresh restart
- temporary recovery directory: removed

Fresh logs/cache created by the restarted runtime are expected baseline runtime data.

## Configuration preservation

The clean-sheet reset preserved the working production configuration and authentication state.

After the Desktop backend update, the only observed config diff from the preserved pre-update config was:

```text
_config_version: 46 -> 49
```

The migrated config passed `hermes config check`.

## Service acceptance

- `hermes-gateway.service`: active
- `hermes-dashboard.service`: active
- post-update mixed-module warning cleared after clean restart
- final session database remained at `0` sessions / `0` messages

## Accepted policy

- synthetic Hermes self-learning training is ended;
- the `selflearning` profile is retired;
- no experiment artifact is production knowledge;
- future Hermes work begins from the clean default profile;
- future persistent knowledge should arise only from real production use and requires separate acceptance before being treated as durable project state.

## Acceptance marker

`HERMES_CLEAN_SHEET=PASS`
