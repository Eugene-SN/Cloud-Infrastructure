# Stage 13 — Backrest WebUI Ingress — Final Acceptance

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

Final marker:

`STAGE13_FINAL_ACCEPTANCE=PASS`

## Scope

Stage 13 publishes the already-running Backrest WebUI at `https://backup.escloud.us/` through the existing accepted edge ingress/auth architecture.

This stage is presentation/ingress only. It does not replace Backrest or Restic and does not change backup repositories, plans/schedules, retention, restore behavior, backup data, or the Backrest service lifecycle.

## Accepted runtime

- Backrest remains host-native and bound only to `127.0.0.1:9898`;
- public path: `backup.escloud.us:443 -> Xray TLS -> nginx 127.0.0.1:8080 -> Authelia -> Backrest 127.0.0.1:9898`;
- TCP/80 for `backup.escloud.us` redirects to HTTPS;
- nginx vhost source: `/etc/nginx/sites-available/backup.escloud.us`;
- enabled vhost: `/etc/nginx/sites-enabled/backup.escloud.us`;
- existing Authelia `one_factor` policy for `backup.escloud.us` is reused unchanged;
- existing shared `escloud.us` certificate already contains `backup.escloud.us`;
- existing public DNS already resolves `backup.escloud.us` to `45.92.156.17`;
- no new public application port or UFW rule was added.

Backrest-native bearer-token behavior is preserved behind the outer Authelia gate; nginx explicitly preserves the client `Authorization` header. ConnectRPC traffic is reverse-proxied without response buffering and with the existing long-lived request timeout pattern.

## Entry audit

`STAGE13_BACKREST_INGRESS_BOUNDED_AUDIT_V1` established:

- Backrest active/running with `NRestarts=0`;
- listener `127.0.0.1:9898` only;
- local Backrest root returned HTTP 200;
- no existing `backup.escloud.us` nginx vhost;
- nginx/Xray/Authelia healthy;
- Authelia already contained the `backup.escloud.us -> one_factor` policy;
- TLS SAN already contained `backup.escloud.us`;
- Xray certificate fingerprint matched the active Certbot lineage;
- DNS resolved to `45.92.156.17`;
- zero failed systemd units.

No mutation was performed by the entry audit.

## Reload verifier recovery

The first deployment attempt created and validated the correct nginx vhost but its immediate single HTTP verification request hit an old nginx worker generation during graceful reload and received the existing default-site HTTP 200 response. The block automatically removed the new vhost and reloaded the prior configuration.

Recovery audits proved:

- no curl proxy or alternate HTTP owner was involved;
- nginx remained the sole TCP/80 owner;
- the default-site response fingerprint matched the observed HTTP 200;
- old nginx workers were still in `worker process is shutting down` state after graceful reload.

The corrected deployment retained the same production vhost and changed only the verifier to poll for the new nginx worker generation. The first poll still saw the old default HTTP 200; the second poll observed the required `301 https://backup.escloud.us/`. The original failure is therefore classified as a verifier/reload-generation race, not a production configuration defect.

## Final server-side acceptance

`STAGE13_BACKREST_WEBUI_INGRESS_DEPLOY_VERIFY_V2` completed with RC=0.

Accepted gates:

- nginx configuration validation PASS;
- exactly two `backup.escloud.us` server blocks present;
- new-generation route gate PASS;
- public HTTP redirect PASS;
- unauthenticated public HTTPS redirects to Authelia PASS;
- Backrest configuration SHA256 unchanged:
  `984b4b996e73b82fe99c5a2339c8d6a5dcf6b09da2219729dfb7c56bb015fa55`;
- Backrest PID unchanged at `1044`;
- Backrest `NRestarts=0`;
- Backrest remained loopback-only;
- nginx, Xray, Backrest and Authelia remained healthy;
- zero failed systemd units;
- final `nginx -t` PASS.

Explicit non-mutation evidence:

- `BACKREST_ENGINE_CHANGED=NO`;
- `BACKREST_REPOSITORIES_CHANGED=NO`;
- `BACKREST_SCHEDULES_CHANGED=NO`;
- `BACKREST_RETENTION_CHANGED=NO`;
- `BACKREST_SERVICE_RESTARTED=NO`;
- `AUTHELIA_CONFIG_CHANGED=NO`;
- `DNS_CHANGED=NO`;
- `TLS_CHANGED=NO`;
- `UFW_CHANGED=NO`.

Server-side marker:

`STAGE13_SERVER_SIDE_INGRESS_DEPLOYMENT=PASS`

## Browser acceptance

The operator completed authenticated browser E2E at `https://backup.escloud.us/` and confirmed:

- Authelia authentication succeeds;
- the real Backrest WebUI loads successfully;
- existing repositories/plans/history are visible.

No backup, restore, repository, plan, schedule, retention, or other backup-runtime mutation was required for browser acceptance.

## Final status

Stage 13 — Backrest WebUI Ingress is **COMPLETE / ACCEPTED**.

The previously deferred `backup.escloud.us` task is closed. Backrest/Restic backup architecture remains unchanged from the accepted Stage 6 baseline.
