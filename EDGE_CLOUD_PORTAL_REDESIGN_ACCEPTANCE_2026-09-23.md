# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Apple Design System console conforming strictly to Apple Human Interface Guidelines (`apple-design`), Emil Kowalski's Design Engineering standards (`emil-design-eng`, `animate`), `taste-design`, and `impeccable`.

1. **Global Installation of Emil Kowalski Skills Repository**:
   - Cloned and installed `https://github.com/emilkowalski/skills` across all system skill directories:
     - `/home/core/.t3/userdata/providers/antigravity/.../config/skills/`
     - `/home/core/.gemini/antigravity-cli/skills/`
     - `/home/core/projects/cloud-infrastructure/.agents/skills/`
     - `/home/core/projects/cloud-infrastructure/.gemini/skills/`
   - Active skills: `apple-design`, `emil-design-eng`, `animate`, `animate-expo`, `animation-vocabulary`, `ask-sonner`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations`, `write-swift`.

2. **Authentic Apple Design System & Palette Overhaul**:
   - Replaced muddy slate backgrounds with authentic Apple system palettes:
     - **Light Theme**: Silky Apple iOS/macOS System Grouped Canvas (`#f2f2f7`), frosted glass cards (`rgba(255, 255, 255, 0.88)` with `backdrop-filter: blur(24px) saturate(180%)`), hairline border (`rgba(0, 0, 0, 0.08)`), and light-catching top edge highlight (`inset 0 1px 0 rgba(255, 255, 255, 0.95)`).
     - **Dark Theme**: True OLED Apple Black (`#000000`), macOS dark frosted glass (`rgba(28, 28, 30, 0.82)` with `backdrop-filter: blur(24px) saturate(180%)`), crisp white hairline rim lighting (`inset 0 1px 0 rgba(255, 255, 255, 0.12)`).
     - **Apple Semantic Accents**: San Francisco System Blue (`#0071e3`), Emerald Green (`#34c759`), Amber/Orange (`#ff9500`), Coral Red (`#ff3b30`), Purple (`#af52de`), and Indigo (`#5856d6`).

3. **Pixel-Perfect Alignment of Services & Workspaces Grid (Apple App Squircles)**:
   - Locked grid cards into rigid, pixel-perfect 3×3 geometry (`height: 104px; box-sizing: border-box;`).
   - Replaced basic flat boxes with authentic Apple App Squircles (48×48px, 12px continuous curve radius) with distinctive gradients:
     - Hermes Agent: Purple/Indigo gradient
     - T3 Code: Apple Blue gradient
     - n8n Automation: Orange gradient
     - Mattermost Chat: Cyan gradient
     - Nextcloud Drive: Sky Blue gradient
     - Stalwart Webmail: Mint Green gradient
     - Mail Admin: Slate/Graphite gradient
     - Maintenance Hub: Amber gradient
     - Backrest Vaults: Violet gradient
   - Titles, status pills, 1-line clamped descriptions, and external route links (`↗`) are strictly aligned across every column and row.

4. **Symmetrical Apple Control Center Widgets (Top Deck)**:
   - **Host Hardware Telemetry (Widget 1)**: Strict order **CPU -> RAM -> NVMe** with Apple capsule tracks (height 6px, rounded pill), utilization stats (`20% · 2 vCPU`, `19.2% · 12.6 GiB free`, `21.4% · 121.0 GiB free`), and detailed hardware breakdowns.
   - **Hybrid Fabric & AI Compute (Widget 2)**: Three Apple Inset rows for Private AI Cluster (`qwen3.8-27b-fp8` on Proxmox VE via NetBird, `Online · 41 ms`), Knowledge Vault Sync (`Synchronized`), and Edge Host Services (`14 Units · 10 Docker`).

5. **Apple Inset Grouped Lists (Bottom Twin Deck)**:
   - **Endpoint Probes**: macOS System Settings style Inset Grouped Table with green pips, service names, port tags, and Apple HTTP status badges (`HTTP 200`, `HTTP 401`).
   - **Subsystems & Mesh Fabric**: Grouped Inset List for Proxmox VE, AI Node, vLLM engine, and NetBird WireGuard, alongside compact systemd unit chips.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `a7dcc1449446e94669ea1734d5db2e2bd5e330a1916dfa6405a42fbe6fb1b8f3`
- `/var/www/app.escloud.us/app.css`: `6f2b158700a5528bd822938883d1e516c0a07865bb587e5805fc9654c42d4800`
- `/var/www/app.escloud.us/app.js`: `9394d9b50e12604c78f3b52f61b45872f132a54e71c459ab508655e632cf67ee`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`

## Verification Evidence

- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- `curl -k https://127.0.0.1/ -H "Host: app.escloud.us"`: HTTP 200
- `edge-monitor.service`: Active (running), `OVERALL: OK`
- Live Browser Preview snapshot: Captured in both Light and Dark modes.
