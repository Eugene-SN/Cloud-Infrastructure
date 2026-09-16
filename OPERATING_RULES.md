# Cloud Infrastructure — Operating Rules

## Project identity

- **Project name:** Cloud Infrastructure
- **Primary repository:** `Eugene-SN/Cloud-Infrastructure`
- **GitHub workflow:** ON
- **Primary VPS node:** `edge`
- **Current FQDN:** `edge.escloud.us`
- `edge` is a logical, location-agnostic node name. Do not encode provider/datacenter/country into target-state naming.

## Project scope

Cloud Infrastructure is the public/cloud-facing layer of one personal infrastructure composed of:

- **Home Infrastructure** — general-purpose home compute/service plane centered on Proxmox VE and home-network services;
- **Personal Agents Infrastructure (PAI)** — local AI/agent/data-processing plane centered on `ai-node`;
- **Cloud Infrastructure** — external 24/7 VPS layer for public routability, foreign location, Internet-facing services, cloud AI integrations, external coordination and off-site roles.

Cloud Infrastructure should complement Home Infrastructure and PAI rather than duplicate them without a concrete requirement.

## Historical baseline invariant

`NL_CORE_VDS_Current_State_Baseline_2026-09-14.md` remains the canonical historical/as-is snapshot of the pre-reinstall legacy VPS.

- Keep historical names such as `nl-core-vds` and legacy paths unchanged in that artifact.
- Do not reinterpret it as current runtime state after the 2026-09-16 rebuild.
- Do not treat the historical deployment as the target architecture.

## Current work stage

Stage 0 preservation is complete and the provider-level clean Ubuntu rebuild has been accepted.

Current state:

1. Recovery archive + provider backup: accepted.
2. GitHub `migration-reference/`: accepted engineering context.
3. Clean Ubuntu substrate for `edge`: accepted (`EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS`).
4. Target-service composition and architecture decisions remain in progress.
5. Target-service deployment has not started.

The clean substrate reset is now historical/current state, not an open migration option.

## Runtime mutation gate

The earlier absolute prohibition on runtime mutation before a complete Architecture Contract is superseded only as follows:

- the clean substrate rebuild and the minimum work required to validate/bootstrap that substrate are accepted;
- further host-level base bootstrap may be performed only when explicitly scoped, verified and not dependent on unresolved target-service architecture;
- restoration/deployment of target services, ingress topology, private backbone, application storage layout and other architecture-dependent components remains gated by later accepted decisions.

Do not infer authorization to restore legacy services merely because their products are already accepted for the future composition.

## Current substrate contract

Accepted live substrate facts include:

- Ubuntu 26.04.1 LTS, `x86_64`, KVM;
- hostname/FQDN `edge.escloud.us`, short hostname `edge`;
- kernel `7.0.0-31-generic` at substrate acceptance;
- 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- root filesystem ~155 GiB class;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64`, gateway `2a0c:b847:ffff::1`;
- SSH public-key access works; root password authentication is disabled;
- OpenSSH is socket-activated through `ssh.socket`;
- post-reboot system state `running`, failed units 0, current-boot error journal empty.

The provider-generated netplan/cloud-init material is working runtime state. Do not replace it byte-for-byte with historical `migration-reference/` networking configuration. Fresh runtime/configuration has priority over historical reference.

## Recovery model

Two independent recovery planes remain valid:

1. **Whole-VPS rollback:** confirmed provider-level backup.
2. **Selective recovery/migration:** external sensitive archive with SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`.

`migration-reference/` is engineering context only and must not be used as an authoritative restore bundle.

## Source-of-truth and persistence rules

For project intent, use the latest applicable `ACCEPTED` decisions. For factual runtime state, priority is:

1. fresh runtime audit;
2. actual live configuration;
3. current repository state;
4. historical docs/reference.

A discrepancy between these is drift and must be resolved explicitly rather than guessed.

Before modifying project files:

1. read current repository state;
2. avoid duplicate documents/facts;
3. update the canonical existing document for that topic;
4. read back critical writes.

Store structured state and decisions, not chat transcripts.

## Decision semantics

Decision statuses:

- `PROPOSED`
- `ACCEPTED`
- `SUPERSEDED`
- `REJECTED`
- `DEPRECATED`

Latest applicable `ACCEPTED` decision has priority. `SUPERSEDED`, `REJECTED`, and `DEPRECATED` entries are historical only.

## Git and secrets

- Do not commit credentials or secrets to GitHub.
- Persistent non-secret configuration/design/runbooks may be stored in Git.
- Sensitive recovery state remains outside GitHub.

## Project-specific design constraints

- Single-operator personal infrastructure; avoid enterprise complexity without a demonstrated use case.
- Prefer simple upstream-supported mechanisms and minimum custom code.
- VPN/proxy services used for DPI bypass are a separate function from any future private infrastructure backbone.
- Any private backbone must be tested on the real Russia ↔ external-VPS path before acceptance; do not assume WireGuard-based connectivity will be reliable under DPI.
- Do not carry legacy service configuration forward blindly; use `migration-reference/` to understand prior logic and the external archive only where exact state/credentials are actually required.
