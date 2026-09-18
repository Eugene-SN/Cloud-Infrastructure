# Stage 04E — Mattermost Core Runtime Acceptance — 2026-09-18

**Status:** ACCEPTED

## Accepted runtime

Fresh runtime verification on `edge` established:

- official `mattermost/docker` deployment;
- upstream repository commit `497414659ee7127677d2b91b44bb4f3ea9d14695`;
- Mattermost Team Edition `11.11.0`;
- PostgreSQL `18-alpine`;
- `mattermost-mattermost-1` running and healthy;
- `mattermost-postgres-1` running;
- both containers use `restart=unless-stopped`;
- Mattermost host backend is loopback-only:
  `127.0.0.1:18065 -> container 8065/tcp`;
- no host publication on `8065`, `8443`, or `5432`;
- PostgreSQL has no host port binding;
- Mattermost Calls host publication is absent;
- Hermes gateway remains active/enabled;
- Hermes config SHA256 remains
  `c57ca6bc0b301250d4825060fcf5f8d90af94c7cee4f1632e0b648189fd994ae`.

The earlier verifier failures documented in the pre-deployment/recovery record were script errors or false negatives and do not invalidate the final V4 runtime acceptance.

`STAGE4E_MATTERMOST_CORE_RUNTIME_ACCEPTANCE=PASS`

## Next task

Expose the accepted private backend through the existing
`Xray -> host nginx -> shared TLS` ingress as
`https://chat.escloud.us`, without Authelia, following current official Mattermost reverse-proxy guidance and preserving the existing edge ingress contract.
