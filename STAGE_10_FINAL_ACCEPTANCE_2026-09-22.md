# Stage 10 — Edge Final Integrated Infrastructure Acceptance

Timestamp: 2026-09-22

Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE10_FINAL_ACCEPTANCE=PASS`

## Scope

Stage 10 performed the bounded final integrated acceptance of Cloud Infrastructure after Stages 0–9 were already COMPLETE / ACCEPTED.

The purpose was not to repeat stage-specific destructive or functional acceptance. Prior PASS evidence was reused where the accepted implementation had not changed. Fresh verification was limited to current integration boundaries, runtime-to-canonical reconciliation, ingress/TLS/auth, persistence, connectivity/data integration, backup/recovery state, maintenance, monitoring/alerts and the Cloud Portal.

No reboot, service-stop recovery simulation, restore overwrite, Syncthing conflict injection, NetBird disconnect, synthetic production failure or real update was performed.

## Reused acceptance evidence

The following accepted evidence remained authoritative and was not unnecessarily repeated:

- Stage 3 NetBird reboot persistence, routed Home/PAI connectivity, split DNS and P2P recovery;
- Stage 4 Hermes/vLLM, Codex and Antigravity E2E; Dashboard OIDC; Mattermost/n8n integrations; private Hermes API; macOS Desktop Remote Gateway;
- Stage 5 Knowledge propagation, outage/reconnect, conflict handling and reboot persistence;
- Stage 6 real isolated D5 restores and application-usability acceptance;
- Stage 7 Master Batch Task 12 and update-driver framework acceptance;
- Stage 8 transition confirmation, deduplication and recovery-alert behavior;
- Stage 9 authenticated browser acceptance and LIVE/STALE/UNAVAILABLE frontend fixtures.

## Fresh integrated audit

`STAGE10_INTEGRATED_READONLY_AUDIT_V1` completed with:

- `STAGE10_FRESH_FAILURES=0`;
- `STAGE10_INTEGRATED_READONLY_AUDIT=PASS`;
- `STAGE10_RUNTIME_MUTATIONS=NONE`;
- `STAGE10_DISRUPTIVE_TESTS=NONE`;
- final RC=0.

Fresh verification confirmed:

### Host and persistence

- host identity `edge.escloud.us`;
- kernel `7.0.0-31-generic`;
- required system services active and enabled: nginx, Docker, containerd, NetBird, Syncthing, Backrest, Semaphore, CloudCLI and edge-monitor;
- required user services active: Hermes Gateway, Hermes Dashboard and Antigravity daemon;
- zero failed systemd units;
- six production Docker workloads running, with all workloads that define healthchecks healthy.

### Listener and trust boundaries

- n8n, CloudCLI, Semaphore, Syncthing GUI/listener, Backrest, Mattermost, Authelia, Stalwart/Bulwark and Hermes Dashboard remain on their accepted loopback/private listeners;
- Hermes machine API remains private on `172.19.0.1:8642`;
- intentional public listeners remain bounded to the accepted SSH/web/mail/VPN surfaces.

### Ingress, TLS and authentication

- nginx configuration validation PASS;
- shared `escloud.us` certificate valid through 2026-12-20 and greater than 14 days from expiry at audit time;
- accepted SAN set present for app/auth/backup/chat/cloud/code/docs/hermes/mail/n8n/sync/update plus apex;
- `app.escloud.us`, `app.escloud.us/api/status`, `update.escloud.us` and `n8n.escloud.us` redirect unauthenticated clients to Authelia;
- `chat.escloud.us` retains the accepted Mattermost-native authentication boundary without Authelia.

### Cross-site connectivity and data integration

- NetBird management and signal connected;
- current edge NetBird version `0.79.0`;
- edge overlay address remains `100.105.178.187/16`;
- Home route to `192.168.1.3` uses `wt0`;
- `pve.lan -> 192.168.1.3` split DNS PASS;
- PVE Syncthing TCP/22000 reachable;
- ai-node vLLM reachable and serves `qwen3.8-27b-fp8`;
- edge Knowledge paths retain accepted ownership/modes;
- edge Syncthing service and loopback listener healthy.

### Backup and recovery state

- Backrest active;
- production config present as root:root mode 0600;
- Backrest operation database present and current enough for the Stage 8 monitor to report operations health OK;
- prior Stage 6 real restore evidence remains reused; no redundant destructive restore was performed.

### Maintenance

Current maintenance model remains:

- schema 3 / `update_units_v3`;
- 16 actionable targets / 23 monitored components / 8 APT-managed child components;
- `CHECK_FAILED=0`;
- `REBOOT_REQUIRED=0`;
- 15 CURRENT plus Hermes UPDATE_AVAILABLE due to the already-known active lazy-dependency drift;
- all autonomous Ubuntu APT paths masked/inactive;
- all effective APT periodic values are `0`.

Current component versions captured during reconciliation include:

- nginx `1.28.3-2ubuntu1.11`;
- Certbot `4.0.0-4`;
- UFW `0.36.2-9build1`;
- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- containerd `2.3.5`;
- NetBird `0.79.0`;
- Syncthing `2.1.5`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Backrest `1.14.1`;
- Restic `0.19.1`;
- Semaphore `2.19.12`;
- n8n `2.39.10`;
- Authelia `4.39.28`;
- Mattermost `11.11.0`;
- PostgreSQL `18.6`;
- Stalwart `0.16.23`;
- Bulwark `1.9.2`;
- Hermes `0.21.3`;
- CloudCLI `1.37.3`;
- Codex CLI `0.155.1`;
- Antigravity CLI `1.2.7`.

Hermes remains UPDATE_AVAILABLE because its application version itself is current while active lazy dependencies contain drift. This is an ordinary manual maintenance item, not an infrastructure acceptance failure.

### Monitoring and portal

- `edge-monitor.service` active with `NRestarts=0`;
- accepted monitor configuration SHA256 preserved:
  `91bacef62dbf5076b405b3b08512aa85ab6bb03ca0c887b7f86521cdd78133c5`;
- current monitor OVERALL state OK;
- Stage 9 portal files and nginx vhost remain byte-for-byte at their accepted hashes;
- no Stage 8 monitor mutation was introduced.

## Runtime-to-canonical reconciliation

Stage 7 final acceptance had explicitly recorded one persistence gap: the deployed runtime contained the final normalized `user_cli` execution context and Hermes lazy-dependency fail-closed behavior while the repository implementation source still predated those changes.

Stage 10 captured the exact deployed `/opt/edge-maintenance/scripts/manual-update` source:

- runtime SHA256 before reconciliation:
  `427e7aa5c708391000180bc5b39306d0a065e1e217356678a2d995c25da8a635`;
- Python compilation PASS;
- source explicitly normalizes core execution to `/home/core`;
- source verifies the core execution context during `user_cli` preflight;
- source performs Hermes active lazy-dependency verification after update and fails closed on drift.

That exact accepted runtime source was persisted back to the canonical repository. Current mutable version facts were also reconciled without rewriting historical acceptance evidence.

The follow-up drift-capture block ended RC=2 only because it invoked unsupported `hermes version`. The failure occurred after the exact runtime source and maintenance version state were already captured. It is classified as a verifier defect, not a runtime failure, and no rerun was required.

## Accepted constraints

Existing accepted constraints remain unchanged:

- Stage 8 has no independent external vantage point, so complete edge/network loss cannot be reported by edge itself;
- controlled Hermes SIGTERM may exit status 1 after graceful shutdown, while requested recovery remains healthy;
- Hermes currently has one ordinary pending manual lazy-dependency maintenance action;
- external Apple-device/Obsidian integration remains outside Cloud Infrastructure;
- user-specific automations/workflows remain post-infrastructure continuous work.

## Final result

All selected Cloud Infrastructure services and cross-project integration boundaries are deployed, accepted and mutually consistent. Fresh integrated verification found no runtime failure. The only canonical implementation drift found during Stage 10 was reconciled.

`STAGE10_FINAL_ACCEPTANCE=PASS`

**Stage 10 — COMPLETE / ACCEPTED.**

The finite Cloud Infrastructure build is complete.

The next workstream is the post-infrastructure continuous **Automation & User Workflows** stream.
