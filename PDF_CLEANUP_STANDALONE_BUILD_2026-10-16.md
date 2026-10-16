# PDF Cleanup — independent runtime build

Date: 2026-10-16. Status: **DEPLOYED / VERIFIED**.
`PDF_CLEANUP_STANDALONE_BUILD=PASS`.

## Authorized scope and mechanism

Remove the current PDF Cleanup build's dependency on the previous image, verify
the replacement, remove retired images and update runtime/repository documentation.
This is post-infrastructure application maintenance; Stage 13 remains accepted.

The canonical Dockerfile now builds directly from the same official Python image:
`python@sha256:504679006065cdab9a85e983e269140d3c5a279492395a6863b25b1ffb377f86`.
It installs runtime-requirements.txt, the unchanged local package with --no-deps,
and runs pip check. The existing source commit is
`9c9bbb375751f85ca1e6f737504f3e99a68fd3d5`.

The exact dependency versions preserve this deployment's environment. This change
does not choose an update policy. Supported pypdf crypto/fonts extras remain enabled.
The launcher still selects an exact image_id from deployment.json; the job adapter,
originals guard and published n8n workflows keep their accepted contracts.

Current production image: `edge/pdf-cleanup:9c9bbb375751-standalone`,
`sha256:d7fe7e73d422ed59128f4dfe889fb90e8c299fa70df42b6024c65c3087ec6be3`.
Its seven Python base layers match the official base. Its three application layers
are independent of both old images' application layers.

## Verification and recovery

The native Docker build check passed without warnings. A no-cache build completed;
pip check passed. Runtime inspection confirms identical Python/package versions
and SHA256s of all five installed package modules. All 35 package tests passed.
Seven real PDFs / 947 pages passed the isolated CLI regression, including all
three CFF Type1 cases, Footer Forms/clipping, a Widget over body text, overlapping
body/footer bounding boxes and whitespace preservation. Outputs match the
published cleaned copies in metadata, TOC/page labels, every PDF object/decoded
stream, all-page raw text/geometry and exact 72 dpi pixels. Only the regenerated
XRef trailer ID is excluded from object comparison. This is a build regression,
not a repeat of the 2026-10-05 full-catalogue algorithm acceptance.

The production manifest now selects the new exact image ID. A successful call
through the actual job adapter/launcher verified temporary snapshot processing,
CLI validation and job release without WebDAV publication. Its synthetic job ID
does not represent an n8n execution. Original launcher/adapter bytes and both
published documentation workflows remain unchanged.

Both retired images, `edge/pdf-cleanup:8257cb36be78` and
`edge/pdf-cleanup:9c9bbb375751-fonts`, were precisely removed after verification.
The active Refinement.Dockerfile was retired. Installed Dockerfile, dependency
list, manifest and README match the repository. The new image still executes
after retirement, with identical runtime/module inspection results.

All 192 files in originals/cleaned/translations/INDEX checks retain their hashes;
both workflow definitions/settings/publication remain unchanged. n8n is healthy;
Nextcloud is installed, maintenance=false and needsDbUpgrade=false. Independent
concurrent container-name normalization was observed; this task recreated no
persistent service. All 13 own BuildKit cache records, temporary PDF snapshots,
outputs, jobs and test containers are absent. Python remains the required public
base; only one PDF Cleanup image remains. No blanket prune was used.

Deployment readback and sanitized results are in
[evidence](deployments/edge/pdf-cleanup/standalone-2026-10-16/README.md).

Existing Backrest edge-state scope includes /opt and does not exclude the source
tree. Recovery retains /opt/pdf-cleanup/source and its Git commit, the canonical
Dockerfile, .dockerignore and runtime-requirements.txt. Build from that context,
verify the result and record its actual image ID in deployment.json. Registry
access to the official Python digest and the recorded package releases is required.
Image IDs can vary across rebuilds because of packaging timestamps/provenance.

During verification, the first comparison rejected the regenerated trailer ID
inside an XRef stream object. This was an assistant verifier defect, not a CLI
failure. Completed CLI output was preserved; comparison resumed with only the
service-generated XRef ID excluded. The decoded XRef stream remained mandatory.
The first CLI stdout was not persisted by the initial harness; the recovery note
records that limitation rather than inventing a complete CLI report.

Historical dated evidence is retained with its original image identities.
Current deployment/recovery instructions are in the canonical
[README](deployments/edge/pdf-cleanup/README.md).
