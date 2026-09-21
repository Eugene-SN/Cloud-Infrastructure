# Stage 7B — CT1000 Master Batch Audit — 2026-09-21

## Scope and evidence

The audit was read-only. It inspected the live Home Maintenance endpoint at
`update.lan` (`192.168.1.19`), Semaphore project/template metadata, the current
action contract, task history and complete outputs for successful and failed
Master Batch tasks. No Home or Edge update was launched.

The audited Home source revision is
`6e7fa48c983a8549e8a5f0fa036006071a941df8`. The current Master template is ID
29, `10. Update — Full Infrastructure Master Batch`, using
`playbooks/all-updates.yml`.

## Proven Home contract

The accepted behavior is a single Semaphore task with these stages:

1. complete pre-scan and maintenance-cache render;
2. cache age, schema, target-set and summary precheck;
3. fixed ordered traversal of every target;
4. `CURRENT` targets recorded as successful `SKIPPED_CURRENT`;
5. `UPDATE_AVAILABLE` targets dispatched sequentially;
6. target failures recorded as `FAILED_CONTINUED` without hiding the failure;
7. complete post-scan;
8. post-scan target/status acceptance and deployment-specific regression gates;
9. a successful final task only when dispatch and every acceptance gate pass.

The Home history contained 19 Master tasks: 9 successful and 10 failed. Task
147 proved a clean 34-target no-op run. Task 139 proved 14 executed updates and
20 current skips in one successful run. Tasks 144 and 145 proved that a driver
result is insufficient: the final task failed while Home Assistant OS remained
`UPDATE_AVAILABLE`. Earlier failures also detected target-count drift, an extra
cache target, driver failures and pending reboot/staging behavior.

## Edge adaptation

Edge preserves this control flow with exactly 16 update units. Its explicit
Master order places APT_EDGE last because that unit may restart foundational
packages. Docker updates retain the digest accepted by the pre-scan. A single
cache timestamp is accepted for the complete batch, avoiding per-target expiry
during a long run while rejecting any concurrent cache replacement.

Semaphore self-update is `individual_only` in Master. The live service uses
`KillMode=control-group`; restarting it from its own Master task could kill the
Ansible process and prevent post-scan acceptance. If Semaphore itself has an
update, Master fails before any target mutation and requires its individual
update workflow first.

Edge post-acceptance requires:

- exact 16-target cache contract;
- every target `CURRENT` and no `CHECK_FAILED`;
- no pending reboot before dispatch or after the post-scan;
- zero failed systemd units;
- ten required system services and three required user services active;
- all six Compose services running and healthy where a healthcheck exists;
- PostgreSQL readiness;
- SQLite integrity for n8n and Authelia;
- valid nginx configuration and clean `dpkg --audit`.

Master remains a manual-only action initiated from `update.escloud.us`; no
timer, scheduler or autonomous update path is introduced.
