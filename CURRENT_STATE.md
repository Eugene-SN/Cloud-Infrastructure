# Cloud Infrastructure — Current State

## Canonical checkpoint

**Stage 0 — COMPLETE / ACCEPTED**  
**Stage 1 — COMPLETE / ACCEPTED**  
**Stage 2 — Edge Core Applications — COMPLETE / ACCEPTED**  
**Stage 02.5 — Remaining Functional Scope Reconciliation & Research — COMPLETE / ACCEPTED**

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.  
`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS` on 2026-09-18.

Primary repository: `Eugene-SN/Cloud-Infrastructure`.

Next production branch:

`03 — Edge Cross-site Connectivity Foundation`

Stage 02.5 final acceptance record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

## Stage 02.5 accepted research state

### Hermes

**Hermes Agent — SELECTED.**

Accepted direction:

- persistent cloud-side agent runtime on `edge`;
- runs in parallel with n8n rather than replacing it;
- preferred host-native placement under `core`;
- Hermes invokes Codex/Antigravity directly rather than through CloudCLI;
- user-specific n8n/Hermes workflows remain post-infrastructure work.

### Cross-site Connectivity Foundation

**Existing self-hosted NetBird — SELECTED / REUSE EXISTING.**

Detailed acceptance record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Accepted target:

- `edge` becomes an ordinary host-native NetBird service peer;
- Home CT300 remains the Home routing/control-plane foundation;
- `edge` receives Home LAN access but not the Home Internet `0.0.0.0/0` resource;
- `edge` keeps direct VPS-provider Internet/default routing;
- Home/PAI clientless hosts reach `edge` through gateway-level routing of `100.105.0.0/16` via CT300 `192.168.1.90`;
- VM100 and MikroTik both participate in route persistence so VRRP ownership does not change private reachability;
- existing `.lan` split DNS is reused on `edge` and `edge.lan` is added through the existing Home DNS mechanism after Stage 3 enrollment/routing acceptance;
- direct WireGuard/Tailscale are rejected as duplicate private backbones; AmneziaWG is contingency only if real Stage 3 transport acceptance fails.

No Stage 02.5 runtime networking/DNS/firewall mutation was performed.

### Data / knowledge project boundary

The previous future-architecture constraint that `ai-node:/srv/ai-data/knowledge/obsidian` must permanently remain canonical is superseded.

**Current factual runtime remains unchanged until Home Infrastructure completes its migration.** The existing vault on `ai-node` remains the current source at this checkpoint.

Accepted future ownership boundary:

- **Home Infrastructure** owns the PVE 24/7 canonical knowledge foundation, PVE-side synchronization service, Home consumers and Home-side backup integration;
- **Personal Agents Infrastructure** owns the `ai-node` active RW synchronized replica and local n8n/OpenClaw/vLLM/OCR/RAG consumers/producers after Home cutover;
- **Cloud Infrastructure** owns only the `edge` active RW synchronized replica and n8n/Hermes/cloud-AI integration.

Cloud Stage 5 is therefore an integration stage. It must begin with a fresh expanded read-only Home/PAI/Cloud audit and must reuse the Home-accepted server-side synchronization mechanism by default.

If PVE canonical migration has not reached explicit Home acceptance when Stage 5 begins, Stage 5 stops before mutation and reconciles the dependency instead of creating a parallel canonical/sync architecture.

MacBook/iPhone/iPad Obsidian synchronization is completely outside Cloud Infrastructure scope and is assigned to a later separate Home Infrastructure user-integration branch.

## Final remaining roadmap

1. **Stage 3 — Edge Cross-site Connectivity Foundation**;
2. **Stage 4 — Edge Hermes Agent Runtime**;
3. **Stage 5 — Edge Knowledge Replication & Data Integration**;
4. **Stage 6 — Edge Backrest & Recovery**;
5. **Stage 7 — Edge Maintenance & Update**, including separate Codex `update.escloud.us` substage;
6. **Stage 8 — Edge Monitoring, Heartbeats & Alerts**;
7. **Stage 9 — Edge Cloud Portal**, including separate Codex `app.escloud.us` substage;
8. **Stage 10 — Edge Final Integrated Infrastructure Acceptance**;
9. post-infrastructure **Automation & User Workflows** as a continuous workstream.

