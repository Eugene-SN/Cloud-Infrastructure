# Edge Stage 1 Public Masking Page Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_PUBLIC_MASKING_PAGE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Legacy continuity classification

The preserved migration archive does not contain the historical `/var/www/escloud.us/public` webroot or exact historical masking-page HTML. The preserved nginx reference does retain the external contract: `escloud.us` is a public masking page rooted at `/var/www/escloud.us/public`, and ordinary HTTPS reaches it through the accepted Xray -> nginx fallback path.

Because the historical HTML artifact is not preserved, the current Stage 1 page is an explicit replacement of the preserved contract, not a reconstructed copy.

## Accepted replacement

- path: `/var/www/escloud.us/public/index.html`;
- SHA256 at acceptance: `316252120c86fd1ed16a03451b432e8f006a5b13cec6bdd68d664dd953b139f5`;
- size at acceptance: 1376 bytes;
- static standalone HTML/CSS;
- no JavaScript;
- no external resources;
- neutral `ES Cloud` public facade;
- does not disclose internal service topology.

## Functional verification

- nginx configuration validation: PASS;
- HTTP delivery from `escloud.us`: PASS and matches the installed file;
- HTTPS delivery through Xray fallback: PASS and matches the installed file;
- `/health` non-regression: PASS;
- Hysteria2 masquerade directory remains `/var/www/escloud.us/public`;
- installed page remains readable as Hysteria2 masquerade content;
- nginx, Xray and Hysteria2 remain active;
- UFW remains active;
- Authelia remains running/healthy;
- failed systemd units: 0.

## Private portal scope boundary

A separate minimal private Cloud page is not introduced merely to create a temporary Stage 1 UI. Authelia already provides the accepted authentication foundation, while the fuller private Cloud Infrastructure portal belongs to the Stage 2 application composition. This avoids a disposable intermediate portal implementation.

## Next Stage 1 work

Close the remaining base-platform scope: accept the persistent/runtime path convention, create and verify the basic Stage 1 base-state checkpoint, document extension points, then run final integrated Stage 1 acceptance.
