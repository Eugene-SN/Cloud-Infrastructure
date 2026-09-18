# Stage 04E — Mattermost Native Server Configuration Acceptance — 2026-09-18

**Status:** ACCEPTED

## Accepted native configuration

Verified effective/runtime state:

- effective Site URL: `https://chat.escloud.us`;
- configuration source for Site URL: official Docker Compose environment variable `MM_SERVICESETTINGS_SITEURL`;
- bot account creation: enabled;
- public user creation: disabled;
- Test Push Notification Service: enabled;
- push server: `https://push-test.mattermost.com`;
- Calls plugin `com.mattermost.calls`: disabled;
- public Mattermost API remains healthy.

The blank `ServiceSettings.SiteURL` value in `config.json` is intentional for this deployment because the official `mattermost/docker` Compose injects `MM_SERVICESETTINGS_SITEURL=https://${DOMAIN}`, which takes precedence over `config.json`.

`STAGE4E_MATTERMOST_NATIVE_SERVER_CONFIG=PASS`

## Next task

Provision the dedicated Hermes Mattermost bot identity/token, determine the operator Mattermost user ID, add the bot to the intended team/channel(s), then configure the Hermes built-in Mattermost gateway using the official Hermes procedure.
