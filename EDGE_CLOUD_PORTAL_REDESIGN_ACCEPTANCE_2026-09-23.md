# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Daylight & Precision Cloud Console conforming to `taste-design`, `frontend-design`, and `impeccable` guidelines.

1. **Light / Daylight Theme & Eye Comfort**:
   - Palette: Clean Modern Daylight Console (`#f8fafc` canvas, `#ffffff` surfaces, `#e2e8f0` crisp hairline borders, deep slate `#0f172a` text, `#64748b` muted slate with WCAG AA >= 4.5:1 contrast).
   - Built-in instantaneous theme toggle (`Daylight` / `Dark`) persisted via `localStorage` and keyboard shortcut (`T`).
   - Clean, luminous layout eliminating the gloomy dark cave feeling while preserving professional contrast and clarity.

2. **Accurate Operational Semantics (Elimination of Localhost Ping)**:
   - Meaningless localhost ping latencies removed from local edge services.
   - Replaced by real operational states:
     - Hermes Agent: `Online` (Gateway & Web UI active)
     - T3 Code: `Ready` (Port 3773 responsive)
     - n8n: `Active` (HTTP 200)
     - Mattermost: `Online` (PostgreSQL healthy)
     - Nextcloud: `Healthy` (Storage & Redis active)
     - Stalwart Webmail: `Active` (JMAP/IMAP active)
     - Mail Admin: `Directory ready`
     - Maintenance Hub: Dynamic updates counter (`1 update` or `Up to date`)
     - Backrest Vaults: Dynamic plans state (`2 vaults synced`)
   - Real network ping is displayed strictly where it belongs: remote NetBird WireGuard mesh fabric nodes (`Proxmox VE Node: 42 ms`, `AI Node Host: 42 ms`).

3. **Compact & Functional Cadence Monitoring**:
   - Eliminated the oversized, useless 5-card server metric ribbon.
   - Introduced a slim, non-intrusive Overview Bar:
     - 4 Health Domains (`Edge host`, `PAI mesh`, `Syncthing`, `Backrest & Ops`) with live status pips.
     - Compact Host Resources (`CPU`, `RAM`, `NVMe free`).
     - Cadence Engine integration: dynamically syncs with backend `intervals_s.fast: 5s`, showing snapshot sequence, timestamp, and a live second-by-second age ticker (`Live · 2s ago`).

4. **Concise, High-Information Content**:
   - Stripped redundant marketing descriptions and essay labels.
   - Clean 3×3 service matrix with clear 1-line functional scopes.
   - Symmetrical 50/50 bottom deck: Probed Ingress Endpoints on the left, Remote Mesh Nodes & Subsystems on the right.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `89fe97e6489406513be1a391a540317c6ff7a52be4d3e4a7a56ab29c828000ab`
- `/var/www/app.escloud.us/app.css`: `c04e98ad59e63b3ad819ff44e5f436ebcb2fedfe6d771813b91abf39e99c83b8`
- `/var/www/app.escloud.us/app.js`: `256e8750d2e6c31ae6f2cae447cd26746f304ffbc31cbad0de0e16bd47b0a2b9`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`
- `/etc/nginx/sites-available/app-escloud-us.conf`: `248512c5ae376f42ecb105df3db79423a3acf90c8213b5a0213a2173b63a2884`

## Verification Evidence

- `impeccable detect`: PASS (`[]` zero issues)
- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- Public asset caching and headers: PASS
- `edge-monitor.service`: Active (running), `OVERALL: OK` (all 4 domains OK)
- Live Browser Preview snapshot: Captured and verified at 1280×800 in Daylight mode.
