---
name: technical-html-translation
description: Translate Chinese technical HTML into English from source, normalize paragraph wrapping, and verify HTML and table preservation; reuse prior wording only for explicitly requested future updates.
version: 1.1.0
platforms: [linux]
metadata:
  hermes:
    tags: [html, translation, tables, weblate, document-diff]
    category: technical-documentation
    requires_toolsets: [terminal, file]
---

# Technical HTML translation

## Clean source translation — current task

The operator's current task is a fresh English translation of lp2468 pages
1–10 from a source-only package and the existing 133-term glossary. Do not read
old English drafts, translation memory, previous targets or prior native session
history. No new document version exists. Historical controlled-diff evidence
does not accept this clean translation.

Use Hermes itself with `custom:ai-node-vllm` / `qwen3.8-27b-fp8` in a new session.
Model context contains extracted Chinese blocks and glossary, not embedded
images, CSS or scripts. Review per-page source/English JSON; do not read/search
raw source or assembled HTML through model tools. Scripts and the browser handle
raw HTML and resources. `scripts/clean_html.py extract SOURCE MANIFEST WORKDIR`
uses the supplied source hash/page manifest and emits page source files and
`extracted.json`. IDs are local extraction IDs, not fabricated Weblate IDs.
Translate every extracted block using `write_file` into
`WORKDIR/results/page-NN.en.json`, mapping each local ID to English inner HTML.
Translate page by page, retain all original inline tags/attributes, quantities,
negations, lists, table separators, product names and commands. Use Lenovo
WenTian for 联想问天 and Product Guide for 产品指南. Normalize the marked
continuous prose paragraphs by removing their PDF wrapping br tags and joining
the text naturally. Audit li/td as well: source-verified word/clause wraps may
be removed at explicit br indices, while independent item/heading separators
remain. Record the source context and each removal; do not preserve or remove
table/list br blindly.

Run `scripts/clean_html.py assemble WORKDIR/extracted.json WORKDIR/results
WORKDIR/results/lp2468.pages-1-10.en.html`. This deterministic helper assembles
the model's translations, requires complete coverage, checks source-relative
tags/attributes/quantities and preserves bytes outside translated inner
fragments, including images/CSS/scripts/resources, with exactly one declared
metadata exception: accepted DocVortex `<html lang="und">` becomes
`<html lang="en">` in the English output. Source stays unchanged; the checker
reports this exception rather than claiming absolute outside-byte equality.
It makes no model calls.
Resolve actual validation failures; never weaken approval or checks to obtain
PASS. Invoke the helper as a script file, never inline python-c or a heredoc.
Review the meaning of all pages and record explicit checked local IDs, actual
issues and corrected IDs. Coverage alone does not approve meaning. The browser
must check all ten pages, prose, tables, images and resources before acceptance.

One native client may use the normal sufficient tool/time budget and per-request
`chat_template_kwargs.enable_thinking=false`; preserve the shared FIFO queue,
provider and approval settings. For subsequent translation runs, select the
native `html-translation` profile (`hermes -p html-translation chat`): its own
endpoint `extra_body` and `auxiliary.compression.extra_body` both set
`chat_template_kwargs.enable_thinking=false`. Main request overrides alone do
not reach the compressor in the tested runtime. The isolated profile preserves
the local Qwen route and starts with its own empty history; never migrate or
restart an in-flight request to apply this setting. Return actual validated English HTML to the
existing Mac/Weblate chat. Mac alone saves validated output in the accepted
translated/temp/en directory. Source, production and Web UI remain unchanged.

## Future incremental updates — only when requested

Use the existing Hermes agent and its local `custom:ai-node-vllm` / `qwen3.8-27b-fp8`
route. Do not launch Codex/Antigravity, use a cloud fallback, or change shared
provider settings. Read [references/lp2468-pilot.md](references/lp2468-pilot.md)
only for the historical 108-unit incremental pilot. This skill does not authorize other documents or
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
   Record explicit native IDs in `checked_unit_ids`; run `check-reviews
   CURRENT.json REVIEW.json [SUPPLEMENT.json ...]`. A textual claim of 108
   reviewed units does not prove coverage. Review omitted IDs before acceptance;
   the helper checks coverage only and never approves translation meaning.
   Invoke the packaged Python helper as a script file for validation. Inline
   `python -c`/`-e` execution can be blocked in native single-query mode; do not
   change approval settings to work around it. Allow enough native tool turns
   for context reads, writing and validation: the real pilot's six-turn
   supplemental limit was exhausted after saving its report. Use the normal
   native budget or the tested pilot option `--max-turns 24`.
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
   If a native export changes repeated unit labels outside these pages, retain
   the strict failure and run `scripts/audit_native_export.py ORIGINAL.html
   ENGLISH.html CURRENT.json`. This separate audit checks every outside text
   node and requires exact source/target text and native tag/line/column
   locations for each repeated label. Unexpected changes still fail. Report
   native deduplication and serialization whitespace separately; neither
   authorizes new changes outside the sample. A controlled diff must preserve
   every other byte of the received draft.

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
draft; use `/tmp` for synthetic fixtures and remove them after the receiving
Mac chat has independently read and acknowledged the results.
