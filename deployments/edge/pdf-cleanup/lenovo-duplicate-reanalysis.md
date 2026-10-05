# Lenovo missing-document duplicate reanalysis

Date2026-10-05. Read-only follow-up requested by the operator.
This refines the earlier filename-based missing count in lenovo-model-audit.md.

## Corrected conclusion

Of the four remote filenames absent from the local model folder:
-Three represent separate documents not duplicated among the twelve local PDFs.
-One is an older edition of the BMC event-reference manual already present in its
fourth edition. It should not be ingested as a second missing document family
when keeping the current edition.

There are **three missing current document families**, not four, after
recognizing that BMC manual relationship. No originals were changed.

| Remote document | Pages | Result |
| --- | ---: | --- |
| wr5220g3_bios_setup_spec_v2.13.pdf | 87 | Separate BIOS Setup Specification |
| lenovo_bmc_event_reference_guide_g3_v3.pdf | 100 | Third edition, April2026; current fourth edition is already local |
| psu_label_matrix.pdf | 7 | Separate PSU labels and model/part-number mapping |
| vmware_code_recipe_file.pdf | 5 | Separate VMware firmware/driver recipe table |

## BMC edition/applicability evidence

lenovo_bmc_event_reference_guide_g3_v3.pdf is the third edition, April2026,
100 pages. Local lenovo_bmc_event_reference_guide_g5_v4.pdf is the fourth edition,
July2026,116 pages. Both carry the same manual title and explicitly state
applicability to WenTian G3/G5 servers on physical page6. The fourth edition also
contains explicit WR5220 G3 references.

The g3/g5 filename fragments do not distinguish exclusive hardware applicability
for this pair. This resolves the earlier UNKNOWN applicability of the G5-named
document: it explicitly includes G3. The files are not byte/text-identical, but
they are editions of one manual family with shared and changed material.

Use one explicit BMC event-reference family mapping for these two catalog
entries and prefer the later catalog update/edition. Do not globally strip G3/G5
from unrelated filenames: that would silently merge potentially different
generation-specific documents.

After that alias merge,18 raw catalog records produce14 current logical families.
Eleven ASP families plus LP1705 are already locally current; three ASP families
are absent. LP1705 continues to require its separate Lenovo Press source.

## Verification

Fresh read of twelve local PDF hashes; temporary GET of the four remote PDFs.
All four remote SHA-256 values were compared with every local PDF.
No byte-identical match exists. All-page text extracted with the existing
PyMuPDF1.28.2 runtime was normalized using NFKC/whitespace removal and compared:
no full text-identical match exists either. Page counts, PDF metadata, document
headings and the BMC edition/introduction were inspected.

The BIOS document concerns detailed BIOS configuration (87 pages).
PSU labels are a seven-page label/part-number/model reference.
VMware Code Recipe is a five-page firmware/driver/version table. These are not
full duplicates of the existing hardware user guide, product guide, OS
installation guide or management-tool manuals.

No claim is made that there is zero overlapping information between related
manuals. The byte/text checks establish lack of exact copies, and the headings/
contents establish distinct document roles. No all-page visual-equivalence or
complete semantic-superset proof was performed.

The first exploratory event-ID regexp matched no identifiers and was not used
as evidence of absence. Classification uses inspected covers/introduction/content.

Full evidence: lenovo-duplicate-reanalysis.json. Remote PDFs were held only in a
verified /tmp workspace and removed after inspection. Docker analysis used the
existing cleanup image, read-only mounts and --rm. No package/image changes,
workflow edits, local-library insertion, originals deletion or cleanup run.

Sources:
https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/wr5220g3_bios_setup_spec_v2.13.pdf
https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_event_reference_guide_g3_v3.pdf
https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/lenovo_bmc_event_reference_guide_g5_v4.pdf
https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/psu_label_matrix.pdf
https://download.lenovo.com/pccbbs/pubs/china-only-product_pdf/vmware_code_recipe_file.pdf
