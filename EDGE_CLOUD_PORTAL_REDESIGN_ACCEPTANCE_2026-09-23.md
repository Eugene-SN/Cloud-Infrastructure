# Edge Cloud Portal Modernization & Sovereign Control Deck Acceptance — 2026-09-23

## Status

**COMPLETE / ACCEPTED**

Final acceptance marker:

`EDGE_CLOUD_PORTAL_REDESIGN_ACCEPTANCE=PASS`

## Scope

Comprehensive UX, technical, and visual modernization of `https://app.escloud.us` (The Sovereign Control Deck) into a 2026 Smoky Minimalist Frosted Glass console adhering to contemporary design trends, `apple-design`, Emil Kowalski's Design Engineering standards (`emil-design-eng`, `animate`), `taste-design`, and `impeccable`.

1. **Smoky Minimalist Glass Aesthetics ("дымка, минимализм и стекло")**:
   - Replaced saturated bright backgrounds with a smoky frosted mist atmosphere (`.smoky-ambient` radial misty vapor layer).
   - **Light Theme**: Subdued cool fog canvas (`#e8ecf1`) with frosted misty glass surfaces (`rgba(255, 255, 255, 0.68)` + `backdrop-filter: blur(28px) saturate(130%)`), muted micro-borders (`rgba(0, 0, 0, 0.06)`), and diffused shadows.
   - **Dark Theme**: Deep smoky obsidian mist canvas (`#0c0e12`) with frosted dark glass (`rgba(18, 21, 26, 0.68)`) and delicate hairline lighting.
   - **Muted Frosted Squircles**: Replaced loud saturated rainbow gradient icons with quiet, sophisticated translucent smoked-glass squircle containers (`var(--apple-squircle-bg)` + `var(--apple-squircle-border)`) with subtle tone-on-tone icons.

2. **Full-Width Horizontal Telemetry Strip (Top Row)**:
   - **Edge Node Telemetry** is now rendered as a sleek horizontal glass strip directly below the header.
   - Displays AMD EPYC 2 vCPU tag on the left, and 3 horizontal metric columns in strict order **CPU Load → Memory → NVMe Storage** with clean vertical hairline dividers, exact utilization percentages, 5px capsule progress tracks, and detailed resource stats (`Load avg`, `GiB used of total`).

3. **Full-Width Horizontal Hybrid Fabric Strip (Row 2)**:
   - **Hybrid Fabric & AI Compute** is positioned as a matching sleek horizontal glass strip directly underneath Edge Node Telemetry.
   - 3 horizontal columns with hairline dividers:
     - **Private AI Cluster**: `Online · 41 ms` status pill, vLLM `qwen3.8-27b-fp8` on Proxmox VE.
     - **Knowledge Vault Sync**: `Synchronized` status pill, Syncthing continuous replication Obsidian vault.
     - **Edge Host Services**: `14 Units · 10 Docker` status pill, systemd & container runtime nominal.

4. **Services & Workspaces Grid (3×3 Squircles)**:
   - Rigid 3×3 grid with uniform 94px card heights, baseline-pinned route links (`↗`), 1-line text clamping, and subtle scale-down tactile feedback (`:active { transform: scale(0.985); }`).

5. **Dual Deck Inset Panels (Bottom Row)**:
   - **Endpoint Probes**: macOS System Settings style Inset Grouped Table with green pips, service names, port tags, and clean HTTP badges (`HTTP 200`, `HTTP 401`).
   - **Subsystems & Mesh Fabric**: Grouped Inset List for Proxmox VE, AI Node, vLLM engine, and NetBird WireGuard, alongside compact systemd unit chips.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `f70a1847aa2073d70e1cb17b0991db9d462ce4728f95181e0dc81379e905c2bf`
- `/var/www/app.escloud.us/app.css`: `c2fa877952165b9084dc7e3e75b7026cf0c2669f7401007c32b37fec88508bd3`
- `/var/www/app.escloud.us/app.js`: `9394d9b50e12604c78f3b52f61b45872f132a54e71c459ab508655e632cf67ee`
- `/var/www/app.escloud.us/favicon.svg`: `88fb448689e751c3523f985d8332184c072c4184696200f5287ab926d3f57590`
- `/var/www/app.escloud.us/manifest.webmanifest`: `d3b0ab81f294010027b70f554c357f0535956485c032582e7e43bd19f5c7e7af`

## Verification Evidence

- `node -c /var/www/app.escloud.us/app.js`: PASS
- `nginx -t`: PASS
- `curl -k https://127.0.0.1/ -H "Host: app.escloud.us"`: HTTP 200
- `edge-monitor.service`: Active (running), `OVERALL: OK`
- Live Browser Preview snapshot: Captured in both Light and Dark modes.
