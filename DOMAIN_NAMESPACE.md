# Cloud Infrastructure — Domain Namespace

## Status

**ACCEPTED target namespace as of 2026-09-17.**

This file defines the intended `escloud.us` hostname allocation for Cloud Infrastructure. It is a naming/ingress contract, not proof that every listed service is already deployed.

## Active / Stage 2 names

| FQDN | Role | State |
|---|---|---|
| `escloud.us` | public masking/decoy page and public edge identity | ACTIVE |
| `edge.escloud.us` | VPS infrastructure hostname for node `edge` | ACTIVE DNS identity; not an application vhost by default |
| `auth.escloud.us` | Authelia | ACTIVE |
| `app.escloud.us` | main private Cloud Infrastructure portal | TARGET Stage 2 |
| `n8n.escloud.us` | n8n automation UI/API/webhooks | TARGET Stage 2; replaces legacy `go.escloud.us` |
| `code.escloud.us` | CloudCLI workspace/interface | TARGET Stage 2 |
| `mail.escloud.us` | Stalwart APIs/admin/JMAP plus Bulwark webmail | TARGET Stage 2 |
| `backup.escloud.us` | Backrest | TARGET Stage 2 |
| `ops.escloud.us` | Semaphore / operational execution | TARGET Stage 2 |

## Reserved future names

| FQDN | Reserved role | Stage |
|---|---|---|
| `docs.escloud.us` | technical documentation library | future |
| `chat.escloud.us` | reserved for a potential future chat/service endpoint | future |
| `cloud.escloud.us` | future file-access layer; implementation unresolved | Stage 4 |
| `sync.escloud.us` | future synchronization layer; implementation unresolved | Stage 4 |

Reserved names do not authorize premature service deployment.

## Legacy name to retire

| FQDN | Historical role | Target disposition |
|---|---|---|
| `go.escloud.us` | n8n | retire after successful migration and acceptance of `n8n.escloud.us` |

Do not preserve `go.escloud.us` indefinitely as an alias unless a concrete compatibility requirement appears.

## DNS contract

Application/service A records point to the current public IPv4 of `edge`, `45.92.156.17`, unless a later architecture decision explicitly changes that relationship.

`edge.escloud.us` is the infrastructure hostname. Current intended records are:

- `A edge.escloud.us -> 45.92.156.17`
- `AAAA edge.escloud.us -> 2a0c:b847:ffff:283::a`

`edge.escloud.us` does not require an nginx vhost, Authelia rule, or inclusion in the shared application TLS certificate unless an HTTPS service is deliberately assigned to that hostname later.

## TLS application certificate target

After the n8n hostname migration, the shared `escloud.us` application certificate should cover:

- `escloud.us`
- `app.escloud.us`
- `auth.escloud.us`
- `backup.escloud.us`
- `chat.escloud.us`
- `cloud.escloud.us`
- `code.escloud.us`
- `docs.escloud.us`
- `mail.escloud.us`
- `n8n.escloud.us`
- `ops.escloud.us`
- `sync.escloud.us`

`go.escloud.us` should be removed from the target SAN set after its migration is accepted.

## Authentication namespace

Authelia remains the common web-login point where application semantics support proxy authentication.

Target protected application names include:

- `app.escloud.us`
- `n8n.escloud.us`
- `code.escloud.us`
- `backup.escloud.us`
- `ops.escloud.us`
- reserved future `docs.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, and `sync.escloud.us` when corresponding services are actually deployed.

`mail.escloud.us` is not blanket-assigned to generic Authelia protection because Stalwart/JMAP/webmail has protocol/API-specific routing and authentication semantics; its Stage 2 mail ingress is handled separately.

## Naming principles

- Prefer stable functional names for infrastructure-facing services where that avoids unnecessary coupling to a product name (`ops` for the operational execution plane, `backup` for backup management).
- Use `n8n.escloud.us` because n8n is an explicitly accepted product and the legacy `go` name is opaque.
- Do not create hostnames or placeholders merely because they existed historically.
- Reserved names are kept only where a concrete future functional role has been identified.
