# Hermes HTML translation pilot — edge portion

Existing Hermes uses `custom:ai-node-vllm` / `qwen3.8-27b-fp8` at
`http://192.168.1.30:8000/v1`. The native resolver and model listing confirm this
route; no fallback is configured. Gateway and Dashboard are active user units.

Runtime skill:
`/home/core/.hermes/skills/technical-documentation/technical-html-translation/`.
Canonical source is `skill/technical-html-translation/` in this directory.
Load it through native `/technical-html-translation` or the verified CLI
`hermes chat --skills technical-html-translation`. No profile, daemon, provider
change, Office dependency or Weblate customization is introduced.

## Chat boundary and input package

The existing Mac chat owns authenticated ai-node/Weblate work. The edge chat
owns Hermes setup, planning, translation and HTML checking. No SSH key or
Weblate credentials are copied to edge.

For the real pilot, the Mac chat supplies a temporary directory containing:

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

Offline helper tests verify zero candidates for unchanged/moved/wrapped prose,
one candidate for one changed quantity, conflicting-match review, and rejection
of number/family/tag/attribute/CSS/script/out-of-scope changes. These synthetic
tests do not constitute the real lp2468 acceptance or prove better translation
quality. Real-sample acceptance awaits the input package from the Mac chat.

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
