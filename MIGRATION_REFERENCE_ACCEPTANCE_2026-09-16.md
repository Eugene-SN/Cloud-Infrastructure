# Cloud Infrastructure — Migration Reference Acceptance — 2026-09-16

**Status:** ACCEPTED

## Purpose

This document records acceptance of the GitHub engineering-context plane created from the audited legacy VPS review bundle.

## Accepted repository tree

Canonical engineering reference path:

`migration-reference/`

The tree is historical/reference material for target design and clean-rebuild migration. It is not an authoritative restore bundle and must not be applied blindly to future `edge`.

## Verification performed

- The uploaded review archive SHA256 matched the server-generated value: `f373627dbed4d4dc70d414ff9ff7fa68bd4bc18d20bfa7d223a7c4d1de933d92`.
- The review archive was extracted and normalized outside the repository.
- Package-default and low-value files were removed.
- The resulting GitHub reference contains 37 files including `SHA256SUMS.txt`.
- `vpn/maintctl.sh` and `vpn/vpnctl.sh` were preserved verbatim.
- Xray VLESS UUIDs were replaced with `<REDACTED_VLESS_UUID_*>` markers.
- Hysteria2 passwords were replaced with `<REDACTED_HY2_PASSWORD>` markers.
- Authelia Argon2 password hash was replaced with `<REDACTED_ARGON2_PASSWORD_HASH>`.
- Codex CloudCLI browser MCP token was replaced with `<REDACTED_MCP_TOKEN>`.
- Dedicated credential state, private keys, authentication databases, Stalwart RocksDB, n8n SQLite state, Authelia secrets/database, CloudCLI auth DB, Codex auth/session/database state and SSH key material were excluded.
- Known source secret values used during normalization were not found by exact repository search after upload.
- GitHub read-back confirmed the redacted Xray, Hysteria2, Authelia and Codex files and the verbatim VPN management scripts.

## Classification

`migration-reference/CLASSIFICATION.md` is the canonical per-class handling summary:

- SAFE VERBATIM
- REDACTED
- REFERENCE ONLY
- DROPPED FROM GITHUB REFERENCE

## Operational meaning

The project now has two accepted preservation planes:

1. **Recovery plane:** external credential-bearing migration archive plus provider-level VPS backup.
2. **Engineering-context plane:** directly readable `migration-reference/` in the private Cloud Infrastructure repository.

During future deployment, use `migration-reference/` to understand/adapt legacy implementation logic and use the external recovery archive only when exact preserved credential/state material is required.

Do not convert reference-only files into target-state configuration without a current design decision and verification against the fresh runtime.
