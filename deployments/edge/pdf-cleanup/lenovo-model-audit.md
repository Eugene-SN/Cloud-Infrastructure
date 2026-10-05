# Lenovo model-folder comparison audit

Date: 2026-10-05. **READ-ONLY / monitoring design**, not deployment acceptance.

## Operator-selected model layout

- Originals: /srv/cloud/technical-documentation/lenovo/originals/WR5220 G3/
- Cleaned: /srv/cloud/technical-documentation/lenovo/cleaned/WR5220 G3/
- English translation: /srv/cloud/technical-documentation/lenovo/translated/en/WR5220 G3/
- Russian translation: /srv/cloud/technical-documentation/lenovo/translated/ru/WR5220 G3/

The operator-created originals folder exists, owned www-data33:33. Model
subfolders under cleaned and translated were absent at this audit. They should
be created through Nextcloud when implementing the model-aware processing path.
The already-established language level of translated/en and translated/ru is
preserved. Other models get equivalent folders when selected for intake.

Cleanup input should be {"model":"WR5220 G3","filename":"lp1705.pdf"}.
The existing thirteen-node cleanup candidate still constructs flat paths:
model support is the required next implementation change, not an already
deployed property. Its node count need not increase to construct model paths.
Use separate validated path components and encode DAV URL segments for spaces.

Keep PDF_CLEANUP_ORIGINALS_DIR at the entire canonical originals root, not a
single model subfolder: the existing guard protects every model subtree.
Actual originals remain outside the cleaner's container; its snapshot is readonly.

## Actual comparison

Fresh ASP catalog:18 records,15 latest document groups. Initially13 local PDFs;
11 exactly match ASP URLs, LP1705 matches Lenovo Press, and one additional -- file
does not match a catalog URL. Existing matched PDFs were streamed from Lenovo
and SHA-256 compared with the locally read bytes; no downloaded PDF was saved.
Missing PDFs were checked with HEAD only. This is a one-time baseline audit,
not a proposal to hash/download every PDF on every scheduled run.

All twelve matched local documents are byte-identical to current remote PDFs.
There are no observed outdated matched files. File mtimes were not used as
vendor publication dates. Copy/synchronization timestamps do not establish a
file's vendor version.

| Local/catalog document | Observed outcome |
| --- | --- |
| lxce_ux_cplus_ug.pdf | SHA-256 identical |
| lxce_onecli_cplus_ug.pdf | SHA-256 identical |
| wr5220g3_bios_setup_spec_v2.13.pdf | Missing locally; remote HEAD200 |
| lxce_bomc_cplus_ug.pdf | SHA-256 identical |
| lenovo_bmc_event_reference_guide_g5_v4.pdf | SHA-256 identical |
| bmc_user_guide_v14.pdf | SHA-256 identical |
| lenovo_wentian_wr5220g3_user_guide_v18.pdf | SHA-256 identical |
| lenovo_snmp_ug_g3.pdf | SHA-256 identical |
| lenovo_bmc_event_reference_guide_g3_v3.pdf | Missing locally; remote HEAD200 |
| lenovo_bmc_g3_redfish_guide_v11.pdf | SHA-256 identical |
| lenovo_wentian_os_installation_guide.pdf | SHA-256 identical |
| lenovo_bmc_g3_commands_guide_v2.pdf | SHA-256 identical |
| lxpm_wentian_ug-v2.pdf | SHA-256 identical |
| vmware_code_recipe_file.pdf | Missing locally; remote HEAD200 |
| psu_label_matrix.pdf | Missing locally; remote HEAD200 |
| lp1705.pdf | SHA-256 identical |

Four current ASP documents are missing locally:
- wr5220g3_bios_setup_spec_v2.13.pdf
- lenovo_bmc_event_reference_guide_g3_v3.pdf
- psu_label_matrix.pdf
- vmware_code_recipe_file.pdf

The initial extra file --lenovo_wentian_wr5220g3_user_guide_v18.pdf was20,554,122
bytes; Lenovo's corresponding unprefixed PDF was30,511,980 bytes, and the hashes
differ. Its origin is UNKNOWN. It disappeared during this read-only audit;
the agent did not issue a deletion. Final folder count is twelve, all surviving
audit files unchanged. The extra file is retained only as an observation in the
audit evidence, not as a current file or a verified vendor document.

LP1705 is not in the ASP catalog. Its Lenovo Press PDF is also byte-identical,
with no ETag and Last-Modified30 September2026. Monitoring it requires that
additional source and Last-Modified fallback.

The G5 event-reference PDF is present locally and byte-identical to Lenovo's
G3-associated catalog entry. Applicability was initially unverified. The subsequent
PDF inspection in lenovo-duplicate-reanalysis.md confirms explicit G3/G5 scope
and identifies it as the fourth edition of the same manual as G3/v3. The missing
counts below describe the initial filename comparison; the follow-up corrects
the number of missing current document families to three.

## Proposed initial registration and update comparison

One native Data Table can hold model + document_family as its logical key,
and local filename, source URL, catalog updated, ETag/Last-Modified and successful
processing status. Keep the remote version separate from the family identity.
The filename policy from the preceding research remains proposed, not accepted;
this audit did not rename any existing originals.

Register the twelve verified existing originals with their current remote
validators instead of downloading them again. That means originals are current,
not that cleaned/translated copies exist. Missing cleaned outputs still need
processing independently of the original's download marker. Do not label an
original-only baseline as successful end-to-end cleanup.

For first intake comparison, the expected result is:
-12 existing/current originals: no replacement download;
-4 missing ASP PDFs: download candidates;
-LP1705 tracked through a separate Lenovo Press source;
-no catalog-matched local file presently requires replacement.

The update marker is source URL + catalog updated + remote ETag. If ETag is
absent, use Last-Modified (and Content-Length where available).
Store success after the corresponding stage actually succeeds. Disappearing
catalog entries must not cause automatic deletion of local documentation.

The same combined WR5220/WR5228 source can be configured for a chosen model
folder. Do not create a duplicate WR5228 library merely by inferring another
selected target from the source's combined model label.

## Comparison-logic checks

Pure local simulations, using the actual verified catalog records:
-12 unchanged baselines -> skip replacement download.
-4 missing baselines -> download candidates.
-Changed ETag, catalog date or source URL -> update.
-Versioned user-guide v18/v19 URLs map to one family.
-BIOS v2.13/v2.14 URLs map to one family.
-The same family under WR5220 G3 and WR5228 G3 has separate model keys.
-LP1705 without an ETag uses Last-Modified changes.

These are tested proposed rules, not a running n8n monitoring workflow.
No Data Table, folders, workflow parameters, originals, cleaned outputs or
translations were created/changed by this audit. The live cleanup candidate
remained unpublished with thirteen nodes and unchanged version during the audit.

Full observations/hashes/validators: lenovo-model-audit.json.
Mechanism research: lenovo-intake-research.md.
Sources:
https://asp.atlenovo.com/asp-service/index.html#/deviceInfo
https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide
https://lenovopress.lenovo.com/lp1705.pdf
https://lenovopress.lenovo.com/lp1705-lenovo-wentian-wr5220-g3-server

## Duplicate reanalysis refinement

The later operator-requested content audit identifies the missing G3 event-reference
PDF as the third edition of the same G3/G5 manual already held in fourth edition.
The filename-based count remains historical evidence; the current-edition missing
count is three document families. See lenovo-duplicate-reanalysis.md.
