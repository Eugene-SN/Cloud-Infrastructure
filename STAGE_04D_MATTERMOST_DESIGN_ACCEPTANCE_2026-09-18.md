# Stage 04D — Mattermost Target Architecture Acceptance — 2026-09-18

**Status:** ACCEPTED / DESIGN GATE COMPLETE / DEPLOYMENT NOT STARTED

## Accepted target

Stage 4D research/design is complete. The accepted Mattermost target for `edge` is:

- **Mattermost Team Edition**;
- deployment based on the current **official Mattermost Docker Compose pattern**;
- separate Mattermost application and dedicated PostgreSQL containers; do not use the Preview all-in-one image;
- no bundled Mattermost nginx container because Cloud Infrastructure already has the accepted host Xray -> nginx -> shared TLS ingress;
- human URL: `https://chat.escloud.us`;
- **no Authelia in front of Mattermost**; `chat.escloud.us` is an explicit exception to the normal service-subdomain Authelia rule because native Mattermost web/desktop/mobile clients and API/WebSocket flows must use Mattermost-native authentication without an interactive forward-auth layer;
- Mattermost application backend remains non-public and is exposed only through the existing host reverse proxy;
- PostgreSQL remains private and is never published as a public listener;
- persistent Mattermost/PostgreSQL state uses local `/srv` storage on `edge`; exact paths are selected in the deployment contract after the fresh runtime audit;
- enable the free Mattermost **Test Push Notification Service (TPNS)** for the official Mattermost mobile applications; the service is accepted for this private installation despite its lack of production SLA;
- **Mattermost Calls is excluded from the current Stage 4 scope by explicit operator decision**; no Calls media service, TURN, or additional Calls UDP/TCP listener is deployed;
- no Kubernetes, HA cluster, Elasticsearch/OpenSearch, Redis, MinIO/S3, custom push proxy, custom mobile build, or custom Mattermost plugin without a later concrete requirement.

## Integration-selection policy

Mattermost integration follows a **native-only current-project rule**.

For every service already deployed or selected in Cloud Infrastructure:

1. first determine whether the service developers/upstream explicitly provide a Mattermost integration or a standard protocol integration that Mattermost explicitly supports;
2. if such a first-party/upstream-supported integration exists, select it, document it in the project and verify it during the owning deployment stage;
3. if no such native/upstream-supported integration exists, **do not build a substitute integration in the current project**;
4. specifically, do not introduce custom plugins, source patches, shim services, direct database coupling, bespoke bridges, compatibility hacks, or an n8n-mediated bridge merely to claim that two products are integrated;
5. an integration absent from upstream support may be revisited only as a separate future task outside the current Cloud Infrastructure build.

Confirmed native integrations at Stage 4D:

- **Hermes ↔ Mattermost:** fixed to Hermes' built-in Mattermost gateway adapter using Mattermost REST API v4 + WebSocket;
  Canonical implementation source: `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost` (use the installed Hermes version/source to verify exact option names at deployment time).
- **n8n → Mattermost:** fixed to n8n's official built-in Mattermost integration/node for the operations it natively supports;
- **Mattermost → mail:** fixed to Mattermost's standard SMTP integration using the existing Stalwart SMTP service.

For any additional direction or product, Stage 4E must verify current upstream support before enabling it. Generic Mattermost APIs/webhooks/slash commands are not automatically treated as permission to build a custom cross-product bridge; they are used only where the other product also provides an explicit supported counterpart for the actual use case.

## Accepted ingress shape

```text
INTERNET
   |
 TCP/443
   |
 Xray
   |
 host nginx + shared TLS
   |
 https://chat.escloud.us
   |
 NO AUTHELIA
   |
 Mattermost native authentication
   |
 private Mattermost backend
   |
 Docker Compose
   |-- Mattermost Team
   `-- dedicated PostgreSQL
```

Only confirmed native/upstream-supported integrations are implemented in the current project. Unsupported cross-product integrations are deferred outside the current Cloud Infrastructure build.

## Stage effect

- Stage 4D research/design gate: **COMPLETE / ACCEPTED**.
- Stage 4E deployment/integration: **NOT STARTED**.
- No Mattermost runtime mutation has been performed by Stage 4D.

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`
