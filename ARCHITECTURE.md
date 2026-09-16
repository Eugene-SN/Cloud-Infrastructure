# Cloud Infrastructure — Edge Architecture Contract

## Status

**Architecture status:** `PROPOSED` — acceptance candidate for branch **03 — Edge Architecture Contract & Topology**.

This document is the canonical target-architecture proposal for `edge`. It consolidates the already accepted functional/service decisions into one deployment contract.

It is **not yet an ACCEPTED runtime authorization**. Until explicit Architecture Contract acceptance:

- do not deploy or restore target services;
- do not change ingress, firewall/public listeners, private backbone, Docker/application storage layout or service authentication;
- the already accepted clean Ubuntu substrate and minimal base bootstrap remain the live state.

After acceptance, this document becomes the architecture authority for target deployment; implementation may refine low-level parameters only where that does not change the contract.

---

## 1. Architecture intent

`edge` is the external 24/7 Cloud Infrastructure node that complements, rather than duplicates, Home Infrastructure and Personal Agents Infrastructure (PAI).

Its primary roles are:

- DPI-resistant foreign Internet egress;
- public Internet ingress and event reception;
- mail;
- always-on automation;
- subscription/cloud-AI execution;
- external monitoring and coordination;
- user/agent working-file access and selected synchronization;
- Obsidian synchronization endpoint while the canonical vault remains on `ai-node`;
- off-site failure-domain participation and disaster-recovery coordination;
- durable orchestration between Cloud and Home/PAI.

It is not a second PVE/Home platform, a second local AI compute node, a general cloud-drive suite, or a generic service laboratory.

### Design priorities

1. Correctness and recoverability.
2. Minimum components and minimum custom glue.
3. Upstream-supported deployment mechanisms.
4. Clear public/private/authentication boundaries.
5. A usable standalone `edge` before Home/PAI integration becomes a dependency.
6. No architecture inherited solely because it existed on `nl-core-vds`.

The sanitized `migration-reference/` remains an engineering reference only. Exact credential-bearing recovery state comes from the external migration archive when required.

---

## 2. Accepted substrate boundary

The accepted live substrate remains:

- logical node / short hostname: `edge`;
- FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, x86_64, KVM;
- 2 vCPU, approximately 15 GiB RAM, 4 GiB swap;
- single ext4 root filesystem, approximately 155 GiB class;
- public IPv4 `45.92.156.17/24`;
- public IPv6 `2a0c:b847:ffff:283::a/64`;
- SSH root access by public key only;
- OpenSSH socket activation through `ssh.socket`;
- provider-generated working Netplan/cloud-init networking remains authoritative unless a later concrete change requires otherwise;
- persistent journald usage ceiling `500M`;
- `/tmp` remains the temporary-data location.

No repartitioning, LVM layer, separate Docker disk, or filesystem redesign is required for the target architecture.

---

## 3. Runtime placement contract

The runtime uses a deliberately mixed **host-native + Docker Compose** model. Containerization is used where it reduces application lifecycle complexity; host-native execution is used where the service owns the public L4 edge, integrates directly with the OS/network, or requires a persistent user HOME/session environment.

### 3.1 Host-native systemd-managed components

| Component | Placement | Contract |
| --- | --- | --- |
| OpenSSH | host / existing Ubuntu package | Keep accepted `ssh.socket` model and key-only root access. |
| nginx | host | Public HTTP port 80 plus loopback HTTP backend for Xray fallback; single reverse-proxy ingress for web applications. |
| Xray | host | Owns public TCP/443 for VLESS/TLS and forwards non-VLESS HTTPS traffic to nginx through a loopback PROXY-protocol fallback. |
| Hysteria2 | host | Owns public UDP/443; uses the same public TLS identity and public masquerade content family as the HTTPS edge. |
| NetBird client | host, conditional acceptance gate | Preferred private-overlay implementation, but not an accepted dependency until real Russia ↔ `edge` path testing passes after this Architecture Contract is accepted. |
| CloudCLI | host under dedicated Unix user `core` | Loopback-only WebUI/service where applicable; working directory under the shared workspace. |
| Codex CLI / app-server | host under `core` | Subscription/auth state remains in the `core` HOME; persistent app-server only where required by CloudCLI/workflows. |
| Antigravity CLI | host under `core` | Same user/workspace model; persistent daemon only if the actual product integration requires one. |

