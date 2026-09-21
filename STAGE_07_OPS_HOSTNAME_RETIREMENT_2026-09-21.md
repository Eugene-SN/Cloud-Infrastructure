# Stage 7 — Former Semaphore Hostname Retirement — 2026-09-21

## Result

**COMPLETE / ACCEPTED**

`STAGE07_OPS_HOSTNAME_RETIREMENT=PASS`

## Accepted state

Semaphore remains available only through the accepted Stage 7 origin:

- `https://update.escloud.us/status/` — maintenance dashboard;
- `https://update.escloud.us/project/1/history` — Semaphore UI;
- `127.0.0.1:3000` — private Semaphore listener;
- `127.0.0.1:18070` — private maintenance dashboard listener.

The former `ops.escloud.us` candidate has no edge application vhost, Authelia rule, certificate SAN, certificate-domain entry, automation fallback or restorable dashboard target. Deleting its Cloudflare DNS record remains an explicit manual operator action outside this edge change.

## Runtime changes

- removed the hostname-specific rule from `/srv/authelia/config/configuration.yml`;
- removed the retired name from `/opt/vpn-stack/state/web-domains.txt`;
- removed both fallback references from `/opt/vpn-stack/scripts/maintctl`;
- added the previously missing `hermes.escloud.us` and `update.escloud.us` entries to the canonical/fallback renewal sets;
- reissued the shared `escloud.us` ECDSA certificate with 13 retained SANs;
- synchronized the new certificate to nginx/Xray, Hysteria2 and Stalwart consumers;
- removed superseded Certbot archive versions whose SAN set contained the retired name;
- removed the obsolete Stage 4 edge recovery archive and refreshed the two Stage 7 dashboard recovery copies plus their checksum manifest.

## Retained certificate SANs

- `escloud.us`
- `app.escloud.us`
- `auth.escloud.us`
- `backup.escloud.us`
- `chat.escloud.us`
- `cloud.escloud.us`
- `code.escloud.us`
- `docs.escloud.us`
- `hermes.escloud.us`
- `mail.escloud.us`
- `n8n.escloud.us`
- `sync.escloud.us`
- `update.escloud.us`

The active certificate is valid from 2026-09-21 through 2026-12-20. The live lineage points to `fullchain5.pem`; the retained `cert1.pem` and `cert5.pem` versions contain no retired SAN.

## Verification

- Authelia `config validate`: PASS; container health returned `healthy`;
- nginx `-t`: PASS; reload completed;
- `maintctl web-check`: `WEB_CHECK|OK`;
- SAN coverage: 13/13 PASS;
- ACME HTTP challenge: 13/13 PASS;
- Certbot staging renewal after archive cleanup: PASS;
- live and synchronized certificate copies: no retired SAN;
- nginx, Semaphore, Xray, Hysteria2 and `certbot.timer`: active;
- update root, dashboard and Semaphore paths preserve the accepted Authelia ingress and return paths;
- targeted scan of `/etc`, `/opt`, `/srv` and `/var/www`: no retired hostname reference after transient rollback material removal;
- Stage 7 dashboard recovery copy SHA-256: `0744d5293d580f4401a91f044f187d252bae28670555ee9080ce10658ba03b3c` for both source and live copies.

## Recovery handling

A root-only transient checkpoint was kept during the certificate/configuration mutation. It was removed only after native validation, certificate renewal, staging renewal and service checks passed, so no edge backup retained the retired hostname. Future recovery uses the accepted current configuration and certificate lineage.

The clean post-change recovery checkpoint is `/srv/backups/edge-stage7-hostname-retirement/recovery-20260921T113555Z`; its plaintext files and retained certificate archive were checked for the retired hostname/SAN.

## External follow-up

The operator will manually delete the Cloudflare DNS record for the retired hostname. No Cloudflare API or panel change was performed from edge.
