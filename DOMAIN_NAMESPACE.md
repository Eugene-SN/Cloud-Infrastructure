# Cloud Infrastructure — Domain Namespace

## Status

**ACCEPTED target namespace reconciled on 2026-09-19 against Stage 4 final acceptance.**

This file defines the intended `escloud.us` hostname allocation for Cloud Infrastructure. It is a naming/ingress contract, not proof that every listed service is already deployed.

## Active names

| FQDN | Role | State |
|---|---|---|
| `escloud.us` | public masking/decoy page and public edge identity | ACTIVE |
| `edge.escloud.us` | VPS infrastructure hostname for node `edge` | ACTIVE DNS identity; not an application vhost by default |
| `auth.escloud.us` | Authelia | ACTIVE |
| `n8n.escloud.us` | n8n automation UI/API/webhooks | ACTIVE |
| `code.escloud.us` | CloudCLI workspace/interface | ACTIVE |
| `mail.escloud.us` | Stalwart APIs/admin/JMAP plus Bulwark webmail | ACTIVE |
| `hermes.escloud.us` | Hermes Dashboard and Desktop Remote Gateway | ACTIVE; native self-hosted OIDC through Authelia; loopback backend |
| `chat.escloud.us` | Mattermost collaboration/control | ACTIVE; Mattermost-native authentication; no Authelia proxy auth |
| `update.escloud.us` | maintenance dashboard and Semaphore UI | ACTIVE; Xray/nginx/Authelia ingress; `/status/` dashboard plus `/project/1/history` Semaphore UI; loopback backends only |

## Accepted future functional names

| FQDN | Intended role | Dependency placement |
|---|---|---|
| `backup.escloud.us` | Backrest backup-management UI | late lifecycle after main service inventory stabilizes |
| `app.escloud.us` | final private Cloud Infrastructure portal/dashboard | separate Codex substage after production monitoring/status sources and final service inventory are known |
| `cloud.escloud.us` | future file-access/web file-management layer | after `edge ↔ ai-node ↔ PVE/Home` connectivity if the selected implementation requires that relationship |
| `sync.escloud.us` | future synchronization layer | after cross-site connectivity; exact implementation unresolved |

## Reserved future names

| FQDN | Reserved role | State |
|---|---|---|
| `docs.escloud.us` | technical documentation library or documentation-facing endpoint | RESERVED; no service implied |

Reserved names do not authorize premature service deployment.

## Retired / unused names

| FQDN | Historical role | Disposition |
|---|---|---|
| `go.escloud.us` | n8n | RETIRED after accepted migration to `n8n.escloud.us` |
| `ops.escloud.us` | prepared candidate for a separate Semaphore UI | RETIRED from edge on 2026-09-21; operator will remove the remaining Cloudflare DNS record manually |

Do not preserve retired or unused names indefinitely unless a concrete compatibility requirement appears. The former `ops.escloud.us` name has no edge vhost, Authelia rule, certificate SAN, automation entry or recovery copy; its external Cloudflare DNS record is pending operator deletion.

## DNS contract

Application/service A records point to the current public IPv4 of `edge`, `45.92.156.17`, unless a later architecture decision explicitly changes that relationship.

`edge.escloud.us` is the infrastructure hostname. Current intended records are:

- `A edge.escloud.us -> 45.92.156.17`
- The former `AAAA edge.escloud.us -> 2a0c:b847:ffff:283::a` is an earlier documented allocation, not evidence of current IPv6 reachability. Current accepted edge public networking is IPv4-only. Verify authoritative DNS separately before any DNS change; this reconciliation changes documentation only.

`edge.escloud.us` does not require an nginx vhost, Authelia rule, or inclusion in the shared application TLS certificate unless an HTTPS service is deliberately assigned to that hostname later.

## TLS application certificate target

The current shared application certificate lineage covers the accepted current application namespace except where a future hostname has not yet been activated. `update.escloud.us` is active in the shared certificate and public ingress.

Future deployment stages should add a hostname to the certificate only when the corresponding service/page is actually being deployed. DNS existence alone remains insufficient evidence of activation for the remaining future names.

The intended namespace includes:

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

`go.escloud.us` and `ops.escloud.us` remain outside the target namespace.

## Authentication namespace

Authelia remains the common web-login point where application semantics support proxy authentication.

Protected application names are expected to include, when corresponding services are actually deployed:

- `app.escloud.us`;
- `n8n.escloud.us`;
- `code.escloud.us`;
- `backup.escloud.us`;
- `update.escloud.us`;
- future/reserved `docs.escloud.us`, `cloud.escloud.us`, and `sync.escloud.us` where appropriate.

`chat.escloud.us` uses Mattermost-native authentication without Authelia. `hermes.escloud.us` uses Hermes-native self-hosted OIDC with Authelia as IdP; nginx does not use `auth_request` for Hermes. See `STAGE_04C_FINAL_ACCEPTANCE_2026-09-18.md` and `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`.

`mail.escloud.us` is not blanket-assigned to generic Authelia protection because Stalwart/JMAP/webmail has protocol/API-specific routing and authentication semantics; its ingress is handled separately.

## UI role separation

`app.escloud.us` and `update.escloud.us` have intentionally distinct responsibilities:

- `app.escloud.us` — navigation plus concise monitoring/status dashboard for the finished Cloud Infrastructure;
- `update.escloud.us` — the complete Stage 7 operator origin: custom maintenance dashboard at `/status/` and full Semaphore UI at `/project/1/history`.

Do not collapse detailed maintenance/update controls into `app.escloud.us` merely for UI consolidation.

## Naming principles

- Prefer stable functional names for infrastructure-facing services where that avoids unnecessary coupling to a product name (`backup`, `update`).
- Use `n8n.escloud.us` because n8n is an explicitly accepted product and the legacy `go` name is opaque.
- Do not create hostnames or placeholders merely because they existed historically.
- Reserved names are kept only where a concrete future functional role has been identified.
- DNS existence alone does not prove service deployment, TLS activation, ingress configuration or application acceptance.
