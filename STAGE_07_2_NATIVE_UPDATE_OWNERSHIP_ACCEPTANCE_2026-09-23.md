# Stage 07.2 — Edge Native Update Ownership Reconciliation

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

## Purpose

Reconcile update ownership for every deployed edge component so supported upstream/vendor-native automatic update lifecycles remain authoritative and Maintenance/Semaphore does not become a competing updater.

## Accepted ownership model

`native_first_hybrid`

Native automatic owners:

- **Codex** — managed-daemon native updater; Maintenance status only.
- **Hermes** — native Hermes cron update plus conditional systemd user settlement timer; Maintenance status only.
- **Ubuntu security updates** — package-owned `apt-daily.timer`, `apt-daily-upgrade.timer` and `unattended-upgrades.service`.

Maintenance/Semaphore manual owners:

- `APT_EDGE` for normal/third-party package upgrades;
- Xray, Hysteria2, Backrest, Restic, Rclone, Semaphore;
- n8n, Authelia, Mattermost, Mattermost PostgreSQL, Stalwart, Bulwark;
- Nextcloud application, Nextcloud PostgreSQL, Nextcloud Redis;
- CloudCLI, Antigravity.

Automatic reboot remains disabled.

## Runtime reconciliation

- old `/etc/apt/apt.conf.d/99-edge-maintenance-manual-only` override removed;
- package-owned Ubuntu security lifecycle restored and enabled;
- Codex native `pid-update-loop` accepted and active;
- Codex advanced natively to `0.156.1` during reconciliation;
- Hermes native update path accepted end-to-end and production schedule activated;
- Hermes current version `v0.21.4`;
- Rclone production runtime confirmed as `/usr/bin/rclone` and persistent `core` user service `projects-webdav.service`;
- Stage 12 Nextcloud app/PostgreSQL/Redis added as separate maintenance targets;
- Bulwark configured track changed from pinned `1.9.2` to `latest`; no real Bulwark update was executed during migration.

## Maintenance/Semaphore v4

Generated target model: `update_units_v4`.

- 18 actionable manual targets;
- 2 monitor-only native-owned rows: `HERMES`, `CODEX`;
- Semaphore Refresh template remains ID 1;
- Master Batch remains ID 18;
- template 14 repurposed from Hermes to Rclone;
- template 16 repurposed from Codex to Nextcloud;
- Nextcloud PostgreSQL and Redis use template IDs 19 and 20;
- Hermes/Codex manual update templates are retired;
- Master Batch evaluates only the 18 manual targets.

## Acceptance evidence

Migration verification produced:

- `GENERATED_MODEL_ACCEPTANCE=PASS`;
- `ALL_MANUAL_DRIVER_PREFLIGHTS=PASS`;
- `MASTER_CACHE_PRECHECK_GATE=PASS|TOTAL=18|CURRENT=14|UPDATE_AVAILABLE=4`;
- `MASTER_PLAN_ONLY_GATE=PASS`;
- `SEMAPHORE_TEMPLATE_ACCEPTANCE=PASS`;
- `NATIVE_OWNER_NON_REGRESSION=PASS`;
- `SERVICE_NON_MUTATION_GATE=PASS`;
- `TEMPORARY_SEMAPHORE_TOKEN_EXPIRED=PASS`;
- `STAGE07_2_MAINTENANCE_SEMAPHORE_MIGRATION=PASS`;
- final RC=0.

No real production component update was executed as part of the migration.

At acceptance, pending manual updates were APT_EDGE, n8n, Bulwark and Antigravity. These are ordinary operator-controlled maintenance state and do not block Stage 07.2 acceptance.

## Supersession

This record supersedes only the **current applicability** of Stage 7's blanket manual-only ownership rule, fixed 16-target model, masked Ubuntu security lifecycle and manual Hermes/Codex update ownership.

Historical Stage 7 acceptance records remain unchanged as evidence of the earlier accepted state.
