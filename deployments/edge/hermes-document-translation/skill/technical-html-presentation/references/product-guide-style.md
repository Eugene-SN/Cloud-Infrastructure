# Product Guide presentation reference

Design authority supplied by the operator:
- Product Guide R5225 G3.pdf, 50 pages, SHA-256
  `c52e64ba805edbbcda976028cd9dd8ed80a6601ef557e49e1208b4d0ad424dea`.
- Product Guide R5225 G3.docx, SHA-256
  `bd5c6b56f619f2b71db1a38ee0e00f04eef354a38b6733dd51c5a3b7f94cca9f`.

The reference was examined read-only through PDF rendering/text/font evidence
and DOCX style/section/table/image relationships. Representative cover, prose,
diagram and specification-table patterns control the reusable style; this is
not a pixel-exact Word clone. The reference itself has occasional editorial/font
inconsistencies. Copy its recurring design, not its technical facts or those defects.

| Role | Observed recurring reference | HTML/print implementation |
|---|---|---|
| Page | portrait 612.12 × 792 pt (Letter) | Letter; flowing content |
| Margins | top 1418, right 1134, bottom 794, left 1247 twips | 70.9 / 56.7 / 39.7 / 62.35 pt |
| Cover identity | two supplied DOTIRON logos, left/right | verified logo slots; never inferred OEM replacement |
| Cover title | black Tahoma Bold 18 pt | h1 |
| Document type/section | black Tahoma Bold 12 pt | subtitle/h2 |
| Subsection | Tahoma Bold 10 pt | h3 |
| Body | Trebuchet MS 9.5 pt | 9.5 pt print, 16 px screen |
| Dense tables | predominantly Trebuchet MS 8.5 pt | 8.5 pt print, automatically growing rows |
| Tables | black 0.75 pt grid, white specification cells | semantic table; real header/row-header roles |
| Some option headers | DADADA gray | guide-options class only when role verified |
| Figures | centered, preserved aspect ratio; caption paired | figure/figcaption, no rewritten technical image |
| Lists | compact bullet hierarchy and hanging indent | actual ul/ol nesting, one marker |
| Footer | right-aligned page label, 10 pt | actual export page number if supported/validated |

Four DOCX sections were detected; one has height 16109 twips rather than the
normal 15840. Do not propagate that isolated geometry into a universal design.
Body/style definitions also include Times New Roman and multiple fills; the
primary PDF body/table patterns above determine this template.
No font files are embedded. Trebuchet/Tahoma fall back to Arial/sans-serif where
unavailable; verify actual rendering on the export host.

## Slots and identity

The HTML shell has only document title/type, verified logo elements and verified
semantic content. It contains no R5225 specification, copied chassis figure,
invented author/date/version, or fixed page count. Inline the CSS for standalone
HTML export. Reuse original document figure/image/SVG resources.

The operator selected style only. Retain Lenovo WenTian and the actual server
model; do not replace them with DOTIRON. The DOCX's two DOTIRON images were
inspected as layout evidence and are deliberately not runtime template assets.
Use only verified source logos; never copy the reference branding into Lenovo
documentation or invent a wordmark from OCR.

Source page indices, TOC page references and new print page numbers are different
things. Preserve verified references, use links only to present targets, and
do not fabricate targets for omitted chapters. Screen height is content-dependent;
the original ten logical pages need not become exactly ten printed pages.

## Validation boundary

Translation validation preserves source structure/bytes. Presentation intentionally
changes CSS and may correct source-verified semantic roles. Record those changes,
then compare content coverage, identifiers/quantities, table geometry and resource
hashes independently. Never claim a byte-preserving translation PASS proves a
restyled document has preserved its content. Inspect screen and actual print pages
for clipping, row splitting, missing resources and orphaned captions.

Use native Hermes skills and supporting assets as documented by
[Nous Research](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills/);
no changes to Hermes core or Web UI are needed.
