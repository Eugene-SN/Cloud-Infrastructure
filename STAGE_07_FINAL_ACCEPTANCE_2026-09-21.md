# Stage 7 Final Acceptance — 2026-09-21

## Result

`STAGE07_FINAL_ACCEPTANCE=PASS`

Stage 7 — Edge Maintenance & Update — is **COMPLETE / ACCEPTED**.

## Accepted scope

Stage 7A and Stage 7B acceptance evidence is reused. Stage 7C is closed by the
final integrated read-only acceptance of the deployed `update.escloud.us`
dashboard and current maintenance runtime.

The accepted production contract is:

- `update.escloud.us` is the only operator launch surface for every real update;
- Semaphore is the backend executor/orchestrator and has zero schedules;
- no autonomous project update timer, cron path, updater daemon or unattended
  APT path is active;
- Ubuntu APT periodic settings resolve to `0`; `apt-daily*` and
  `unattended-upgrades.service` are masked/inactive;
- maintenance model `update_units_v3` contains exactly 16 actionable update
  units and 23 monitored components, including eight non-actionable APT children;
- Refresh is template ID `1`, individual update templates are IDs `2–17`,
  and manual Master Batch is template ID `18`;
- one generated runtime `actions.json` is used;
- Master Batch keeps the accepted CT1000-derived lifecycle: fresh scan, fixed
  exact plan, skip CURRENT, execute UPDATE_AVAILABLE, isolate/report failures,
  APT_EDGE last, full post-scan and final health gates;
- Docker application version, image track/tag and image digest semantics remain
  separate;
- Hermes, CloudCLI, Codex and Antigravity run through the normalized `core`
  execution context with cwd `/home/core`;
- Hermes active lazy-dependency drift is fail-closed. A partial dependency
  refresh is not accepted as a successful Hermes update.

## Final verification

`STAGE07_FINAL_INTEGRATED_READONLY_ACCEPTANCE_V1` completed with RC=0.

Verified:

- required runtime files: PASS;
- manual-only APT policy: PASS;
- autonomous APT units: masked/inactive;
- Semaphore schedules: `0`;
- persistent project update launchers: none;
- enablement/template contract: 16 individual templates + Master ID `18`;
- one generated action artifact: PASS;
- normalized `user_cli` context and preflights for Hermes, CloudCLI, Codex and
  Antigravity: PASS;
- fresh read-only Refresh: PASS;
- fresh maintenance state: 15 CURRENT, one Hermes UPDATE_AVAILABLE,
  `CHECK_FAILED=0`, `REBOOT_REQUIRED=0`;
- Docker version model: PASS;
- Stage 7C dashboard source and JavaScript syntax: PASS;
- loopback dashboard delivery: PASS;
- public `update.escloud.us` Authelia boundary: PASS;
- nginx same-origin contract: PASS;
- accepted Master Batch Task 12 evidence: PASS;
- Master health recheck: PASS;
- production system/user services: PASS;
- six Docker workloads: running/healthy as applicable;
- failed systemd units: none;
- no real production update was executed by the final acceptance audit.

The Hermes UPDATE_AVAILABLE state is not an acceptance failure. The installed and
available Hermes application version are the same; the current status represents
the already-known active lazy-dependency drift now detected by the fail-closed
driver. Its next correction is an ordinary operator-triggered Hermes update from
the Maintenance WebUI.

## Repository persistence note

The final runtime audit proves the normalized `user_cli` execution behavior and
Hermes fail-closed lazy-dependency behavior deployed on edge. The current
repository implementation-source snapshot still predates those two final Codex
runtime changes. Treat the verified runtime as authoritative and do not redeploy
the older repository copy over it until that source drift is reconciled. This is
a persistence/reproducibility issue, not a Stage 7 runtime acceptance failure.

## Next stage

Stage 8 — Edge Monitoring, Heartbeats & Alerts.
