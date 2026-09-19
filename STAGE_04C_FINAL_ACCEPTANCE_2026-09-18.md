# Stage 04C — Hermes Dashboard/OIDC Final Acceptance

**Date:** 2026-09-18  
**Status:** COMPLETE / ACCEPTED  
**Marker:** `STAGE4C_HERMES_DASHBOARD_OIDC_ACCEPTANCE=PASS`

## Accepted architecture

- Public endpoint: `https://hermes.escloud.us`.
- Existing Xray TLS ingress -> nginx `127.0.0.1:8080 proxy_protocol` -> Hermes Dashboard `127.0.0.1:9119`.
- Dashboard backend is loopback-only; no public TCP/9119 listener.
- Hermes native `self-hosted` OIDC is the only interactive provider.
- Authelia `4.39.27` is the OIDC Identity Provider. nginx does not use `auth_request` for Hermes.
- Browser callback: `https://hermes.escloud.us/auth/callback`.
- Public authorization-code client with PKCE/S256 and refresh-token support.
- Dashboard runs as persistent `core` user-systemd unit `hermes-dashboard.service`.

## Deployment evidence

- Exact Hermes source: `d177b119e9c56c9ddc0b7379ffce52341ec06584`, Hermes `0.21.3`.
- Upstream Dashboard frontend build completed successfully.
- `hermes-dashboard.service` active/enabled, `NRestarts=0`.
- `/api/status` returns `auth_required=true`, provider `self-hosted`, browser cookie and native PKCE flows.
- Authelia configuration passed `authelia config validate` before activation; OIDC discovery returns HTTP 200 and advertises S256.
- Existing Certbot `4.0.0` `escloud.us` lineage was expanded using its established webroot mechanism. `hermes.escloud.us` is present in the shared certificate SAN set; no second certificate and no nginx Certbot plugin were introduced.
- nginx effective configuration proxies only to `127.0.0.1:9119` with WebSocket forwarding and the accepted forwarded headers.

## Interactive acceptance

- Real browser OIDC callback observed: `/auth/callback` HTTP 302 followed by authenticated session APIs HTTP 200.
- Real Dashboard session/message traffic and growing message payloads were observed through the public endpoint.
- Real `/api/ws` upgrades returned HTTP 101.
- The operator confirmed the Dashboard and remote interaction worked.
- Main gateway remained active and the Dashboard backend remained loopback-only.

## Recovery

Root recovery snapshot: `/srv/backups/edge-stage4c/recovery-20260918T171719Z`.

The earlier `CERTBOT_NGINX_PLUGIN_GATE=FAIL` was an assistant command-generation defect. It stopped before mutation and is not a production failure.

## Superseded current-state assumptions

The former nginx forward-auth/session-token-first design is superseded. The accepted current contract is Hermes-native self-hosted OIDC with Authelia as IdP and native Desktop RFC8252/PKCE support.
