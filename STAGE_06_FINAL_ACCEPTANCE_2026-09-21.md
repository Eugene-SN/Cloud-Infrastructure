# Stage 06 — Edge Backrest & Recovery — Final Acceptance

Timestamp: 2026-09-21T11:15:00+03:00

Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE06_FINAL_ACCEPTANCE=PASS`

## Accepted scope

Stage 6 delivered and verified the production backup and recovery architecture for edge, including the bounded ai-node corrections accepted during the cross-project backup audit.

### edge

- Backrest and Restic production runtime accepted;
- dedicated Knowledge backup remains independent and local-only on edge;
- general `edge-state` plan deployed at `01/07/13/19`;
- local retention: all snapshots within `7d`, grouped by `host,tags`;
- application-consistent staging accepted for transactional state;
- successful append-only D5 copy path to CT208 accepted;
- CT208 owns D5 State retention: daily30, weekly8, monthly6, yearly0;
- real isolated D5 restore and application-usability tests passed for:
  - Mattermost PostgreSQL dump + Mattermost application;
  - n8n;
  - Authelia;
  - Stalwart;
  - Bulwark;
  - 24 staged agent SQLite databases;
- Stage 6 temporary restore artifacts removed;
- production containers and Backrest passed final non-regression;
- zero failed systemd units at final acceptance.

### ai-node

- tier-copy grouping corrected to `host,tags`;
- n8n application-consistent staging accepted;
- restored n8n SQLite is self-contained with `journal_mode=delete`;
- full-system backup excludes Docker/containerd runtime layers;
- after successful D5 full copy, local full retention keeps latest two snapshots grouped by `host,tags`;
- restore mount layout corrected to current runtime mounts;
- real isolated D5 n8n restore and application boot passed;
- production `pai-n8n`, `pai-vllm`, Backrest and Knowledge contract passed final non-regression;
- zero failed systemd units at final acceptance.

## CloudCLI drift reconciliation

A pre-existing CloudCLI drift was closed before final Stage 6 acceptance.

Root cause:

- `cloudcli.service` intentionally uses `/srv/ai-workspace` as both `WorkingDirectory` and `WORKSPACES_ROOT`;
- the directory was absent, causing repeated `status=200/CHDIR` restart failures.

Accepted recovery:

- restore `/srv/ai-workspace` as `core:core`, mode `0755`;
- retain the existing systemd unit contract unchanged.

Final verification:

- CloudCLI active and enabled;
- `NRestarts=0` after recovery;
- listener `127.0.0.1:18140` present;
- local HTTP backend returned `200`;
- no CHDIR recurrence after recovery.

## Reboot decision

No Stage 6 reboot acceptance was required. Stage 6 did not introduce kernel, bootloader, network, storage topology, or mount-topology changes requiring reboot validation. Service persistence is covered by the accepted enabled-service/runtime contracts and prior reboot acceptance of the infrastructure foundation.

## Acceptance chain

- Stage 6.6 deployment contract: ACCEPTED;
- Stage 6.7 production deployment: `STAGE06_7_FINAL_ACCEPTANCE=PASS`;
- Stage 6.8 isolated restore/application recovery: `STAGE06_8_FINAL_ACCEPTANCE=PASS`;
- Stage 6.9 final non-regression/persistence: `STAGE06_9_FINAL_ACCEPTANCE=PASS`;
- Stage 6 final: `STAGE06_FINAL_ACCEPTANCE=PASS`.

## Next stage

Proceed to **Stage 7 — Edge Maintenance & Update**.
