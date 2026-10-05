# Full-catalogue production verification — 2026-10-05

Current acceptance: [record](../../../../PDF_CLEANUP_PRODUCTION_ACCEPTANCE_2026-10-05.md).
All 95 actual paths / 11,584 pages / 6,579,007 useful glyphs pass; originals unchanged.

- evidence.json: final per-file adapter results + all-page independent reviews, source/runtime identity and aggregate checks.
- final-audit.json: actual filesystem SHA/path sets, INDEX records/static interface and unchanged originals/INDEX.md/translations/launcher/adapter.
- manifest.json + source-hashes.json: frozen input scope and candidate identity.
- fonttools-*.json, pre-fonts-* and fonts logs: three CFF warning files, unchanged native/content evidence, production dependency repeat and final reviews.
- lifecycle.json + audit-worker-resume.json: completed proof preservation, tool-session RC uncertainty and assistant harness corrections.
- production-cleanup.json: exact own cache/image deletion and reference-backed runtime-parent retention.
- workflow-nonregression.json: unchanged active/draft versions and node counts.
- scripts/logs: exact one-off harness and actual outputs; scripts use a temporary existing credential export which is deliberately absent here.

Native DAV helper uses the read-only-audited Docker address for this one-time test.
It is not scheduler configuration or a new persistent network contract. The production
workflow continues using nextcloud.edge.internal. Synthetic numeric job IDs are
not n8n execution IDs. No PDF, credential value or decrypted export is retained.

The first full run used the code-only image. The final image adds pypdf's supported
fonts extra with the same executable source and previous libraries; three affected
PDFs were rerun and all independently reviewed final bytes are bound by SHA256.
The other 92 successful outputs have no CFF dependency warning and remain unchanged.
