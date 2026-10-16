# Shared GitHub credential source — 2026-10-16

`EDGE_GITHUB_MCP_TOKEN_SOURCE=PASS`

Operator requested automatic use of one current GitHub credential source,
removing manual updates to Codex, Hermes and Antigravity configurations.

The active stored gh credential is authoritative. Client Authorization fields
remain native protected generated copies; no common file-reference/header-command
mechanism is documented across all three clients. An automatic reconciler keeps
the three entries aligned with gh and applies changes to cached connections.
No GitHub authorization was issued, rotated, revoked or switched during this work.

Verified properties:

- Native gh credential extraction uses the audited core store, never an inherited
  GH_TOKEN/GITHUB_TOKEN override; values stay out of process arguments, status,
  journal, test fixtures and Git.
- Nine isolated tests cover source A→B rotation in all native formats, preserving
  unrelated fields, mode600, no-op behavior, unavailable source, transport drift,
  concurrent user edits, competing auth sources, durable reload retry and source environment isolation.
  One test initially called its own mocked credential reader; the fixture was
  corrected and all nine tests pass. No production defect was inferred.
- Native systemd validates all three units. The user path and timer are enabled
  and active, with core lingering. Timer interval is 60 seconds after completion;
  path events provide earlier notification. No permanent daemon/container is added.
- An initial explicit refresh read the real source, rewrote the three native
  configurations atomically and completed application. Codex's managed daemon
  remains PID2730265; its native RPC reloaded MCP. Hermes's native reload drained
  and replaced the gateway, its Dashboard restarted, and Antigravity restarted
  with Connected status. Subsequent scheduled no-op runs changed no client PID
  or configuration mtime. Stopped clients are not started by synchronization.
- A preliminary Codex proxy experiment timed out because a raw byte tunnel was
  given JSON lines. The helper process was reaped; the implementation uses the
  documented WebSocket control socket reported by native daemon version metadata.
- Real native get_me passed in Codex's current chat (44 tools), the installed
  Hermes runtime and Antigravity CLI (SUCCESS). All use the existing account.
- Nineteen monitoring tests pass. Source/application failure, stale success,
  disabled triggers and incomplete reload state affect the existing GitHub MCP
  incident. Live GitHub HTTP/container, credential sync and overall Edge are OK.
- Master Health passes for 9 system services, 4 user services, 12 Docker units,
  22 permanent containers, 2 SQLite databases and PostgreSQL readiness.
- Added distribution package python3-websockets (15.0.1-1build2 at installation),
  using the normal APT lifecycle; no other package upgrade/removal. PyYAML was
  already installed. The existing shared HTTP server/image/networks are retained.
- Temporary protected recovery copies, own test conversation/artifacts/cache
  entry and task directory removed after verification. Unrelated repository
  changes are preserved. Native audit logs keep their established lifecycle.

The real gh credential was not changed to test rotation: differing-token behavior
is covered by isolated tests; real deployment/application uses the current valid
credential. Native gh reauthorization remains necessary if GitHub invalidates or
expires that credential. Source polling is not an external GitHub validity probe.
Existing Backrest includes gh, client settings, script, units and state paths;
coverage is verified without running another full backup/quiesce.

Sanitized evidence: [token-sync-evidence-2026-10-16.json](token-sync-evidence-2026-10-16.json).
Contract and recovery: [README.md](README.md).
