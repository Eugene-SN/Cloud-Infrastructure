# Stage 04E — n8n ↔ Mattermost Integration Acceptance — 2026-09-18

**Status:** ACCEPTED

## Accepted runtime state

The native n8n -> Mattermost integration is operational using the official built-in n8n Mattermost node in n8n `2.39.7`.

Provisioning/authentication state:

- n8n version: `2.39.7`;
- built-in node type: `n8n-nodes-base.mattermost`, typeVersion `1`;
- credential type: `mattermostApi`;
- exactly one production Mattermost credential:
  - name: `Mattermost API - chat.escloud.us`;
  - ID: `16a0a988ad514ab1`;
- Mattermost bot username: `n8n`;
- Mattermost bot ID: `4ty8tfwmdir9mxkeua3n7658mc`;
- exactly one active Mattermost access token for the bot, description `n8n-native-mattermost`;
- credential API validation against `/api/v4/users/me`: HTTP 200;
- existing operator DM channel ID: `srzsm58fepgujjfnyxb8f7zo3o`.

## Native node E2E acceptance

A throwaway clone of the production n8n SQLite/config state was created under `/tmp` using SQLite online backup semantics so the production WAL-backed database remained untouched.

The throwaway workflow used:

- `n8n-nodes-base.manualTrigger`;
- official `n8n-nodes-base.mattermost` node;
- resource `message`;
- operation `post`;
- the existing production `mattermostApi` credential;
- the existing `eugene ↔ n8n` direct-message channel.

Execution succeeded.

Acceptance marker:

`N8N_MATTERMOST_NATIVE_E2E_OK_20260918T135107Z`

Mattermost database verification proved exactly one matching post:

- post ID: `1fgnm3fumbyy8b4usrrs41kouc`;
- author/user ID: `4ty8tfwmdir9mxkeua3n7658mc` (`n8n`);
- channel ID: `srzsm58fepgujjfnyxb8f7zo3o`;
- message: `N8N_MATTERMOST_NATIVE_E2E_OK_20260918T135107Z`.

## Production non-regression

After the E2E probe:

- production n8n workflow count remained `0`;
- production n8n execution count remained `0`;
- no probe workflow existed in the production database;
- Mattermost credential count remained `1`;
- the original Mattermost credential ID remained `16a0a988ad514ab1`;
- n8n health remained `{"status":"ok"}`;
- Mattermost API health remained `status=OK`;
- throwaway container and host `/tmp` artifacts were removed successfully;
- only the Mattermost acceptance post was intentionally retained as evidence.

## Acceptance markers

- `STAGE4E_N8N_MATTERMOST_NATIVE_E2E=PASS`;
- `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`.

The n8n↔Mattermost integration is therefore **COMPLETE / ACCEPTED**.

This acceptance does **not** by itself close Stage 4E. The accepted Stage 4E contract separately requires real native mobile-client/push verification; the current repository contains configuration evidence for TPNS but no recorded successful iOS/iPad login plus delivered push notification. Stage 4E also retains the explicit disposition of the currently enabled prepackaged `mattermost-ai` plugin and a final Stage 4E non-regression check after normalization.

## Remaining Stage 4E / Stage 4 work

Stage 4E remains **IN PROGRESS** until:

- official Mattermost mobile client login is verified against `https://chat.escloud.us`;
- a real TPNS notification is delivered to the official mobile client;
- the prepackaged `mattermost-ai` plugin is explicitly dispositioned rather than silently adopted;
- Stage 4E-specific non-regression passes after the final normalization.

Stage 4 itself remains IN PROGRESS. Separately, Hermes controlled stop/restart behavior where SIGTERM currently exits status 1 must be resolved or explicitly characterized before final server-side acceptance; remaining Hermes 4A/4B/4C, then 4F/4G/4H/4I, remain pending.
