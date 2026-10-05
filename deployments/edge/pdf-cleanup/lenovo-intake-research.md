# Lenovo WR5220 G3 / WR5228 G3 documentation intake research

Date: 2026-10-05. Status: **READ-ONLY AUDIT / PROPOSED DESIGN**.
No production configuration, workflow, Data Table or document was changed.
The prior cleanup candidate and its pending acceptance remain unchanged.

## Confirmed portal mechanism

Source page: https://asp.atlenovo.com/asp-service/index.html#/deviceInfo
The browser search option combines WR5220 G3 and WR5228 G3, with Type 7D8Y.
ProductId: SERVERS/LENOVOWENTIAN/WR5220G3WR5228G3
FullGuid: 339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E/E003AB30-9C7D-403E-B672-7B5EFB52C070/5D07DC93-3C2A-4986-BBB4-A04A44FAB99E

The User Guides tab makes this GET request:
https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide

Its query parameter fullGuid has the exact value above. The frontend also sends
_t as a cache timestamp. A direct request without _t/cookies/authentication
returned HTTP200 and JSON business status200 from edge and from Node26.7.0
inside the actual n8n2.40.7 container.

Response structure: {msg,status,data:[{title,updated,url,isChinese,sourceLanguage}]}.
The complete catalog is returned in one request; UI pagination is local.
Browser component source confirms GET with fullGuid; it is a website backend,
not a verified documented/versioned public API contract.

Observed: 18 records, 16 distinct PDF URLs, languages zc (16 records) and en (2).
One LXPM URL is duplicated; another appears with two older dates. Grouping by
trimmed/whitespace-normalized title and sourceLanguage and keeping the latest
updated row produces 15 title groups for this snapshot. The subsequent PDF
inspection in lenovo-duplicate-reanalysis.md confirms that two BMC event-reference
titles are editions of one manual, reducing the current logical families to14.
This is catalog
normalization, not a proven permanent document-identity rule: BIOS title itself
contains V2.13 and can change with a future release.

## Observed latest document groups

| Document | Catalog updated | Current remote basename |
| --- | --- | --- |
| 联想问天 WR5220 G3 WR5228 G3 服务器用户手册 | 2026-09-17 | lenovo_wentian_wr5220g3_user_guide_v18.pdf |
| Lenovo XClarity Essentials OneCLI cPlus 用户指南 | 2026-08-27 | lxce_onecli_cplus_ug.pdf |
| Lenovo XClarity Essentials BoMC cPlus 用户指南 | 2026-08-27 | lxce_bomc_cplus_ug.pdf |
| Lenovo XClarity Essentials UpdateXpress cPlus 用户指南 | 2026-08-27 | lxce_ux_cplus_ug.pdf |
| Lenovo BMC 日志参考手册 | 2026-07-31 | lenovo_bmc_event_reference_guide_g5_v4.pdf |
| WR5220 G3 BIOS Setup Spec V2.13 | 2026-04-21 | wr5220g3_bios_setup_spec_v2.13.pdf |
| Lenovo BMC IPMI 命令规范 | 2026-04-13 | lenovo_bmc_g3_commands_guide_v2.pdf |
| Lenovo BMC 企业版用户操作指南 G3 | 2026-04-10 | bmc_user_guide_v14.pdf |
| Lenovo BMC SNMP 参考手册 | 2026-04-10 | lenovo_snmp_ug_g3.pdf |
| Lenovo BMC G3 REDFISH 接口规范 | 2026-04-10 | lenovo_bmc_g3_redfish_guide_v11.pdf |
| Lenovo BMC G3 日志参考手册 | 2026-04-10 | lenovo_bmc_event_reference_guide_g3_v3.pdf |
| 联想问天服务器操作系统安装指南 | 2026-03-23 | lenovo_wentian_os_installation_guide.pdf |
| Lenovo XClarity Provisioning Manager WenTian 用户指南 | 2026-02-04 | lxpm_wentian_ug-v2.pdf |
| 联想服务器电源标签 | 2025-05-06 | psu_label_matrix.pdf |
| VMware Code Recipe File 3.0 | 2023-10-30 | vmware_code_recipe_file.pdf |

The catalog includes G3/v3 and G5/v4 event-reference filenames. Subsequent PDF
inspection confirmed that both manuals explicitly cover G3/G5 (physical page6)
and are the third and fourth editions of the same manual. G5/v4 is already local
and is the current edition of this family. See lenovo-duplicate-reanalysis.md
for the evidence and corrected missing-document count.

