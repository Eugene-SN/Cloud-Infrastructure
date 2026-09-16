# Source classification

## SAFE VERBATIM
- `vpn/maintctl.sh`
- `vpn/vpnctl.sh`
- VPN systemd units and certificate sync script
- nginx base / real-IP / ACME reference
- mail Compose and Stalwart storage descriptor
- mail nginx routing
- Stalwart Fail2Ban filters
- Authelia structural configuration
- CloudCLI/Codex systemd units
- selected SSH/runtime metadata

## REDACTED
- `vpn/xray.config.redacted.json`: VLESS UUIDs removed
- `vpn/hysteria.config.redacted.yaml`: Hysteria passwords removed
- `auth/users_database.redacted.yml`: Argon2 password hash removed
- `ai/codex-config.redacted.toml`: CloudCLI browser MCP token removed

## REFERENCE ONLY
- legacy core-stack Compose
- legacy Codex runner/API
- legacy mail Fail2Ban jail
- legacy nginx VPN/application route map
- provider cloud-init netplan snapshot
- runtime listener/firewall/container metadata

## DROPPED FROM GITHUB REFERENCE
- private keys and certificate private material
- VPN UUID/password state files and user CSVs
- Stalwart RocksDB/mail data
- Bulwark session secret and telemetry
- n8n SQLite/runtime state
- Authelia secret files/database
- CloudCLI auth database
- Codex `auth.json`, sessions, caches and SQLite state
- SSH key material
- package-default Fail2Ban catalog
- stock nginx helper/package-default files
