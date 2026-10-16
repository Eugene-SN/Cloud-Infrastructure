# Shared GitHub MCP HTTP acceptance — 2026-10-16

Operator requested one permanent local HTTP service for Codex, Hermes and
Antigravity, real client verification and retirement of the STDIO deployment.

`EDGE_SHARED_GITHUB_MCP_HTTP=PASS`

- One `github-mcp` Compose container runs the same v2.0.2 image ID
  `sha256:ffced0d76e77428532a2ced185516992d77fd146d69eec2f244e6237d1a97796`.
  Loopback `127.0.0.1:18082` and internal `github-mcp:8082` reach native `/`.
  Unauthenticated requests return 401; authenticated initialize, tools/list
  (44 tools) and get_me pass. Internal DNS/HTTP tested from the existing n8n container.
- Codex's existing managed app-server accepted `config/mcpServer/reload` and
  its current chat connection returned 44 tools and a successful get_me.
  The existing daemon PID stayed running; seven STDIO containers exited.
- Installed Hermes runtime completed native HTTP discovery and get_me.
  Its four utility tools make 48 registered entries; the initial verifier's
  assumption of 44 total entries was corrected without changing the service.
- Native Antigravity CLI completed get_me and returned SUCCESS. Its existing
  daemon was restarted, verified on the installed executable, with stable PID
  and latest connection status Connected. The task's test conversation,
  artifacts, annotation, presence file and exact cache entry were removed.
- All three native configurations remain mode600; only their GitHub entries
  changed semantically. Existing token reused, no token in Git or server PAT env.
- `unless-stopped` and bounded json-file 10m ×3 verified from Docker inspect.
  Native upstream request-state key stored in root600 `.env`; existing Backrest
  edge-state paths include this configuration and protected client files. This
  verifies backup-plan coverage; no full backup/quiesce was run. The stateless
  service is reproducible from Git, a new native request-state key and existing gh credentials.
- Edge Monitor reports GitHub container/HTTP OK and overall OK. Seventeen
  monitoring tests pass, including challenge status, dependency failures,
  Docker parent suppression, deduplication and recovery without sending alerts.
- Maintenance now has 19 manual units / 12 Compose units. GITHUB_MCP registry
  discovery returns CURRENT 2.0.2 with matching live/remote digest. Native Compose
  preflight, maintenance contract and all 19 isolated update dispatch tests pass.
  Semaphore template 24 was created and read back through its native API.
  Its creation succeeded before an installer bookkeeping error (`Path.chown`);
  the file ownership was then corrected directly, without recreating the template.
  No image update or scheduled updater was introduced.
- Master health passes: 9 system services, 4 user services, 12 Docker units,
  22 permanent containers, 2 SQLite databases, PostgreSQL readiness.
- Removed installed STDIO launcher, both obsolete source copies, old pending
  STDIO image record, and 140 exact orphan CID directories. All CIDs were verified
  absent from Docker; no launcher process remained. No image, volume or unrelated
  service was deleted as part of this migration.
- Seven published and seven draft n8n workflows had no GitHub MCP/MCP Client
  reference; MCP credentials absent. Plane deployment files had no GitHub MCP
  endpoint. Shared internal endpoint is ready for an actual future consumer.

Fresh sanitized runtime evidence: [`evidence-2026-10-16.json`](evidence-2026-10-16.json).
The temporary research/recovery tree and task-owned test artifacts were removed
after verification. Native agent/CLI audit logs retain their normal upstream lifecycle.
Unrelated pre-existing repository edits were preserved outside this commit.
