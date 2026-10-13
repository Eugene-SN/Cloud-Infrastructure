# Edge update driver audit — 2026-10-13

Operator scope: fix Hysteria2 and Nextcloud (including equal-version image
digest updates), audit every other updater, and separately approved fixes for
Xray and Backrest. No updates or restarts are authorized for verification.

Task66 evidence: eight executed targets, ten current skips, two failed targets
(Hysteria2 and Nextcloud); post-run health passed and only Nextcloud remained
UPDATE_AVAILABLE. The reboot marker is informational under the superseding
2026-10-13 decision. Task66 is not relabeled as successful.

| Target | Checks and outcome |
| --- | --- |
| HYSTERIA2 | Reproduced leaked RETURN cleanup after function scope ended; isolated function/EXIT fix tested on success and failed download; native preflight passed. |
| XRAY | Same dormant defect reproduced and corrected with separate approval; native configuration validation passed. |
| BACKREST | Confirmed absent downloader, wrong archive name and unsuitable positional version invocation; existing helper corrected; preparation, installation and health failure fixtures passed without real service commands. |
| NEXTCLOUD | Confirmed missing target CLI argument and skipped same-version refresh; version/digest dispatch, pinned image pull, app/cron recreation, readiness and both image IDs tested at isolated boundaries. Native Compose preflight passed. |
| SEMAPHORE | External dispatch contract, candidate/download failure, SQLite rollback and final-outcome tests passed; native preflight passed. No additional change to its handler. |
| RESTIC | Native version/preflight and supported self-update CLI inspected; isolated dispatch passed. |
| RCLONE | Native version/preflight, stable selfupdate CLI and core user context inspected; isolated dispatch passed. |
| N8N | Live Compose identity and preflight matched cache; pinned-image dispatch tested. |
| AUTHELIA | Live Compose identity and preflight matched cache; pinned-image dispatch tested. |
| POSTGRESQL | Live Compose identity and preflight matched cache; pinned-image dispatch tested; readiness passed. |
| MATTERMOST | Live Compose identity and preflight matched cache; pinned-image dispatch tested. |
| STALWART | Native version/Compose preflight passed; version/track/digest dispatch tested against current CLI. |
| BULWARK | Live Compose identity and preflight matched cache; pinned-image dispatch tested. |
| NEXTCLOUD_REDIS | Live Compose identity and preflight matched cache; service-scoped dispatch tested. |
| PLANE | Native preflight passed including upstream/site topology and existing recovery snapshot; isolated dispatch and eight topology drift cases tested. No backup operation was started. |
| WEBLATE | Live Compose identity and preflight matched cache; pinned-image dispatch tested. |
| WEBLATE_VALKEY | Live Compose identity and preflight matched cache; service-scoped dispatch tested. |
| APT_EDGE | Native preflight, isolated dispatch and apt-get simulation checked; zero simulated installations/removals. Three OpenSSH packages were deferred by native APT phasing, without adding a project policy. |

The eight APT-managed monitored components share APT_EDGE and health validation;
they are not independent custom update drivers. Hermes, Codex, Ubuntu security
and Antigravity retain their existing native ownership; this audit does not
modify or execute their automatic update mechanisms.

Health: nine system services, four user services, eleven Docker units/twenty-one
services, two SQLite databases and PostgreSQL readiness passed. No extra defect
was confirmed in the remaining checked routes. This does not establish that
every future upstream release or migration will succeed: real update execution
was deliberately excluded, and application-specific migrations cannot be
proven by a preflight or a command-boundary fixture alone.

Recovery: original handler files and ownership/mode metadata are retained in
`/tmp/semaphore-handler-recovery/drivers-task66`. The migration-reference
maintctl file is historical and is not overwritten with current runtime state.

## Verification commands

```bash
python3 maintenance/edge/tests/verify-update-drivers.py
python3 maintenance/edge/tests/verify-backrest-update.py
sudo -n python3 maintenance/edge/tests/verify-maintctl-update.py
python3 maintenance/edge/tests/verify-master-contract.py
python3 maintenance/edge/tests/verify-contract.py /var/www/maintenance-status/maintenance.json
sudo -n python3 maintenance/edge/tests/verify-plane-contract.py
python3 maintenance/edge/tests/verify-semaphore-update.py
node maintenance/edge/tests/verify-semaphore-dashboard.js
python3 maintenance/edge/tests/verify-semaphore-pve.py
ansible-playbook --syntax-check -i localhost, maintenance/edge/playbooks/master-batch.yml
```
