# Mattermost Global Message Prune — Final Acceptance

Date: 2026-09-25

Status: COMPLETE / ACCEPTED

Acceptance marker: `MATTERMOST_GLOBAL_MESSAGES_PERMANENT_PRUNE=PASS`

## Scope

All Mattermost message history was permanently removed while preserving users, channels and conversation structures.

Deleted corpus:

- original post rows: 181;
- one post was permanently deleted during the first interrupted run;
- remaining 180 posts were permanently deleted through the Mattermost application API;
- final post rows: 0;
- final active post rows: 0;
- final soft-deleted post rows: 0;
- final thread reply rows: 0;
- final thread rows: 0;
- final thread membership rows: 0;
- final FileInfo rows: 0.

## Procedure

Permanent deletion used the Mattermost application/API path `DELETE /api/v4/posts/{id}?permanent=true` with a system-admin PAT.

`ServiceSettings.EnableAPIPostDeletion` was enabled only for the deletion window and restored to `false` afterward.

The operation used the existing Mattermost PostgreSQL container for database verification. A temporary recovery point containing the pre-prune PostgreSQL dump and original config was preserved through recovery from the interrupted first run and removed only after final acceptance.

## Verification

Final verification confirmed:

- Mattermost API health HTTP 200;
- Mattermost container healthy;
- `posts=0`;
- `threads=0`;
- `threadmemberships=0`;
- `reactions=0`;
- `readreceipts=0`;
- `temporaryposts=0`;
- `fileinfo=0`;
- all discovered auxiliary post/root reference columns contained zero rows;
- active users preserved: 6;
- active public channels preserved: 2;
- active private channels preserved: 3;
- active DM channels preserved: 4;
- active group-DM channels: 0;
- `EnableAPIPostDeletion=false` restored;
- `edge-monitor.service` restored and healthy;
- temporary recovery artifact removed after PASS.

No direct SQL deletion of Mattermost posts was used.
