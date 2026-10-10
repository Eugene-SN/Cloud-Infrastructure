# English quality rules from the lp2468 review

The reviewed 10-page draft has 187 translated blocks. All source/target pairs
and screen pages were inspected. HTML coverage and resource checks do not
make its literal English suitable for publication.

## Official English reference

Use the [Lenovo ThinkSystem SR665 V3 Product Guide (LP1608)](https://lenovopress.lenovo.com/lp1608.pdf)
for English terminology and natural technical phrasing. The inspected PDF has
161 pages, SHA-256 `952f8ca345e0a3cc6b2e8cd77a70ed4c05160758eedfacab2138a2b530c74ea6`.
Pages 1–4 demonstrate concise introduction, performance, availability,
manageability, security and energy sections; page 14 establishes AnyBay storage
context and page 18 expands TDP. This is an English language reference, not a
parallel translation of WR6220 G5. Current lp2468 remains the factual authority.

Prefer clear subjects and active technical verbs, short sentences within each
original paragraph, and parallel noun phrases in specification lists. Keep a
limit once, with the same quantity and conditions. Keep failure prediction
qualified; a monitoring capability is not a guarantee. Keep optional capabilities
optional. Use singular/plural and sentence case naturally in running text.

The supplement records source evidence and English page references separately.
An exact reference term differs from a contextual adaptation: fan module, host
network port and chassis intrusion detection preserve the Chinese meaning but
are not claimed as verbatim LP1608 names. Never substitute a chassis intrusion
switch for unspecified monitoring, a rack latch for a rack ear, or open-loop
cooling for a cold plate without matching-source evidence.

Do not copy the SR665 identity, AMD processor family, configurations, counts,
power ratings, management branding, warranty or promotional claims. Parallel
phrasing is reusable only after every source fact and condition is verified.

## Operator glossary

Use the operator's 252-entry [wentian-en.json](wentian-en.json) before choosing
technical wording. Its supplement adds 31 gaps confirmed in the reviewed pages,
with context and actual evidence block IDs. The original 252 entries were parsed
after the CSV's non-data language-list preamble;
all entries are Simplified Chinese → English. Keep the CSV flags and source hash.
Do not invent Russian entries. Short terms are terminology guidance; full
sentences and model-bound entries are conditional reuse candidates.

## Grounded cases, not replacements to apply blindly

| Chinese/context | Draft problem | Rule for future translation |
|---|---|---|
| 整机规格; page02-block014/page09-block161 | Whole machine specifications | System specifications for this hardware context; consistent with table/TOC role. |
| 整机爆炸图; page02-block015 | Whole machine exploded view | System exploded view; do not fabricate an absent diagram. |
| 内存支持类型; page03-block038 | Memory supported types | Supported memory types. |
| 左耳 / 右耳 with front I/O; page10-block175 | Left ear / Right ear | Include rack-mounting context: left/right rack ear. “Rack latch” requires matching-model component evidence, not analogy alone. |
| 1*温感（进风口温度检测）; page10-block175 | 1*temperature sensing | One temperature sensor; preserve inlet-temperature function and count. |
| 同一驱动器托架内; page06-block098 | within the same drive tray | The operator glossary maps 硬盘托架 to drive bay in this compatibility context; preserve AnyBay mixing semantics. |
| 最多可支持36个NVMe SSD; page06-block098 | up to 36 ... at most | One limit expression, same quantity. |
| 确保…I/O密集型工作负载; page06-block097 | to ensure I/O-intensive workloads | State support for the workloads in natural English; keep all original slot/GPU/optional conditions. |
| 故障（或即将出现故障）的组件; page08-block133 | impending-faulty components | Components that have failed or are at risk of failure, without implying guaranteed prediction. |
| Intro page01-block001/page07-block103 | long chained semicolon sentences | Separate English sentences inside the same semantic paragraph; no hard-coded br. |

Never transfer numbers from an example. WR6220 6900P and 6900E+ have different
core/TDP limits in the source. The R5225 reference uses AMD; it cannot correct
this Intel guide. General versus enhanced/configuration-specific limits must
not be collapsed (for example 6 versus 18 PCIe slots).
Keep the source's 80% SSD power reduction; do not copy another draft's 75%.

Source ambiguities stay visible for review:
- page10-block186 says 存储/无存储湿度. Do not silently substitute non-operating.
- page08-block146/page10-block183 say 国产 TPM, not 国密. Do not invent a
  cryptographic standard or another vendor.
- The intro's P-core/E-core and memory terminology can be inconsistent with other
  source sections; flag contradictions, do not “repair” specifications by analogy.

Reviews must quote actual source/target text with IDs. The first previous review
invented a copyright/revision section and dates; a later one asserted “rear battery”
where the source listed I/O/power. These are review errors, not document facts.

## Rendering issues to route to presentation

The actual draft has OCR logo words (“Lenovo / LENOVO / PRES S”), uneven TOC
leaders/number-only entries, mixed literal bullet glyphs and list tags, body
prose classified as headings, and a muted specification caption.
Do not manually patch these during an audit. A presentation run needs a
source-verified role/exception plan and independent content/resource checks.
The obsolete PDF prose br wraps are already absent from the current draft;
normal browser line wrapping is expected.

Basis: current draft SHA-256
`69997a57f452448866fe745b5ca2039269ad853abed5df5d6856466c8f66026b`.
This is a reviewed machine draft, not a new normalized translation or acceptance
of any untested future output.
