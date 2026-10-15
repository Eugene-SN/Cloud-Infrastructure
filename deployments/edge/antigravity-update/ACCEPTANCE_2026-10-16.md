# Antigravity automatic daemon updates — 2026-10-16

Host: edge.escloud.us. Times below are Europe/Moscow, UTC+3.
Operator approved the minimal operational schedule around the vendor updater.
Deployment and current-version application checks: **VERIFIED**.

## Cause and ownership correction

In the inspected native 1.2.14/1.3.6 binaries, the persistent daemon startup
branch bypasses `entrypoints.MaybeLaunchCLI -> updater.triggerUpdateShared`.
The separate daemon status refresh checks update availability every 30 minutes;
installation is request-driven via `ApplyUpdate`. Enabled background updates
therefore did not establish periodic installation and daemon restart.
Native `agy remote-control start` re-registration was tested earlier in this
investigation and did not register an install scheduler. Codex has a different
native `pid-update-loop`, explaining its functioning automatic installation.

This corrects the 2026-09-25 acceptance inference without reinstating an
Antigravity manual Maintenance/Semaphore target. Native `agy update` is the
installer; the independent systemd schedule and application verifier are our
explicitly approved operational integration.

## Evidence

| Check | Observed result |
|---|---|
| Actual native release transition, 01:47:06–01:47:11 | 1.2.14 → 1.3.6; download, extraction, verification and installation reported successful by `agy update` |
| Actual application of that release, 01:47:12–01:47:15 | Old PID 1278 replaced by PID 2835303; its own log records version 1.3.6 and Connected |
| Final helper, 02:17:56–02:18:00 | Native no-change update check PASS; PID 2860071 preserved; executable identity, version and Connected verified |
| Controlled native daemon restart, 02:19:03 | PID 2896471; log version 1.3.6; Connected at 02:19:06.543809 |
| Final helper, 02:19:03–02:19:10 | PASS, version 1.3.6, PID 2896471 retained, `restarted=false`; fresh daemon log identified by PID |
| Timer | enabled/active; next scheduled run 2026-10-16 04:30:00 MSK; daily; Persistent=true |
| Bounds | oneshot 15 minutes; native update command 12 minutes; readiness 60 seconds |
| Existing edge-monitor | updater health OK, empty reasons, successful status/PID/version visible in snapshot; incident state OK, notified_active=false |
| Recovery | One retained native binary 1.2.14, SHA256 `0d0d3eba22daf29504dd290151c7ed9a4d33b0c6aa0acfc5da27bc3b01d2f029` |
| Native daemon unit and account settings | SHA256 identical to initial pre-change recovery manifest |
| Manual Maintenance contract | PASS; Antigravity remains absent from manual units/actions/rows |
| Failed system/user units | None at verification |

Release-transition evidence belongs to the initial helper. The final helper
was installed after 1.3.6 was already current, so a **new release transition
through the final helper has not yet been observed in production**. Its
changed-executable restart/backup branches were tested offline. The final
helper was verified live for native checks, unchanged PID behavior and readiness
of a freshly restarted native daemon. Production was not deliberately downgraded
to manufacture another update. The first natural subsequent release will
exercise the combined final path, with monitoring already enabled.

Evidence locations retained on edge:

- `journalctl --user -u antigravity-native-update.service` — vendor update and
  operational check events, with systemd timestamps.
- `/home/core/.gemini/antigravity-cli/log/cli-20261016_014712.log` — real 1.3.6
  application after the 1.2.14 update, PID 2835303.
- `/home/core/.gemini/antigravity-cli/log/cli-20261016_021903.log` — current native
  daemon startup, version and connection, PID 2896471.
- `/home/core/.local/state/antigravity-native-update/status.json` — latest check
  with durable last-success timestamp.
- `/run/edge-monitor/snapshot.json` → `applications.antigravity_update`.
- `/var/lib/edge-monitor/state.json` → `incidents.antigravity-update`.

## Verification and cleanup

19 offline tests passed: nine updater lifecycle/readiness tests, five updater
monitoring/notification tests and five existing workflow-monitor tests.
Coverage includes unchanged PID, replacement and pending foreground update,
backup retention, failed/interrupted install, stopped/flapping daemon,
wrong version/PID, Disconnected status, stale success, disabled timer, failed
oneshot and notification/recovery deduplication. External commands and webhook
delivery were substituted in negative tests; no synthetic production alarms.
`systemd-analyze --user verify` accepted both units. The existing Maintenance
contract verifier passed against the live status file.

Canonical and installed helper/units/monitor/config/ownership descriptors are
matched by SHA256. Native daemon unit and authentication settings are unchanged.
The superseded hourly timer content and shell helper were replaced. The initial
ad-hoc recovery tree was normalized to `previous-agy` + `previous.json`; its
duplicate settings/unit backups and pointer were removed after equality checks.
Temporary deployment backups are removed after Git persistence/readback.
Unrelated existing Hermes translation changes are preserved and excluded from
the commit.

No guarantee is made about unknown future vendor CLI/service/log contracts.
The files are independently owned and outside the vendor-managed paths;
unexpected upstream changes fail visibly through ordinary monitoring.