Do not containerize the subscription CLI layer merely for uniformity: its useful state is user-session/auth/workspace state and it needs direct access to the host workspace.

### 3.2 Docker Compose application stacks

Use several small Compose projects separated by lifecycle/function rather than one legacy-style monolithic stack:

| Compose project | Services |
| --- | --- |
| `edge-auth` | Authelia |
| `edge-automation` | n8n |
| `edge-mail` | Stalwart, Bulwark |
| `edge-data` | SFTPGo, CouchDB for Self-hosted LiveSync, Syncthing |
| `edge-ops` | Backrest, Semaphore, Uptime Kuma |

The Cloud portal and maintenance page are lightweight static assets served directly by host nginx; they do not require a dedicated portal container.

### 3.3 Docker networking rules

- Each Compose project gets its own default bridge network unless a same-stack service relationship requires another local network.
- Do not recreate the legacy shared `internal` / `egress` / `monitoring` / static `runner` network topology without a concrete need.
- Web/admin backends publish only to host loopback (`127.0.0.1:<port>`) and are reached through nginx.
- Deliberate native Internet protocols are the exception: Stalwart publishes only the mail protocol listeners explicitly required by the contract.
- Private native protocols may bind to the future NetBird interface/IP after its acceptance gate passes.
- Do not expose the Docker socket or deploy a Docker-socket proxy merely to populate monitoring/portal metadata.

### 3.4 n8n execution boundary

n8n remains containerized. It does **not** receive the host Docker socket and it does not require restoration of the legacy custom Codex runner API.

For workflows that must execute CloudCLI/Codex/Antigravity on the host:

- n8n uses its standard SSH capability to execute as `core` on `edge`;
- the dedicated key is an n8n credential and the corresponding `core` login has no password;
- cloud-agent commands run with the real `/home/core` auth/session state and `/srv/edge/workspace` data;
- root/infrastructure maintenance remains outside this channel and belongs to Semaphore/operator workflows.

This avoids both Docker-host escape plumbing and a custom permanent runner service.

Use the n8n embedded/default single-instance database model unless a verified workload later requires a database migration. Do not add PostgreSQL, Redis, queue mode or worker replicas pre-emptively.

---

## 4. Public ingress and domain contract

### 4.1 L4 ownership

Public listener ownership is intentionally explicit:

| Listener | Owner | Purpose |
| --- | --- | --- |
| TCP/22 | OpenSSH | Administrative SSH, key-only. |
| TCP/80 | nginx | ACME HTTP-01 and HTTP→HTTPS/approved plain-HTTP responses. |
| TCP/443 | Xray | VLESS/TLS plus fallback of ordinary HTTPS traffic to nginx. |
| UDP/443 | Hysteria2 | Hysteria2 transport and masquerade behavior. |
| TCP/25 | Stalwart | SMTP server-to-server. |
| TCP/465 | Stalwart | Authenticated implicit-TLS submission as retained from the working mail design. |
| TCP/993 | Stalwart | IMAPS. |

No other public application ports are part of the initial contract. A later application may add a listener only by explicit change, not by convenience.

### 4.2 HTTPS path

The normal web path is:

```text
Internet TCP/443
      |
      v
   Xray TLS
   |       \
   |        \ ordinary HTTPS / non-VLESS
   |         v
 VLESS   loopback PROXY protocol
             |
             v
          nginx
             |
       host loopback ports
             |
        web backends
```

nginx therefore remains the single HTTP routing layer even though Xray owns public TCP/443.

Hysteria2 independently owns UDP/443 and serves/uses the same plausible public content family for masquerade.

### 4.3 TLS / certificate model

- ACME is a property of the host ingress layer, not a separate platform service.
- Use HTTP-01 through nginx on TCP/80 unless a later concrete requirement makes DNS-01 materially simpler.
- Maintain one certificate/SAN set covering `escloud.us` and all active public service hostnames needed behind the Xray TLS front end; mail may use the same certificate where appropriate.
- Xray, Hysteria2, nginx-dependent flows and Stalwart receive the certificate through their native host/bind-mount mechanisms.
- Renewal must reload/restart only consumers that actually require it and must have a post-renewal verification gate.
- Do not pin certificates or restore legacy certificate files when fresh ACME issuance is possible; preserved TLS material is recovery input only.

### 4.4 Target domain map

