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

2. **Full-Width Horizontal Telemetry Strip (Top Row)**:
   - **Edge Node Telemetry** rendered as a sleek horizontal glass strip directly below the header.
   - Displays AMD EPYC 2 vCPU tag on the left, and 3 horizontal metric columns in strict order **CPU Load → Memory → NVMe Storage** with clean vertical hairline dividers, exact utilization percentages, 5px capsule progress tracks, and detailed resource stats (`Load avg`, `GiB used of total`).

3. **Full-Width Horizontal Hybrid Fabric Strip (Row 2)**:
   - **Hybrid Fabric & AI Compute** positioned as a matching sleek horizontal glass strip directly underneath Edge Node Telemetry.
   - 3 horizontal columns with hairline dividers:
     - **Private AI Cluster**: `Online · 41 ms` status pill, vLLM `qwen3.8-27b-fp8` on Proxmox VE.
     - **Knowledge Vault Sync**: `Synchronized` status pill, Syncthing continuous replication Obsidian vault.
     - **Edge Host Services**: `14 Units · 10 Docker` status pill, systemd & container runtime nominal.

4. **Authentic Darkened Brand Icons & Frosted Glass Tiles ("оригинальные затемненные иконки и эффект стекла")**:
   - **Official Vector Logos Installed**:
     - `Hermes Agent`: Official Nous Research / Hermes emblem (`/icons/hermes.svg`).
     - `T3 Code`: Official VS Code runtime vector logo (`/icons/vscode.svg`).
     - `n8n Automation`: Official n8n pipeline node logo (`/icons/n8n.svg`).
     - `Mattermost Chat`: Official Mattermost teardrop compass logo (`/icons/mattermost.svg`).
     - `Nextcloud Drive`: Official Nextcloud 3-ring cloud logo (`/icons/nextcloud.svg`).
     - `Stalwart Webmail`: Official Bulwark / Stalwart shield logo (`/icons/stalwart.svg`).
     - `Stalwart Mail Admin`: Stalwart shield with discrete `ADM` chip (`/icons/stalwart.svg`).
     - `Maintenance Hub`: Official Semaphore UI logo (`/icons/semaphore.svg`).
     - `Backrest Vaults`: Official Backrest / Restic cube logo (`/icons/backrest.png`).
   - **Darkened & Subdued ("затемнить и сделать менее яркими")**:
     - Applied muted CSS filters (`filter: brightness(0.82) contrast(0.92) saturate(0.65); opacity: 0.85`) so icons blend softly into the smoked glass without screaming neon saturation.
   - **True Frosted Glass & Transparency on Tiles**:
     - Translucent glass backgrounds (`rgba(255, 255, 255, 0.40)` in light mode, `rgba(18, 22, 28, 0.48)` in dark mode) paired with `backdrop-filter: blur(24px) saturate(140%)` and top-edge hairline highlights (`inset 0 1px 0 rgba(255,255,255,0.85)`).
     - Hover transitions smoothly to elevated frosted glass with soft specular sheen.

5. **Dual Deck Inset Panels (Bottom Row)**:
   - **Endpoint Probes**: macOS System Settings style Inset Grouped Table with green pips, service names, port tags, and clean HTTP badges (`HTTP 200`, `HTTP 401`).
   - **Subsystems & Mesh Fabric**: Grouped Inset List for Proxmox VE, AI Node, vLLM engine, and NetBird WireGuard, alongside compact systemd unit chips.

## Accepted Deployed File Hashes

- `/var/www/app.escloud.us/index.html`: `2731c7d25476c2f70e194077471b140efb103d2de69ddc0bd8a7fd40fd726b28`
- `/var/www/app.escloud.us/app.css`: `31c36fbef98ce5e143a932ed9573433047fe5d248fcafdb15518c8830b917b31`
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
- Live Browser Preview snapshots: Verified with authentic brand marks and frosted glass tiles.
