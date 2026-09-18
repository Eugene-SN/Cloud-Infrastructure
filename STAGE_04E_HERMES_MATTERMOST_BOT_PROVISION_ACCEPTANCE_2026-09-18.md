# Stage 04E — Hermes ↔ Mattermost Bot Provisioning Acceptance — 2026-09-18

**Status:** ACCEPTED / E2E MESSAGE TEST PENDING

## Accepted provisioning state

- Mattermost bot username: `hermes`;
- Mattermost bot ID: `sceogxkhh3nh9y89uc6eza9ije`;
- bot owner: `eugene`;
- bot enabled;
- bot access token created and successfully validated against `/api/v4/users/me`;
- bot is a member of team `es-cloud`;
- bot is a member of bootstrap channel `town-square`;
- Hermes Mattermost environment configured under `/home/core/.hermes/.env`;
- `MATTERMOST_URL=https://chat.escloud.us`;
- `MATTERMOST_TOKEN` present;
- `MATTERMOST_ALLOWED_USERS=mof5mc6w3jds8qp36b678qrzoc`;
- Hermes gateway restarted and remains active;
- temporary mmctl admin credential was removed.

`STAGE4E_HERMES_MATTERMOST_BOT_PROVISION=PASS`

## Remaining acceptance gate

A real Mattermost message must traverse the full path:

`Mattermost -> Hermes gateway -> qwen3.8-27b-fp8/vLLM -> Hermes gateway -> Mattermost`

and return the requested response.

This E2E message test is the only remaining gate for the Hermes ↔ Mattermost integration acceptance.
