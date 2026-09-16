# Cloud Infrastructure — Inventory

## Inventory semantics

This file distinguishes:

- **LIVE-SUBSTRATE** — confirmed present on the rebuilt `edge` host;
- **LEGACY-AS-IS** — present in the 2026-09-14 `nl-core-vds` historical baseline;
- **TARGET-ACCEPTED** — explicitly accepted product/direction for a future stage, but not proof that it is deployed now;
- **TARGET-PLANNED** — accepted direction whose implementation is still pending;
- **UNDER-REVIEW** — existing or candidate component whose future role is unresolved and must be decided in the relevant implementation stage;
- **DO-NOT-CARRY-AS-IS** — legacy implementation not intended to be preserved unchanged.

This inventory is not a substitute for fresh runtime verification.

## Nodes

| Node | Role | State |
|---|---|---|
| `nl-core-vds` | Legacy external VPS identity | LEGACY-AS-IS historical only |
| `edge` / `edge.escloud.us` | Current Cloud Infrastructure VPS | LIVE-SUBSTRATE; Stage 1 IN PROGRESS |
| `ai-node` | PAI compute/data/knowledge node | Existing external dependency/context |
| PVE/Home Infrastructure | Home general-purpose infrastructure plane | Existing external dependency/context |

## Current live `edge` substrate

Confirmed accepted live substrate includes:

- Ubuntu 26.04.1 LTS;
- hostname `edge`, FQDN `edge.escloud.us`;
- provider IPv4/IPv6 networking;
- key-only SSH with `ssh.socket` activation;
- 4 GiB swap;
- QEMU guest agent;
- persistent journald-use ceiling `500M`;
- minimal architecture-independent bootstrap.

No target application/service stack is implied by this substrate inventory.

## Accepted application/product anchors

These products are accepted for future use unless a concrete incompatibility or changed requirement appears. Their presence here does **not** mean they are currently deployed on the rebuilt `edge`.

| Component | Legacy baseline presence | Future status | Notes |
|---|---:|---|---|
| Xray | yes | TARGET-ACCEPTED | DPI-bypass / foreign Internet access |
| Hysteria2 | yes | TARGET-ACCEPTED | complementary DPI-bypass transport |
| nginx | yes | TARGET-ACCEPTED | public web ingress/reverse-proxy anchor |
| n8n | yes | TARGET-ACCEPTED | always-on automation/webhook plane |
| CloudCLI | yes | TARGET-ACCEPTED | cloud AI workspace/interface |
| Stalwart | yes | TARGET-ACCEPTED | mail server |
| Bulwark | yes | TARGET-ACCEPTED | webmail frontend |
| Authelia | yes | TARGET-ACCEPTED | common web-authentication anchor |
| Codex CLI | yes | TARGET-ACCEPTED | subscription cloud-model tooling |
| Antigravity CLI | no at legacy baseline | TARGET-PLANNED | accepted additional cloud AI CLI |

Deployment/integration details are selected and accepted inside the relevant implementation stage.

## Backup / operations direction

| Component | Legacy baseline presence | Future status | Notes |
|---|---:|---|---|
| Restic | yes | TARGET-ACCEPTED as backend/tool | legacy same-host repository is not final DR design |
| Backrest | no | TARGET-PLANNED | accepted backup-management direction; stage-specific implementation pending |
| Homepage | yes | DO-NOT-CARRY-AS-IS | replace with dedicated Cloud Infrastructure page |
| Maintenance Center | yes | DO-NOT-CARRY-AS-IS | replace with maintenance page + Semaphore |
| Semaphore | not in legacy baseline | TARGET-PLANNED | accepted maintenance execution direction |

## File/storage/synchronization — Stage 4 unresolved

No final file/sync implementation is accepted yet merely from prior proposals.

| Component | Legacy baseline presence | Future status | Notes |
|---|---:|---|---|
| Filestash | yes | UNDER-REVIEW | compare against Stage 4 requirements |
| SFTPGo | no | UNDER-REVIEW candidate only | not accepted merely from withdrawn proposal |
| `/srv/cloud` | yes | UNDER-REVIEW legacy path | historical directory; not target path by assumption |
| Syncthing | yes | UNDER-REVIEW | evaluate role separately from task transport and Obsidian |
| Self-hosted LiveSync / CouchDB | no | UNDER-REVIEW candidate only | not accepted final Obsidian mechanism |
| Obsidian `edge` role | canonical vault is elsewhere | UNDER-REVIEW | canonical vault remains on `ai-node` |

## Private connectivity — Stage 6 unresolved

| Component | Future status | Notes |
|---|---|---|
| NetBird | UNDER-REVIEW candidate only | not accepted from withdrawn architecture proposal; test real path if considered |
| WireGuard/direct tunnel alternatives | UNDER-REVIEW | choose from actual Stage 6 flows |
| Authenticated HTTPS over Home public IP | UNDER-REVIEW | compare where simpler/adequate |

## Legacy components requiring stage-specific necessity review

| Component | Legacy baseline presence | Future status |
|---|---:|---|
| Codex App Server service | yes | UNDER-REVIEW in relevant cloud-AI/core stage |
| custom Codex runner | yes | UNDER-REVIEW; do not restore automatically |
| Cockpit | yes | UNDER-REVIEW |
| Fail2Ban | yes | UNDER-REVIEW for Stage 1/security requirements |
| monitoring nginx | yes | DO-NOT-CARRY-AS-IS / monitoring requirements redesigned later |
| monitoring/version/backup exporters | yes | DO-NOT-CARRY-AS-IS / requirements redesigned later |
| Docker socket proxy | yes | UNDER-REVIEW dependency-only |
| speedtest subsystem | yes | UNDER-REVIEW |

## Current stage boundary

Current canonical branch/stage:

`01 — Edge Clean Rebuild & Base Platform Deployment` / Stage 1 — **IN PROGRESS**.

Only the clean rebuild/substrate and minimal bootstrap subset is complete. Stage 1 requirements/service-selection, remaining Base Platform deployment and Stage 1 acceptance are still pending.

## Historical baseline facts

The detailed legacy inventory remains in:

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`

Use that document for exact historical versions, ports, hashes, paths, networks and deployment drift. Do not treat those historical values as current runtime after the rebuild.
