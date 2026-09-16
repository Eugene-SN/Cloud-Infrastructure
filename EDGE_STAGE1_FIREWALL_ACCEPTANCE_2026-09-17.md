# Edge Stage 1 Firewall Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_FIREWALL_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted host firewall policy

UFW is enabled as the minimal host-ingress firewall for the public VPS.

Accepted defaults:

- incoming: deny;
- outgoing: allow;
- routed: deny;
- IPv6 processing: enabled;
- logging: low.

Accepted public Stage 1 allowances, for both IPv4 and IPv6:

- `22/tcp` — SSH;
- `80/tcp` — nginx HTTP / ACME;
- `443/tcp` — Xray TLS/VLESS ingress;
- `443/udp` — Hysteria2 ingress.

No additional host-ingress allow rules are accepted in Stage 1.

## Effective kernel rule verification

Loaded UFW user rules were verified directly rather than by parsing tabular `ufw status` output:

- IPv4 chain `ufw-user-input`: exactly one ACCEPT rule for each accepted protocol/port;
- IPv6 chain `ufw6-user-input`: exactly one ACCEPT rule for each accepted protocol/port;
- IPv4 INPUT chain integrated with the UFW chain sequence;
- IPv6 INPUT chain integrated with the UFW6 chain sequence;
- effective INPUT base policy observed as DROP during acceptance.

## Docker firewall interaction

Docker-generated firewall behavior remains intact:

- FORWARD policy remains DROP;
- FORWARD still enters `DOCKER-USER` before Docker forwarding chains;
- `DOCKER-USER` contains no custom rules;
- Docker-generated rules were not replaced or disabled;
- current Authelia publication remains `127.0.0.1:19091 -> 9091/tcp` only.

Current policy is therefore:

- UFW protects host-bound ingress;
- application containers should remain loopback-published by default and reach the public Internet through the accepted nginx/Xray ingress path;
- no custom `DOCKER-USER` policy is required for the current Stage 1 state.

## Functional non-regression

After enabling UFW:

- current SSH session remained connected;
- `ssh.socket` remained active;
- SSH TCP/22 listener remained present;
- local nginx HTTP health: PASS;
- public IPv4 HTTP/80: PASS;
- public IPv4 HTTPS through Xray TCP/443: PASS;
- Xray -> nginx fallback: PASS;
- Authelia HTTPS path: PASS;
- Hysteria2 service and UDP/443 listener: PASS;
- Docker, nginx, Xray and Hysteria2 remained active;
- Authelia remained running/healthy;
- failed systemd units: 0.

## Recovery-history note

Three earlier enable attempts were rolled back automatically because verification scripts contained parsing/chain-name errors, not because the firewall policy or runtime connectivity failed. The final V4 acceptance corrected those verifiers and completed successfully. No additional firewall remediation is required.

## Next Stage 1 work

Audit the remaining Stage 1 base-platform scope as one bounded set: public/decoy page, remaining persistent-layout conventions, private Cloud Infrastructure page boundary, base-state backup, extension points, and final integrated Stage 1 acceptance requirements.
