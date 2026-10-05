# Lenovo PDF cleanup on edge

Status 2026-10-05: **DEPLOYED / VERIFIED**. This supersedes the earlier unpublished,
single-filename candidate. Current integration evidence: integration-evidence.json.

## Placement and runtime

| Purpose | Path |
| --- | --- |
| Originals | /srv/cloud/technical-documentation/lenovo/originals/<model>/<vendor filename>.pdf |
| Cleaned copies | /srv/cloud/technical-documentation/lenovo/cleaned/<model>/<vendor filename>.pdf |
| Translations | /srv/cloud/technical-documentation/lenovo/translated/{en,ru}/<model>/ |
| CLI and adapter | /opt/pdf-cleanup/run and /opt/pdf-cleanup/job-command.py |
| Temporary processing | /tmp/pdf-cleanup-<random>/ |

All persistent cloud writes use native Nextcloud WebDAV, reusing the existing
Nextcloud and edge SSH credentials. Nextcloud owns these files as www-data 33:33.
Model directories are created once through Nextcloud during onboarding. No direct
insertion, files:scan, new credential, service, n8n mount or allowlist is needed.

Source was imported from Eugene-SN/documentation-ai
46f179e9e5c83ff2c12b7ba084efef124afaf338. The imported package with its portable
originals guard and three guard tests is executable commit
8257cb36be7856a0abe89ea27562f847fcf45a8e; no upstream merge.
Package 0.1.3 uses Python 3.14.8, PyMuPDF 1.28.2 and pypdf 6.19.0 in one-shot
Docker image edge/pdf-cleanup:8257cb36be78. Identities are in deployment.json.
This integration does not modify the image, algorithm, launcher or adapter.

## Autonomous CLI and originals protection

The package command is **pdf-cleanup INPUT.pdf OUTPUT.pdf [--dry-run]**.
It works independently of n8n, Nextcloud and the job adapter. The CLI owns PDF
parsing, source/output validation, original hashes, alias/existing-output
protection and atomic publication. Validation checks page count/geometry, native
body content, images, vectors, bookmarks and unaffected annotations.

PDF_CLEANUP_ORIGINALS_DIR resolves to the agreed originals tree; cleanup output
inside that tree is forbidden. This allows the authorized source monitor to
replace originals without allowing cleanup to write there. The launcher runs as
core 1000:1000, mounts the temporary snapshot read-only and output/tmp writable,
and does not mount the authoritative originals tree. Internal source.pdf and
cleaned.pdf are temporary technical names; no vendor document is configured.

## Universal n8n input

