# Edge Stage 1 Public Masking Page Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_PUBLIC_MASKING_PAGE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED** until the remaining base-platform scope and final integrated acceptance are complete.

## Accepted implementation

The accepted public masking page is the intentional new Stage 1 design at:

- path: `/var/www/escloud.us/public/index.html`;
- title: `ES Cloud — Private Workspace`;
- size: `22014` bytes;
- SHA256: `73ff3e57afa08c4f007f72902c1f2d3c8cf4e53920eabd10a86e32630106318e`;
- owner/group: root/root;
- mode: `0644`.

The page is a self-contained static private-workspace/file-access facade with no external runtime dependencies.

## Interaction contract

Potential navigation actions such as sign-in, workspace access, files, shared links, account and help open the same local authentication dialog.

This dialog is deliberately a visual masking-page interaction only:

- credentials are not submitted to a backend;
- credentials are not transmitted over the network by page JavaScript;
- credentials are not stored in localStorage/sessionStorage/cookies;
- credentials are cleared after a submit attempt;
- no additional real authentication layer is introduced.

Real service authentication remains outside this public masking-page simulation and is provided by the accepted application/Authelia architecture where applicable.

## Technical verification

Deployment verification passed:

- nginx configuration syntax: PASS;
- HTTP response body is byte-identical to the installed file: PASS;
- HTTPS through Xray TCP/443 fallback to nginx is byte-identical: PASS;
- `/health` remains `ok`: PASS;
- Hysteria2 masquerade root remains `/var/www/escloud.us/public`: PASS;
- nginx active: PASS;
- Xray active: PASS;
- Hysteria2 active: PASS;
- Docker active: PASS;
- UFW active: PASS;
- Authelia `running/healthy`: PASS;
- failed systemd units: `0`;
- `PRODUCTION_NON_REGRESSION=PASS`.

User visual review accepted the page on 2026-09-17.

## Superseded recovery path

The historical pre-rebuild page was previously identified as:

- title: `escloud.us — Private File Exchange`;
- observed size: `27017` bytes;
- observed Last-Modified: `2026-07-09T16:44:02Z`.

The selective migration archive omitted the historical `/var/www/escloud.us/public` tree. A provider-level whole-VPS backup remains a historical recovery source, but exact recovery of that old page is no longer required for Stage 1 because the user explicitly accepted the new intentional masking-page implementation.

The earlier simplified 1376-byte `ES Cloud` page with SHA256 `316252120c86fd1ed16a03451b432e8f006a5b13cec6bdd68d664dd953b139f5` remains rejected/superseded and is not a valid accepted implementation.

## Scope boundary

This acceptance covers only the public masking-page component. It does not by itself complete Stage 1 or authorize the final Stage 1 checkpoint before the remaining bounded Stage 1 scope is reconciled and verified.
