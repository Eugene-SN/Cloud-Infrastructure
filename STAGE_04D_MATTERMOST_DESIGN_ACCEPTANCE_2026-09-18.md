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

The target requires Mattermost to integrate with Hermes, n8n, Stalwart and other useful `edge` services, but **the exact integration mechanism for each service is intentionally not frozen at Stage 4D**.

During Stage 4E:

1. inspect all currently supported upstream/native integration mechanisms available in the deployed versions of both sides;
2. prefer the most direct vendor/upstream-supported mechanism with the least operational coupling and no unnecessary intermediary;
3. compare native nodes/adapters, official APIs, webhooks, slash commands, SMTP or other documented interfaces as applicable;
4. use custom plugins, source patches, shim services, direct database access or bespoke bridges only if every practical native/upstream-supported mechanism has a demonstrated incompatibility and the operator explicitly accepts the exception;
5. do not encode speculative future workflows into the infrastructure deployment.

Known native integration surfaces discovered during research include Hermes' Mattermost support, n8n's official Mattermost integration surface, Mattermost's documented API/webhook/slash-command mechanisms, and standard SMTP. These are **candidates/evidence of native support, not preselected per-direction implementation decisions**.

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

Service integrations remain native-first and are selected/verified during Stage 4E rather than hard-coded by this design record.

## Stage effect

- Stage 4D research/design gate: **COMPLETE / ACCEPTED**.
- Stage 4E deployment/integration: **NOT STARTED**.
- No Mattermost runtime mutation has been performed by Stage 4D.

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`
