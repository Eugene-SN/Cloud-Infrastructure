# Accepted pilot boundary

- Existing project `tehnicheskaya-dokumentaciya`; component
  `lp2468-wr6220-g5-html`; English translation ID 10; source `zh_Hans`.
- Only 108 unique units: positions 3–69 and 170–210 inclusive; pages 1–3 and
  9–11. Other pages remain Chinese intentionally. Do not translate Markdown,
  JSON documents, Russian, other models or all 64 pages.
- Weblate `http://192.168.1.30:17880`; Qwen
  `http://192.168.1.30:8000/v1`, model `qwen3.8-27b-fp8`.
- Source on ai-node:
  `/srv/ai-data/cloud/technical-documentation/lenovo/converted/WR6220 G5/html/lp2468.html`.
  Expected SHA256:
  `28c83bd6bb8afb9a056f1f6182f9fa4b93fab2d5935e9f3d09f8a3f5490082e7`.
- Current draft:
  `/srv/ai-data/cloud/technical-documentation/lenovo/translated/temp/en/WR6220 G5/html/lp2468.html`.
  Last operator-provided SHA256:
  `ee82fae7906f3139f66e85fc7500d708109a5d0b73d2fe1b555e19b435d41bf6`.
- Expected structure: 64 sections, 55 images, 51 tables, 359 `tr`, 1457 `td`.
  Source has 226 `br`; the draft has 219, removing exactly seven wrapping
  breaks in one introductory paragraph on page 1. Other structure is preserved.
- `联想问天` → `Lenovo WenTian`; `产品指南` → `Product Guide`. Do not substitute
  ThinkSystem. Reuse the existing 133-term Weblate glossary, freshly audited.
- Native download:
  `/download/tehnicheskaya-dokumentaciya/lp2468-wr6220-g5-html/en/`.
  Allow the measured multi-minute export latency; a successful download must
  contain an HTML attachment, not a redirected login page.
- Keep MinerU stopped and preserved. Do not change Weblate UI/code/provider,
  shared vLLM, models, originals, `converted`, recovery state, n8n or schedules.

## Work ownership

The Mac/Weblate chat exports the scoped native units, glossary, existing
translation-memory candidates, source and draft HTML with fresh hashes. It
transfers only document data to edge, never credentials. Edge's Hermes chat
produces plans, proposed changed translations and checks. The Mac chat saves
genuine proposals in Weblate as state-20 drafts, performs native downloads and
maintains the agreed ai-node paths/control sample. No edge-to-ai-node SSH access
or copied private key is needed for this division of work.

## Required tests

On copies of the actual scoped snapshot: unchanged input produces zero
translation candidates; moved blocks and confirmed paragraph wrapping produce
zero candidates; changing one block produces one candidate. Translate that
candidate through Hermes/Qwen into `/tmp`, validate and review it, and prove
every other translation is retained. Do not publish artificial content.

Finally audit the real draft, native download and original hash. Record real
sample tests separately from synthetic helper tests. None of these checks
establishes improved translation quality without a reviewed before/after result.
