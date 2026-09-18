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

Research confirmed first-party/native Mattermost integration paths that are now fixed for the current project:

- **Hermes ↔ Mattermost:** Hermes' built-in Mattermost gateway adapter using Mattermost REST API v4 + WebSocket;
- **n8n → Mattermost:** n8n's official built-in Mattermost integration/node for the operations it supports;
- **Mattermost → Stalwart:** Mattermost's documented SMTP integration using the existing Stalwart SMTP service.

### Accepted native-only rule

For every other service or direction:

1. verify whether the current upstream/developers explicitly provide a Mattermost integration or an explicitly supported standard protocol counterpart;
2. if yes, document and implement that supported path in the owning project stage;
3. if no, leave the service unintegrated with Mattermost in the current Cloud Infrastructure project;
4. do not manufacture the missing integration using custom plugins, patches, shim services, direct database access, bespoke bridges, compatibility hacks, or an n8n relay solely to connect products;
5. unsupported integrations may be reconsidered only as separate future work outside the current project.

Mattermost APIs/webhooks/slash commands remain valid native primitives, but they do not by themselves authorize a custom bridge to another product whose developers do not provide a supported Mattermost-facing counterpart.

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
- native-integration availability audit for every relevant service/direction; implement only confirmed upstream-supported paths;
- resource delta, persistence and reboot/non-regression verification.

## Source set used during research

- Mattermost server releases and licensing documentation;
- Mattermost deployment/container/PostgreSQL/file-storage documentation;
- Mattermost mobile/push/TPNS documentation;
- Mattermost Integrations Guide (`https://docs.mattermost.com/integrations-guide/integrations-guide-index`) and linked official API/webhook/slash-command/no-code documentation;
- Mattermost official container deployment guide (`https://docs.mattermost.com/deployment-guide/server/deploy-containers`) and current `mattermost/docker` deployment files;
- Mattermost community forum and user deployment discussions;
- Hermes official Mattermost setup guide (`https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost`) plus current Hermes adapter/source;
- n8n official Mattermost integration page (`https://n8n.io/integrations/mattermost/`) and built-in Mattermost node documentation/source.

## Research closure

Stage 4D is complete. The accepted target is recorded in:

`STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

No Mattermost runtime mutation has been performed yet.
