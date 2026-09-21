# Stage 06.7 — Production General-Plan Deployment — Final Acceptance

Timestamp: 2026-09-21T10:45:00+03:00

Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE06_7_FINAL_ACCEPTANCE=PASS`

## Edge acceptance

- production Backrest plan `edge-state` is deployed;
- schedule: `01/07/13/19` local;
- local repository: `/srv/backup/backrest/repositories/edge-state-local`;
- local retention: all snapshots within `7d`, grouped by `host,tags`;
- consistency staging is the authoritative transactional source for n8n, Authelia, Mattermost/PostgreSQL, Stalwart/Bulwark and known agent SQLite state;
- live transactional source paths are excluded from the general snapshot where staged state is authoritative;
- first accepted local snapshot: `6e8747d3ed5f7657087d508d06f297a2968312abefffcc142f3c587c77c5d4eb`;
- copied D5 snapshot: `0ff42011611bc213cf412d5c68e06f1a0395e8ba0ec2f2dcff3a2dd4681cc766`;
- local and D5 metadata/content verification passed;
- CT208/D5 client path is append-only; CT208 owns D5 maintenance;
- D5 retention: daily 30, weekly 8, monthly 6, yearly 0, grouped by `host,tags`;
- local monthly 100% data check and monthly prune are configured;
- dedicated Knowledge backup remains independent at `04/10/16/22`, rolling local `14d`, no D5.

## ai-node bounded corrections acceptance

The accepted bounded corrections were applied without redesigning the existing backup topology:

1. `ai-node-tier-copy` retention grouping corrected to `host,tags`;
2. `pai-n8n` now uses application-consistent SQLite staging at `/var/lib/backrest-staging/ai-node-n8n/current`;
3. staged n8n SQLite is normalized to a self-contained `journal_mode=delete` database with no WAL/SHM dependency;
4. `ai-node-full-system` excludes `/var/lib/containerd/**` and `/var/lib/docker/**`;
5. successful full D5 copy applies local `--keep-last 2 --group-by host,tags --prune`;
6. full-restore runtime mount directories were reconciled to `ai-data`, `g-data`, `backup`, `scratch`, `hdd`, and `data-cloud`.

Controlled `ai-node-ai-state` acceptance:

- local snapshot: `6be74a983a08c36ecafae9935757f699e446727cc4e93c06b8f7b34eee01adb2`;
- D5 copied snapshot: `ea7984427dab2559c56c4daaeff0508410a94c8009189554914851c516265019`;
- copied n8n SQLite SHA256 matched local and D5;
- D5-restored SQLite: `journal_mode=delete`, `integrity_check=ok`;
- local retention ran with `host,tags`;
- production `ai-node-ai-state` schedule restored to `15 6 * * *`;
- Knowledge path/schedule remained unchanged;
- Backrest, `pai-n8n`, and `pai-vllm` non-regression passed.

## Scope boundary

Stage 06.7 proves production backup creation, application-consistent staging, local retention, and D5 copy behavior. It does **not** replace Stage 06.8, which remains the mandatory isolated restore and application-usability acceptance.

## Next

Proceed to **Stage 06.8 — Isolated Restore & Application Recovery Acceptance**.
