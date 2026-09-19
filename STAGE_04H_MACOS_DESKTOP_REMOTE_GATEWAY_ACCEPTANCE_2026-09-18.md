# Stage 04H — macOS Hermes Desktop Remote Gateway Acceptance

**Date:** 2026-09-18  
**Status:** COMPLETE / ACCEPTED  
**Marker:** `STAGE4H_MACOS_DESKTOP_REMOTE_GATEWAY=PASS`

## Accepted path

Hermes Desktop uses the upstream Remote Gateway contract against `https://hermes.escloud.us` and the server's native self-hosted OIDC/RFC8252 PKCE flow. No session-token workaround and no public TCP/9119 are used.

## Evidence

- Operator confirmed successful Desktop connection and operation.
- Two real `/auth/native/authorize` requests returned HTTP 302.
- Two real `/auth/callback` requests returned HTTP 302.
- Two real `/auth/native/token` exchanges returned HTTP 200.
- Two remote `/api/ws` upgrades returned HTTP 101 at separate times.
- Authenticated remote session/message traffic returned HTTP 200 and showed live response growth.
- Traffic reached the public server from a remote client address, proving the tested conversation was not served by an accidental local bundled backend.
- The repeated authorization/token and WebSocket sequences provide reconnect/session-renewal evidence.
- Dashboard backend remained `127.0.0.1:9119`; no public backend port was required.

The Desktop integration is accepted against the exact deployed server Hermes commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`.