[LenovoPdfCleanup](https://n8n.escloud.us/workflow/ENo9jFkwcE4PFOyL)
is published in the operator's personal project. Its single Subworkflow Input
declares an array named files:

```json
{"files":[
  {"path":"Model A/manual-v2.pdf","previous_path":"Model A/manual-v1.pdf"},
  {"path":"Model B/guide.pdf"}
]}
```

Paths are relative to originals. The same relative path is used under cleaned;
spaces, Unicode and nested directories are URL-encoded component by component.
There is no default document or filename and no Manual Start with sample input.
Optional previous_path identifies a different filename in the same directory.
The old cleaned filename is removed only after the new cleaned PDF is saved.
A missing old file (404) is harmless. CLI --dry-run remains independent.

## Node review and visual layout

The workflow has 17 executing nodes, grouped into three native canvas groups.
Groups add no executing nodes. Input, path preparation and the one-PDF loop
precede the grouped operations.

| Node | Required operation |
| --- | --- |
| Subworkflow Input | Receive the caller's files array |
| Normalize Request | Expand the list and construct confined original/cleaned paths |
| Each PDF | Process one file at a time |
| Download Original Snapshot | GET the original through Nextcloud |
| Create Temporary Job | Create the CLI workspace on edge |
| Capture Job | Restore PDF binary data after the SSH command and attach its workspace |
| Upload Working Copy | Transfer the snapshot to edge through native SSH |
| Run PDF Cleanup CLI | Invoke the existing standalone CLI |
| CLI Succeeded | Skip publication if processing failed |
| Download Cleaned PDF | Read the CLI output through native SSH |
| Publish Cleaned PDF | PUT the output under the corresponding model directory |
| Previous Cleaned Filename | Select deletion only when an older filename exists and upload succeeded |
| Remove Previous Cleaned PDF | DELETE that older derived filename |
| Remove Temporary Job | Remove the exact processing workspace |
| Read Cleanup INDEX | Read current catalogue state, preserving earlier completed-file markers |
| Return Result | Report transport/CLI failures, then mark successful publication |
| Save Cleanup INDEX | Persist the successful file's completion marker |

SSH execute returns stdout/exit code and does not carry input binary data forward;
the installed Ssh.node.js confirms why Capture Job remains necessary.
The two If nodes control operations, not PDF content validation.
The Code nodes prepare paths/binary data and the result/catalogue record.
There are no repeated PDF validators, external hash/ETag nodes, sidecars,
separate finalizer, backup, queue or notification workflow.

Canvas stages are **Рабочая копия PDF**, **Очистка и сохранение** and
**Отметка в INDEX.html**. The earlier 13-node candidate handled one fixed
filename: removing its manual trigger and adding a list loop, old-derived-file
replacement and index updates results in 17 nodes for the accepted functionality.

## Caller and completion markers

TechnicalDocumentationSync first downloads **all** changed originals and saves
INDEX.html. Only then does Clean Saved PDFs call this workflow once with their
files list, waiting for sequential cleanup. Original catalogue visibility does
not wait for cleanup.

A source update sets cleanup_status=pending and clears cleaned_at/cleaned_path.
After each successful cleaned PUT, the child writes cleanup_status=cleaned,
cleaned_at and the relative cleaned_path into the existing catalog-data JSON.
The collapsed **Сведения** shows status, completion date and a cleaned-PDF link.
Other records and the compact folder overview are retained; INDEX.md is untouched.

Successful markers are saved per file. A later handled processing/publication
error does not erase preceding markers. It stops the caller after original
downloads and the original index are already saved. There is no automatic
cleanup retry queue: rerun cleanup with the affected paths; the source monitor
does not re-download an unchanged version solely because cleanup is pending.
Existing documents are not automatically bulk-cleaned by this integration.

## Verification and recovery

- SDK/native workflow validation: 17 nodes, no warnings; three native groups.
- Logic tests cover relative paths, Unicode URLs, lists, revision deletion only
  after upload, marker preservation and CLI/upload/removal failures.
- Native execution 11976 cleaned two real PDFs in different model directories.
- Native execution 12000 rejected traversal before file operations.
- Caller execution 12015 downloaded those two current source PDFs, saved INDEX,
  invoked child 12016 once and waited for both cleaned copies and markers.
- Published source-monitor run 12020 found zero changes: no download, cleanup
  invocation or index write.
- All 78 original hashes and INDEX.md stayed unchanged. CLI/adapter/launcher
  hashes stayed unchanged; temporary jobs and cleanup containers are absent.
- Browser verification confirms nine-folder overview, collapsed Сведения,
  completion text/date and correctly encoded relative cleaned link.

Only two PDFs were processed in these integration tests, not all 78 documents.
Earlier package/guard/render checks are historical evidence in test-evidence.json;
optimization-evidence.json and simplification-evidence.json describe superseded
graphs. The unchanged image passed eleven upstream and three guard tests.
The original all-page render comparison covers one document and is not proof
of correct classification for every future PDF layout.

Handled processing/transfer failures remove the job. Forced cancellation, host
failure or SSH loss can leave one; inspect its marker/container before exact
removal. The workflow processes its downloaded snapshot; same-document concurrent
source changes are not checked, and simultaneous callers should be avoided.

LenovoPdfCleanup01.ts is the generated SDK source; LenovoPdfCleanup01.json is the
current unpinned definition, including native group metadata and credential
references. The retained artifact basename does not set the live workflow name.
build-workflow.py regenerates the graph and syntax-checks embedded languages.
Native version history and the Git definitions provide workflow recovery.
The CLI source/runtime manifest describes rebuild recovery; use the existing
accepted backup mechanism for persistent documents. Preserve originals.
There are no ad-hoc production rollback copies, OCR or translation changes.

Authoritative node mechanisms:
[n8n SSH](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.ssh/),
[HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/),
[Execute Sub-workflow](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/).

## WA G3 onboarding runtime corrections

The new WA7780 G3 user guide exposed the missing upstream-supported pypdf AES
dependency. The Docker build now requests `pypdf[crypto]` (cryptography 50.0.2)
while retaining Python 3.14.8, PyMuPDF 1.28.2, pypdf 6.19.0 and package 0.1.3.
The imported upstream commit, portable originals guard and core source bytes
are unchanged. The canonical image tag is retained; deployment.json records
the rebuilt image identity. All fourteen upstream/edge guard tests passed.

An actual Redfish timeout also exposed a cancellation defect: killing the core
launcher did not terminate the root-owned sudo/Docker client, whose output pipe
kept the adapter waiting. The existing 900-second limit is retained. The timeout
branch now stops its exact `pdf-cleanup-<execution_id>` container through Docker
before collecting the process result. A live test shortened only the harness
wait to two seconds: it returned timeout in 7.31 seconds, removed its container,
kept the snapshot hash unchanged and released its temporary job. No workflow
node, service, retry queue or backup is added. Docker stop semantics were checked
against the installed CLI help and official Docker documentation.

The current CLI can reject ambiguous pagination/table overlaps. Such rejection
preserves the original and does not publish a cleaned PDF or completion marker;
no content-protection check is weakened during model onboarding. Final source,
execution and publication evidence is under technical-documentation/
`wa-g3-expansion-evidence.json`.

Expanded isolated quality research (no production deployment):
[2026-10-05 report](../../../PDF_CLEANUP_QUALITY_RESEARCH_2026-10-05.md)
and [research artifacts](quality-research-2026-10-05/README.md).
The experiments expose pagination-classification and independent-rendering
limitations. The candidate patch is not a production acceptance or a replacement
for the installed source described above.
