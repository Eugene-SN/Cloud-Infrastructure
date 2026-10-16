# Named-container verification, 2026-10-16

Current acceptance: [PDF_CLEANUP_NAMED_CONTAINER_2026-10-16.md](../../../../PDF_CLEANUP_NAMED_CONTAINER_2026-10-16.md).

| Evidence | Purpose |
| --- | --- |
| production-before.json, manifest-before.json, image-before.json, workflow-before.json | Exact pre-change production/source/workflow baseline |
| unit-red.log, unit-green.log | Boundary test red/green evidence |
| create.log, container-created.json | Native Compose creation of the one persistent container |
| first-smoke.json, invalid-and-missing.json | Actual adapter and failure checks |
| workflow-evidence.json | SDK validation/update, real three-file n8n success, controlled publication failure and unchanged failure INDEX hash |
| timeout-cleanup.json, recovery-execution.json | Actual stop/reap/cleanup and successful subsequent workflow run |
| compare-pdfs.py, pdf-comparison.json | Recursive PDF object/decoded stream equivalence against pre-change accepted output copies |
| state-comparison.json | All originals and caller unchanged; only intended publication changes |
| verify-runtime.py, final-runtime.json | Read-only native configuration, same-container/image, clean workspace, source/config parity and service checks |
| workspace.json, cleanup.json | Own temporary artifact accounting and final removal |

No PDFs, extracted packages, HTTP session headers/cookies or credentials are
retained here. The temporary comparison inputs/dependency have been removed;
compare-pdfs.py is the verifier source, not a permanently installed dependency.
