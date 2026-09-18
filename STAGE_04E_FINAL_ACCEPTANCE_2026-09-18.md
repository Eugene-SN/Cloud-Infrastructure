# Stage 04E — Mattermost Final Acceptance — 2026-09-18

**Status:** COMPLETE / ACCEPTED

## Scope

Stage 4E deployed and accepted the private Mattermost collaboration/control surface plus its supported native integrations required by the current Cloud Infrastructure architecture.

## Accepted runtime

Mattermost:

- Mattermost Team `11.11.0`;
- PostgreSQL `18-alpine`;
- official `mattermost/docker` deployment at commit `497414659ee7127677d2b91b44bb4f3ea9d14695`;
- application host binding only `127.0.0.1:18065 -> 8065`;
- PostgreSQL has no host publication;
- public endpoint `https://chat.escloud.us` through Xray -> host nginx -> shared TLS;
- Mattermost-native authentication; no Authelia;
- effective SiteURL `https://chat.escloud.us`;
- bot account creation enabled;
- public user creation disabled;
- TPNS configured at `https://push-test.mattermost.com`;
- Calls disabled;
- Mattermost↔Stalwart SMTP explicitly not required / not enabled;
- prepackaged Agents plugin `mattermost-ai` `2.6.1` remains installed but is explicitly disabled.

Hermes↔Mattermost:

- dedicated bot `hermes`, ID `sceogxkhh3nh9y89uc6eza9ije`;
- private service channel `hermes`, ID `6s6o3iftjprwfg5p4d1gg1bwho`;
- operator membership/allowlist accepted;
- real E2E response `HERMES_MATTERMOST_E2E_OK` passed.

n8n↔Mattermost:

- official n8n `2.39.7` built-in Mattermost node;
- exactly one production `mattermostApi` credential, ID `16a0a988ad514ab1`;
- dedicated bot `n8n`, ID `4ty8tfwmdir9mxkeua3n7658mc`;
- official native-node E2E marker `N8N_MATTERMOST_NATIVE_E2E_OK_20260918T135107Z`;
- production n8n remained at zero workflows and zero executions after the isolated acceptance probe.

Mobile/TPNS:

- the operator explicitly accepted the official iOS Mattermost/mobile TPNS gate as PASS;
- this acceptance is operator-observed rather than independently machine-observed in this branch.

## Final non-regression evidence

`STAGE4E_FINAL_NON_REGRESSION_V1` returned RC=0 and verified:

- Mattermost local health: PASS;
- Mattermost public health: PASS;
- PostgreSQL query: PASS;
- accepted Mattermost SiteURL/config: PASS;
- TPNS configuration: PASS;
- Agents disabled: PASS;
- Calls disabled: PASS;
- Hermes and n8n Mattermost identities/token counts: PASS;
- private Hermes service channel and memberships: PASS;
- n8n health: PASS;
- production n8n workflows: `0`;
- production n8n executions: `0`;
- production n8n Mattermost credentials: exactly `1`;
- Hermes gateway active: PASS;
- Hermes gateway enabled: PASS;
- Hermes gateway `NRestarts=0`.

## Acceptance markers

- `STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`;
- `STAGE4E_HERMES_MATTERMOST_BOT_PROVISION=PASS`;
- `STAGE4E_HERMES_MATTERMOST_CHANNEL_NORMALIZATION=PASS`;
- `STAGE4E_HERMES_MATTERMOST_E2E=PASS`;
- `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`;
- `STAGE4E_MATTERMOST_AGENTS_NORMALIZATION=PASS`;
- `STAGE4E_MATTERMOST_MOBILE_TPNS=PASS`;
- `STAGE4E_FINAL_NON_REGRESSION=PASS`;
- `STAGE4E_FINAL_ACCEPTANCE=PASS`.

Stage 4E is **COMPLETE / ACCEPTED**.

## Remaining Stage 4 work

Stage 4 itself remains IN PROGRESS.

Continue with:

1. remaining Stage 4A Hermes capability verification/normalization;
2. Stage 4B direct Codex/Antigravity executor integration;
3. Stage 4C Hermes Dashboard/ingress/auth;
4. Stage 4F private n8n machine interface and agent integration;
5. Stage 4G server-side integrated acceptance;
6. Stage 4H final macOS Hermes Desktop integration;
7. Stage 4I final Stage 4 acceptance/repository persistence.

The separately identified Hermes controlled-stop `SIGTERM -> exit 1` behavior is a known upstream bug and remains a Stage 4 lifecycle constraint to characterize at final server-side acceptance; no local masking patch is accepted.