| Hostname | Role | Human auth boundary |
| --- | --- | --- |
| `escloud.us` | Public plausible/decoy root used by ordinary HTTPS and VPN masquerade. | Public; no operational data. |
| `edge.escloud.us` | Node identity / SSH DNS name; HTTP may redirect to root. | Not an application portal. |
| `auth.escloud.us` | Authelia. | Authelia itself. |
| `app.escloud.us` | Private Cloud Infrastructure portal/status landing page. | Authelia. |
| `go.escloud.us` | n8n editor/UI. | Authelia plus native n8n auth where upstream requires it. |
| `hooks.escloud.us` | Public n8n webhook/event ingress. | No interactive Authelia; endpoint-specific secret/signature semantics. |
| `mail.escloud.us` | Bulwark webmail + required Stalwart JMAP/discovery/account routes. | Native mail/application auth. |
| `work.escloud.us` | CloudCLI workspace UI. | Authelia plus native auth if the application requires it. |
| `files.escloud.us` | SFTPGo WebClient; WebDAV may be routed under an explicit DAV path. | OIDC/Authelia for browser UI; SFTPGo native auth for DAV/native protocols. |
| `sync.escloud.us` | Self-hosted LiveSync CouchDB endpoint. | CouchDB/LiveSync credentials, not Authelia. |
| `ops.escloud.us` | Semaphore. | Authelia OIDC where validated; retain local fallback only if required operationally. |
| `backup.escloud.us` | Backrest WebUI. | Authelia; native auth retained only if required. |
| `status.escloud.us` | Uptime Kuma UI/status surface. | Authelia for the operational UI; exact push paths may bypass it using push tokens. |
| `maint.escloud.us` | Minimal maintenance page served directly by nginx. | May remain public-safe/unauthenticated so it still works when application auth is under maintenance; it must contain no sensitive operational data. |

Legacy names such as `docs.escloud.us`, `code.escloud.us`, `chat.escloud.us`, or the old meaning of `cloud.escloud.us` are not carried forward merely because they existed.

### 4.5 DNS contract

- Public authoritative DNS remains external; `edge` does not become an authoritative or recursive DNS server.
- Active web/service hostnames receive A/AAAA records pointing at the accepted `edge` public addresses.
- `MX` for the mail domain points to `mail.escloud.us`.
- SPF, DKIM, DMARC and provider PTR/rDNS are treated as part of the Stalwart mail deployment and must be verified before mail acceptance.
- Do not change historical mail DNS blindly; audit live authoritative DNS before cutover.

---

## 5. Authentication boundaries

Authelia is the common **human web-login** layer, not a universal replacement for every application/protocol credential.

### 5.1 Authelia contract

- Keep the simple file-backed single-operator identity model unless a real need for an external identity directory appears.
- Use Authelia as an OIDC provider where the target application supports OIDC correctly.
- Otherwise use nginx/Authelia forward-auth for ordinary browser applications where that trust model is supported.
- Keep native application authentication when the application cannot safely delegate it.
- Do not create a blanket `^/api/.*$` authentication bypass as in the legacy reference.

### 5.2 Required non-Authelia authentication

- Xray: VLESS client identity.
- Hysteria2: native Hysteria2 authentication.
- SSH: public keys.
- SMTP/IMAP/JMAP/mailbox operations: Stalwart/native mail credentials and application semantics.
- SFTP/WebDAV: SFTPGo native credentials/SSH keys where applicable; OIDC is for browser sessions.
- Obsidian LiveSync: CouchDB/LiveSync credentials; optionally LiveSync E2EE on the client layer.
- NetBird: NetBird peer identity.
- machine webhooks/APIs: endpoint-specific tokens, signatures, or application credentials.

### 5.3 Explicit unauthenticated/bypass surfaces

Only narrowly defined machine/public endpoints may bypass Authelia, including:

- ACME challenge paths;
- `hooks.escloud.us` webhook routes designed to be public receivers;
- Uptime Kuma push endpoint paths containing their own push tokens;
- protocol discovery paths that must be public for a supported client and are safe to expose;
- the public decoy and public-safe maintenance pages.

Every bypass is exact-host/path scoped. There is no generic `/api` bypass.

---

## 6. File, workspace and synchronization architecture

### 6.1 Working-file service: SFTPGo

Select **SFTPGo Open Source** as the target VPS working-file layer instead of restoring Filestash.

Its role is to provide one consistent view over selected `edge` working data through:

