# AGENTS.md — Cloud Infrastructure

These are durable project-specific rules for any agent working in this repository.

## Required context before work

Read, in this order when relevant:

1. `OPERATING_RULES.md`
2. `DECISIONS.md`
3. `CURRENT_STATE.md`
4. `ARCHITECTURE.md`
5. `INVENTORY.md`
6. `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` when legacy/as-is VPS facts are needed.

## Stable project rules

- Treat `nl-core-vds` as the legacy/as-is host name and `edge` as the target logical node name.
- Never rewrite the historical baseline to use target-state naming.
- Cloud Infrastructure must complement Home Infrastructure and Personal Agents Infrastructure; do not duplicate home/PAI functionality merely because it can run on a VPS.
- During the current phase, settle the service/function composition first. Network, ingress, private-backbone and deployment topology come later.
- Do not re-open accepted product choices merely to compare alternatives unless a concrete incompatibility, regression or changed requirement appears.
- Do not infer that an installed legacy service belongs in the target state, and do not infer that an unused legacy service is unnecessary.
- Do not mutate runtime infrastructure while the project is in analysis/design-only mode.
- Preserve accepted decision chronology; do not convert hypotheses or rejected proposals into current state.

## Accepted core application choices

Unless a later decision supersedes them, do not search for replacements for:

- Xray
- Hysteria2
- n8n
- CloudCLI
- nginx
- Stalwart + Bulwark
- Authelia
- Codex CLI
- Antigravity CLI

Authelia is intended as the common web-authentication entry point under `escloud.us`. Native application authentication may be disabled only where that operating mode is explicitly supported and does not break application/API/session semantics.

## Knowledge/Obsidian invariant

The canonical Obsidian knowledge vault remains on `ai-node` at:

`/srv/ai-data/knowledge/obsidian`

Do not make `edge` a new canonical source of truth by assumption. The role of `edge` for Obsidian is still to be designed: possible roles include sync endpoint, peer/mirror, remote workspace or no direct vault hosting. The chosen method must avoid paid Obsidian Sync and must not combine multiple primary synchronization mechanisms for the same vault.

## Files and synchronization

Filestash and Syncthing are not yet accepted as target-state components. Evaluate them from concrete requirements, especially:

- VPS working storage accessible from MacBook, iPhone and `ai-node`;
- web browsing/editing of selected VPS files;
- cloud-agent workspaces;
- synchronization of working files/scripts and, separately, Obsidian needs.

Do not conflate task transport for cloud AI CLIs with general file synchronization.
