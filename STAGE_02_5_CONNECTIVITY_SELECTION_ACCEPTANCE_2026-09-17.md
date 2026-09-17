# Stage 02.5 — Cross-site Connectivity Selection Acceptance

**Date:** 2026-09-17  
**Status:** ACCEPTED / RESEARCH-ONLY  
**Runtime mutation during this decision:** NO

## Scope

This record accepts the cross-site connectivity architecture for Cloud Infrastructure after a fresh read-only audit of Home Infrastructure NetBird, VM100 `gateway-core`, CT300 `remote-access`, PVE networking and the NetBird control plane.

The implementation itself is deferred to the future connectivity deployment stage.

## Fresh audited Home state

The read-only audit established:

- Home LAN: `192.168.1.0/24`.
- VRRP VIP: `192.168.1.254`.
- VM100 `gateway-core`: LAN `192.168.1.2`, normal VRRP MASTER behavior, Mihomo policy-routing plane.
- CT300 `remote-access`: `192.168.1.90/24`, host default gateway `192.168.1.1`.
- Existing self-hosted NetBird routing peer: `100.105.97.126/16`.
- NetBird account IPv4 overlay: `100.105.0.0/16`.
- NetBird uses the current `Networks` model; legacy routes are empty.
- Existing `Home Network` resources:
  - `Home LAN` = `192.168.1.0/24`;
  - `Internet` = `0.0.0.0/0`.
- `Routing Peers` contains only `netbird-router`.
- `User Devices` contains interactive user devices.
- Existing `Home LAN Access` policy grants `User Devices` access to `192.168.1.0/24`.
- Existing `Internet via Home Gateway` policy grants `User Devices` access to `0.0.0.0/0`.
- Existing NetBird DNS pushes `192.168.1.1:53` only for match domain `lan`, with search-domain behavior enabled and no NetBird primary DNS override.
- NetBird management and signal are connected to `https://netbird.encores.ru:443`.
- Existing relay `rels://netbird.encores.ru:443` is available via WebSocket/TCP 443 and STUN is available on UDP 3478.

## Verified routing behavior

CT300 deliberately separates its own Internet traffic from NetBird-routed Internet traffic.

Normal CT300 host traffic uses:

```text
CT300 -> 192.168.1.1 MikroTik -> Internet
```

Traffic arriving from NetBird interface `wt0` uses policy table `6300`, which contains:

```text
default via 192.168.1.254 dev eth0
100.105.0.0/16 dev wt0
192.168.1.0/24 dev eth0
```

with an `iif wt0` policy rule selecting that table.

Therefore the current user-device Internet Exit is intentionally:

```text
Remote NetBird device
 -> CT300
 -> VRRP VIP 192.168.1.254
 -> VM100/Mihomo during normal operation
 -> Home Internet path
```

If VM100 fails and the VIP moves to MikroTik, the NetBird Internet Exit architecture remains address-stable and can fall back through MikroTik. Preservation of the Mihomo policy itself is not promised when VM100 is unavailable. A controlled end-to-end VRRP failover test remains an implementation-stage acceptance item rather than a research-stage mutation.

Traffic from NetBird to `192.168.1.0/24` is directly connected on CT300 and does not require the VRRP VIP.

## Accepted target architecture

Reuse the existing self-hosted Home NetBird as the **bidirectional routed private fabric** between Cloud Infrastructure and Home/PAI.

`edge` becomes an ordinary host-native NetBird service peer. CT300 remains the Home routing peer. No second overlay product is introduced.

Target private topology:

```text
                         NetBird private fabric
                            100.105.0.0/16
                                   |
                 +-----------------+-----------------+
                 |                                   |
               edge                                CT300
         ordinary service peer               existing routing peer
                 |                             192.168.1.90
                 |                                   |
                 |                           Home LAN 192.168.1.0/24
                 |                           /        |        \
                 |                         PVE     ai-node    CT220...
                 |
         direct VPS Internet
         remains provider-local
```

This is a routed L3 fabric, not an L2 bridge.

## `edge -> Home/PAI`

Create a dedicated NetBird service group for Cloud Infrastructure. `edge` receives access to the existing `Home LAN` resource `192.168.1.0/24` through CT300.

`edge` must **not** receive the existing `Internet` resource `0.0.0.0/0`.

Consequently:

- Home/PAI private traffic goes through NetBird;
- normal `edge` Internet egress remains through the VPS provider;
- Xray, Hysteria2, nginx, mail and cloud-AI Internet behavior are not routed through Home.

## `Home/PAI -> edge`

Home/PAI services must be able to initiate private connections to `edge` without installing NetBird on every Home host.

The accepted direction is NetBird Site-to-VPN style routing:

