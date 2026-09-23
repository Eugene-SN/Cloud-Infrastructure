# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck).

1. **Service Plane Updates**:
   - Complete replacement of retired CloudCLI (`127.0.0.1:18140`) with T3 Code (`code.escloud.us`, port 3773).
   - Direct integration of Stage 12 Nextcloud (`cloud.escloud.us`) and Stage 13 Backrest UI (`backup.escloud.us`).
   - Dedicated vector SVG monochrome icons for all 9 operator services.
   - Real-time latency and health badges rendered dynamically on service cards.

2. **Frontend Engine & Performance**:
   - In-place DOM reconciliation without layout destruction or scroll jump.
   - Visibility-aware polling via Page Visibility API (`document.hidden` pause/resume).
   - Manual refresh button with rotation animation and global shortcut (`R`).
   - Hardware-accelerated transitions via CSS `transform: scaleX(...)` on telemetry meters.
   - Progressive disclosure accordion for all 14 supervised systemd units and 10 Docker containers.
   - Tabular monospace numbers (`tabular-nums`) across all metrics, timestamps, and latencies.

3. **PWA & Ingress Assets**:
   - Dedicated SVG favicon (`/favicon.svg`) and compatibility `/favicon.ico`.
   - Web App Manifest (`/manifest.webmanifest`) configured for standalone operator launch.
   - Nginx caching rule for public assets (`favicon.*`, `manifest.webmanifest`, `robots.txt`) with `Cache-Control: public, max-age=86400` and CORS headers.

4. **Design Quality & Compliance**:
   - Verified via `impeccable detect`: 0 anti-patterns, 0 contrast warnings, 0 layout shifts, zero slop.
   - Conforms strictly to `DESIGN.md` (*The Sovereign Control Deck*).

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `c94bf659f429d24060098e3d09594df0d10e6f303d295fe2af856536d50bb894`
- `/var/www/app.escloud.us/app.css`: `563f111dedabb3b70573ea37db30c8a29d3e19df85ef74df0a4958b15e8b3eea`
- `/var/www/app.escloud.us/app.js`: `7e8f981b1f6acd45418db1ef4ec161f4b90c139d547f019e4854c162bd5d002b`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`
- `/etc/nginx/sites-available/app-escloud-us.conf`: `248512c5ae376f42ecb105df3db79423a3acf90c8213b5a0213a2173b63a2884`

## Verification Evidence

- `impeccable detect`: PASS (`[]` zero issues)
- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- Public asset caching and headers: PASS
- `edge-monitor.service`: Active (running), `OVERALL: OK` (all 4 domains OK)
