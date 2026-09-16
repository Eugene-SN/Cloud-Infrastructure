# Cloud Infrastructure — Current State

## Snapshot status

**Project stage:** service/function discovery and target-composition analysis.

**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

**Runtime mutation status:** none performed by this project initialization.

## Legacy VPS baseline

The canonical as-is source for the existing VPS is:

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`

Baseline SHA256 of the source imported for project initialization:

`5bb56c10723c2f6e950d9d4a28bbd76989870da6e01d221429417cf806139368`

The baseline records the legacy host as `nl-core-vds`. That name and all legacy names in the baseline remain historical facts and must not be retroactively normalized to `edge`.

The baseline is not the desired-state architecture.

## Legacy host summary from the 2026-09-14 baseline

- Host: `nl-core-vds`
- Ubuntu 26.04.1 LTS at baseline
- KVM VPS
- 2 vCPU
- ~16 GiB RAM
- ~155 GiB root storage
- public IPv4 `45.92.156.17`
- IPv6 present
- TCP/443: Xray
- UDP/443: Hysteria2
- nginx behind Xray fallback
- Docker Compose projects: `core-stack`, `mail-stack`
- NetBird absent from the VPS at baseline
- Restic repository located on the same VPS/root filesystem
- Git deployment state did not exactly reproduce production
- known mail Fail2Ban stale-log-path defect
- old browser stack removed

For complete facts, use the baseline file rather than this summary.

## Accepted target-service direction

Accepted without further alternative search unless a concrete incompatibility emerges:

- Xray
- Hysteria2
- nginx
- n8n
- CloudCLI
- Stalwart
- Bulwark
- Authelia
- Codex CLI
- Antigravity CLI

Notes:

- Xray/Hysteria2 serve the user-facing foreign-VPS/DPI-bypass use case and are not the architectural wrapper around all `edge` services.
- Authelia is the intended common web-authentication entry point under `escloud.us`; native per-app auth may be disabled only where explicitly supported and operationally correct.
- Codex CLI + Antigravity CLI are the accepted core for subscription-based cloud model usage.

## Accepted replacement directions

- Future backup operations: clean Backrest deployment using Restic rather than carrying forward the current local-only Restic arrangement as the final design.
- Homepage: replace with a dedicated Cloud Infrastructure page analogous in purpose to `home.lan`, including monitoring/status and useful integrations.
- Legacy custom Maintenance Center: replace with a maintenance page + Semaphore model analogous to the accepted Home/PVE approach.

## Open service decisions

Still under analysis:

- Filestash or alternative file/storage access layer.
- Syncthing or alternative synchronization model.
- Role of `edge` in Obsidian access/synchronization.
- Codex App Server as a persistent service.
- custom Codex runner.
- Cockpit.
- Fail2Ban scope.
- legacy monitoring nginx/exporters.
- Docker socket proxy.
- dedicated speedtest subsystem.
- any additional new Cloud Infrastructure services not yet selected.

## Obsidian / knowledge state

Canonical Obsidian vault remains on `ai-node`:

`/srv/ai-data/knowledge/obsidian`

`edge` is not currently a canonical knowledge source. Its possible role as sync endpoint, peer/mirror, remote workspace or gateway remains under analysis.

Requirement: find a robust free/self-hosted synchronization approach for MacBook, iPhone/iPad and `ai-node` without paid Obsidian Sync.

## Architecture state

No final decisions have yet been made for:

- private backbone;
- service-to-service topology;
- final domains/ingress layout;
- runtime/container topology;
- final storage layout;
- final monitoring stack;
- off-site DR destination/topology;
- in-place migration versus clean Ubuntu reinstall.

A clean reinstall of the VPS remains an allowed future outcome after the final service composition and Architecture Contract are agreed.
