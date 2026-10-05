# PDF cleanup: проверяемый candidate

**CANDIDATE / NOT DEPLOYED.** Production source, image, launcher, job adapter,
cloud files and n8n workflows remain unchanged by this workstream.

The chosen test set is documented in
[`PDF_CLEANUP_TEST_SELECTION_2026-10-05.md`](../../../../PDF_CLEANUP_TEST_SELECTION_2026-10-05.md).
It contains 18 unique PDFs / 3132 pages; 31 other unique PDFs / 3266 pages form
the separate regression set. The 95 catalogue paths map to 49 SHA256 contents.

`candidate.patch` applies to the installed edge import of documentation-ai
`46f179e9e5c83ff2c12b7ba084efef124afaf338` plus its existing originals guard.
Base/result SHA256 and complete per-document results are in `evidence.json`.
Apply only to an isolated source copy. This artifact is not a deployment command.

The candidate changes generic geometry qualification and precise PDF operand
editing. No model names, filenames, vendor-specific document titles or paths
are used as runtime detection rules. Text is removed by editing identified
original operand byte ranges, rather than reserializing untouched instructions.
Standalone CLI/JSON and the existing guard contract are preserved.

The parser extension uses the actual pypdf 6.19.0 object/inline-image parsers
and ContentStream control flow. Dependencies remain PyMuPDF and pypdf; PDFium,
NumPy and Pillow are independent research dependencies, not new production
requirements. Changing these underlying libraries requires compatibility tests;
no new version pin or update policy is introduced.

## Reproduce without production writes

Use the existing image ID recorded in evidence. Create a temporary source copy,
apply the patch, and use a read-only `/audit` mount containing that copy as
`candidate/` plus these scripts. Snapshot source PDFs by SHA256 into read-only
`/input`. `/out` is the only writable research mount. The image's console script
imports the candidate through `PYTHONPATH=/audit/candidate/src:/out/review-deps:/audit`.
Keep `PDF_CLEANUP_SOURCE_COMMIT=uncommitted`, `TMPDIR=/out` and a valid absolute
`PDF_CLEANUP_ORIGINALS_DIR`. The source snapshots and real originals must never
be writable output mounts.

Manifest schema: `documents` (all relative paths/SHA256/sizes), `unique_documents`
(one representative per SHA256), `baseline` (production file paths and SHA256).
`selection_and_geometry.py` creates `/out/selection.json`; the names in this
research selector identify regression cases only and are not part of the CLI.

`refinement_runner.py sample WORKER WORKERS` processes whole selected PDFs;
`holdout` processes the other contents. Two workers were used on edge's two CPUs.
Each file undergoes the full cleanup function used by the CLI, native validation, all-page PDFium comparison
at 144 dpi, source SHA256 verification and a second detection pass. The candidate
source is frozen for the final series and every record stores its exact hashes.

Package tests are included in the patch. Independent reviewer controls are
`test_reviewer.py`. `test_real_regression.py` reproduces the WR6220 page-14
nonpainted semantic-character case; it requires the actual source snapshot and
the diagnostic/result PDF described in that script. `cli_smoke.py` tests the real
console entrypoint, exact copying and invalid originals configuration.

All actual vendor PDFs, diagnostic images and external libraries remain temporary
and are removed after evidence is preserved. They are not included in Git.

`spot_check.py` reproduces four manually inspected source/candidate page pairs.
The images are temporary; observed checks are recorded in the report.

Final verification: **49/49 PDFs, 6398 pages PASS** (18 sample + 31 regression).
All-page PDFium reports zero pixels changed outside exact removal masks, zero
body-glyph/order failures and zero document-property changes. Second detection
requires the corrected written-stage native evidence described below.
All 115 production baseline files and the image ID are unchanged.
35 package tests, 7 independent controls and 2 actual CLI controls pass.
See `evidence.json`, `results/`, `production-final-audit.json` and `logs/`.

The original full-series runner looked up native inspection by the final output
path, although cleanup inspects a temporary `.part` file before atomic hardlink
publication. Its fallback reused source native data. Full-series native/content
and PDFium comparisons remain valid; the original `second_pass` fields are
superseded. The saved runner now selects the actual written-stage evidence.
`repeat_runner.py` separately regenerates outputs with the identical frozen
candidate and checks all 49 files with that written-stage native data, asserting
that the inspector's stage SHA256 equals the published output SHA256. Exact
copies may reuse source evidence only after equality of source/output SHA256.
This follow-up does not repeat the already passed all-page PDFium comparison.

Corrected follow-up: **49/49 PDFs, 6398 pages PASS; zero repeat targets**.
Written-stage inspector SHA256 equals each published output SHA256.
See `repeat-results/` and `evidence.json.second_detection_check`.
