# Hermes HTML translation pilot — edge portion

Existing Hermes uses `custom:ai-node-vllm` / `qwen3.8-27b-fp8` at
`http://192.168.1.30:8000/v1`. The native resolver and model listing confirm this
route; no fallback is configured. Gateway and Dashboard are active user units.

Runtime skill:
`/home/core/.hermes/skills/technical-documentation/technical-html-translation/`.
Canonical source is `skill/technical-html-translation/` in this directory.
Load it through native `/technical-html-translation` or the verified CLI
`hermes chat --skills technical-html-translation`. The clean translation profile
below isolates inference settings and history. Shared daemons/provider settings,
Office dependencies and Weblate customization are unchanged.

## Chat boundary and input package

The current operator task is a clean English translation of original lp2468
pages 1–10, not a version comparison. Skill 1.2.0 uses `source.html`,
`glossary.json` and a fresh source-only `manifest.json`; it starts a new native
session without old English targets or TM. `scripts/clean_html.py` extracts
actual source leaf blocks, assembles Hermes-generated per-page translations and
checks structure/assets/quantities relative to that source. Audited PDF word
wraps in p/li/td may be removed; semantic item breaks remain. No fixed 108-unit
position set is used for this path. Full meaning and browser review are required.
The English output changes only root `lang="und"` to `lang="en"` outside the
translated fragments; this declared metadata exception is recorded explicitly.

Subsequent clean runs use the native `html-translation` profile, selected with
`hermes -p html-translation chat --skills technical-html-translation`.
Its profile-local named endpoint and `auxiliary.compression.extra_body` both
carry `chat_template_kwargs.enable_thinking: false`; native kwargs construction
was asserted offline, without another inference call. Main request overrides
alone did not propagate to compression in the current pilot. The profile does
not change the selected default profile or shared Gateway/Dashboard config.
Upstream mechanisms: [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles/)
and [auxiliary configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/).

Current real result is a verified machine draft: 187 newly translated source
blocks, ten browser-checked pages, two tables, one loaded image, 22 audited PDF
wrap removals and 56 retained separators. Translator and final read-only audit
both exit 0. The final audit actually reads all187 pairs; ten quoted anchors and
independent Mac semantics are verified. Unsupported free-form native review
claims are excluded from acceptance. Five verifier regressions pass.
Evidence and final output hash: `first10-clean-evidence.json`.

Mac reviewed all 187 actual source/target blocks and all ten rendered pages.
That read-only review found literal English, inconsistent component terms and
presentation defects; the existing HTML remains an unapproved machine draft.
Skill 1.2.0 adds source-quoted English review rules and the operator's 252 original
glossary entries plus 31 contextual additions. LP1608 is English terminology
guidance only; source facts and Lenovo WenTian/model identity remain authoritative.

The native technical-html-presentation skill 1.0.0 provides a shared HTML/CSS
Product Guide template derived from the operator's edited R5225 DOCX/PDF.
Apply style only, retain Lenovo WenTian, and use a source-verified semantic-role
plan on a separate output. No DOTIRON logo or R5225 specification is shipped.
Both skills are installed in the default and isolated html-translation profiles.
Native discovery/reference loading, 15 existing helper tests and a synthetic
screen/print table fixture pass. This is skill/template preparation, not proof
of a newly improved model output: no new translation or Web UI changes occurred.
Evidence: style-glossary-evidence.json.

The 108-unit package and controlled-diff results below are historical incremental
workflow evidence, not acceptance of the current clean translator. Diff applies
only to explicitly requested future document updates.

The existing Mac chat owns authenticated ai-node/Weblate work. The edge chat
owns Hermes setup, planning, translation and HTML checking. No SSH key or
Weblate credentials are copied to edge.

For the historical incremental pilot, the Mac chat supplied a directory containing:

- `source.html`, the exact original lp2468 HTML;
- `draft.html`, the current English sample/native download;
- `previous.json` and `current.json`, native unit snapshots with metadata
  `translation_id: 10`, `language: "en"`,
  `component: "lp2468-wr6220-g5-html"`, and a `units` array of objects
  `{id, position, source, target, state, location}`;
- `glossary.json` and relevant native translation-memory candidates;
- fresh provenance hashes and snapshot/export times.

Only an audited wrapped paragraph receives `wrapped_prose: true`. Only a
translation verified against the real source receives `verified: true`.
Existing state-20 text can be retained without claiming approval. The helper
requires exactly 108 unique selected units at positions 3–69 and 170–210.

Hermes returns `plan.json`, changed-unit proposals and review results to the Mac
chat. That chat alone saves real drafts, maintains the ai-node control sample
and confirms native downloads. Synthetic fixtures never enter Weblate.

## Verification status

Ten offline helper tests verify zero candidates for unchanged/moved/wrapped prose,
one candidate for one changed quantity, conflicting-match review, and rejection
of number/family/tag/attribute/CSS/script/out-of-scope changes. These synthetic
tests do not constitute the real lp2468 acceptance or prove better translation
quality. The real package was subsequently transferred by the Mac chat and
tested: unchanged/moved/wrapped copies produce zero candidates, one controlled
change produces one translated block, and 107 targets remain byte-identical.
See `REAL_PILOT_2026-10-10.md` and `real-pilot-evidence.json`.

The real native Hermes/Qwen synthetic smoke test produced one changed-block
translation and retained 107 blocks; block checks passed. Its first short
8-turn invocation returned 1 despite writing the checked artifacts. A read-only
continuation of the same session finished with native result exit code 0.
Recorded inference usage is 10 calls, all to the existing private Qwen route;
this is not a claim of one inference call or a live-document quality result.
The local browser fixture also passed using the CLI-supported per-process
`--no-sandbox` argument; host sandbox settings were not changed. The synthetic
session, temporary files and browser session were removed. Sanitized evidence:
`setup-evidence.json`.

Run the stdlib test program `test_html_workflow.py` for offline verification.
Use the installed Hermes parser to validate Hermes frontmatter: the Codex
skill validator does not support Hermes `platforms`/`version` fields.

## Repeating the historical incremental workflow

Load the installed skill with native `/technical-html-translation`, or
`hermes chat --skills technical-html-translation`. Supply the actual package
directory with native `--in` and the task file with `--query-file`; the verified
explicit route is `--provider custom:ai-node-vllm --model qwen3.8-27b-fp8`.
Native `--format stream-json` records tool/results and process status. Use the
normal native tool budget or the tested `--max-turns 24`; a six-turn cap was
insufficient for the supplemental review's reads, write and validation.

For a bounded SDK review, the installed `AIAgent.run_conversation` accepts an
explicit `conversation_history` for the request without deleting stored history.
Its supported `request_overrides` can pass
`{"extra_body":{"chat_template_kwargs":{"enable_thinking":false}}}` for one
client. These were tested in the existing native session with CLI skill preload,
session restoration and native tools; global settings were preserved.

Validate through the packaged `html_workflow.py` script (`plan`, `check-blocks`,
`check-reviews`) and `audit_native_export.py`; invoke them as Python script
files, not inline `python -c`. Keep the strict outside-page result visible when
native repeat locations are present. Check raw model IDs and quotations against
the actual snapshot before claiming coverage or meaning. Only the Mac chat
publishes genuine proposals; artificial changes remain temporary.