- HTTPS WebClient for browser/iPhone/iPad access;
- WebDAV where a mounted/client filesystem interface is useful;
- SFTP for `ai-node`, MacBook or administrative transfer where appropriate;
- one application permission model over the same underlying files.

Browser WebClient authentication should use Authelia/OIDC after validation. Native SFTP/WebDAV continue to use SFTPGo-native credentials because interactive OIDC cannot replace those protocols.

Initial native SFTP exposure should be private-only after the NetBird gate passes (for example, a non-SSH-system port bound to the NetBird address). Do not take TCP/22 away from OpenSSH.

### 6.2 Shared workspace

`/srv/edge/workspace` is the common user/agent working-data root for:

- CloudCLI/Codex/Antigravity host workflows;
- n8n file-based workflow payloads;
- SFTPGo user access;
- selected ingestion/output flows.

It is **working data**, not application state and not the Obsidian canonical vault.

Recommended logical subtrees:

```text
/srv/edge/workspace/
├── inbox/
├── jobs/
├── projects/
├── shared/
└── outbox/
```

Exact ownership/UID mapping is established during deployment after the runtime users are known. Do not make the tree world-writable merely to avoid UID/GID design.

### 6.3 General file synchronization: Syncthing

Select Syncthing only for **explicitly chosen non-Obsidian machine-to-machine directories**, primarily `edge ↔ ai-node` working data that genuinely benefits from continuous bidirectional synchronization.

- Do not sync all `/srv/edge` application state.
- Do not use Syncthing as the task-execution protocol merely because files are involved.
- Keep its administrative UI loopback/private.
- Prefer direct/private peer addressing after the NetBird path is accepted; normal Syncthing transport remains a fallback implementation detail if required.

### 6.4 Obsidian synchronization: Self-hosted LiveSync + CouchDB

Select **Self-hosted LiveSync with CouchDB on `edge`** as the single primary Obsidian synchronization mechanism.

Contract:

- canonical filesystem vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`;
- `edge` CouchDB is a synchronization/replication endpoint, not the canonical knowledge source;
- MacBook, iPhone, iPad and the `ai-node` Obsidian client use the same LiveSync endpoint at `sync.escloud.us`;
- do not combine LiveSync and Syncthing as simultaneous primary sync mechanisms for this vault;
- CouchDB data is backed up, but it does not replace the independent backup of the canonical vault on PAI;
- block/avoid exposing CouchDB administrative UI paths that clients do not require.

---

## 7. `edge ↔ Home/PAI` connectivity contract

### 7.1 Separation of functions

The Xray/Hysteria2 foreign-egress function is independent from private infrastructure connectivity. Do not route private Home/PAI integration through the user-facing DPI-bypass stack merely because it already exists.

### 7.2 Preferred private overlay: NetBird, gated by real-path acceptance

NetBird is the preferred private-overlay implementation because it can provide direct peer connectivity and, when needed, resource/network routing. However, existing project rules require empirical Russia ↔ external-VPS validation before it becomes an accepted dependency.

Therefore the Architecture Contract accepts the following **gate**, not an untested assumption:

1. after this Architecture Contract is accepted, install/join the NetBird client on `edge` as a dedicated connectivity test step;
2. verify direct and relayed operation, reconnect behavior, latency/throughput sufficient for the intended flows, and survival of the real DPI path;
3. only after PASS may services bind private endpoints to NetBird or depend on it;
4. if it fails, do not stack another overlay product automatically — use the application-layer durable HTTPS/pull model below and reopen private-transport selection only for flows that truly require it.

For current NetBird deployments, prefer the actively developed **Networks** model over deprecated Routes for new routed resources. Do not advertise or bridge the whole Home LAN by default: direct NetBird peers are preferred for `edge`, `ai-node` and other capable hosts, and routed resources are added only for actual non-peer Home endpoints.

`edge` is not a default route for Home and is not a general public gateway into Home services.

### 7.3 Durable orchestration is transport-independent

Cross-site automation must remain correct even when Home/PAI or the private overlay is temporarily unavailable.

The baseline store-and-forward model is:

```text
Internet/user event
      |
      v
     n8n  -- persist execution/job state
      |
      +-- stage large payload in /srv/edge/workspace/jobs/<job-id>/
      |
      +-- attempt delivery/invocation over accepted private HTTPS/API path
      |
      +-- retry/resume later if destination is unavailable
      |
      +-- receive/poll status + result
