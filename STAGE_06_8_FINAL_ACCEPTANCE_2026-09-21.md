# Stage 06.8 — Isolated Restore & Application Recovery Acceptance

Timestamp: 2026-09-21T11:10:00+03:00

Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE06_8_FINAL_ACCEPTANCE=PASS`

## Edge D5 isolated restore

Production D5 snapshot used:

`0ff42011611bc213cf412d5c68e06f1a0395e8ba0ec2f2dcff3a2dd4681cc766`

Accepted evidence:

- isolated filesystem restore from D5 completed successfully;
- n8n SQLite: `integrity_check=ok`;
- Authelia SQLite: `integrity_check=ok`;
- 24 staged agent SQLite databases passed integrity checks;
- Mattermost custom-format PostgreSQL dump restored into isolated PostgreSQL 18;
- restored Mattermost database contained 99 tables, 5 users, 20 posts and 1 team;
- restored Mattermost application booted against the restored database and returned HTTP 200 from `/api/v4/system/ping`;
- n8n restored application booted successfully; restored database contained 1 workflow and 2 credential rows;
- Authelia restored application booted successfully with restored database and storage encryption key;
- Stalwart booted on restored state; `CURRENT` and referenced manifest were valid;
- Bulwark booted on restored state and restored session secret was present;
- production containers and Backrest remained running.

A PostgreSQL 18 test-harness defect was identified and corrected during acceptance: PostgreSQL 18 requires the temporary data mount at `/var/lib/postgresql`, not the legacy `/var/lib/postgresql/data`. This was a test harness issue, not a backup or restore defect.

## ai-node D5 isolated restore

Production D5 snapshot used:

`ea7984427dab2559c56c4daaeff0508410a94c8009189554914851c516265019`

Accepted evidence:

- isolated restore from D5 completed successfully;
- restored n8n SQLite: `journal_mode=delete`, `integrity_check=ok`, 139 tables;
- restored n8n state contained 3 workflows and 1 credential row;
- no WAL/SHM dependency was present;
- production n8n image booted successfully against the restored state;
- post-boot state remained readable with the same workflow/credential counts;
- production `pai-n8n`, `pai-vllm`, and Backrest remained healthy/running.

## Scope boundary

Stage 06.8 proves real D5 restore and application usability for the accepted Stage 6 backup design without overwriting production.

Stage 06.9 remains the final Stage 6 non-regression/persistence/cleanup acceptance, including reconciliation of the pre-existing CloudCLI `CHDIR` runtime drift.

## Next

Proceed to **Stage 06.9 — Final Stage 6 Non-Regression & Acceptance**.
