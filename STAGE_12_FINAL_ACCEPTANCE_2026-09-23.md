# Stage 12 — Final Acceptance

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE12_FINAL_ACCEPTANCE=PASS`

## Accepted scope

Stage 12 delivers two separate user file-access capabilities on edge:

1. personal cloud drive through Nextcloud at `cloud.escloud.us`;
2. direct project/workspace access through WebDAV at `go.escloud.us`.

## Nextcloud

Accepted runtime:

- Nextcloud `34.0.4.1` / `34.0.4`;
- compose: `/opt/nextcloud/compose.yaml`;
- backend: `127.0.0.1:18080`;
- persistent application state: `/srv/nextcloud`;
- user-visible portable files: `/srv/cloud`;
- public endpoint: `https://cloud.escloud.us/`;
- existing Xray -> nginx public ingress reused;
- native macOS client/File Provider acceptance passed;
- iPad client behavior validated;
- final core marker: `STAGE12_NEXTCLOUD_CORE_FINAL_AUDIT=PASS`.

## Workspace-access selection

Private SMB was implemented and functionally validated locally, but end-to-end Home LAN testing demonstrated that clientless access to the edge NetBird overlay would require production Home routing/firewall changes or an additional proxy.

That tradeoff was rejected for this use case.

Final accepted decision:

- Samba/SMB: **REJECTED / REMOVED**;
- Home VM100/MikroTik/CT300 changes: **NONE**;
- replacement: WebDAV over existing HTTPS ingress.

Samba cleanup passed with:

- zero installed Samba packages;
- no Samba binaries or systemd units;
- no TCP/139 or TCP/445 listeners;
- no Samba UFW rules;
- no Samba config/state/cache/log paths;
- installation APT cache removed;
- workspace data unchanged;
- marker: `STAGE12_SAMBA_FULL_REMOVAL=PASS`.

## WebDAV workspace access

Accepted runtime:

- target: exactly `/home/core/projects/`;
- target owner: `core:core`;
- rclone: `1.75.1`;
- service: `projects-webdav.service` under the persistent `core` user systemd instance;
- backend: `127.0.0.1:18081` only;
- public endpoint: `https://go.escloud.us/`;
- ingress: Xray TLS :443 -> nginx `127.0.0.1:8080` -> rclone `127.0.0.1:18081`;
- authentication: HTTP Basic over HTTPS;
- Authelia intentionally excluded from the WebDAV protocol path;
- shared Certbot lineage expanded to include `go.escloud.us`;
- existing deploy hook synchronized Xray/Hysteria2/Stalwart certificate copies.

Acceptance:

- unauthenticated PROPFIND -> 401;
- authenticated PROPFIND -> 207;
- MKCOL -> PASS;
- PUT/GET -> PASS;
- MOVE/rename -> PASS;
- DELETE file/directory -> PASS;
- target returned clean after synthetic E2E;
- service active/running with zero restarts during acceptance;
- Xray/Hysteria/nginx active;
- zero failed systemd units;
- local marker: `STAGE12_PROJECTS_WEBDAV_LOCAL_ACCEPTANCE=PASS`;
- public marker: `STAGE12_GO_WEBDAV_PUBLIC_INGRESS_DEPLOYMENT=PASS`.

## macOS client acceptance

- Finder connects to `https://go.escloud.us/`;
- credentials are stored in macOS Keychain;
- automatic login-time server connection is configured through the native macOS mechanism;
- Finder RW access is accepted;
- `.DS_Store` suppression is handled client-side via macOS network-store policy rather than server cleanup automation.

## Final state

`cloud.escloud.us` and `go.escloud.us` are both production Stage 12 services.

No Home Infrastructure mutation is required by either capability.

Stage 12 is **COMPLETE / ACCEPTED**.