```

Rules:

- every durable cross-site job receives a workflow/job identifier;
- n8n persistent execution state is the default queue/state primitive;
- large payloads are staged in the workspace instead of embedded indefinitely in workflow metadata;
- retries must be safe through idempotency or workflow-specific duplicate protection;
- success/failure must be observable;
- no RabbitMQ, Kafka, NATS, Redis queue, or separate message broker is introduced unless n8n persistence proves insufficient for a concrete flow;
- if inbound reachability to Home/PAI is undesirable or unavailable, Home/PAI may poll/claim work from `edge` over ordinary outbound HTTPS instead of exposing a new public Home endpoint.

This makes reliable orchestration independent of whether NetBird uses direct WireGuard, relay transport, or is temporarily unavailable.

---

## 8. Service-to-service interaction contract

| Producer / client | Consumer | Path / rule |
| --- | --- | --- |
| Browser/device | web applications | TCP/443 → Xray fallback → nginx → Authelia/OIDC/native auth as defined above. |
| Xray clients | Internet | Xray direct outbound. |
| Hysteria2 clients | Internet | Hysteria2 direct outbound. |
| n8n | Stalwart | SMTP/application protocol for system mail and mail-trigger workflows. |
| Stalwart | n8n | inbound mail processing through supported mail/API/workflow integration, not direct database access. |
| n8n | CloudCLI/Codex/Antigravity | SSH to host `core`; no Docker socket and no legacy custom runner API by default. |
| n8n | working files | bind-mounted `/srv/edge/workspace` subtree needed by workflows. |
| SFTPGo | working files | `/srv/edge/workspace` only; no access to arbitrary app-state trees. |
| Syncthing | `ai-node` | selected working-data directories only. |
| Obsidian clients | CouchDB | HTTPS `sync.escloud.us`; native LiveSync/CouchDB auth. |
| n8n | Home/PAI workflows | NetBird/private HTTPS after gate PASS, with persisted retry; outbound-pull fallback where appropriate. |
| Uptime Kuma | Home/PAI/public endpoints | active checks plus push/dead-man heartbeats. |
| Home/PVE/PAI | Uptime Kuma | tokenized push heartbeat endpoints; operational UI remains authenticated. |
| Backrest/Restic | remote backup repository | encrypted Restic repository in a separate failure domain. |
| Semaphore | maintenance targets | operator-triggered maintenance/update tasks; does not become the generic event automation engine. |
| Cloud portal | operations surfaces | links/status presentation only; it is not a second scheduler or monitoring database. |

Direct cross-application database access is not part of the architecture.

---

## 9. Persistent storage layout

Use a small number of purpose-based roots rather than the legacy `/srv/ai-workspace` tree:

```text
/opt/edge/
├── stacks/               # Compose definitions and deployment manifests
├── scripts/              # persistent project scripts/runbooks
└── portal/               # static portal/maintenance source assets

/etc/edge/
├── env/                  # host-local non-secret environment/config fragments
└── secrets/              # root-controlled secret files; never Git

