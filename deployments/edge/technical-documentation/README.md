# TechnicalDocumentationSync

Daily source monitoring, original PDF replacement and compact HTML catalogue
maintenance followed by sequential PDF cleanup. Deployed and verified on
2026-10-05; this is a post-infrastructure operator automation. Its published
child is LenovoPdfCleanup (ENo9jFkwcE4PFOyL).

- Workflow: https://n8n.escloud.us/workflow/QouVaVNhAqSiYq5D
- Schedule: daily at 07:00, workflow timezone `Europe/Minsk` (UTC+3).
- Sources: Lenovo ASP catalogues and configured Lenovo Press PDFs for nine model
  collections; the enabled source definitions are in `models.json`.
- Model folders: WR3220 G5, WR5215 G5, WR5220 G3, WR5220 G5, WR5225 G3,
  WR6220 G5, WA5480 G5, WA5680 G5 and WA5685 G5. WR5220/WR5228 and
  WA5480/WA5488 paired model groups use the primary model's folder.
- Files: `/srv/cloud/technical-documentation/lenovo/originals/<model>/`.
- Index: `/srv/cloud/technical-documentation/lenovo/originals/INDEX.html`.
- Existing `INDEX.md` remains unchanged.

## Mechanism

The workflow uses 17 native nodes: schedule/manual triggers, seven HTTP actions,
five Code nodes, one PDF loop, one filename-change branch and one child-workflow
call. All nodes serve source comparison, replacement, index update or cleanup.
Three native canvas groups show source comparison, original downloads and
INDEX.html followed by cleanup, without additional executing nodes. It has no
backup, notification, separate database, Data Table, SSH executor or host service.

`Read INDEX → Models and Index → Read Lenovo ASP → Latest Document Families →
Read Remote Version → Changed Documents` identifies work. The loop downloads
one PDF, uploads it through Nextcloud and deletes its previous filename only
after the new upload succeeds. Completed records are merged into INDEX.html
once, after the loop, with changed records marked as awaiting cleanup. Then
Clean Saved PDFs calls LenovoPdfCleanup once with the saved relative paths and
optional previous filenames, waiting for its sequential processing. The original
index is already visible while cleanup runs. A zero-change run stops before any
download, write or cleanup call.

ASP records are grouped by document family and the latest catalogue date wins.
The observed LXPM duplicates and equivalent BMC G3/G5 event-reference editions
are explicitly handled. The BMC alias applies only to that confirmed family.
New families are added automatically. Short display titles already stored in
the index remain stable across revisions; known family labels are configured
once in `Models and Index`. Other new families initially use the source title.
WR5225 G3 BIOS families retain their Genoa/Turin platform suffix and remove
only the revision number, so those two manuals update independently.

Version state is `remote_validator` inside the existing `catalog-data` JSON
block in INDEX.html. Comparison uses source URL/date and ETag, with
Last-Modified/content-length fallback for Lenovo Press. The marker saved after
transfer comes from the actual GET response. Changed PDFs have their old
edition/page-count metadata reset to unknown rather than retaining stale values.
Date, size, source URL, actual filename and save time are updated automatically.
Both JavaScript catalogue data and the no-JavaScript folder list are regenerated.

On a source update, cleanup_status becomes pending and cleaned_at/cleaned_path
are cleared. The child saves a completion marker after each successful cleaned
PDF publication. The collapsed Сведения displays status, completion date and
the relative link to cleaned/<model>/<vendor filename>.pdf. Other documents'
markers survive source updates. INDEX.html itself stores this state; no separate
database, sidecar or extra catalogue page is introduced.

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

A cleanup failure does not undo saved originals or delay the original index.
Rerun the cleanup workflow with the affected paths; there is no added automatic
cleanup retry queue. The source monitor does not re-download an unchanged source
version merely to retry pending cleanup. Existing unchanged PDFs are not
automatically bulk-cleaned.

## Adding models

The [2026-10-05 source audit](source-audit-2026-10-05.md) lists candidate PDFs
for eight additional model groups, sorted by model and document type, with
download links, catalogue dates and duplicate/older-edition exclusions.
[Machine-readable source evidence](source-audit-2026-10-05.json) accompanies it.
That report records the read-only discovery step. The operator subsequently
authorized enabling all eight groups in this same workflow, including the
additional SAP certification reference listed for WR5220 G5.

Create the model folders once through Nextcloud under originals, cleaned and
translated/en and translated/ru. Append a model object in `models.json`:
`folder`, Lenovo ASP `fullGuid`, optional `press` PDFs and stable `labels`.
`build.py` embeds this configuration into `Models and Index`; no runtime file
dependency is added to n8n. The model folder is part of every document key/path,
so shared manuals remain independent between model collections. No additional
workflow nodes are needed. The monitor writes originals and INDEX.html; its
cleanup child writes cleaned copies in the same model structure. Translation
remains future work.

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

The operator-authorized eight-model expansion added 63 PDFs in execution 11657
and updated INDEX.html to 78 documents across nine collections. All 63 uploads
returned HTTP 201 and the index PUT returned HTTP 204. Published production run
11773 found zero changes and performed no downloads or writes. Filesystem and
authenticated Nextcloud listings agree on every model filename/count; PDF
signatures and sizes agree with the index, and shared source copies have equal
hashes. All fifteen pre-existing WR5220 G3 PDFs and INDEX.md remain byte-identical.
Thirty-two model directories were created through WebDAV, including empty
cleaned/en/ru output folders. Only the model configuration and document-family
code changed; the workflow still has sixteen nodes and the same credentials
and daily schedule at that expansion checkpoint. Recovery can use the previous native version
`4949672a-7e59-47e2-9977-0883df390ad6` and the prior repository definition;
downloaded originals remain persistent data. Evidence: `model-expansion-evidence.json`.

An initial assistant text-field error and an installed HTTP Request raw/text
response incompatibility were corrected. The index PUT now uses native response
`autodetect`, verified against the actual empty HTTP 204 response. The transient
verification connection was removed before publication.

The subsequent cleanup integration is recorded in
../pdf-cleanup/integration-evidence.json. Native parent execution 12015 saved
two current source PDFs, PUT INDEX.html, then called child 12016 once and waited
for both cleaned outputs and completion markers. Published run 12020 found zero
changes and performed no downloads, index writes or cleanup calls. All 78 original
hashes and INDEX.md remained unchanged. Both workflows have 17 executing nodes
and three native canvas groups; credentials, model configuration and schedule
are unchanged. Original-only workflow version
af23c9a9-9b54-495f-b684-f6e37f7b7163 remains native historical recovery state.

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
`test-fixtures-models.json` contains the nine fresh model catalogues used to
verify the expansion. `model-expansion-evidence.json` records the first sync,
the published no-change run and filesystem/WebDAV verification.

Authoritative mechanisms:

- [n8n Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [n8n Code node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Nextcloud WebDAV operations](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html)

The Lenovo ASP endpoint is the site's observed internal API; a published
compatibility contract is unknown. The automation uses the confirmed anonymous
GET response of the current site. Cleanup is integrated through the existing
standalone CLI; translation remains separate work.
