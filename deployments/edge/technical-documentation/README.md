# TechnicalDocumentationSync01

Daily source monitoring, original PDF replacement and compact HTML catalogue
maintenance. Deployed and verified on 2026-10-05; this is a post-infrastructure
operator automation, independent of the unpublished PDF cleanup candidate.

- Workflow: https://n8n.escloud.us/workflow/QouVaVNhAqSiYq5D
- Schedule: daily at 07:00, workflow timezone `Europe/Minsk` (UTC+3).
- Sources: Lenovo ASP WR5220 G3 / WR5228 G3 catalogue and Lenovo Press LP1705.
- Current model folder: `WR5220 G3`.
- Files: `/srv/cloud/technical-documentation/lenovo/originals/WR5220 G3/`.
- Index: `/srv/cloud/technical-documentation/lenovo/originals/INDEX.html`.
- Existing `INDEX.md` remains unchanged.

## Mechanism

The workflow uses 16 native nodes: schedule/manual triggers, seven HTTP actions,
five Code nodes, one PDF loop and one filename-change branch. All nodes serve
the requested source comparison, file replacement or index update. It has no
backup, notification, separate database, Data Table, SSH executor or host service.

`Read INDEX → Models and Index → Read Lenovo ASP → Latest Document Families →
Read Remote Version → Changed Documents` identifies work. The loop downloads
one PDF, uploads it through Nextcloud and deletes its previous filename only
after the new upload succeeds. Completed records are merged into INDEX.html
once, after the loop. A zero-change run stops before any download or write.

ASP records are grouped by document family and the latest catalogue date wins.
The observed LXPM duplicates and equivalent BMC G3/G5 event-reference editions
are explicitly handled. The BMC alias applies only to that confirmed family.
New families are added automatically. Short display titles already stored in
the index remain stable across revisions; known family labels are configured
once in `Models and Index`. Other new families initially use the source title.

Version state is `remote_validator` inside the existing `catalog-data` JSON
block in INDEX.html. Comparison uses source URL/date and ETag, with
Last-Modified/content-length fallback for Lenovo Press. The marker saved after
transfer comes from the actual GET response. Changed PDFs have their old
edition/page-count metadata reset to unknown rather than retaining stale values.
Date, size, source URL, actual filename and save time are updated automatically.
Both JavaScript catalogue data and the no-JavaScript folder list are regenerated.

All writes use the existing encrypted `Nextcloud - operator automation`
credential (`6MEdI2Cs7tEUiM7o`) and native WebDAV. No direct filesystem write or
`occ files:scan` is involved. Same-name updates overwrite through PUT; renamed
revisions use PUT followed by DELETE. A missing old filename (404) is harmless
on a retry; other deletion errors stop the workflow. Disappearance from the
website alone does not remove a local document.

If a transfer fails, the native HTTP node stops execution and the pending
version is not recorded in the index. A subsequent daily/manual run retries
it. There is no added retry controller or queue. Files transferred before a
later index-write failure can be transferred again on that retry.

## Adding models

Create the model folder once through Nextcloud and append a model object in
`Models and Index`: `folder`, Lenovo ASP `fullGuid`, optional `press` PDFs and
stable `labels`. The model folder is part of every document key/path, so shared
manuals remain independent between model collections. No other workflow nodes
need to change. Currently only WR5220 G3 is enabled.

The current legacy WebDAV endpoint does not register Nextcloud's modern
Auto-Mkcol plugin. Do not assume that an auto-folder header works on this path.
Folder creation during model onboarding keeps the daily workflow unchanged.

## Verification and recovery

The initial source-byte audit established validators for twelve existing PDFs.
The first sync added BIOS Setup Spec, PSU Label Matrix and VMware Code Recipe:
the physical folder and HTML index both contain fifteen current documents.
Their hashes match the earlier source audit, and all twelve previous PDFs and
INDEX.md remain byte-identical. A full manual and published production run both
returned zero changes, without file or index writes.

The filename-change branch and index merge passed a native n8n test with pinned
v19 input. That test makes no external writes and persists no workflow pin data.
Offline tests also cover source duplicates, same-URL ETag changes, stable labels,
model isolation and HTML escaping. Sanitized execution evidence: `evidence.json`.

An initial assistant text-field error and an installed HTTP Request raw/text
response incompatibility were corrected. The index PUT now uses native response
`autodetect`, verified against the actual empty HTTP 204 response. The transient
verification connection was removed before publication.

`TechnicalDocumentationSync01.json` is the read-back deployed definition,
including settings, node layout and existing credential references.
`build.py` produces the SDK definition. After SDK creation, explicitly bind the
four Nextcloud HTTP nodes to the existing credential and set workflow timezone
`Europe/Minsk`; the MCP SDK creation does not auto-assign HTTP credentials.
Republish the tested definition after changes. Recovery uses that definition,
the current INDEX.html state and the already accepted platform recovery system.
No task-specific backup was introduced.

To regenerate/validate the source locally, run `build.py --validation-output`
with a temporary JSON path and pass its containing directory to `test-logic.js`.
`test-fixtures.json` contains fixed, public source/catalogue data for those tests.

Authoritative mechanisms:

- [n8n Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [n8n Code node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Nextcloud WebDAV operations](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html)

The Lenovo ASP endpoint is the site's observed internal API; a published
compatibility contract is unknown. The automation uses the confirmed anonymous
GET response of the current site. Cleanup and translation remain separate work.
