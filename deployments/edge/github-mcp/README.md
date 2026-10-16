# Shared GitHub MCP on Edge

The 2026-10-16 deployment replaces the per-connection Docker STDIO launcher.
Codex, Hermes and Antigravity use one permanent upstream HTTP server.

| Property | Accepted runtime |
|---|---|
| Deployment | `/opt/github-mcp/compose.yaml`, service/container `github-mcp` |
| Host clients | `http://127.0.0.1:18082/` |
| Containers on existing `edge_internal` | `http://github-mcp:8082/` |
| Image track | `ghcr.io/github/github-mcp-server:latest`; deployed v2.0.2, unchanged image |
| Lifecycle | Docker Compose, `restart: unless-stopped` |
| Tools | `repos,issues,pull_requests,actions` plus `get_me`, 44 discovered tools |
| Logs | Docker `json-file`, `max-size=10m`, `max-file=3` |
| Monitoring | Existing Edge Monitor, container state plus unauthenticated HTTP 401 |
| Updates | Existing Maintenance `GITHUB_MCP`, Semaphore template 24, manual only |
| Recovery | Existing Backrest `edge-state`, including `/opt` and protected client configurations |

The native HTTP handler is mounted at `/`. The host port binds only to loopback;
Docker peers use the existing private network. No public route is installed.
Multiple MCP client connections share the same server process and container.
The image is distroless and has no shell/curl health probe; Edge Monitor performs
the HTTP check from the host. This is a liveness/authentication-challenge check,
not a continuous GitHub credential or external API test.

## Authentication and clients

Upstream HTTP consumes a GitHub bearer on each request. The server does not
receive a static GitHub PAT in its environment. All three protected mode600
client files use the existing operator credential obtained from `gh auth token
--hostname github.com`; no new account or token was created. Native fields are
Codex `url`/`http_headers`, Hermes `url`/`headers`, and Antigravity
`serverUrl`/`headers`. Secret-free examples are in
[`../interaction-fabric/clients`](../interaction-fabric/clients).

The headers contain the credential value at configuration time. A later token
rotation must also update these three native client entries and reload their
connections; they do not dynamically rerun `gh auth token` on each request.
Codex supports `config/mcpServer/reload` without daemon restart; Hermes has native
MCP configuration reconciliation/reload; Antigravity has its native MCP manager
reload, or the existing user daemon can be restarted when applying configuration.

`/opt/github-mcp/.env` is root-owned mode600 and contains only
`GITHUB_MCP_SERVER_MRTR_STATE_KEY`, a base64-encoded random 32-byte key. This is
upstream's HTTP request-state encryption setting for multi-round-trip operations.
It is not a GitHub credential and is not committed. Restoring the protected
deployment directory restores it. The Backrest plan already includes both `/opt`
and `/home/core`, with no exclusion of these paths. This work verified plan
coverage; it did not run another full backup or quiesce application databases.

The seven draft and seven published n8n workflow definitions contain no GitHub
MCP or MCP Client nodes, and n8n has no MCP credential. Plane deployment files
contain no GitHub MCP endpoint. Neither was given an invented integration.
A future actual Docker consumer can use the shared internal address and its
appropriate GitHub bearer through its supported MCP HTTP client.

## Verification, cleanup and recovery

The live Codex app-server connection, installed Hermes MCP runtime and native
Antigravity CLI each completed `get_me`. Codex and Hermes discovery returned
the preserved 44 GitHub tools. Codex reloaded loaded chats without restarting the daemon;
Antigravity's existing daemon was restarted and verified on its installed binary
with `Connected` status. Other client settings remained semantically identical.

The seven former STDIO containers exited after Codex configuration reload.
Removed the installed launcher, both retired source copies, the obsolete pending
STDIO image-capture record, and 140 orphan CID directories after verifying every
CID was absent from Docker and no old launcher remained. Historical acceptance
records retain their original evidence; current examples and documentation use HTTP.

Before cutover, protected exact client/launcher/config copies were kept only in
the task's temporary recovery directory. They were removed after verification.
The stateless service can be rebuilt from the committed Compose file, a newly
generated upstream 32-byte request-state key and the existing gh credential in
protected native client headers. No application data volume needs restoration.
For snapshot recovery, restore the matching Compose file, `.env` and client files
from Backrest, start the Compose service and reload clients;
check native HTTP 401, tools discovery and an authenticated `get_me` in each client.
For a deliberate transport rollback, Git history contains the previous launcher
and secret-free client shapes; recover credentials from the existing protected
backup or gh context. This is a recovery procedure, not a second retained runtime.

Acceptance: [`ACCEPTANCE_2026-10-16.md`](ACCEPTANCE_2026-10-16.md).

## Authoritative references

- [Exact upstream HTTP implementation, v2.0.2](https://github.com/github/github-mcp-server/tree/v2.0.2/pkg/http)
- [GitHub MCP configuration](https://github.com/github/github-mcp-server/blob/v2.0.2/docs/server-configuration.md)
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp), [native app-server reload and tool calls](https://learn.chatgpt.com/docs/app-server)
- [Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Antigravity MCP configuration](https://antigravity.google/docs/mcp/)
- [Semaphore native API](https://semaphoreui.com/api-docs)
