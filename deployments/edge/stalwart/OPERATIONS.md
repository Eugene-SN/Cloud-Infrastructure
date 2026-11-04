# Edge Stalwart 1.0.2

Verified 2026-11-04. This is the manual upstream migration of 0.16.27 to 1.0.2;
Maintenance has no migration implementation. PVE was not accessed or changed.

## Active layout

- Compose: `/opt/mail-stack/compose.yaml`, service/container `stalwart`.
- Image: `stalwartlabs/stalwart:v1.0`, verified as 1.0.2, digest
  `sha256:154e55adecadfcc4a67044b9b94d482a20286e1101c97a2b322224bb596053d5`.
- Host configuration/TLS: `/srv/mail/stalwart/etc`.
- Host RocksDB: `/srv/mail/stalwart/lib`; local JSON configuration names
  `/var/lib/stalwart-v1/`, mounted in the container at that path.
- Native Docker volume inheritance also exposes the same host data directory
  at `/var/lib/stalwart`; both mounts refer to the same migrated store.
- Data ownership: UID/GID 2000. Public SMTP 25, SMTPS 465, IMAPS 993 and existing
  HTTP ingress are preserved. Only Stalwart was recreated by this operation.

Ordinary supported 1.x updates use the existing Maintenance Stalwart driver.
Read the upstream release notes for any release-specific compatibility steps.
Old images are removed after successful application verification. Do not retain
old image archives; recovery fetches an exact digest when needed.

## Verified migration and known differences

Official utility: `stalwartlabs/stalwart-migrate:1.0.5`, digest
`sha256:37c2aaea4c4500d9cc9f39d67dbdbd5ccab42c4ea89a26f064f4f53941f58dd6`;
upstream source commit `6447da1975d0a693efc04ebe03ee7442acbe01fd`.
The standard build is required for official Stalwart Docker images, including
Community deployments; the `-oss` tool is for custom non-enterprise builds.

All 16 native categories were selected, with blob mode `copy`. Incremental
copy ran with 0.16 serving users. A graceful stop preceded `run --final --yes
--verify-full`. All 3 accounts passed, with 0 mismatches, 0 unexplained
mismatches and 0 outstanding errors. The measured stop-to-healthy interval was
70.05 seconds. Native reverse migration into a separate test store also checked
all 3 accounts, with 0 mismatches and 0 errors, before the final cutover.

Operator-approved choices: recommended per-setting defaults, accept required
v1 OAuth registration behavior, and grant new permissions matching old role
permissions. OAuth tokens require a new sign-in; ordinary password IMAP/SMTP
is preserved. CalDAV/CardDAV/WebDAV clients may resynchronize, and the search
index is rebuilt by v1.

The native final report has 42 outstanding warnings. These include 21 registry
records that the native reader cannot decode and reports as already ignored
by 0.16.27; their creation/corruption cause was not established. They were not
silently repaired. Twelve legacy LLM spam-score tags have no v1 counterpart.
Other warnings concern removed settings/permissions. These differences mean
literal preservation of every legacy serialized object must not be claimed.
The full original store remains intact for recovery and investigation.
No `--allow-errors`, mass-removal override or data-category exclusion was used.

Post-cutover checks: native Docker healthy and exact running image/version,
IMAPS TLS 1.3/capabilities, SMTPS certificate/EHLO, native live HTTP 200 and
public WebUI HTTP 200. Plane's existing encrypted SMTP credentials authenticated
with response 235, without sending mail. This does not prove client-side Apple
Mail synchronization. Maintenance reports Stalwart 1.0.2/CURRENT.

## Recovery material and native reverse migration

Private recovery root: `/srv/mail/stalwart-migration` (0700). Required contents:

- `source-v016/`: original cold configuration, TLS and complete RocksDB store;
- `compose-v016.yaml`: original Compose file;
- `state/`: native forward migration state, original readable setting values,
  approved answers, logs and final report;
- `receipt.json`: recorded identities, verification results and cutover times;
- `RECOVERY.md`: this runbook.

These data have a concrete recovery role. They are not old application images.
The previous Docker image and its temporary archive have been removed. Fetch
this exact old image only if recovery is initiated:

```bash
docker pull stalwartlabs/stalwart@sha256:c429b311c93db5606598abc1c68225a85a6953183848ae01bee9c6a98885836c
```

Recovery is operator-directed. Recheck the active layout before using these
commands after any later configuration/storage change. Once v1 has served users,
do not replace its data with the cold 0.16 snapshot: that would lose later writes.
Use the official reverse copy into a new empty 0.16 store.

1. Stop only Stalwart gracefully (`docker stop --timeout -1 stalwart`).
2. Create `/srv/mail/stalwart-migration/rollback/{etc,lib,state}` as new empty
   directories owned by 2000:2000. Copy the original local store JSON from
   `source-v016/etc/config.json` into `rollback/etc/config.json`, changing only
   its `path` to `/var/lib/stalwart-rollback/`. Preserve the original tuning
   fields and use the latest active TLS files in the recovery configuration.
3. Run the exact official tool, which is fetched automatically when absent:

```bash
docker run --rm --name edge-stalwart-rollback --network none \
  --mount type=bind,src=/srv/mail/stalwart/etc,dst=/etc/stalwart-v1,readonly \
  --mount type=bind,src=/srv/mail/stalwart/lib,dst=/var/lib/stalwart-v1 \
  --mount type=bind,src=/srv/mail/stalwart-migration/state,dst=/var/lib/stalwart-migrate,readonly \
  --mount type=bind,src=/srv/mail/stalwart-migration/rollback/etc,dst=/etc/stalwart-rollback,readonly \
  --mount type=bind,src=/srv/mail/stalwart-migration/rollback/lib,dst=/var/lib/stalwart-rollback \
  --mount type=bind,src=/srv/mail/stalwart-migration/rollback/state,dst=/var/lib/stalwart-rollback-state \
  stalwartlabs/stalwart-migrate@sha256:37c2aaea4c4500d9cc9f39d67dbdbd5ccab42c4ea89a26f064f4f53941f58dd6 \
  rollback --source /etc/stalwart-v1/config.json \
  --target /etc/stalwart-rollback/config.json \
  --state /var/lib/stalwart-rollback-state \
  --forward-state /var/lib/stalwart-migrate --yes --verify-full
```

4. Require successful native verification and review the report. Do not use
   `--allow-errors`. Preserve the entire v1 store. Activate the reverse-copy
   data/config under the canonical host paths, with the old image pinned by
   the exact digest above. The restored Compose data mount must target
   `/var/lib/stalwart-rollback`, matching its local JSON. Recreate only Stalwart
   with `--no-deps --pull never`, then verify its version, TLS and authentication.
5. After a verified recovery, remove the replaced unused image through the
   existing `docker-service-images` mechanism.

Native rollback limitations: v1 queued outgoing mail, outbound report
aggregation, scheduled tasks and telemetry are not copied back. Preserve the
v1 store and account for them separately; do not claim lossless restoration of
these categories. The initial reverse rehearsal tested the copied account data
and settings, not an unforeseen production incident or future external stores.

Official contracts:
[upgrade](https://stalw.art/docs/install/upgrade/),
[migration](https://stalw.art/docs/migration/upgrade-0-16/),
[rollback](https://stalw.art/docs/migration/upgrade-0-16/rollback/).
