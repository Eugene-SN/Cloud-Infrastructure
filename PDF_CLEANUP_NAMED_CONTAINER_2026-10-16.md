# PDF Cleanup: one persistent on-demand container

2026-10-16, Europe/Moscow. **DEPLOYED / VERIFIED**.
Operator-authorized post-infrastructure change; Stage 13 remains accepted.

## Request and resulting architecture

The operator explicitly chose one named container with fixed paths, started on
demand and stopped after processing, retaining dependencies and removing temporary
files. This supersedes the former per-execution container/job-directory lifecycle.
The earlier independent image build remains valid; a workflow run does not rebuild
or download the image, install packages, or create a container.

`pdf-cleanup` uses the existing image
`edge/pdf-cleanup:9c9bbb375751-standalone`, ID
`sha256:d7fe7e73d422ed59128f4dfe889fb90e8c299fa70df42b6024c65c3087ec6be3`.
Container ID throughout creation, repeated runs, failures and recovery:
`4d300f6e8fda774c107531fa11a124ac7cfca8b73cb8b6fb13cd8aa84db4329e`.
Normal idle state is `exited`; automatic removal/restart are disabled.

Canonical configuration: `/opt/pdf-cleanup/compose.yaml`. UID/GID 1000:1000,
read-only root filesystem, no network/port, no idle daemon/API/queue. Fixed mounts:

| Host | Container | Purpose |
| --- | --- | --- |
| `/srv/cloud/technical-documentation/lenovo/originals` | `/originals:ro` | Read already downloaded originals directly |
| `/opt/pdf-cleanup/work` | `/work:rw` | Fixed request/output; contents cleared after use |
| `/opt/pdf-cleanup/job-command.py` | `/app/job-command.py:ro` | Single host adapter/container CLI entry point |
| tmpfs | `/tmp` | Parser temporary data, removed on stop |

The workspace mount root remains core-owned, mode 0700, and empty when released.
Existing originals' ownership/permissions did not change. Installed packages and
source commit `9c9bbb375751f85ca1e6f737504f3e99a68fd3d5` remain unchanged.

## Execution, workflow and removed components

The adapter writes `/work/job.json`, invokes native `docker start --attach
pdf-cleanup`, validates the current exit status/CLI JSON/output, then leaves
`/work/cleaned.pdf` for n8n's existing SSH download. The CLI exits after the PDF.
n8n publishes through native Nextcloud WebDAV and releases workspace contents.
This keeps Nextcloud publication/cache handling in its existing supported path.
The request marker rejects a pending second job; different executions cannot
release each other's output. The workflow processes its batch sequentially.

Published `LenovoPdfCleanup` (`ENo9jFkwcE4PFOyL`) now has 13 nodes / two groups,
down from 17 nodes / three groups. Draft and published version both equal
`5b174000-7fd8-4c01-887e-d944cd2398ba`. Native SDK validation passed, followed
by an atomic 26-operation update without warnings or credential changes.

Removed nodes: Download Original Snapshot, Create Temporary Job, Capture Job,
Upload Working Copy. Remove Temporary Job became Clear Workspace. Retired the
separate `/opt/pdf-cleanup/run` launcher and its repository copy, random work
directories, duplicate original transfers and per-job Docker creation/removal.
No new background service, workflow clone, trigger, network or volume was added.

Input remains `files:[{path,previous_path?}]`. The parent
TechnicalDocumentationSync (`QouVaVNhAqSiYq5D`) and its published version,
nodes/connections/settings are unchanged. Its existing download-all → save INDEX
→ cleanup-list contract remains. Existing previous-filename deletion runs only
after replacement publication; completion is recorded only after CLI,
publication, optional deletion and workspace cleanup succeed.

The 900-second processing timeout remains. Timeout/interruption handling stops
the container before waiting for its root-owned attached Docker client, then
clears the workspace. A host outage or forced cancellation between processing
and publication can leave an unconsumed result: inspect the stopped container
and request marker, then release that execution before retrying. No cleanup
daemon was introduced to conceal that recovery boundary.

