# Edge storage lifecycle — 2026-10-26

Operator-authorized implementation: remove obsolete Hermes update archives and
disable their creation; migrate T3 to stable with Codex and Antigravity; remove
empty Nextcloud preview directories; remove successful-update recovery copies;
evacuate Edge backup snapshots to the existing PVE repository before reclaiming
local snapshots and data. Preserve application/user data and unrelated work.

Application update policy: retain temporary recovery material only while the
update is unresolved. After the installed runtime passes its existing readiness
checks, remove superseded application binaries and update recovery copies.
Backrest history remains on PVE under its existing server-side retention.

## Deferred stage: Documentation, profiles and Codex artifacts

This stage is a plan only. No deletion or changes to these working trees,
profiles, frozen jobs, receipts or proofs are authorized by the present stage.

1. Inventory each of the 154 task directories under the Codex Documentation
   worktree `.local` (about 7.8 GiB): owner, completion/cancellation state,
   current callers and the minimal regression inputs still required.
2. Keep the currently used test environment and Weblate/PostgreSQL fixtures;
   remove unused `native-stage/native-import` and completed/retired copied
   runtimes only after caller checks. Do not delete the worktree or uncommitted
   source changes. Keep concise result records instead of whole runtime trees.
3. Reconcile Documentation's 127 pre-change backups (about 0.58 GiB), old pilots
   and benchmarks (about 0.49 GiB). One pending recovery currently reads
   `repair-feedback-namespace-20261025T185208Z/lib/documentation/validation_loop.py`
   and its installation manifest. Move necessary proof provenance into the job
   contract before removing its application-backup dependency.
4. Trace completed jobs and repair attempts in `pipeline/workspaces/jobs`
   (about 4 GiB). Preserve frozen identities, current inputs/outputs and the
   transitive proof/receipt graph. Close or explicitly cancel pending cards
   before deleting their workspaces; add task-completion cleanup at the owner.
5. Inspect old Hermes environment/tool generations, redundant Git packs, Codex
   release history and caches using their native owners. Do not mix application
   recovery cleanup with user conversation history or the HTML Translation
   profile's active data.
6. Verify each exact target is unreferenced; record before/after allocated bytes,
   run proportionate regression checks, and prove current service/job behavior
   plus absence of removed artifacts. Do not launch translations or alter model
   settings as part of storage cleanup.

## Completion evidence

- Root filesystem: initial usage about 114.3 GiB (`df -h`: 115G); final measured
  usage 61.90 GiB, available 92.14 GiB. About 52.4 GiB reclaimed. Live workload
  writes can change these figures after the measurement.
- Hermes: removed six obsolete ZIP archives (4,889,829,376 allocated bytes)
  and three pre-update quick snapshots. Installed the existing cron wrapper
  with `--no-backup`; gateway and dashboard remained active.
- T3: native update from nightly to stable **0.1.2**, followed by the official
  installer to register the stable CLI launcher. The service runs from
  `runtime/versions/0.1.2`; no previous runtime version remains. Native update
  defaults to the installed release's stable channel. Managed Antigravity ACP
  upgraded from 1.1.1 to **1.3.0**; after authentication/model discovery checks,
  removed the inactive 1.1.1 release. T3 now occupies about 1.76 GiB. User data,
  existing conversations, provider settings and credentials were preserved.
  Browser provider refresh confirmed Codex authenticated with eight models and
  Antigravity authenticated with eleven models. No model task was submitted.
  The temporary audit browser session was revoked after verification.
- Nextcloud 35.0.2: removed **779,057 empty preview directories**, reclaiming
  3,191,017,472 directory bytes. All nine preview files retained identical
  SHA256 hashes; 72 nonempty ancestor directories remain. Production containers
  stayed running. The installed preview storage code matches upstream 35.0.2;
  empty-directory accumulation is an upstream issue and can recur. No vendor
  patch or additional cleanup timer was introduced.
- Application update policy: successful Antigravity readiness removes its prior
  binary/metadata; successful Semaphore, Backrest/Restic and VPN update paths
  remove exact matching update recovery copies. Failure paths retain temporary
  recovery material. Removed verified obsolete Semaphore, Antigravity, VPN and
  retired Stage 2 migration copies. Existing native owners/schedules remain.
- Backrest: evacuated and verified 29 local State snapshots and 144 Knowledge
  snapshots. PVE now contains **205 snapshots**: 60 State, 144 Knowledge and one
  other existing snapshot. Both Edge repositories now contain zero snapshots;
  their combined skeleton is about 2.2 MB. Removed copied State staging and
  obsolete root Restic caches. Destination retention was not changed and no
  destination forget/tag/prune was performed. A remote hostname-file extraction
  matched Edge; this is a spot read, not a full application restore test.
- Verification: 10 Antigravity tests, five evacuation tests and the isolated
  Semaphore lifecycle contract passed. Shell syntax and installed/canonical file
  comparisons passed. T3 HTTP returned 200; Hermes and Antigravity daemons,
  Backrest, Semaphore, Xray and Hysteria were active; the infrastructure monitor
  reported `OK`. Nextcloud, n8n and Weblate containers retained their uptime.

## Native maintenance policy

Use `t3 update --channel stable --yes` for future T3 releases. For managed ACP,
use T3's provider update, verify its active manifest, authentication and model
discovery, then remove only inactive release directories. The current native
ACP installer retains old releases; this cleanup remains part of the update
procedure rather than a new independent updater or timer.

Apply `maintenance/edge/patches/vpn-update-retention.patch` to the existing
`/opt/vpn-stack/scripts/maintctl` when redeploying that private runtime script.
Hermes, Antigravity and Edge maintenance canonical scripts contain their new
policies directly; deploy those canonical files rather than restoring old ones.

Primary references: [T3 stable release](https://github.com/pingdotgg/t3code/releases/tag/v0.1.2),
[official installer](https://t3.codes/install.sh),
[Nextcloud empty-preview issue](https://github.com/nextcloud/server/issues/46425),
[Nextcloud preview-directory report](https://github.com/nextcloud/server/issues/65668).
