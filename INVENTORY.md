# Cloud Infrastructure — Inventory

## Inventory semantics

This file distinguishes:

- **LEGACY-AS-IS** — present in the 2026-09-14 `nl-core-vds` baseline;
- **TARGET-ACCEPTED** — accepted for future `edge` service composition;
- **TARGET-PLANNED** — accepted direction but not present in the legacy baseline;
- **UNDER-REVIEW** — existing or candidate component whose future role is unresolved;
- **DO-NOT-CARRY-AS-IS** — current implementation is not intended to be preserved unchanged.

This is not proof of current runtime health after 2026-09-14. Revalidate volatile facts before implementation.

## Nodes

| Node | Role | State |
|---|---|---|
| `nl-core-vds` | Legacy external VPS | LEGACY-AS-IS historical identity |
| `edge` | Future primary Cloud Infrastructure VPS node | TARGET-ACCEPTED logical name |
| `ai-node` | PAI compute/data/knowledge node | Existing external dependency/context |
| PVE/Home Infrastructure | Home general-purpose infrastructure plane | Existing external dependency/context |

## Accepted application core

| Component | Baseline presence | Future status | Notes |
|---|---:|---|---|
| Xray | yes | TARGET-ACCEPTED | DPI-bypass / foreign Internet access function |
| Hysteria2 | yes | TARGET-ACCEPTED | complementary DPI-bypass transport |
| nginx | yes | TARGET-ACCEPTED | public web ingress/reverse proxy role |
| n8n | yes | TARGET-ACCEPTED | 24/7 automation/webhook/integration plane |
| CloudCLI | yes | TARGET-ACCEPTED | cloud AI workspace/interface |
| Stalwart | yes | TARGET-ACCEPTED | mail server |
| Bulwark | yes | TARGET-ACCEPTED | webmail/groupware frontend |
| Authelia | yes | TARGET-ACCEPTED | common web authentication under `escloud.us` |
| Codex CLI | yes | TARGET-ACCEPTED | subscription-based cloud model tooling |
| Antigravity CLI | no at baseline | TARGET-PLANNED | accepted second core subscription-based cloud AI CLI |

## Backup / operations direction

| Component | Baseline presence | Future status | Notes |
|---|---:|---|---|
| Restic | yes | TARGET-ACCEPTED as backend/tool | current same-host repository is not final DR design |
| Backrest | no | TARGET-PLANNED | clean deployment on future `edge` |
| Homepage | yes | DO-NOT-CARRY-AS-IS | replace with dedicated Cloud Infrastructure page |
| Maintenance Center | yes | DO-NOT-CARRY-AS-IS | replace with maintenance page + Semaphore |
| Semaphore | not in VPS baseline | TARGET-PLANNED | accepted maintenance execution model analogous to Home/PVE |

## File/storage/synchronization

| Component | Baseline presence | Future status | Notes |
|---|---:|---|---|
| Filestash | yes | UNDER-REVIEW | compare against requirements for web file access plus network-style access from MacBook/iPhone/`ai-node` |
| `/srv/cloud` | yes | UNDER-REVIEW | legacy directory; emptiness is not a removal criterion |
| Syncthing | yes | UNDER-REVIEW | evaluate working-file/script sync separately from AI task transport and Obsidian sync |
| Obsidian edge role | legacy data subtree existed, canonical now elsewhere | UNDER-REVIEW | canonical vault is on `ai-node`; edge role not selected |

## Legacy components requiring separate necessity review

| Component | Baseline presence | Future status |
|---|---:|---|
| Codex App Server service | yes | UNDER-REVIEW |
| custom Codex runner | yes | UNDER-REVIEW |
| Cockpit | yes | UNDER-REVIEW |
| Fail2Ban | yes | UNDER-REVIEW |
| monitoring nginx | yes | DO-NOT-CARRY-AS-IS / requirements to be redesigned |
| monitoring/version/backup exporters | yes | DO-NOT-CARRY-AS-IS / requirements to be redesigned |
| Docker socket proxy | yes | UNDER-REVIEW dependency-only |
| speedtest subsystem | yes | UNDER-REVIEW |

## Historical baseline facts that must not be normalized away

The detailed legacy inventory remains in:

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`

Use that document for exact historical versions, ports, hashes, paths, networks and deployment drift.
