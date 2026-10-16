# Standalone PDF Cleanup build — 2026-10-16

Status: **DEPLOYED / VERIFIED**. `PDF_CLEANUP_STANDALONE_BUILD=PASS`.
Seven real PDFs / 947 pages match the published results. Both retired images
and all 13 own cache records are absent; 192 production file hashes and both
documentation workflow definitions/publication/settings are unchanged.

Authoritative workstream record: [report](../../../../PDF_CLEANUP_STANDALONE_BUILD_2026-10-16.md).

- Dockerfile + runtime-requirements.txt in the parent directory are the current recipe.
- build.log/build-metadata.json/images-built.json record the independent no-cache build.
- runtime-before.json/runtime-after.json record identical Python versions, packages
  and installed executable module SHA256s. unit-tests.log records 35 passing tests.
- selection.json/regression.py/regression-results.json/regression.log record
  isolated source/reference copies, native CLI results and comparisons against
  currently published cleaned PDFs. Compare document metadata, page labels/TOC,
  every object/decoded stream, all-page raw text/geometry and exact 72 dpi pixels.
  Only the regenerated XRef trailer ID is excluded from object comparison.
- regression-initial.log preserves the initial verifier defect. The first
  completed CLI output was reused, without rerunning that successful cleanup;
  the initial CLI stdout was not retained. Later CLI reports are persisted.
- production-before.json/capture-state.py record hashes of originals, cleaned,
  translations and INDEX files, plus identities and definition/settings hashes
  of the two documentation workflows. Credential values are not exported.
- recovery-contract.json confirms the existing Backrest scope covers
  /opt/pdf-cleanup/source, without creating a new backup mechanism.
- adapter-smoke.py exercises the production adapter and launcher on a temporary
  snapshot without WebDAV publication; verify-final.py performs final readback.
- adapter-smoke.json, install-result.log, final-verification.json and
  service-health.json record actual deployment and service non-regression.
- retired-images-removed.json/cache-cleanup.json/build-cache-after.json record
  precise removal; runtime-after-retirement.json proves the remaining image runs.
- own-build-cache.json identifies the exact records created by this workstream.
  Cache cleanup uses explicit IDs, never a blanket prune.

workspace.json is an audit trail for the temporary workspace; its recorded path
must be absent at completion. No PDF, package download or credential export is
retained in this evidence directory. Historical 2026-10-05 full-catalogue evidence
remains a separate algorithm baseline; this work does not claim a new full-catalogue run.