/srv/edge/
├── state/                # persistent application state by service
│   ├── authelia/
│   ├── n8n/
│   ├── mail/
│   ├── sftpgo/
│   ├── livesync/
│   ├── syncthing/
│   ├── backrest/
│   ├── semaphore/
│   └── uptime-kuma/
├── workspace/            # user/agent working data
└── public/               # public-safe static decoy/maintenance content
```

Principles:

- package-managed host services may continue using their normal upstream `/etc`, `/var/lib` and `/var/log` paths where relocation adds no value;
- `/opt/edge` contains deployable non-secret definitions, not live databases;
- `/etc/edge/secrets` is excluded from Git and included in encrypted backup;
- `/srv/edge/state` is service state and is never casually synchronized between hosts;
- `/srv/edge/workspace` is the intentional cross-service working-data surface;
- subscription CLI state remains in `/home/core` where the tools expect a real HOME; only verified necessary auth/config subtrees are included in backup;
- caches, downloaded package layers and reproducible temporary data are excluded from backup;
- temporary/test artifacts use `/tmp` unless they intentionally become persistent project state.

---

## 10. Backup and disaster-recovery topology

### 10.1 Backup roles

Backrest is the `edge` backup management plane and Restic is the backup engine.

The final DR topology has three distinct sources of recovery truth:

1. **GitHub project repository** — architecture, decisions, non-secret deployment definitions and runbooks.
2. **Remote encrypted Restic repository in Home Infrastructure** — primary ongoing off-site application/configuration backup for `edge` after the private transport/endpoint is verified.
3. **Provider-level whole-VPS backup** — independent image-level rollback/recovery path.

The existing external Stage 0 migration archive remains preserved legacy/selective-recovery material; it is not the ongoing backup mechanism for the rebuilt node.

A Restic repository stored only on the `edge` root filesystem does **not** satisfy DR and must not be described as the primary backup.

### 10.2 Backup scope

At minimum include:

- host target configuration that is not trivially reconstructed from Git;
- `/etc/edge`, including encrypted-at-rest-in-Restic secret files;
- persistent `/srv/edge/state` required for accepted services;
- selected `/home/core` auth/config state required to restore subscription tooling;
- `/srv/edge/workspace` according to explicit inclusion/retention rules.

Use service-aware quiesce/export/snapshot hooks where a live database cannot be backed up consistently as ordinary files. A successful Restic command alone is not restore acceptance.

### 10.3 Restore order

1. clean accepted Ubuntu substrate;
2. host networking/SSH/runtime foundation;
3. nginx + TLS + Xray/Hysteria2;
4. Authelia and basic portal;
5. remote backup access and Backrest;
6. mail;
7. n8n and cloud-AI subscription tooling;
8. file/sync/Obsidian services;
9. operations/monitoring integrations;
10. Home/PAI orchestration.

Restores must be verified by application-level acceptance, not only file presence.

### 10.4 Reverse backup role

`edge` is **not** initially a general-purpose backup target for Home/PBS/PAI. Selected small, high-value Home/PAI off-site copies may be added later only with an explicit capacity/retention decision. Avoid circular backup topology in which each side is the other's only copy.

---

## 11. Monitoring and operations contract

### 11.1 Monitoring

Select **Uptime Kuma** as the lightweight Cloud monitoring/dead-man layer.

Use it for:

- public HTTP/TCP availability checks;
- selected mail/VPN/application health checks;
- push/dead-man heartbeats from PVE/Home/PAI;
- selected backup/job-health signals;
- notifications;
- status presentation linked from the private Cloud portal.

`edge` primarily provides an external failure-domain view of Home/PAI. Total `edge` failure itself should be observed from Home/existing external mechanisms; an application running on `edge` cannot prove that its own host is down.

Do not deploy Prometheus, Grafana, Loki, Elasticsearch or full central log replication without a concrete requirement.

### 11.2 Logs

- host services use journald/syslog-compatible upstream mechanisms;
- accepted journald cap remains `500M`;
- Docker services use bounded local log rotation;
- application logs remain local unless a real troubleshooting/retention requirement justifies export.

### 11.3 Operational ownership

- **systemd / Docker Compose:** service lifecycle;
- **Semaphore:** operator-triggered infrastructure maintenance/update procedures;
- **n8n:** event/schedule/business/agent automation;
- **Backrest:** backup orchestration;
- **Uptime Kuma:** availability/heartbeat state;
- **Cloud portal:** presentation/navigation only.

Do not recreate the legacy custom Maintenance Center, a second scheduler, or custom Docker-control API.

The static maintenance page must remain servable directly by nginx even if n8n, portal integrations or most containers are stopped.

---

## 12. Deployment sequence after Architecture Contract acceptance

Every stage follows relevant inspection → mutation → verification. A later stage must not be used to hide an incomplete acceptance in an earlier one.

### Stage 1 — Runtime foundation

- fresh read-only substrate audit;
- install current stable Docker Engine + Compose plugin because accepted target applications require containers;
- create/verify `core` and required service paths;
- create `/opt/edge`, `/etc/edge`, `/srv/edge` contract roots;
- establish explicit public-listener/firewall baseline;
- verify no substrate regression.

### Stage 2 — Public edge / TLS / VPN coexistence

- audit authoritative DNS first;
- establish ACME/SAN certificate lifecycle;
- deploy nginx host ingress and public-safe decoy;
- deploy Xray TCP/443 with ordinary-HTTPS fallback to nginx;
- deploy Hysteria2 UDP/443 with masquerade;
- verify IPv4/IPv6, HTTPS virtual hosts, VLESS and Hysteria2 independently and concurrently.

### Stage 3 — Identity and portal foundation

- deploy Authelia;
- enable the required OIDC-provider function;
- deploy static `app.escloud.us` portal skeleton and `maint.escloud.us` maintenance page;
- establish exact host/path auth rules with no generic API bypass;
- verify session/login/redirect behavior.

### Stage 4 — Private-connectivity acceptance gate

- install/join NetBird on `edge` only after the contract is accepted;
- test the actual Russia ↔ `edge` path, including direct and relay behavior and reconnects;
- record `PASS` or reopen private-transport selection;
- no later component may silently depend on NetBird if this gate fails.

### Stage 5 — Backup foundation

- deploy Backrest;
- establish the remote Home Infrastructure Restic repository over the accepted transport;
- back up the current base/ingress/auth state;
- perform a bounded restore/read-back test before adding major stateful services.

### Stage 6 — Mail

- deploy Stalwart + Bulwark from clean manifests;
- restore only required preserved mail state/configuration/credentials from the recovery plane;
- validate MX/PTR/SPF/DKIM/DMARC and SMTP/submission/IMAP/JMAP/webmail behavior;
- verify backup/restore hooks for mail state.

### Stage 7 — Automation and cloud-AI workspace

- deploy n8n in Docker;
- deploy CloudCLI/Codex/Antigravity under host user `core`;
- restore only required preserved subscription/auth state;
- implement n8n→`core` execution through SSH rather than the legacy custom runner API;
- verify webhook ingress, scheduled workflows, mail transport and long-running CLI workflows.

### Stage 8 — Operations and external monitoring

- deploy Semaphore and Uptime Kuma;
- complete maintenance page/Semaphore workflow split;
- add Home/PVE/PAI push heartbeats and critical public checks;
- integrate links/status into the Cloud portal;
- verify notification paths.

### Stage 9 — Files, working sync and Obsidian

- deploy SFTPGo and bind it only to `/srv/edge/workspace`/explicit shares;
- deploy Syncthing for approved non-Obsidian directories only;
- deploy CouchDB for Self-hosted LiveSync;
- migrate Obsidian clients to LiveSync as the single primary sync mechanism while retaining the `ai-node` filesystem vault as canonical;
- verify file access from MacBook/iPhone/iPad/`ai-node`, conflict behavior and backups.

### Stage 10 — Durable Home/PAI workflows

- implement concrete `edge ↔ Home/PAI` flows only after their producers/consumers exist;
- persist n8n job state and stage large payloads in the workspace;
- add retry/idempotency/result-state semantics;
- use NetBird/private APIs when the Stage 4 gate passed; use Home/PAI outbound polling/claiming where that is more reliable or simpler;
- validate destination-offline/recovery cases explicitly.

### Stage 11 — Final production acceptance

- listener/public-exposure audit;
- authentication-boundary audit;
- service health and reboot persistence;
- backup + bounded restore acceptance;
- cross-site failure/retry test;
- production non-regression check;
- update `CURRENT_STATE.md`, `DECISIONS.md`, `INVENTORY.md` and this architecture document to accepted runtime facts.

---

## 13. Explicit non-goals / rejected carry-forward patterns

The target does **not** include by default:

- restoration of the legacy monolithic core Compose stack;
- Homepage;
- custom Maintenance Center;
- legacy custom Codex runner API;
- Docker socket proxy for portal/monitoring;
- public exposure of arbitrary container ports;
- a dedicated message broker;
- PostgreSQL/Redis for n8n without demonstrated need;
- full Prometheus/Grafana/Loki stack;
- a second authoritative DNS/recursive DNS plane;
- general public gateway/proxy access from Internet to Home services;
- a general Home/PBS backup mirror on `edge`;
- Syncthing as the Obsidian primary sync mechanism;
- paid Obsidian Sync;
- generic `/api` authentication bypasses;
- package/version/digest pinning solely for reproducibility when upstream stable update paths are appropriate.

---

## 14. Acceptance boundary

This document becomes the **ACCEPTED Edge Architecture Contract** only after explicit user acceptance.

Acceptance authorizes implementation of the architecture in the staged order above, not arbitrary redesign. The NetBird private-transport choice remains deliberately conditional on the mandatory real-path test; accepting this contract accepts that test gate and fallback model, not an unverified claim that NetBird already works on the required path.

Until that explicit acceptance, the live runtime remains the accepted clean Ubuntu substrate plus minimal base bootstrap only.
