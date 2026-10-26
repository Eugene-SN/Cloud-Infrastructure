# Hermes update storage policy

2026-10-26: `native-auto-update.sh` remains the existing native Hermes cron
entrypoint. It invokes `hermes update --yes --no-backup --no-gateway-restart`.
The existing settlement mechanism handles a changed release. No new service or
schedule is introduced. Hermes ZIP imports are not part of production recovery;
Backrest owns historical backups. Do not reintroduce `--backup` into this script.

The former `--backup` flag overrode `updates.pre_update_backup: false` and
created full archives even when the source version did not change. Six such
archives and three pre-update quick snapshots were removed after checking the
current services and absence of pending update settlement. Active profiles,
databases, skills and Documentation working files were preserved.