lp1705.pdf (Lenovo Press Product Guide) is absent from this API response.
If its updates are required, Lenovo Press is an additional source:
https://lenovopress.lenovo.com/lp1705-lenovo-wentian-wr5220-g3-server
https://lenovopress.lenovo.com/lp1705.pdf
The separately observed Product Guide page reports updated30 September2026.

## Download checks

Anonymous HEAD requests from edge returned HTTP200/application/pdf with
Content-Length, ETag, Last-Modified and Accept-Ranges:bytes for:
- lenovo_wentian_wr5220g3_user_guide_v18.pdf: 30,511,980 bytes,
  ETag "ac81274a7046dd1:0", Last-Modified17 September2026.
- wr5220g3_bios_setup_spec_v2.13.pdf: 13,620,825 bytes,
  ETag "515c165251cedc1:0", Last-Modified17 April2026.

A Range GET bytes0-15 of the user guide returned206, actual PDF signature,
Content-Range bytes0-15/30511980. No complete PDF was downloaded or installed.
This proves the tested links work anonymously now, not every future link.

## Proposed minimal n8n design

One new workflow, proposed name LenovoDocumentationSync01, and one native
Data Table, proposed name LenovoDocuments. No separate database, browser runner,
API service or generic orchestration layer.

Proposed schedule: daily. Manual trigger for initial review/testing.
Logical sequence:
1. GET Lenovo catalog; read the small Data Table.
2. Normalize duplicate/older catalog entries into document candidates.
3. HEAD current PDF links for ETag (Last-Modified fallback).
4. Compare catalog updated + source URL + remote validator with completed rows.
   Emit only new/changed documents. Empty output ends the run.
5. Process changed documents one at a time: GET PDF as binary, Nextcloud PUT
   into the agreed originals directory, call LenovoPdfCleanup01 and wait.
6. Upsert the completed row only after publication/cleanup success; continue
   with the next document.

Data Table fields can remain small: document_key, filename, source_url,
source_updated, remote_validator, processed_at. The key/filename identify the
document family independently of its versioned remote URL. Keep a stable local
filename on updates. Proposed examples (not deployed/accepted):
lenovo_wentian_wr5220g3_user_guide_v18.pdf -> wr5220g3_user_guide.pdf
wr5220g3_bios_setup_spec_v2.13.pdf -> wr5220g3_bios_setup_spec.pdf
lenovo_bmc_g3_redfish_guide_v11.pdf -> lenovo_bmc_g3_redfish_guide.pdf

Mapping must be explicit for initial document families; do not rely on title or
URL alone as a permanent ID. New unmatched families need a noncolliding filename
and become additional rows. Version/title changes should update the same family.

Originals: /srv/cloud/technical-documentation/lenovo/originals/
Cleaned: /srv/cloud/technical-documentation/lenovo/cleaned/
Only the download workflow replaces originals. The cleaner processes its read-only
snapshot and keeps the existing originals guard. Use existing Nextcloud WebDAV
credentials and successful binary transfers, preserving native versions.

ETag comparison is the actual update detector: it catches source-byte changes
even if URL/catalog date stays unchanged when the server updates its validator.
It adds no PDF content validation to n8n. Content preservation remains in the CLI.

Failed download must not proceed to publication. Failed cleanup leaves the row
uncompleted for retry; the previous cleaned file may still represent an older
original until cleanup succeeds. Do not mark that old cleaned copy as current.
Keep prior Data Table rows/files when an entry disappears from the catalog:
absence in a transient response is not evidence for deleting local documentation.

Do not deduplicate persistently before successful work: storing seen markers
before download/cleanup would risk skipping a failed document at the next poll.
Saving the receipt at the end allows ordinary retry without a separate queue.
Forced overlapping runs/same-basename updates need caller sequencing. The
existing cleanup candidate is unpublished; production integration/publication
belongs to the next explicitly authorized implementation scope.

## Small implementation verification plan

First test list/normalization without file writes. Then process one approved PDF,
verify original and cleaned placement through Nextcloud and successful CLI output.
Repeat unchanged catalog: zero downloads/cleanup calls. Simulate new date, changed
URL/ETag and versioned filename: update the same local family. Simulate transfer/
cleanup failure: no completed receipt; retry at the next run. Start bulk intake
only after these properties pass. No new enterprise checks or notifications.

References:
- Portal and its live browser network/source response above.
- https://docs.n8n.io/build/work-with-data/data-tables/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
