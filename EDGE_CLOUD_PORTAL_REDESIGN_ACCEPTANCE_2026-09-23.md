# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Precision Cloud Console conforming to `taste-design`, `frontend-design`, and `impeccable` guidelines.

1. **Anti-Slop Visual Ergonomics & Palette**:
   - Palette: Deep Modern Graphite (`#11141a` canvas, `#171b23` surface, `#1e232e` elevated, `#242b38` hover, `#272f3e` hairline borders) replacing oppressive pure-black void backgrounds.
   - Restrained human typography: sentence case everywhere, eliminating shouting uppercase (`ALL CAPS`). Natural font weights (`font-weight: 500` headings, `font-weight: 400` body and labels).
   - Strict 1.25x typographic scale steps: Body 14px, Section Headers 21px, Panels 16px, Telemetry metrics 17px with tabular monospace numbers (`font-variant-numeric: tabular-nums`).
   - High Contrast compliance: WCAG AA contrast ratio >= 4.5:1 across all body and muted text (verified via `impeccable detect`).

2. **Proportional Architecture & Mathematical Grid**:
   - 54px sticky navigation bar with breadcrumb (`ESCLOUD / Infrastructure`), node badge `edge.escloud.us`, centered status capsule (`All systems operational · HH:MM:SS`), live status tag, and subtle sync button (`[R]`).
   - Horizontal Unified Telemetry Strip: 5 mathematically balanced cells with crisp hairline vertical dividers (Health status with 4 domain pips, CPU load average `1m · 5m · 15m`, Memory with transform-based fill meter, Root storage with transform-based fill meter, and Node uptime).
   - 3×3 Symmetrical Service Matrix: 9 core operator services (Hermes, T3 Code, n8n, Mattermost, Nextcloud, Stalwart Webmail, Stalwart Admin, Maintenance Hub, Backrest) in uniform cards with 36px monochrome icon containers, subtle hover elevation, and latency chips.
   - Symmetrical 50/50 Bottom Operations Deck:
     - Left Panel: Clean tabular data view of Probed HTTP Endpoints with HTTP status tags (`HTTP 200`, `HTTP 401`), latency in ms, and state.
     - Right Panel: Subsystem Infrastructure cloud (14 systemd units, 10 Docker containers, Hybrid Mesh & Nodes rows, Resilience & Storage rows).

3. **Service Plane Updates**:
   - Complete replacement of retired CloudCLI (`127.0.0.1:18140`) with T3 Code (`code.escloud.us`, port 3773).
   - Real-time latency and health badges rendered dynamically on service cards.

4. **Frontend Telemetry Engine**:
   - In-place reactive DOM updates without layout destruction or scroll jump.
   - Polling engine querying `/api/status` every 5000ms.
   - Manual sync trigger with rotation feedback and global shortcut (`R`).
   - Hardware-accelerated CSS `transform: scaleX(...)` on telemetry meters to avoid browser reflow.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `ecc4a1e0bf292e91a783c845b8e6f6248da2b5921bfde4ced5740ae64c1c0bee`
- `/var/www/app.escloud.us/app.css`: `2d73b43ea840eb3c5eb16e595f9c7c8fc8ddbdaff8fe6bd07e9bf3236e066da1`
- `/var/www/app.escloud.us/app.js`: `9fc53bfb48cd0b503d8ce06e788ab18eb037953e347ea8391e1dc28c493a1fa9`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`
- `/etc/nginx/sites-available/app-escloud-us.conf`: `248512c5ae376f42ecb105df3db79423a3acf90c8213b5a0213a2173b63a2884`

## Verification Evidence

- `impeccable detect`: PASS (`[]` zero issues)
- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- Public asset caching and headers: PASS
- `edge-monitor.service`: Active (running), `OVERALL: OK` (all 4 domains OK)
- Live Browser Preview snapshot: Captured and verified at 1280×800.
