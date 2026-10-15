# Antigravity daemon updates on edge

Approved 2026-10-16. The native `antigravity-cli-daemon.service` owns the
daemon. Its generated unit and the vendor executable are not patched.
An independently named user timer invokes the supported `agy update`
command daily at **04:30 Europe/Moscow (UTC+3)**. `Persistent=true` catches
a missed scheduled run after downtime; `core` user lingering is enabled.
There is no second daemon, custom downloader, manifest parser or Semaphore
update action. The native interactive background updater remains enabled.

## Contract and installed files

| Canonical file | Installed path |
|---|---|
| `update.py` | `/home/core/.local/state/antigravity-native-update/update.py` |
| `antigravity-native-update.service` | `/home/core/.config/systemd/user/antigravity-native-update.service` |
| `antigravity-native-update.timer` | `/home/core/.config/systemd/user/antigravity-native-update.timer` |

The oneshot has a 15-minute bound; the native update command has a 12-minute
bound, leaving time for process replacement and readiness verification.
Only version probes set `AGY_CLI_DISABLE_AUTO_UPDATE=true`. The update
command does not inherit that override. Commands are noninteractive.

The helper copies the current running executable before invoking `agy update`.
If the installed executable differs from `/proc/$MainPID/exe`, it retains
that complete copy as `previous-agy`, records its version in `previous.json`,
and restarts the native daemon. No-change checks preserve its PID and the
previous-version backup. Native updater errors fail the check without
restarting the daemon. An interrupted update also retains the running binary
when disk and running executable diverge. Rollback is manual.

Success requires an active, stable PID running the installed executable and
its own CLI log reporting the installed version and latest connection status
`Connected`. Two observations two seconds apart must agree, within 60 seconds.
This establishes startup readiness, not future connection availability.
A stopped daemon, missing/changed log format, version mismatch or connection
timeout fails visibly. There is no fallback that reports a false success.

`status.json` is replaced atomically, preserves `last_success_at` on failure,
and records result, version, PID, restart decision and daemon log path.
Existing edge-monitor observes this file, timer enabled/active state and
oneshot Result. Failed/stuck checks and success older than 26 hours raise one
`antigravity-update` incident through the existing notification path.
No synthetic production alerts are sent by the tests.

## Inspection and recovery

Run user-service commands as `core`, with its user manager environment:

```bash
systemctl --user status antigravity-native-update.timer
systemctl --user start antigravity-native-update.service
journalctl --user -u antigravity-native-update.service --no-pager -n 60
cat /home/core/.local/state/antigravity-native-update/status.json
```

For an operator-directed binary rollback, stop the update timer and any
running update oneshot, then stop the native daemon. Confirm the recorded
previous binary version using `AGY_CLI_DISABLE_AUTO_UPDATE=true previous-agy
--version`. Copy `previous-agy` to a temporary file beside `.local/bin/agy`,
set mode 0700 and atomically rename it over `agy`. Start the native daemon
and verify its version and `Connected` log for its new PID. Keep the update
timer stopped until the failed release or prerequisite is addressed; restarting
the timer permits the vendor updater to install the current release again.
The monitor correctly reports the intentionally stopped update schedule.

The sole permanent recovery binary is `previous-agy`; temporary candidate
copies are removed after each completed check. Superseded first-fix shell
script and ad-hoc recovery directory are removed after verification.

## Compatibility and evidence

The timer/helper are outside vendor-managed binary/config directories and do
not modify the native daemon unit. Normal binary replacement or native service
re-registration does not target these independently named files. A future
vendor change to the command, service name or log format cannot be guaranteed
compatible; the monitor makes such a failure visible instead of patching or
silently bypassing the new behavior.

Official references checked 2026-10-16:

- [Native daemon lifecycle](https://www.antigravity.google/docs/remote-control?tab=cli)
- [CLI troubleshooting](https://www.antigravity.google/docs/cli/troubleshooting/)
- Exact installed CLI: `agy help update`; versions 1.2.14 and 1.3.6 and native
  service registration were inspected during root-cause investigation.

The daemon startup branch bypasses the interactive CLI background installer
trigger. The daemon's periodic update-status check does not itself request
installation. This schedule fills that integration gap while retaining the
vendor installer. It supersedes the 2026-09-25 assumption that enabled native
background updates proved a complete automatic daemon install/restart cycle.

Validation and live evidence: `ACCEPTANCE_2026-10-16.md`.
