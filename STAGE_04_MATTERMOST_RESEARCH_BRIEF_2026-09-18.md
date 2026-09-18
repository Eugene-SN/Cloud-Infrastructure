# Stage 04 — Mattermost Deep Research Brief — 2026-09-18

**Status:** PRELIMINARY DEEP RESEARCH COMPLETE / DEPLOYMENT NOT STARTED / ARCHITECTURE ACCEPTANCE REQUIRED BEFORE MUTATION

## Purpose

Add a lightweight private Mattermost collaboration/control surface to Stage 4 and integrate it efficiently with Hermes, n8n and other compatible services already present on edge, without turning Mattermost into a second orchestration engine.

Mattermost itself is selected by operator requirement. Exact deployment method, network/auth details and integration topology remain subject to Stage 4D acceptance before any production mutation.

## Current upstream facts

- Current stable Mattermost Server release at research time: **11.11.0**, released 2026-09-16.
- Mattermost Team Edition remains available as the fully open-source MIT-licensed edition.
- Do not pin 11.11.0 as a project baseline. Deployment follows the project's normal latest-stable policy.
- Mattermost requires PostgreSQL 14+ for new deployments.
- Official small-host guidance starts at approximately 1 vCPU / 2 GB RAM; fresh edge headroom must still be audited immediately before deployment.
- Mattermost recommends single-team deployments for simpler integration behavior.
- PostgreSQL core search is intended for deployments below roughly 2–3 million posts/file entries, so Elasticsearch/OpenSearch is not justified by default for this private instance.
- Local file storage is technically supported for simple/single-node deployments. S3/MinIO/NFS is not automatically required.
- Mattermost current docs present Linux/APT as a normal production path while Docker quick-start/Compose is evaluation-oriented; official Team Edition container images exist. Stage 4D must explicitly compare supportability, cleanliness, update/backup behavior and resource overhead before selecting native APT vs official-image Compose.

## Intended role

- **Mattermost** — private collaboration/control/notification surface.
- **Hermes** — persistent agent runtime, reasoning, tools and delegation.
- **n8n** — deterministic orchestration.
- **Codex CLI / Antigravity CLI** — specialist executors delegated through Hermes by default.
- **CloudCLI** — manual cloud-AI workspace.
- **Stalwart** — existing mail subsystem and preferred SMTP source for Mattermost notifications/password resets.
- Later monitoring/maintenance/backup stages may deliver alerts/status into Mattermost, but those later workflows remain owned by their own stages.

## Hermes integration

Hermes upstream has a native Mattermost gateway adapter using Mattermost REST API v4 plus WebSocket real-time events. It supports DMs, channels, text, files, images, slash commands and proactive/home-channel delivery.

Target model:

1. enable Mattermost bot accounts;
2. create a dedicated Hermes bot account;
3. use the bot token instead of a human/System Admin token;
4. allow only the operator's Mattermost user ID by default;
5. keep mention requirements conservative in shared channels and enable free-response only where useful;
6. configure a Mattermost home channel for proactive Hermes delivery;
7. connect the host-native Hermes gateway to an internal Mattermost endpoint, not through public nginx + Authelia;
8. verify REST auth, WebSocket reconnect, DM, channel, attachment/image, slash-command and proactive-delivery behavior.

Relevant Hermes settings include MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_ALLOWED_USERS, MATTERMOST_ALLOWED_CHANNELS, MATTERMOST_HOME_CHANNEL, MATTERMOST_REQUIRE_MENTION, MATTERMOST_FREE_RESPONSE_CHANNELS and MATTERMOST_REPLY_MODE.

## n8n integration

n8n includes an official built-in Mattermost node supporting channel/user operations, normal and ephemeral posts, and reactions.

Preferred design:

- dedicated Mattermost bot/API credential in n8n;
- official Mattermost node for supported outbound/API actions;
- for Mattermost -> n8n inbound flows, prefer Mattermost outgoing webhooks or custom slash commands targeting n8n Webhook endpoints rather than adding a third-party Mattermost trigger node by default;
- use the Mattermost REST API through n8n HTTP Request only when the built-in node lacks a required operation;
- use an internal/private route from the n8n container to Mattermost rather than public Authelia-protected ingress.

Stage 4D must audit the current n8n Docker network and choose the simplest supported internal route without exposing a new public API port.

## Stalwart integration

Mattermost expects SMTP in a production-style deployment for password reset and notifications.

Target direction:

- reuse existing Stalwart;
- prefer a dedicated Mattermost sender identity/address;
- test SMTP connection, password-reset mail and notification delivery;
- do not deploy a second SMTP service.

Exact local/container SMTP route and credentials are decided from fresh runtime state after placement is selected.

