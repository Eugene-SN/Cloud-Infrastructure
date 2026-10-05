# Technical documentation cleanup integration — 2026-10-05

Status: **DEPLOYED / VERIFIED**, within the operator-authorized application
workflow scope. This does not open or accept a new finite infrastructure stage;
the accepted infrastructure checkpoint remains Stage 13.

## Operator decisions and final behavior

The operator requested a universal cleanup input without a configured PDF name,
followed by integration into TechnicalDocumentationSync. The final selected
sequence supersedes background/per-file interleaving proposals:

1. Download every changed original.
2. Save INDEX.html immediately with awaiting-cleanup markers.
3. Call LenovoPdfCleanup once with the saved paths and wait while it processes
   the files sequentially.
4. After each successful cleaned-file publication, update its completion marker
   in the collapsed Сведения menu.

Original and cleaned directories mirror model paths under
/srv/cloud/technical-documentation/lenovo/{originals,cleaned}/. Vendor filenames
are retained. On a renamed revision, each old original/cleaned filename is
removed only after its corresponding replacement upload succeeds. INDEX.md and
translated output are unchanged.

The accepted input is files: an array of relative path objects, with optional
previous_path for a renamed revision. There is no sample document, filename
default, manual cleanup trigger, new credential or controller service.

## Node review and layout

Both workflows have 17 executing nodes and three native canvas groups.
TechnicalDocumentationSync adds one Execute Sub-workflow after its existing
Save INDEX node. Its model configuration, daily 07:00 Europe/Minsk schedule and
source comparison are unchanged.

LenovoPdfCleanup groups snapshot preparation, CLI/publication, and completion
markers. Original validation stays in the autonomous CLI. The SSH node source
on the deployed n8n 2.40.7 confirms that command output drops input binary, making
the snapshot reattachment Code node necessary. The two If nodes control failed
processing and optional previous-name deletion. Native groups and aligned node
positions add no executing tiles, services or new abstraction workflows.

## Evidence

- Native SDK validation passed without warnings.
- Execution11976: two real PDFs from different model folders processed serially,
  published through Nextcloud, and marked cleaned individually.
- Execution12000: invalid traversal input rejected before file/job operations.
- Parent12015 and child12016: two actual source downloads/overwrites returned
  HTTP204; INDEX PUT completed before the single child call; the parent waited
  for both cleaned PUTs and completion markers.
- Published run12020: zero changed documents; no download, index write or cleanup
  call.
- Filesystem audit: 78 unchanged original PDF hashes, nine model folders,
  unchanged INDEX.md, two cleaned PDFs and matching completion paths/dates.
- CLI, launcher and adapter hashes stayed unchanged. n8n is healthy; Nextcloud
  35.0.1 has maintenance=false and needsDbUpgrade=false.
- Browser check: nine-folder overview, collapsed Сведения, completion text/date,
  encoded cleaned link. No extra columns were added to the compact overview.
- No processing job or one-shot cleanup container remains.

Published versions:
- LenovoPdfCleanup (ENo9jFkwcE4PFOyL):
  382fc37d-61ec-4311-8c80-0bcb774a2221.
- TechnicalDocumentationSync (QouVaVNhAqSiYq5D):
  53999b07-1a21-4dd2-8aef-2ec2bb43e29b.

Source, current unpinned exports, tests, runtime manifest and sanitized evidence:
deployments/edge/pdf-cleanup/ and deployments/edge/technical-documentation/.
Detailed results: deployments/edge/pdf-cleanup/integration-evidence.json.

## Limits and recovery

Only two existing PDFs were processed for verification; the remaining unchanged
documents are not implicitly scheduled for bulk cleanup. Successful per-file
markers survive a later handled failure. Cleanup failure leaves the already
saved originals/index available; rerun cleanup with the affected paths.
There is no automatic retry queue for cleanup of an unchanged source version.

The caller sequences files within one execution. Concurrent manual/daily runs
on the same document are not guarded. Forced cancellation or SSH loss can leave
a temporary job, whose execution marker must be inspected before exact removal.

Recover definitions from native version history or the Git exports. The previous
original-only monitor version af23c9a9-9b54-495f-b684-f6e37f7b7163 remains native
history. The unchanged CLI has its recorded source/image/guard manifest and the
accepted backup mechanism; no ad-hoc production rollback copy was added.
Preserve originals and unrelated workflows. No OCR or translation was deployed.
