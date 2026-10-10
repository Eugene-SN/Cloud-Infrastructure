# Real lp2468 Hermes pilot — 2026-10-10

Historical controlled-diff evidence only. The operator subsequently clarified
that no new document version exists: this test does not accept the current
clean translator. The current task translates original pages 1–10 from scratch;
existing evidence is preserved without reuse of its English targets.

Scoped workflow VERIFIED. Evidence: `real-pilot-evidence.json`.
Mac/Weblate transferred the actual 108-unit source/draft/glossary package through
Mac → edge SSH and independently checked original hashes. No keys were copied.
No historical version was available: move/wrap/80% → 75% versions are explicitly
controlled temporary tests of this real sample, never publication candidates.
All 108 existing translations remain state-20 drafts; glossary has 133 entries.

| Case | Translated | Reused |
| --- | ---: | ---: |
| Unchanged | 0 | 108 |
| Moved | 0 | 108 |
| Audited prose wrapping | 0 | 108 |
| Controlled semantic diff | 1 | 107 |

Hermes/Qwen translated only unit 4871: “Supports various solid-state drives
(SSDs), with power consumption approximately 75% lower than hard disk drives
(HDDs)”. The previous wording differs only in 80% → 75%; 107 targets and every
other draft HTML byte are unchanged. This tests fidelity/reuse, not an actual
product specification update or a claim of improved baseline prose.

HTML checks retain 64 sections, 55 images, 51 tables, 359 rows and 1457 cells.
The received baseline removes seven audited introductory paragraph breaks.
Strict source-to-draft outside-page validation remains FAIL: five existing
native repeated-unit labels outside the six pages and nine whitespace changes.
The separate exact native tag/line/column audit finds zero unexpected changes.
It does not suppress the strict failure or authorize new outside changes.
Draft-to-controlled-copy validation passes, with zero new outside changes and
all other bytes preserved. Browser review of pages 1–3 and 9–11 finds zero
measured clipped tables/text and 55 loaded images, none broken.

The primary native semantic report claimed 108 but listed only 98 IDs; that
claim was rejected. A bounded supplement reviewed the omitted 10. The installed
native coverage validator confirms the union 108/108 with no missing IDs.
Four concatenated/paraphrased quote fields are rejected as literal evidence;
actual snapshot pairs remain authoritative. Native and independent Mac review
found no confirmed material meaning defect. Coverage does not auto-approve
meaning, and no draft was approved, rewritten or published.

Native Hermes v0.21.6+373.g46d7718 uses qwen3.8-27b-fp8 on the existing private
vLLM 0.30.0 route. Initial exit 143 has unknown cause; only the own stalled test
continuation was stopped (130) before the queue decision. Main continuation
completed with 0. The supplement saved its genuine report but exhausted 6 turns
and returned 1; uncaptured partial/completed flags remain UNKNOWN. One final
validation-only native turn ran the installed script, with max_turns 24:
exit 0, completed=true, partial=false, exactly one terminal call, no new review
or translation. Inline python-c approval failure was resolved by invoking the
script file, without changing approval settings. Per-client request_overrides
explicitly disabled thinking; no shared settings or FIFO priorities changed.

Skill1.0.2 is available; ten regression tests pass. Gateway/Dashboard are active
and global config hash is unchanged. Source, actual English draft, full document,
Weblate, Web UI and shared vLLM/provider configuration are untouched.

Edge send_message_to_thread is absent from the initial Desktop dynamic-tools
registration, including after reconnect; the exact Desktop filtering condition
is unknown. Native registration was not repaired. Automatic coordination works
through Mac delegated messages and Mac reading edge commentary/results through
native thread reads and existing authenticated SSH, without operator relay.