The old conditional `Remaining Infrastructure Services` stage is removed because Stage 02.5 selected no additional standalone infrastructure product requiring that slot.

Backrest-before-Semaphore remains mandatory. Monitoring remains late-stage so it is built once against the substantially complete inventory. `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

## Host / foundation

- logical node/FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- KVM x86_64, 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- IPv4 `45.92.156.17/24`, IPv6 `2a0c:b847:ffff:283::a/64`;
- timezone `Europe/Moscow`;
- root SSH key-only through `ssh.socket`;
- Docker Engine `29.8.1`, Compose `5.5.1`, containerd;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27` on public TCP/443 with nginx fallback;
- Hysteria2 `2.12.3` on public UDP/443;
- UFW active: default deny incoming, allow outgoing, deny routed;
- intentional public TCP listeners: 22, 80, 443, 25, 465, 993; UDP 443;
- application WebUI backends remain loopback-only unless explicitly accepted otherwise.

Shared service account `core`: UID/GID `1000:1000`, password locked, no sudo/docker group. `core` linger is enabled for Antigravity Remote Control.

## Authentication / ingress

### Authelia

- version `4.39.27`;
- backend `127.0.0.1:19091 -> 9091`;
- fresh operator/auth state;
- public `auth.escloud.us` accepted.

Protected private web namespace includes `n8n`, `code`, future `app`, `backup`, `ops`, `update`, `docs`, `cloud`, `sync`, `chat`. `mail.escloud.us` intentionally uses native mail-stack authentication.

## TLS

Shared Certbot lineage: `/etc/letsencrypt/live/escloud.us`.

Current SAN set includes `escloud.us`, `app`, `auth`, `backup`, `chat`, `cloud`, `code`, `docs`, `mail`, `n8n`, `ops`, `sync.escloud.us`. `update.escloud.us` has been created in DNS for the future maintenance/update page; certificate/ingress activation remains deferred to Stage 7.

## Stage 2 applications

### n8n

- version `2.39.7`;
- backend `127.0.0.1:15678` only;
- public `https://n8n.escloud.us/` through Authelia;
- fresh application state at Stage 2 acceptance.

### CloudCLI

- version `1.37.3` under `/home/core/.local`;
- backend `127.0.0.1:18140` only;
- public `https://code.escloud.us/` through Authelia;
- fresh local application/auth state at acceptance.

### Codex CLI

- version `0.154.0` official standalone runtime;
- fresh ChatGPT authorization;
- Remote Control through Unix control socket only;
- no public Codex network listener.

### Antigravity CLI

- version `1.2.5`;
- fresh Google OAuth;
- Remote Control instance `edge`;
- persistent user service accepted.

## Mail — production accepted

- Stalwart `0.16.22`;
- Bulwark `1.9.2`;
- loopback web backends: Stalwart `127.0.0.1:18083`, Bulwark `127.0.0.1:18084`;
- public mail protocols: TCP/25 SMTP, TCP/465 SMTPS submission, TCP/993 IMAPS;
- `es@escloud.us` useful mailbox/account/address-book/calendar/identity state migrated with fresh credentials;
- fresh Stalwart/Bulwark auth/session/DKIM material;
- MX/PTR/SPF/DKIM/DMARC accepted;
- Gmail outbound and inbound bidirectional E2E verification passed.

## Stage 2 final integrated acceptance

Final recovery run proved foundation services, Stage 2 applications, mail, public ingress/listeners, loopback backend contract, UFW, readiness/health, TLS/DNS/DKIM identity and accepted config non-regression.

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

## Recovery / preserved state

- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- migration-preservation archive: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, retained outside GitHub for legacy-reference/recovery use; do not indiscriminately restore legacy credentials.

## Current next step

Stage 02.5 is closed. The next production task is **Stage 3 — Edge Cross-site Connectivity Foundation**.
