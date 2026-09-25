# Nextcloud Policy Reconciliation Acceptance — 2026-09-25

## Status

**COMPLETE / ACCEPTED**

Acceptance marker: `NEXTCLOUD_POLICY_RECONCILIATION_FINAL=PASS`.

## Runtime baseline

- Nextcloud Server `35.0.1`.
- Healthy: installed, maintenance disabled, no DB upgrade pending.
- Primary working account: OIDC-backed `Eugene` through Authelia.
- Recovery/bootstrap account: local Database `admin`.
- Existing macOS and iOS permanent filesystem tokens preserved.
- Background jobs: `cron`.

## Accepted application policy

### Required / retained

- `files`
- `dav`
- `settings`
- `provisioning_api`
- `files_sharing`
- `files_trashbin`
- `files_versions`
- `dashboard`
- `notifications`
- `user_oidc`
- `viewer`
- `webhook_listeners`
- `workflowengine`

UI apps intentionally retained include `interfonts`, `side_menu`, `files_pdfviewer`, `text`, `theming` and `related_resources`.

Integration-oriented apps intentionally retained include `sharebymail`, `notifications`, `webhook_listeners` and `workflowengine`.

### Disabled by reconciliation

- `logreader`
- `privacy`
- `serverinfo`
- `twofactor_totp`
- `twofactor_webauthn`

`files_versions` was enabled.

### Always-enabled platform components

Nextcloud runtime marks these relevant components as `alwaysEnabled`; they remain enabled and are not bypassed:

- `cloud_federation_api`
- `federatedfilesharing`
- `lookup_server_connector`
- `oauth2`
- `profile`
- `twofactor_backupcodes`

OAuth2 registered-client count: `0`.

## Federation policy

Federated sharing functionality is disabled through supported global `files_sharing` configuration:

- `outgoing_server2server_share_enabled=no`
- `incoming_server2server_share_enabled=no`
- `outgoing_server2server_group_share_enabled=no`
- `incoming_server2server_group_share_enabled=no`
- `lookupServerEnabled=no`

The always-enabled platform applications remain present.

## Account and Dashboard policy

- OIDC `Eugene` is the primary working administrator.
- Local `admin` is retained only as recovery/bootstrap administrator.
- Global application policy applies to both accounts.
- Global Dashboard layout: `files-favorites`.
- Existing per-user Dashboard layout overrides removed.
- Both existing users inherit the global Dashboard policy.
- Per-user presentation/state settings outside this reconciliation remain user-specific.

## Authentication

- Authelia OIDC provider verified.
- Nextcloud-native TOTP disabled.
- Nextcloud-native WebAuthn disabled.
- `twofactor_backupcodes` remains an unused always-enabled platform component.
- Existing native-client authentication tokens preserved.

## Verification

- Required file-cloud apps: PASS.
- OIDC provider: PASS.
- Federation policy: PASS.
- Dashboard global inheritance: PASS.
- Native auth tokens preserved: PASS.
- Nextcloud health: PASS.
- `/status.php`: HTTP 200.
- unauthenticated `/remote.php/dav/` PROPFIND: HTTP 401.
- Background jobs: `cron`, PASS.

Final marker: `NEXTCLOUD_POLICY_RECONCILIATION_FINAL=PASS`.
