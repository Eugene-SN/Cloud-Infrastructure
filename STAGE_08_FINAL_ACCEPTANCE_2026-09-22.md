# Stage 08 Final Acceptance — 2026-09-22

## Status

**COMPLETE / ACCEPTED**

Acceptance marker:

`STAGE08_FINAL_ACCEPTANCE=PASS`

## Scope

Stage 8 — Edge Monitoring, Heartbeats & Alerts.

The accepted scope is intentionally edge-only. It does not add an independent external vantage point, monitoring database, heavyweight metrics/logging stack or separate monitoring WebUI.

## Accepted architecture

- one host-native persistent Python `edge-monitor.service`, supervised by systemd;
- FAST 5s / NORMAL 20s / SLOW 60s / OPERATIONS 300s collection cadences;
- two consecutive failed ordinary endpoint probes required before `FAIL`;
- concurrent application probes where appropriate;
- atomic live snapshot at `/run/edge-monitor/snapshot.json`;
- durable transition/notification state at `/var/lib/edge-monitor/state.json`;
- monitoring domains: EDGE, APPLICATIONS, HOME_PAI, KNOWLEDGE, OPERATIONS;
- direct dedicated Mattermost incoming webhook to the private `Monitoring` channel;
- notifications only on meaningful transition and recovery; unchanged failure remains silent;
- Backrest freshness derived from structured `/var/lib/backrest/oplog.sqlite` successful snapshot operations;
- Stage 7 maintenance state is read as metadata only; `UPDATE_AVAILABLE` is informational and monitoring does not trigger Stage 7 Refresh.

## Initial deployment evidence

`STAGE08_2_EDGE_MONITOR_INITIAL_DEPLOYMENT=PASS`

Confirmed:

- `edge-monitor.service` enabled and active;
- `Restart=always`, `RestartSec=2s`, `NRestarts=0`;
- snapshot cadence advanced correctly;
- all five domains initially `OK`;
- both Backrest plans initially `OK`;
- maintenance state: `CHECK_FAILED=0`, `REBOOT_REQUIRED=0`, `UPDATE_AVAILABLE=1`;
- direct Mattermost webhook loopback test passed;
- zero failed systemd units.

## Final transition / deduplication / recovery evidence

`STAGE08_3_TRANSITION_DEDUP_RECOVERY_TEST=PASS`

A synthetic monitor-only HTTP probe was added temporarily without stopping or mutating any production service.

Verified sequence:

1. Healthy synthetic baseline: `state=OK`, `failures=0`; no notification was emitted.
2. Synthetic endpoint changed to a closed loopback port.
3. After two failed NORMAL cycles: `state=FAIL`, `failures=2`; exactly one failure notification was emitted.
4. Failure held for an additional interval; notification count did not change.
5. Healthy endpoint restored: `state=OK`, `failures=0`; exactly one recovery notification was emitted.
6. Original `/etc/edge-monitor/config.json` was restored byte-for-byte.
7. Original config SHA256 before and after: `91bacef62dbf5076b405b3b08512aa85ab6bb03ca0c887b7f86521cdd78133c5`.
8. Synthetic config entry, live snapshot entry and durable notification-state entry were all absent after cleanup.
9. Production non-regression: service enabled/active, `NRestarts=0`, EDGE/APPLICATIONS/HOME_PAI/KNOWLEDGE/OPERATIONS all `OK`, `OVERALL_STATE=OK`, zero failed systemd units.

Mattermost post count during the controlled test changed from 1 baseline post to 2 after FAIL, remained 2 during unchanged FAIL, then became 3 after recovery. This proves transition delivery plus unchanged-state deduplication.

## Accepted limitations

- Complete loss of `edge` or its external connectivity cannot be reported while the node itself is unreachable because Stage 8 deliberately has no independent vantage point.
- This is an accepted current-scope limitation, not an unresolved Stage 8 failure.

## Final result

All selected Stage 8 requirements are deployed and verified. No additional production-failure simulation or monitoring-stack expansion is required.

**Stage 8 — COMPLETE / ACCEPTED.**

Next finite infrastructure stage: **Stage 9 — Edge Cloud Portal**.
