# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Precision Cloud Console.

1. **Service Plane Updates**:
   - Complete replacement of retired CloudCLI (`127.0.0.1:18140`) with T3 Code (`code.escloud.us`, port 3773).
   - Direct integration of Stage 12 Nextcloud (`cloud.escloud.us`) and Stage 13 Backrest UI (`backup.escloud.us`).
   - Dedicated vector SVG monochrome icons with distinct soft-tone background chips for all 9 operator services.
   - Real-time latency and health badges rendered dynamically on service cards.

2. **2026 Precision Layout & KPI Ribbon**:
   - 64px sticky navigation header with brand symbol, node badge `edge.escloud.us`, live status indicator, timecode, and keyboard-driven refresh button (`[R]`).
   - 5-card KPI Telemetry Ribbon: Global Health (with 4 domain pips), CPU load average (`1m, 5m, 15m`), Memory allocation with CSS meter bar, NVMe storage utilization with CSS meter bar, and continuous node uptime.
   - Asymmetric two-column operational layout (60% Primary Workplane / 40% Side Telemetry Deck).
   - Real-time Application Endpoints table displaying HTTP response codes (`HTTP 200`, `HTTP 401`), latency in ms, and status.
   - Subsystem Runtime chips showing all 14 systemd services and 10 Docker containers with status pips.
   - Hybrid Fabric and Home PAI section with live mesh latency to Proxmox VE, AI Node host, vLLM engine, and NetBird mesh.
   - Operations and Resilience section showing Backrest snapshot vaults, Syncthing knowledge sync, and OS upgrade status.

3. **Frontend Engine & Performance**:
   - In-place reactive DOM updates without layout destruction or scroll jump.
   - Polling engine querying `/api/status` every 5000ms.
   - Manual refresh button with rotation animation and global shortcut (`R`).
   - Hardware-accelerated transitions via CSS `transform: scaleX(...)` on telemetry meters to avoid browser reflow.
   - Tabular monospace numbers (`tabular-nums`) across all metrics, timestamps, and latencies.

4. **Design Quality & Compliance**:
   - Verified via `impeccable detect`: 0 anti-patterns, 0 contrast warnings, 0 layout shifts, zero slop.
   - Conforms strictly to `DESIGN.md` (*2026 Edition: Obsidian & Precision Cloud Console*).
   - High contrast compliance (WCAG AA >= 4.5:1 for all text).

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `84e4013d84618443ae4d72725f4ac52d7420274a70da9a0020b151ec5799c757`
- `/var/www/app.escloud.us/app.css`: `b2878f6ecc8ae3c0f60767d369d44783c444cd47f9172f908af6bf968565c28f`
- `/var/www/app.escloud.us/app.js`: `900de78af458b495e3fb18983b1651db2592b1b4d4c2776015a9f7ca336d0ad4`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`
- `/etc/nginx/sites-available/app-escloud-us.conf`: `248512c5ae376f42ecb105df3db79423a3acf90c8213b5a0213a2173b63a2884`

## Verification Evidence

- `impeccable detect`: PASS (`[]` zero issues)
- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- Public asset caching and headers: PASS
- `edge-monitor.service`: Active (running), `OVERALL: OK` (all 4 domains OK)