```text
Home/PAI host
 -> normal Home gateway
 -> route 100.105.0.0/16 via 192.168.1.90
 -> CT300
 -> NetBird
 -> edge
```

Implementation-stage requirements:

- add the NetBird account route `100.105.0.0/16 via 192.168.1.90` to both VM100 and MikroTik so VRRP gateway ownership does not change reachability;
- add only the narrow VM100 forwarding exception required for LAN-to-NetBird-account routed traffic;
- do not create per-host static routes where a gateway-level route is sufficient;
- first reuse and verify the existing NetBird-managed Site-to-VPN masquerade behavior already visible in the CT300 ruleset; do not duplicate it with a second manual NAT rule unless implementation evidence proves it necessary.

NetBird clients on PVE, `ai-node`, CT220 or other Home guests are not baseline requirements. Install an individual peer only when a concrete consumer needs direct peer identity/P2P behavior that routed access cannot provide.

## Private DNS

Reuse the existing Home `.lan` namespace and NetBird split-DNS behavior.

For `edge`:

- queries for `*.lan` use `192.168.1.1:53` through the existing NetBird match-domain configuration;
- ordinary Internet DNS remains the VPS normal resolver path;
- no new DNS server is introduced;
- `edge` does not become authoritative/recursive DNS for Home.

After `edge` enrollment and bidirectional routing are deployed, add an `edge.lan` record through the existing canonical Home DNS mechanism, pointing to the stable NetBird address of `edge`.

This enables private naming such as:

```text
edge -> ai-node.lan
edge -> pve.lan
Home/PAI -> edge.lan
```

while public service names under `*.escloud.us` remain a separate Internet-facing namespace.

## Technology disposition

- Existing self-hosted NetBird: `SELECTED / REUSE EXISTING`.
- Existing CT300 routing peer: `REUSE EXISTING`.
- Existing Home `Networks` model: `REUSE EXISTING`.
- Existing `.lan` split DNS: `REUSE EXISTING`.
- Direct WireGuard as a parallel backbone: `REJECTED` because it duplicates the accepted overlay and lacks the already deployed NetBird management/relay model.
- Tailscale as a parallel overlay: `REJECTED` because it duplicates the accepted self-hosted NetBird control/relay plane.
- AmneziaWG: contingency only if real deployment acceptance demonstrates an unresolved NetBird transport/DPI failure.
- Public HTTPS remains complementary for genuinely public/webhook interfaces; it is not the private backbone.

## Stage-order change

The dependency order is changed so connectivity is implemented before Hermes.

Accepted order:

1. **Stage 3 — Edge Cross-site Connectivity Foundation**.
2. **Stage 4 — Edge Hermes Agent Runtime**.
3. Stage 5 — Edge Cross-site Data & Knowledge Services.
4. Later lifecycle/monitoring/portal stages retain their existing relative order, subject to the already accepted conditional-stage normalization rule.

Reason: Stage 4 Hermes can then be deployed and accepted in one coherent stage including both cloud executors and the local vLLM path instead of deliberately leaving `Hermes -> vLLM` unfinished until a later connectivity stage.

Stage 3 establishes transport, routing and private naming only. The concrete vLLM service exposure/bind and Hermes provider integration remain Stage 4 consumer configuration.

## Stage 3 implementation acceptance requirements

At minimum Stage 3 must verify:

- host-native NetBird peer enrollment on `edge`;
- `edge` has Home LAN reachability but does not receive Home Internet Exit;
- `edge` default Internet route remains provider-local;
- `edge -> ai-node`, `edge -> PVE` and selected safe Home targets work privately;
- `.lan` split DNS works from `edge` without hijacking general DNS;
- Home/PAI clientless hosts can initiate private traffic to `edge` through the gateway-level `100.105.0.0/16 -> CT300` route;
- VM100/MikroTik routing is recoverable and preserves VRRP semantics;
- NetBird direct/relay behavior is observed on the real path;
- existing public `edge` ingress and mail/VPN behavior is non-regressed;
- reboot persistence is verified;
- a controlled VRRP failover test proves the expected Home connectivity behavior if the implementation-stage recovery plan permits it.

## Stage 4 Hermes implication

Stage 4 can now deploy Hermes with a complete infrastructure acceptance target:

```text
n8n -> Hermes -> Codex/AGY -> Hermes -> n8n
                 |
                 +-> local vLLM on ai-node over the accepted private fabric
```

The exact vLLM bind/exposure contract is not preselected by this connectivity record; Stage 4 must inspect and minimally expose the required endpoint through the accepted private path.

## No runtime mutation

This Stage 02.5 acceptance records research and architecture only. No `edge`, Home, PVE, VM100, CT300, NetBird, DNS or firewall production mutation was performed by this decision.