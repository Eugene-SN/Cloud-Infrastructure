# Stage 3 — Edge Cross-site Connectivity Foundation Acceptance — 2026-09-18

**Status:** COMPLETE / ACCEPTED / PASS  
**Branch:** `03 — Edge Cross-site Connectivity Foundation`

## Final result

`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Stage 3 is complete. The accepted Cloud ↔ Home/PAI private transport is the existing self-hosted NetBird fabric with `edge` as an ordinary host-native service peer and CT300 as the Home routing peer.

## Accepted production topology

### edge

- NetBird version `0.78.2`;
- host-native systemd service;
- NetBird IPv4 `100.105.178.187/16`;
- WireGuard UDP port `51820`;
- provider-local public/default Internet remains through `45.92.156.17/24` via `45.92.156.1`;
- no Home Internet `0.0.0.0/0` resource is assigned to `edge`;
- Home LAN route `192.168.1.0/24 dev wt0`;
- Home `.lan` split DNS through `192.168.1.1:53`;
- public/global IPv6 is absent from `ens3`; IPv6 remains enabled for link-local/NetBird overlay use.

### Home / CT300

- CT300 remains the existing NetBird routing/control-plane foundation at `192.168.1.90`;
- CT300 NetBird IPv4 `100.105.97.126/16`;
- existing NetBird-managed Home routing/masquerade is reused;
- no duplicate manual NAT was added.

## Accepted reverse-direction scope

Stage 3 does **not** inject the NetBird account overlay into the whole Home LAN.

Current accepted behavior:

- `edge -> Home/PAI`: private NetBird routed path;
- Home/PAI -> Cloud services: normal public VPS IPv4 / `escloud.us` service ingress by default;
- hosts that are themselves NetBird peers may use normal peer-to-peer overlay connectivity;
- VM100 and MikroTik were not modified for a hypothetical clientless `100.105.0.0/16` route;
- no `edge.lan` record was created;
- LAN-wide clientless Home/PAI -> `edge` overlay routing remains a deferred on-demand extension for a concrete private-only workload.

This preserves the accepted scope-normalization decision recorded on 2026-09-18.

## Recovery / lifecycle implementation

Accepted `edge` NetBird lifecycle:

- `Restart=always`;
- effective `RestartSec=5s`;
- pre-start helper `/usr/local/sbin/netbird-stage3-prestart`;
- helper SHA256 `c789206363be25dabbb3b2372fc584467f79d8ec0416c5bbae71c346e26f43a4`;
- drop-in `95-stage3-wt0-cleanup.conf` removes stale `wt0` state before service start.

The helper exists only to recover stale local interface state; it does not replace NetBird routing or policy logic.

## Fault / recovery acceptance

### edge NetBird process crash

Accepted earlier in Stage 3:

- process-crash recovery stayed within the `<=10s` service/data target;
- P2P returned within the accepted `<=15s` process-crash target;
- sustained post-recovery traffic passed with zero packet loss.

### CT300 NetBird process crash

Accepted earlier in Stage 3:

- Docker/container recovery and real data-plane restoration completed within accepted thresholds;
- final CT300 <-> edge P2P remained direct and stable;
- sustained post-recovery traffic passed.

### CT300 full reboot

Accepted earlier in Stage 3:

- LXC became usable within the accepted reboot threshold;
- NetBird data and P2P recovered within accepted thresholds measured from actual CT300 boot;
- sustained post-recovery traffic passed.

## edge final reboot acceptance

The final post-fix reboot produced:

- actual boot ID `a9565c84-3b3e-4a53-8344-adaf32471425`;
- total boot time `14.881s`;
- wait-online active/success;
- `ens3` state `routable (configured)` / online;
- only public IPv4 `45.92.156.17` plus link-local IPv6 on `ens3`;
- NetBird autostart PASS with `NRestarts=0`;
- CT300 peer connected P2P;
- `192.168.1.0/24 dev wt0` persisted;
- `pve.lan -> 192.168.1.3` split-DNS resolution persisted;
- 30/30 zero-loss traffic to CT300 overlay, PVE and `ai-node`.

`STAGE3_EDGE_FINAL_REBOOT_ACCEPTANCE_V2=PASS`.

## External CT300 reboot watcher

Synchronized CT300 observation of the same final reboot:

- first overlay outage epoch: `1789707335803`;
- first public outage epoch: `1789707339169`;
- actual edge boot epoch: `1789707342518`;
- first public recovery epoch: `1789707351384`;
- first overlay/P2P recovery epoch: `1789707355705`;
- public recovery from actual edge boot: approximately `8.866s`;
- working overlay/P2P recovery from actual edge boot: approximately `13.187s`;
- final connection type: P2P;
- final endpoints: CT300 `192.168.1.90:51820` <-> edge `45.92.156.17:51820`;
- final latency approximately `40.4ms`;
- 30/30 post-reboot CT300 -> edge overlay packets succeeded with 0% loss.

The watcher's printed aggregate duration line contains a cosmetic literal-`n` formatting defect; the individual epoch timestamps are authoritative and internally consistent.

`STAGE3_EDGE_FINAL_REBOOT_REMOTE_WATCH_CT300_V2=PASS`.

## Reboot lifecycle correction encountered during Stage 3

Stage 3 reboot testing exposed an independent Stage 1 Docker configuration error: `live-restore=true` caused an approximately 90-second late-shutdown stall on the current edge runtime.

That issue was corrected and separately accepted in:

`EDGE_REBOOT_LIFECYCLE_FIX_ACCEPTANCE_2026-09-18.md`

Current authoritative Docker state is `live-restore=false`; production application containers use `restart=unless-stopped`.

The correction is part of the accepted current platform state but is not part of NetBird's architecture.

## Final acceptance gates

- `EDGE_FULL_REBOOT_NEW_BOOT=PASS`;
- `EDGE_BOOT_WAIT_FIX_PERSISTENCE=PASS`;
- `EDGE_PUBLIC_IPV4_ONLY_PERSISTENCE=PASS`;
- `EDGE_NETBIRD_AUTOSTART=PASS`;
- `EDGE_NETBIRD_CONTROL_PLANE=PASS`;
- `EDGE_NETBIRD_P2P=PASS`;
- `EDGE_HOME_ROUTE_PERSISTENCE=PASS`;
- `EDGE_SPLIT_DNS_PERSISTENCE=PASS`;
- `EDGE_POST_REBOOT_DATA_PLANE=PASS`;
- `FINAL_P2P_GATE=PASS`;
- `EDGE_51820_ENDPOINT_GATE=PASS`;
- `CT300_TO_EDGE_POST_REBOOT_ZERO_LOSS_GATE=PASS`.

## Stage transition

Stage 3 is COMPLETE / ACCEPTED.

The next independent production branch is:

`04 — Edge Hermes Agent Runtime`

Stage 4 must use the already accepted Stage 3 NetBird transport and must not reopen Stage 3 routing/product choices absent a concrete incompatibility.