## Verification

| Check | Observed result |
| --- | --- |
| Adapter boundaries | Three tests passed: invalid paths before IO, cross-execution release rejection, retired create action rejection |
| Real adapter smoke | PDF processed/released; fixed mounts, retained container ID |
| Invalid/missing inputs | Rejected, no temporary output left |
| Native n8n execution 45688 | Success, three real PDFs, real SSH/WebDAV publication and INDEX updates |
| PDF equivalence | All 255 objects and decoded streams / six pages match previously accepted outputs, excluding regenerated XRef trailer IDs |
| Controlled publication failure 45691 | Expected workflow error; workspace empty and INDEX hash unchanged |
| Controlled timeout | Test-only 1-second limit; stopped/reaped in 6.34 seconds, expected exit 137, no OOM, workspace empty |
| Recovery execution 45701 | Native n8n success after timeout, same container, exit 0, workspace empty |
| Production comparison | Same 192 file paths; all 95 original PDFs unchanged; only three intended cleaned PDFs and INDEX.html changed |
| Final runtime | One PDF container, stopped/exit 0; installed runtime files equal Git sources; no old launcher; source Git clean |
| Non-regression | n8n healthy; native Nextcloud status installed, no maintenance/DB upgrade; infrastructure containers remain running |

Success inputs: `WA5680 G5/lp2506.pdf`, `WA5685 G5/lp2507.pdf`,
`WR6220 G5/lp2502.pdf`. No full-catalogue rerun is claimed for this lifecycle
change. Prior independent image-build verification and full-catalogue algorithm
acceptance remain separate dated evidence.

Tests used the installed native n8n test_workflow mechanism: only the subworkflow
trigger was pinned for real success/recovery runs; the fault test additionally
pinned the publication response to controlled HTTP 503. No live credentials,
production fault, temporary test workflow or permanent pinned node was introduced.
Execution history deliberately retains the successful runs and expected fault.
Evidence exports omit HTTP cookies/headers and binary content.

One PDF-comparison verifier initially compared dictionary string representations,
producing a false mismatch; canonical recursive dictionary comparison corrected
that verifier. An oversized raw execution export was replaced with compact node
summaries. These were assistant verification/export defects, not runtime failures.

## Recovery, cleanup and documentation

Existing Backrest `/opt` coverage plus source Git, recorded Dockerfile/dependencies,
Compose and adapter provide recovery. Restore or rebuild the recorded image only
if absent, validate native Compose configuration, create the one stopped named
container once without build/pull, then use the ordinary workflow. Changes to the
image/container configuration require a one-time recreation; jobs do not.
Historical records remain evidence; their old lifecycle instructions are superseded.

Temporary PDF copies, temporary extracted verifier dependency, own Python cache
and the isolated `/tmp/pdf-cleanup-named-0480_zjx` scratch directory are removed.
The accepted runtime retains its source, image, dependencies and empty workspace.
No blanket Docker prune was used. Edge Monitor's long-running service list remains
unchanged; the intentionally stopped workload is not treated as an outage.

README, workflow JSON/SDK generator, manifest, current state, decisions, roadmap,
architecture and Docker inventory/naming documentation describe the same contract.
Unrelated existing working-tree changes are excluded from this work's commit.

Evidence: [runtime and workflow checks](deployments/edge/pdf-cleanup/named-container-2026-10-16/README.md).
Upstream mechanism references: [Docker start](https://docs.docker.com/reference/cli/docker/container/start/),
[Compose create](https://docs.docker.com/reference/cli/docker/compose/create/),
[bind mounts](https://docs.docker.com/engine/storage/bind-mounts/),
[Compose service specification](https://docs.docker.com/reference/compose-file/services/),
[n8n SSH](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.ssh/).
These mechanisms were checked against installed Docker 29.9.0/Compose 5.6.0 and
the installed native n8n tool implementation before deployment/testing.

`PDF_CLEANUP_NAMED_CONTAINER=PASS`
