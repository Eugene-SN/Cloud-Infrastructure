# Edge Stage 1 Public Masking Page Acceptance — 2026-09-17

**Status:** REVOKED / NOT ACCEPTED  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Corrected acceptance result

`EDGE_STAGE1_PUBLIC_MASKING_PAGE_ACCEPTANCE=REVOKED`

The earlier PASS recorded in this file was incorrect and is superseded by this correction. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Why the earlier acceptance was invalid

The Stage 1 rebuild installed a new simplified replacement at `/var/www/escloud.us/public/index.html` with SHA256 `316252120c86fd1ed16a03451b432e8f006a5b13cec6bdd68d664dd953b139f5` and size 1376 bytes. That file was technically functional, but it was not the previously created public masking page the project intended to carry forward.

Existing project evidence identifies the prior page as:

- path: `/var/www/escloud.us/public/index.html`;
- title: `escloud.us — Private File Exchange`;
- observed size: 27017 bytes;
- observed Last-Modified: `2026-07-09T16:44:02Z`;
- page purpose: public masking / private-file-exchange facade.

The selective migration archive does not contain the historical `/var/www/escloud.us/public` tree, so absence from that archive does not prove the prior page did not exist or should be replaced.

## Current runtime state

The simplified 1376-byte `ES Cloud` page is currently installed and functional through HTTP, Xray->nginx HTTPS fallback, and the Hysteria2 masquerade root. It is therefore a temporary runtime placeholder only and is **not accepted** as the intended Stage 1 masking page.

## Required recovery

Recover the exact earlier `escloud.us — Private File Exchange` artifact from an authoritative retained source rather than reconstructing it from memory. The whole-VPS provider backup is the primary known recovery source because the selective migration archive omitted `/var/www`.

After recovery, verify the recovered file identity/content and public HTTP/HTTPS/Hysteria behavior, then issue a new masking-page acceptance record.

## Scope boundary

Do not proceed to final Stage 1 acceptance while this recovery remains unresolved.
