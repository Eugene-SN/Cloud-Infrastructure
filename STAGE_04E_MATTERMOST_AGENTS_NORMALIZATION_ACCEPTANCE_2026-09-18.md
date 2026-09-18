# Stage 04E — Mattermost Agents Normalization Acceptance — 2026-09-18

**Status:** ACCEPTED

## Context

The prepackaged Mattermost Agents plugin (`mattermost-ai`) was automatically present and enabled in the Mattermost Team Edition runtime. It is not part of the accepted Cloud Infrastructure agent architecture because Hermes remains the selected persistent agent runtime/reasoning/delegation layer.

The plugin was therefore normalized to disabled state using the supported Mattermost plugin-management path rather than removed or patched.

## Accepted runtime state

Verified after normalization:

- Mattermost plugin ID: `mattermost-ai`;
- display name: `Agents`;
- version: `2.6.1`;
- installed: YES;
- enabled-list count: `0`;
- disabled-list count: `1`;
- `config.json` effective plugin state: `PluginStates["mattermost-ai"].Enable=false`;
- Mattermost API health: PASS;
- n8n health: PASS;
- `hermes-gateway.service`: active;
- no restart was required for the plugin normalization.

Calls and Playbooks remain disabled as separately observed runtime state.

## Acceptance markers

- `MATTERMOST_AI_ENABLED=NO`;
- `MATTERMOST_AI_DISABLE_RECOVERY=PASS`;
- `STAGE4E_MATTERMOST_AGENTS_NORMALIZATION=PASS`.

The failed verifier in the immediately preceding attempt was not a runtime failure: `mmctl plugin disable mattermost-ai` had already succeeded, while the verifier incorrectly required an explicit `false` config value instead of accepting runtime-disabled semantics. The recovery verification subsequently proved both runtime-disabled state and explicit `false` config state.

## Remaining Stage 4E work

The remaining Stage 4E functional gate is the accepted native mobile-client path:

- successful login using the official Mattermost mobile client against `https://chat.escloud.us`;
- real TPNS push delivery to that registered device.

After that, run a bounded Stage 4E-specific non-regression verification and persist the final Stage 4E acceptance.
