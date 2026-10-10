---
name: technical-html-translation
description: Manage incremental Chinese-to-English technical HTML translation, reuse Weblate wording, and verify document and table preservation.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [html, translation, tables, weblate, document-diff]
    category: technical-documentation
    requires_toolsets: [terminal, file]
---

# Incremental technical HTML translation

Use the existing Hermes agent and its local `custom:ai-node-vllm` / `qwen3.8-27b-fp8`
route. Do not launch Codex/Antigravity, use a cloud fallback, or change shared
provider settings. Read [references/lp2468-pilot.md](references/lp2468-pilot.md)
before running this pilot. This skill does not authorize other documents or
translation languages.

## Procedure

1. Inspect the input package prepared by the Mac/Weblate chat: source HTML,
   current English draft, scoped Weblate units, glossary and provenance hashes.
   Confirm identities and hashes before modifying anything. Edge handles
   Hermes and document processing; the Mac chat handles authenticated ai-node
   and Weblate operations. Edge does not need a copied SSH key or Weblate secret.
   Missing input means the live test remains incomplete.
2. Run `scripts/html_workflow.py plan PREVIOUS.json CURRENT.json --out PLAN.json`.
   Input units are `{id, position, source, target, state, location}`; `source`
   and `target` may be Weblate's single-item arrays. Only mark `wrapped_prose`
   true after confirming breaks are PDF wrapping inside one paragraph.
3. Read the plan and surrounding paragraph/table context. Reuse exact verified
   source matches first, including moved blocks. Existing state-20 drafts can
   be retained, but are not approved translations. Conflicting targets require
   review. Read the exported Weblate translation-memory candidates/glossary for
   changed blocks; ask the Mac chat for a fresh export if needed. Similarity is
   a suggestion, never authority to copy different model
   names, capabilities, numbers, units or negations.
4. Translate only `translate` entries. For this skill Hermes itself uses Qwen
   with the document context and glossary; do not replace it with an unverified
   OpenAI-compatible JSON intermediary. Put translations in a local JSON file
   using `write_file`. The JSON file is an internal exchange format, not a
   document to translate. Validate it with the helper before any publication.
5. Run `scripts/html_workflow.py check-blocks PLAN.json TRANSLATIONS.json`.
   Investigate failed number/tag/term/Chinese checks; never bypass them to get
   PASS. Perform a meaning review for terminology, quantities and negations.
6. Return genuine proposed translations and review results to the Mac/Weblate
   chat. That chat owns publication, state-20 draft saving and native downloads;
   this edge skill does not publish or auto-approve. A synthetic changed block
   is strictly temporary and must never be published. If there are no changes,
   make zero translation requests and zero translation writes;
   orchestration/review calls are counted separately.
7. On the native English HTML returned by the Mac chat, run `verify-html
   ORIGINAL.html ENGLISH.html`. Review the selected pages in the existing browser, including
   the introductory paragraph and tables. Count broken images and clipped text;
   inspect screenshots when available. Use the same model for semantic review;
   do not invoke an external vision model through `vision_analyze`.

## HTML and table treatment

Preserve CSS, scripts, images, links, attributes, paragraph/list boundaries,
row/column order, merged-cell spans and all nonselected content. Maintain
English prose flow without obsolete Chinese PDF line wraps. Do not remove
breaks in table items/lists or redesign a technical report as a landing page.

The installed `claude-design` skill can inform a requested HTML design review;
its general redesign/variants procedure does not override the pilot's fixed
HTML/CSS contract. `popular-web-designs` and `design-md` are unnecessary for this
preservation test. Office/PDF dependencies are unnecessary.

Report observed results, translation-call counts and unresolved failures in a
few lines. Keep one control sample outside `converted` before replacing a real
draft; use `/tmp` for synthetic fixtures and remove them after the test.
