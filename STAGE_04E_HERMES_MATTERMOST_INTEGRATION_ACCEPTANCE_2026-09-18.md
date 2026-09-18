# Stage 04E — Hermes ↔ Mattermost Integration Acceptance — 2026-09-18

**Status:** ACCEPTED

## Accepted end-to-end state

Hermes ↔ Mattermost integration is operational and accepted.

Verified:

- Mattermost bot account: `hermes`;
- bot display name: `Hermes Agent`;
- bot ID: `sceogxkhh3nh9y89uc6eza9ije`;
- bot token validated against Mattermost API and stored in Hermes environment;
- allowed operator Mattermost user ID: `mof5mc6w3jds8qp36b678qrzoc`;
- Hermes gateway active after integration configuration;
- real end-to-end Mattermost message returned exactly `HERMES_MATTERMOST_E2E_OK`;
- dedicated private service channel slug: `hermes`;
- service channel display name: `Hermes Agent`;
- service/home channel ID: `6s6o3iftjprwfg5p4d1gg1bwho`;
- operator `eugene` and bot `hermes` are members of the service channel;
- `MATTERMOST_HOME_CHANNEL=6s6o3iftjprwfg5p4d1gg1bwho`;
- primary interactive surface: direct message with `Hermes Agent`;
- proactive delivery surface: private `Hermes Agent` service channel;
- Mattermost requires team members, including the bot, to remain members of default channel `town-square`; that membership is accepted as a Mattermost invariant and is not used as the Hermes service channel;
- public Mattermost API remains healthy.

Acceptance markers:

- `STAGE4E_HERMES_MATTERMOST_BOT_PROVISION=PASS`
- `STAGE4E_HERMES_MATTERMOST_CHANNEL_NORMALIZATION=PASS`
- `STAGE4E_HERMES_MATTERMOST_E2E=PASS`

## Operational model

- Human ↔ Hermes interactive conversations use Mattermost Direct Messages with **Hermes Agent**.
- Cron results, reminders, notifications and other proactive Hermes deliveries use the private **Hermes Agent** service channel.
- `town-square` is not used for Hermes operations despite mandatory default-channel membership.

## Next task

Proceed with the accepted Stage 4E sequence: native n8n ↔ Mattermost integration, using a dedicated Mattermost service channel for n8n where appropriate. Stalwart SMTP usefulness/necessity remains a later discussion and is not enabled automatically.