## Public ingress and private machine paths

The project already has chat.escloud.us in the shared TLS SAN set and protected service namespace. It is therefore the preferred human-facing URL unless Stage 4D finds a concrete incompatibility.

Target contract:

- human UI: https://chat.escloud.us;
- reuse Xray -> nginx -> shared TLS -> Authelia;
- Mattermost application backend remains non-public;
- preserve WebSocket upgrade handling, especially /api/v4/websocket;
- Hermes and n8n use internal Mattermost URLs and native Mattermost credentials;
- no direct public PostgreSQL listener;
- no direct public Mattermost backend port.

### Mandatory auth/client compatibility research

Authelia forward-auth is simple for browsers, but native desktop/mobile clients can fail when a reverse proxy redirects API/WebSocket requests to an interactive browser login page. Mattermost's own pre-authentication-secret feature is Enterprise Advanced-only and is therefore not an assumed Team Edition solution.

Before deployment Stage 4D must explicitly research/test:

1. browser use of chat.escloud.us behind Authelia plus native Mattermost login;
2. Mattermost Desktop/mobile compatibility through the same ingress;
3. whether path-specific Authelia policy, native Mattermost auth on API/WebSocket paths, a NetBird-only client path, or another supported arrangement is required;
4. whether any exception to the project-wide service-subdomains-behind-Authelia rule is actually necessary.

No API/WebSocket bypass may be introduced silently.

## Lightweight topology principles

The target is small but not functionally crippled.

Do not add by assumption:

- Kubernetes;
- HA cluster;
- Elasticsearch/OpenSearch;
- Redis unless the selected current Mattermost architecture requires it;
- MinIO/S3 unless local storage proves inadequate;
- separate push proxy unless mobile push requirements justify it;
- Calls media stack / additional UDP listeners unless voice/video use is explicitly accepted;
- custom Mattermost plugins if native Hermes integration, REST API, n8n, webhooks and slash commands cover the requirement.

These are scale/feature-specific subsystems with independent operational cost, not ordinary features being stripped from Mattermost.

## Integration map to validate

Human -> chat.escloud.us -> Xray/nginx/TLS/Authelia -> Mattermost

Mattermost -> Stalwart SMTP

Mattermost <-> Hermes Gateway -> Qwen3.8/vLLM + Codex CLI + Antigravity CLI

Mattermost <-> n8n -> deterministic workflows and later integrations

## Required Stage 4D audit before deployment

1. fresh edge CPU/RAM/storage headroom;
2. current Mattermost stable release and Team Edition feature/licensing check;
3. native APT vs official-image Docker/Compose comparison;
4. PostgreSQL placement/version/lifecycle;
5. persistent data and local file-storage layout;
6. update path and later Stage 6 backup scope;
7. nginx WebSocket/proxy contract;
8. Authelia vs Mattermost web/desktop/mobile behavior;
9. internal Hermes -> Mattermost route;
10. internal n8n -> Mattermost route;
11. Stalwart SMTP route and sender identity;
12. bot/webhook/slash-command permission model;
13. initial team/channel model sufficient for infrastructure acceptance without user-specific workflows;
14. resource delta and reboot persistence.

## Preliminary authoritative sources

- Hermes Mattermost integration:
  https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/mattermost.md
- Hermes Messaging Gateway:
  https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/index.md
- Mattermost server releases:
  https://docs.mattermost.com/product-overview/mattermost-server-releases
- Mattermost Team Edition/version archive:
  https://docs.mattermost.com/product-overview/version-archive
- Mattermost licensing:
  https://docs.mattermost.com/product-overview/faq-license
- Mattermost requirements:
  https://docs.mattermost.com/deployment-guide/software-hardware-requirements
- Mattermost PostgreSQL:
  https://docs.mattermost.com/deployment-guide/server/prepare-database
- Mattermost file storage:
  https://docs.mattermost.com/deployment-guide/server/prepare-file-storage
- Mattermost integration/API:
  https://docs.mattermost.com/developers/integrate/getting-started
- Mattermost SMTP:
  https://docs.mattermost.com/administration-guide/configure/smtp-email
- n8n Mattermost node:
  https://github.com/n8n-io/n8n-docs/blob/main/docs/integrations/builtin/app-nodes/n8n-nodes-base.mattermost.md

## Research status

Mattermost product inclusion in Stage 4 is accepted.

Not yet accepted until Stage 4D closure:

- native vs container runtime;
- exact PostgreSQL placement;
- exact private backend/network topology;
- final Authelia/client compatibility pattern;
- exact SMTP route;
- exact initial channels;
- optional Calls/push/search/object-storage subsystems.

No Mattermost runtime mutation has been performed by this research record.
