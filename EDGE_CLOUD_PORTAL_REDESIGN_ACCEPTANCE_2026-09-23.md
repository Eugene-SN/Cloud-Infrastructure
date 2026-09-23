# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Smoky Minimalist Frosted Glass console adhering to contemporary design trends, `apple-design`, Emil Kowalski's Design Engineering standards (`emil-design-eng`, `animate`), `taste-design`, and `impeccable`.

1. **Clean Header & Live Timer Removal ("убрать таймер Live ...s ago")**:
   - Completely removed redundant `Live ...s ago` heartbeat capsule from header right.
   - Header now cleanly hosts the minimalist monospace date and real-time clock, theme toggle button, and manual refresh control.

2. **Refined 3×3 Grid Flow & Information Architecture**:
   - **Row 1 (AI & Development)**: Hermes Agent → T3 Code → n8n Automation.
   - **Row 2 (Communication Suite)**: Mattermost Chat → Stalwart Webmail (center) → Stalwart Mail Admin (right).
   - **Row 3 (Storage & System Ops)**: Nextcloud Drive (bottom row, left) → Maintenance Hub (center) → Backrest Vaults (right).

3. **+20% Enlarged Brand Logos & Frosted Squircles**:
   - Scaled official vector brand icons from `22px` to `26.5px` (+20%).
   - Adjusted frosted squircle container to `46×46px` with continuous `13px` corner curvature, preserving balanced Apple-style margins and tactile hover feedback.

4. **Enhanced Glassmorphism & High-Transparency Frosted Mist**:
   - Elevated all frosted glass components (`.console-header`, `.apple-card`, `.app-tile`) to `blur(36px) saturate(160%)` and `-webkit-backdrop-filter: blur(36px) saturate(160%)`.
   - Card backgrounds set to `rgba(255, 255, 255, 0.42)` in light theme and `rgba(32, 38, 50, 0.46)` in dark theme, with `.app-tile` surfaces dialed to `0.30`–`0.36` alpha.
   - Enhanced multi-stop radial smoky ambient background layer refracting through transparent glass surfaces.

5. **Calibrated Palette Shifts ("светлая тема немного темнее, темная немного светлее")**:
   - **Light Theme**: Shifted from bright chalk/pale white to a deep, sophisticated cool fog mist (`#d5dce6`).
   - **Dark Theme**: Shifted from pitch-black obsidian to a softer titanium charcoal (`#191c23`) with graphite translucent glass.

6. **Full-Width Horizontal Telemetry & Fabric Strips**:
   - **Edge Node Telemetry**: AMD EPYC 2 vCPU tag and strict order **CPU Load → Memory → NVMe Storage** with clean vertical hairline dividers.
   - **Hybrid Fabric & AI Compute**: Private AI Cluster, Knowledge Vault Sync, and Edge Host Services.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `1de1db210614ab6fc1547caef0ad7e7c1689b8478ed8d7b6f1142b173af5c8ce`
- `/var/www/app.escloud.us/app.css`: `3a9ee2e6c424f7608ba1c71b0e28ae82ef384a2a6a71dae6b890bdf44f46fac5`
- `/var/www/app.escloud.us/app.js`: `9394d9b50e12604c78f3b52f61b45872f132a54e71c459ab508655e632cf67ee`
- `/var/www/app.escloud.us/icons/hermes.svg`: `951b45c5ce168af1bedd2bed0a543de74f4e42acf03522e1e52db56d040f319e`
- `/var/www/app.escloud.us/icons/vscode.svg`: `98d2dc1ad1d82b3684880e174a09a5c35737977dfdbe97dbe040ef2d55e10e75`
- `/var/www/app.escloud.us/icons/n8n.svg`: `45b282108f60b12df6cba68e3fa633d56970eab4d2ac6b1eef43a60b5ea29af5`
- `/var/www/app.escloud.us/icons/mattermost.svg`: `44c729c1821ae15dac700c89af6dabcb8ccac91a5048a15f96d940c81b862548`
- `/var/www/app.escloud.us/icons/nextcloud.svg`: `892404c0c7c74cb22d6c728e967fcf5cb680f7d343db1cdfef92186d44cce6d3`
- `/var/www/app.escloud.us/icons/stalwart.svg`: `6cd0bac38e04a282482413d2a63276104b3208926eb58c2cb715d2622eaca3ea`
- `/var/www/app.escloud.us/icons/semaphore.svg`: `37841b729da7444230308279cf7ae3133e0ddbcaa8f34a2ebe5e1c9fcb894a2b`
- `/var/www/app.escloud.us/icons/backrest.png`: `7d3d305aec33820e1be88dfcdfad8e478db483304281e7b2b013513f108f1220`

## Verification Evidence

- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- `curl -k https://127.0.0.1/ -H "Host: app.escloud.us"`: HTTP 200
- `edge-monitor.service`: Active (running), `OVERALL: OK`
- Live Browser Preview snapshots: Verified with reordered grid, enlarged brand logos, and removed timer.
