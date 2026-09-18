# Stage 04E — Mattermost Ingress Acceptance — 2026-09-18

**Status:** ACCEPTED

## Accepted ingress

Fresh runtime verification established:

- public URL: `https://chat.escloud.us`;
- private backend: `http://127.0.0.1:18065`;
- ingress path: public TCP/443 -> Xray -> host nginx -> Mattermost;
- nginx service vhost: `/etc/nginx/sites-available/chat-escloud-us.conf` enabled from `sites-enabled`;
- nginx config validation passed before and after deployment;
- public Mattermost API `/api/v4/system/ping` returns `status=OK`;
- public root returns Mattermost `11.11.0`;
- WebSocket handshake on `/api/v4/websocket` returns `101 Switching Protocols`;
- Authelia is not in front of Mattermost;
- no UFW mutation;
- no Xray mutation;
- existing n8n, CloudCLI and mail ingress remained non-regressed.

Accepted nginx vhost SHA256:
`6a4ba86be94c0c2bbcd6a62d5680aa8c8817c02ec36d4271f9dd9513d3a89b75`.

`STAGE4E_MATTERMOST_INGRESS_ACCEPTANCE=PASS`

## Next task

Complete native Mattermost application setup:

1. create the first workspace/account through the normal first-run web flow; the first account on a new Mattermost system becomes System Admin;
2. configure only the accepted native settings needed for this project;
3. verify official web/mobile client login and TPNS;
4. then create/configure the dedicated Hermes bot and proceed with the official Hermes Mattermost gateway integration.
