# Edge ↔ Mac chat coordination audit — 2026-10-10

Result: registration boundary identified; bidirectional delivery NOT restored.
The real 108-unit lp2468 pilot remains pending. No document, Weblate, Hermes
provider, vLLM, Desktop configuration or app-server lifecycle was changed.

## Confirmed evidence

- Edge CLI and managed app-server both report `0.162.1`; native daemon version
  reports running, with the existing Unix control socket. The process uses
  `app-server --remote-control --listen unix:// --managed-daemon`.
- The latest inspected Mac chat `01a121de-3b75-7d33-8fa3-650ece5d8b90` used
  `send_message_to_thread` successfully when delegating to edge. Its latest
  inspected turn is completed and the chat reports idle.
- Both initial and forked edge rollout metadata identify the originator as
  `Codex Desktop` and persist a client-supplied `codex_app` namespace containing
  32 tools. It includes `read_thread` and `wait_threads`, but excludes
  `send_message_to_thread`, `create_thread`, `fork_thread` and `handoff_thread`.
- The current callable tool catalog has the same omission. The global callable
  namespace has no `codex_app__send_message_to_thread` implementation.
- Edge user configuration has no `codex_app` MCP server, no setting naming
  `send_message_to_thread`, and no explicit feature disabling chat coordination.
  The existing named MCP servers are unrelated to Desktop chat coordination.
- Native `codex app-server generate-json-schema --experimental` confirms that
  `ThreadStartParams` accepts `dynamicTools`, whereas `ThreadResumeParams` in
  this exact installed version has no such field. Generated audit files were
  removed from `/tmp` immediately after inspection.
- Native CLI `codex queue` addresses tasks through a connected app-server;
  `codex agents` describes its scope as the shared local app-server. No supported
  authenticated endpoint for the Mac app-server was supplied or discovered.

## Mechanism and limits

Official [App Server documentation](https://learn.chatgpt.com/docs/app-server)
describes client-provided dynamic tools, their persistence in rollout metadata,
and client execution through `item/tool/call`. This matches the edge metadata:
the missing operation was omitted before model tool discovery. Adding an SSH
key or a Weblate credential would not register a Desktop chat tool.

Inference: the remaining defect or capability restriction is in the Desktop
registration path for this remote chat. Evidence does not distinguish an
intentional host capability filter, a Desktop bug, or another client condition.
Do not present any of these hypotheses as the established cause.

Unknown: the Desktop-side selection condition and a supported way to replace
the registered namespace for this existing chat. A restart, update or reconnect
has not been demonstrated to fix it. None was performed as an experiment.

The installed resume schema gives no direct namespace replacement field.
Editing rollout metadata/state databases would neither establish a supported
registration path nor provide the missing Desktop handler, so it was not done.

## Required continuation

Continue the same task from an agent turn with access to the Mac Desktop
registration path. Inspect the actual host capability/tool selection, repair
or refresh it through a verified supported mechanism, then prove delivery
edge → existing Mac chat and a reply back before marking coordination restored.
`MAC_HANDOFF.md` contains the already prepared scoped sample-transfer request.
Once the package arrives, execute the real-copy 108-unit Hermes tests and HTML
review described there. No new chat or alternate service was created.

## Incidental diagnostics

Native doctor reports healthy installation, configuration, auth, databases,
provider connectivity and managed daemon, plus three thread-index issues. Their
causal relationship to the missing Desktop tool is unknown; no index repair
was attempted. An assistant report-extraction script incorrectly assumed a
list-shaped `checks` value and failed; this was a verifier defect, not a
production failure. The successful native doctor evidence was retained.
