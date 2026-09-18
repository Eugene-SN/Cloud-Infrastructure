# Stage 04 — Mattermost Deep Research Brief — 2026-09-18

**Status:** RESEARCH COMPLETE / TARGET ARCHITECTURE ACCEPTED / DEPLOYMENT NOT STARTED

Final design acceptance:

`STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`

## Purpose

Research deployment and integration options for a lightweight private Mattermost collaboration/control surface in Stage 4, with emphasis on reliable long-term operation, native clients, Hermes/n8n integration, low maintenance overhead and no unnecessary enterprise components.

## Research findings retained

- Mattermost Team Edition is the selected free/self-hosted edition.
- Small private deployments are a good fit for the official Docker pattern with a dedicated PostgreSQL service.
- The official Preview all-in-one image includes its own database but is an evaluation image and is not the target for persistent production use.
- Existing host Xray/nginx/shared TLS makes Mattermost's optional bundled nginx unnecessary.
- Mattermost native mobile/desktop clients rely on Mattermost API/WebSocket behavior; an interactive forward-auth proxy in front of the whole service is a poor fit.
- Mattermost's dedicated pre-authentication-secret mechanism is a separate commercial feature and is not the baseline for Team Edition.
- The free Mattermost Test Push Notification Service (TPNS) can deliver push notifications to the official iOS/Android Mattermost applications connected to a self-hosted server, but it has no production SLA.
- Calls has separate media/network requirements and is explicitly out of current scope.
- For this scale there is no current justification for Kubernetes, HA, Elasticsearch/OpenSearch, Redis, MinIO/S3, a custom push proxy or custom mobile builds.

## Accepted target topology

- Mattermost Team Edition;
- current official Mattermost Docker Compose pattern;
- separate Mattermost and dedicated PostgreSQL containers;
- local persistent `/srv` state;
- existing host Xray -> nginx -> shared TLS;
- `https://chat.escloud.us` as the human endpoint;
- no Authelia in front of Mattermost;
- Mattermost-native authentication for clients;
- Mattermost backend and PostgreSQL remain private;
- free TPNS enabled for official mobile clients;
- Calls disabled for the current stage.

## Integration research

Research confirmed multiple upstream/native integration surfaces:

- Hermes has Mattermost integration support;
- n8n has an official Mattermost integration surface, including its documented Mattermost integration page/node;
- Mattermost exposes documented REST API, WebSocket, webhooks and slash-command mechanisms;
- SMTP is a standard Mattermost integration surface for mail delivery.

These findings **do not preselect the exact per-service integration mechanism**.

### Accepted integration-selection rule

During Stage 4E, for every service-to-Mattermost connection:

1. enumerate all current native/upstream-supported mechanisms available in the deployed versions;
2. compare them for reliability, simplicity, lifecycle/update compatibility and operational coupling;
3. select the most native/direct supported option that satisfies the actual use case;
4. avoid custom plugins, patched source, shim services, direct database coupling or bespoke bridges unless native options are proven insufficient and the operator explicitly accepts the exception.

Examples such as Hermes native Mattermost support, the n8n Mattermost node, Mattermost webhooks/slash commands or SMTP remain **candidate mechanisms**, not fixed implementation decisions in this research record.

## Public ingress decision

`chat.escloud.us` is an explicit exception to the normal Cloud Infrastructure service-subdomain Authelia rule:

```text
Internet
  -> Xray
  -> host nginx + shared TLS
  -> chat.escloud.us
  -> Mattermost native authentication
  -> private Mattermost backend
```

Authelia is not inserted in front of Mattermost.

## Push decision

Use Mattermost Test Push Notification Service (TPNS) with the official Mattermost mobile applications. This allows push delivery for the self-hosted Mattermost server without a custom push proxy or custom mobile build. Lack of production SLA is accepted for this private deployment.

## Calls decision

Mattermost Calls is not required at this stage and is excluded from deployment/acceptance. Do not open Calls-specific TCP/UDP ports, deploy TURN, or add Calls media components.

## Remaining deployment-time audit items

These are implementation details, not open architecture questions:

- fresh `edge` CPU/RAM/storage headroom;
- current stable Mattermost/Team image tags at deployment time;
- exact Compose files/environment values based on current upstream;
- exact `/srv` paths and ownership;
- exact loopback/private backend binding;
- PostgreSQL credentials and lifecycle;
- nginx WebSocket proxy details;
- TPNS configuration;
- exact initial Mattermost account/team/channel state needed for acceptance;
- native integration mechanism selection per connected service;
- resource delta, persistence and reboot/non-regression verification.

## Source set used during research

- Mattermost server releases and licensing documentation;
- Mattermost deployment/container/PostgreSQL/file-storage documentation;
- Mattermost mobile/push/TPNS documentation;
- Mattermost integration/API/webhook/slash-command documentation;
- Mattermost community forum and user deployment discussions;
- Hermes Mattermost integration documentation/source;
- n8n official Mattermost integration documentation/source.

## Research closure

Stage 4D is complete. The accepted target is recorded in:

`STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

No Mattermost runtime mutation has been performed yet.
