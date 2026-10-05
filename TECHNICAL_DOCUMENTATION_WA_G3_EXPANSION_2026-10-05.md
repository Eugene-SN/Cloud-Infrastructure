# WA G3 documentation monitoring — 2026-10-05

Status: monitoring DEPLOYED / VERIFIED; cleanup PARTIAL, with five demonstrated
CLI failures. This is an operator-authorized application/workflow expansion;
the accepted infrastructure checkpoint remains Stage 13.

TechnicalDocumentationSync (`QouVaVNhAqSiYq5D`) remains published at
`6ed111f3-306d-4cf1-8dc4-2a107c2c1b26`, with seventeen nodes, three native groups
and the unchanged daily 07:00 Europe/Minsk schedule. The existing nine model
definitions remain unchanged; five definitions and a generic description were
added. No workflow node, service, credential, database, backup or retry queue
was added.

| Model folder | Added originals | Published cleaned copies |
| --- | ---: | ---: |
| WA5480 G3 | 11 | 10 |
| WA5680 G3 | 1 | 1 |
| WA7780 G3 | 2 | 0 |
| WA7785a G3 | 2 | 0 |
| WA7880a G3 | 1 | 1 |

The official ASP SubSeries and machine-type catalogues were compared for all
five models. WA7780 G3 uses 7DF1 because SubSeries omits its user manual;
WA7880a G3 uses 7DLR because SubSeries returns null data. Other three catalogues
agree at both levels. Latest-family selection excludes one duplicate LXPM
entry and the older BMC event reference. Eighteen distinct offered PDF URLs
returned HTTP 200/application/pdf; seventeen current files were selected.
Official Lenovo Press searches found no model PDF for these exact G3 models;
interactive OSIG and G5 results were excluded.

Twenty model directories were created through Nextcloud WebDAV under
`/srv/cloud/technical-documentation/lenovo/{originals,cleaned,translated/en,translated/ru}`.
Translations are prepared folders, not an enabled translation process. All
cloud publications use WebDAV; no backend write/files:scan was used.

Runs 12122 and 12186 saved all seventeen originals and INDEX.html now contains
95 records across fourteen model folders. The index is saved before cleanup.
The CLI was resumed only for newly downloaded files; twelve cleaned copies are
published and correctly marked in the existing hidden details. The old 78
originals, two cleaned PDFs, all old catalogue records and INDEX.md are unchanged.
WebDAV listings and filesystem filenames/sizes/publication markers agree.

The remaining failures are:

- WA7780 G3 user guide: page 46 footer candidate overlaps table text.
- WA7780 G3 BIOS guide: page 2 unverified numbering in footer frame.
- WA7785a G3 user guide: page 34 footer candidate overlaps table text.
- WA7785a G3 BIOS guide: page 2 unverified numbering in footer frame.
- WA5480 G3 BMC G3 Redfish reference: cleanup exceeds 900 seconds, including
  a retry after the runtime dependency correction.

These originals remain saved. They have no cleaned PDF, cleaned_at/path or
false completion marker; their existing index state is pending. Unchanged
failed documents are not automatically retried. Layout/performance fixes for
the CLI remain a separate task; no content-preservation check was weakened.

Two demonstrated runtime defects were corrected during onboarding. The Docker
build now requests upstream-supported `pypdf[crypto]`, installing cryptography
50.0.2 for AES PDFs. Python 3.14.8, PyMuPDF 1.28.2, pypdf 6.19.0 and package 0.1.3
are retained. The imported commit `46f179e9e5c83ff2c12b7ba084efef124afaf338`,
portable originals guard and core SHA256
`4b29b752fe9dcc3b8f8d08f509b5c840e354ecb0a398fe72bea092fdd4cb4c72` remain unchanged.
The canonical image tag remains `edge/pdf-cleanup:8257cb36be78`; its rebuilt ID
is `sha256:3ff39309bab88fca2d28edb606879afbe5ce18fa366d48ade3e9440cbd82c06e`.

The adapter's existing 900-second timeout previously killed core's launcher
while leaving the root-owned Docker attach process/container holding output
pipes. It now stops the exact execution-owned container through Docker before
collecting the process result. A live forced timeout used a two-second harness
wait and completed in 7.31 seconds, removed the container and retained the
snapshot hash. Real retry 12232 subsequently ended with its timeout error at
14:15:34 UTC and removed both container and temporary job automatically.
Official mechanisms: [pypdf installation](https://pypdf.readthedocs.io/en/latest/user/installation.html),
[Docker stop](https://docs.docker.com/reference/cli/docker/container/stop/).

Validation: all fourteen upstream/edge originals-guard tests, five adapter
regressions, fourteen-model/95-key source and replacement/date logic checks,
native SDK validation, authenticated publication readback and production
no-change run 12269 passed. That run checked fourteen models/95 current
documents, found zero changes, performed no download/index write/cleanup call
and completed in 7.514 seconds. n8n readiness returned 200; Nextcloud remains
35.0.1 with maintenance/db-upgrade flags false. Own temporary jobs, browser
snapshot, bytecode cache, obsolete image and temporary image tag were removed.

Reproducible definitions and sanitized evidence:
`deployments/edge/technical-documentation/wa-g3-expansion-evidence.json`,
`source-audit-g3-2026-10-05.{json,md}`, model fixtures and native workflow exports;
runtime corrections are in `deployments/edge/pdf-cleanup/`.
