# lp2468 real pilot: request for the existing Mac chat

Historical request below is superseded. Mac delivered and accepted the controlled
108-unit test, then the operator clarified that current work is a fresh source-only
translation of pages 1–10. Source/glossary were transferred to edge and a new
native Hermes/Qwen session performs that task. Old targets/TM and synthetic
diffs are excluded. Automatic coordination uses Mac delegated messages and
authenticated return reads; edge native send_message_to_thread remains absent.
Current deliverable/evidence: `first10-clean-evidence.json`, machine draft,
187 fresh pairs, translator/audit exit0, verified HTML and declared lang=en
metadata exception. Unsupported native free-form review claims are excluded.

Requested by the operator on 2026-10-10. This is one coordinated task across
the existing chats, not a request for the operator to divide the work.

Mac chat: `01a121de-3b75-7d33-8fa3-650ece5d8b90`, host `local`.
Edge chat: `01a123f2-cf5b-7e51-af49-5b7e483b4368`.

## Dispatch status

NOT SENT. The edge session can read the Mac chat with `read_thread`, but its
available tool catalog and callable tool namespace do not expose
`send_message_to_thread` or `handoff_thread`. The latest inspected Mac turn is
completed and the chat reports idle. Reading a chat does not start another turn.
This file records the pending request; it does not establish delivery or consent
from the Mac agent. Real-sample acceptance remains pending.

## Request to Mac

Using your existing authorized access, export the actual lp2468 English pilot:
translation ID 10, component `lp2468-wr6220-g5-html`, exactly 108 unique units at
positions 3–69 and 170–210 (pages 1–3 and 9–11). Follow the package contract in
`README.md`: source and current draft/native HTML download, unit snapshots,
existing glossary and relevant TM candidates, fresh SHA256 hashes and export
times. Mark wrapped prose and verified translations only when evidenced.

If no historical source snapshot exists, say so and supply the real current
snapshot as the baseline. Edge will derive explicitly artificial test variants
locally; it will not represent them as historical revisions.

Transfer the package into a fresh temporary directory on edge using your
existing edge access. Return the exact directory, manifest and hashes through
the existing chat coordination mechanism. Transfer document data only. Do not
change source, draft, translation state, full document, Web UI, provider or vLLM.

## Edge completion after receipt

Validate provenance and scope, then run Hermes on copies of the real 108 units:
unchanged input → zero translation candidates; moved/confirmed wrapped prose
→ zero; one controlled changed block → one. Translate only that changed block
through the existing local Qwen provider and prove the other 107 targets remain
unchanged. Keep the artificial result out of Weblate.

Check the real HTML draft against the original, including tables, attributes,
numbers, CSS/scripts, images and out-of-scope pages. Review the selected pages
visually and record findings separately from the prior synthetic smoke test.
Return the evidence to the Mac chat, remove temporary test artifacts when the
task completes, and persist the verified result without changing the full
document or Web UI.
