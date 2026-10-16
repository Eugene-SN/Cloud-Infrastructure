# PDF Cleanup on edge

Status 2026-10-16: **DEPLOYED / VERIFIED**. One persistent on-demand container.
Current record: [acceptance](../../../PDF_CLEANUP_NAMED_CONTAINER_2026-10-16.md).
Evidence: [named-container-2026-10-16](named-container-2026-10-16/README.md).

## Runtime and paths

| Component | Current contract |
| --- | --- |
| Container | `pdf-cleanup`; normally `exited`, started only for an explicit job |
| Image | `edge/pdf-cleanup:9c9bbb375751-standalone`; exact installed ID in deployment.json |
| Runtime configuration | `/opt/pdf-cleanup/compose.yaml` |
| Single adapter | `/opt/pdf-cleanup/job-command.py`; host controller and container CLI entry point |
| Originals | `/srv/cloud/technical-documentation/lenovo/originals` mounted at `/originals:ro` |
| Workspace | `/opt/pdf-cleanup/work` mounted at `/work:rw`; core 1000:1000, mode 0700 |
| Job request / output | `/work/job.json` and `/work/cleaned.pdf`, removed after publication or a handled failure |
| Parser temporary files | `/tmp` tmpfs; cleared when the container stops |
| Publication | Existing n8n Nextcloud WebDAV into `cleaned/<model>/<vendor filename>.pdf` |

The existing image, Python 3.14.8, PyMuPDF 1.28.2, pypdf 6.19.0,
cryptography 50.0.2, fontTools 4.66.1, cffi 2.1.1 and pycparser 3.0 are unchanged.
Source remains 9c9bbb375751f85ca1e6f737504f3e99a68fd3d5, package 0.1.3.
Installed dependencies stay in the image between jobs. Ordinary workflow runs
neither build/pull an image nor install/remove packages.

Compose creates the named container once. The adapter uses native
`docker start --attach pdf-cleanup`; the installed CLI processes one requested
PDF and exits. There is no idle daemon, new API, queue, scheduler, Docker network
or public port. Restart policy is no, automatic removal is disabled, and the
container ID remains unchanged across successful, failed and timed-out jobs.
The container root filesystem is read-only; temporary data belongs in work/tmpfs.
The manifest records the installed image; it is no longer a per-job image selector.

Existing originals are readable by UID 1000 through the read-only mount; their
ownership/permissions were not modified. The CLI's originals-output guard remains
active with PDF_CLEANUP_ORIGINALS_DIR=/originals. Input hash/content validation
remains inside the unchanged CLI. It reads the original directly; the existing
parent downloads all changed originals before invoking cleanup.

## Workflow

[LenovoPdfCleanup](https://n8n.escloud.us/workflow/ENo9jFkwcE4PFOyL)
has 13 nodes / two groups. Its published version is
5b174000-7fd8-4c01-887e-d944cd2398ba. The input remains:

```json
{"files":[{"path":"Model/manual.pdf","previous_path":"Model/old-manual.pdf"}]}
```

Paths are relative PDFs beneath originals. previous_path is optional and must
name a different PDF in the same folder. No document name is configured in the
workflow. Invalid/traversal paths are rejected before processing. The current
caller, TechnicalDocumentationSync, retains its existing graph, publication and
schedule: download all changed originals, save INDEX, invoke this child once with
the list, and process it sequentially. Unchanged files do not trigger cleanup.

Flow: validate input → loop over PDFs → adapter starts the named container →
download its result through native SSH → publish through native Nextcloud WebDAV
→ remove an obsolete cleaned filename only after successful replacement → clear
workspace → update the existing INDEX.html completion fields → next PDF.

Removed: Download Original Snapshot, Create Temporary Job, Capture Job and Upload
Working Copy. The original is no longer downloaded from Nextcloud and uploaded
back to edge for processing. The old separate run launcher, random job directories
and per-execution Docker container creation/removal are retired.

Two canvas groups describe processing/publication/workspace cleanup and INDEX
completion. Return Result reports success only after CLI validation, publication,
optional prior-derived-file deletion and workspace release succeed. Handled errors
leave preceding successful markers and the caller's downloaded originals/index
available. Read/save INDEX occur after workspace release. No retry queue is added.

## Adapter lifecycle and recovery

The host entry takes base64 JSON with action=process, execution_id and relative
path. It writes the fixed request, attaches to the existing container, returns
its JSON report and leaves the output for the workflow's SSH download. The release
action clears workspace contents without deleting the mount root or dependencies.
A pending request rejects a second caller until release; the workflow is sequential.

The existing processing limit is 900 seconds. On timeout or an interruption caught
by the adapter, stop the container before waiting for the root-owned Docker client,
then clear workspace. A controlled timeout verified this path in 6.34 seconds;
a subsequent native n8n run succeeded using the same container ID. The container
also exits on a CLI error, and failed processing removes its temporary output.

A host outage or forced cancellation between processing and publication can leave
an unconsumed result. Inspect the stopped container and job marker, then release
that execution through the adapter before retrying. There is no background cleanup
service. The next successful publication owns the normal output cleanup.

Restore source/runtime configuration through the existing Backrest edge-state /opt
coverage. Restore the Dockerfile, runtime-requirements.txt, .dockerignore, adapter,
Compose and manifest from Git; preserve the canonical source Git under
/opt/pdf-cleanup/source. If the image is missing, rebuild from the recorded Python
base and dependency versions and verify it before creating the container. Native
Compose config validates the runtime file. Create with no build/pull against the
installed image, without starting an idle process. Image/config updates require
recreating this one container once; ordinary jobs only start and stop it.

## Verification and history

Native SDK validation and atomic workflow update passed without warnings. Real
n8n execution 45688 processed three PDFs and published all three with INDEX updates.
All PDF objects/decoded streams match accepted outputs, excluding regenerated
XRef trailer IDs. Controlled publication failure 45691 cleaned the workspace and
left INDEX unchanged. Recovery execution 45701 passed after the timeout test.
Invalid/missing paths, cross-execution release protection and unchanged source
hashes are covered by tests/readback. No temporary test workflow was created.

The unchanged algorithm's full-catalogue baseline is
[2026-10-05](../../../PDF_CLEANUP_PRODUCTION_ACCEPTANCE_2026-10-05.md).
Independent image build evidence is
[2026-10-16](../../../PDF_CLEANUP_STANDALONE_BUILD_2026-10-16.md).
Those dated records retain their historical lifecycle/configuration identities;
the current named-container record supersedes per-execution runtime instructions.
