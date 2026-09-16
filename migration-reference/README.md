# Migration Reference — legacy `nl-core-vds`

Status: historical engineering reference for Cloud Infrastructure target design and clean-rebuild migration.

This tree is **not** a restore bundle and is **not** authoritative runtime configuration for future `edge`. It preserves expensive-to-reconstruct implementation logic from the legacy VPS so it can be selectively adapted during a clean deployment.

## Security boundary

The authoritative credential-bearing recovery archive remains outside GitHub. This reference intentionally excludes private keys, application databases, authentication databases, OAuth/session credentials, SSH keys, Authelia secret files, Codex `auth.json`, CloudCLI `auth.db`, Stalwart RocksDB and n8n SQLite state.

Where a source text file contained a credential value needed to understand structure, only the value was replaced with an explicit `<REDACTED_...>` marker.

## Important migration notes

- `vpn/maintctl.sh` and `vpn/vpnctl.sh` are preserved verbatim and contain implementation logic but no hard-coded current VPN user credentials.
- The scripts still depend on legacy `/opt/vpn-stack` paths/state. Adapt them only after the new Xray/Hysteria layout is accepted.
- The legacy Fail2Ban mail jail is reference-only. Its Docker wildcard log path was already proven stale against the current Stalwart container.
- `automation/core-stack-compose.reference.yml` includes rejected/unresolved legacy services and is not the target Compose file.
- `ai/codex-runner-*` is the legacy execution bridge, retained only for analysis.
- `ingress/vpn-stub.reference.conf` contains the old AI Workspace route map and is not the future ingress contract.
- `host/netplan-50-cloud-init.reference.yaml` records the old provider network state. Never restore it blindly after reinstall.
