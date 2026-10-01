# Plane P2-1 — outbound SMTP via Stalwart

Status: **COMPLETE / ACCEPTED**. Final marker: `PLANE_P2_1_SMTP=PASS`.

Operator authorization: implement only outbound SMTP on production edge, provision a dedicated mailbox with a new unique password, configure native God Mode/runtime settings, send exactly one native Plane test email to an existing operator mailbox, verify delivery, remove temporary state, and commit/push directly to main. Part 1 and the Part 2A capability audit are accepted prerequisites. No other Part 2 stage was started.

## Confirmed baseline and mechanism

Fresh runtime: Plane Community `1.4.2`, backend image `sha256:90032ce088708889b60c00d491897916f4deb882facda27db59fd10fb68729ef`; Stalwart `0.16.24`, image `sha256:ec011be228596e37e65f41aab17deed573859614430472f7eeb42178c50d87b7`. Native Plane auth and existing public URL remain unchanged. Pre-stage local main and fetched origin/main were `935ef717615b3a7487c264c37be593a520a5e0c0`, with a clean worktree.

Exact installed `plane/license/api/views/configuration.py` implements native God Mode PATCH, encrypting configuration rows marked `is_encrypted` and invalidating instance caches. `get_email_configuration()` reads runtime database values because the deployed `SKIP_ENV_VAR` is true. Existing settings initially had SMTP disabled, empty host/user/password/from, port 587, TLS=1 and SSL=0.

Native `EmailCredentialCheckEndpoint` reads these effective settings and calls Django `EmailMultiAlternatives.send(fail_silently=False)`. Its subject is fixed to `Email Notification from Plane`; it accepts `receiver_email`, not a custom subject. No custom patch or replacement mail sender was used.

Authoritative references: [Plane SMTP configuration](https://developers.plane.so/self-hosting/govern/communication), [exact v1.4.2 native configuration/test implementation](https://github.com/makeplane/plane/blob/v1.4.2/apps/api/plane/license/api/views/configuration.py), [runtime configuration reader](https://github.com/makeplane/plane/blob/v1.4.2/apps/api/plane/license/utils/instance_value.py), [Stalwart native Account creation](https://www.stalw.art/docs/management/cli/create/), [temporary recovery administrator](https://www.stalw.art/docs/configuration/recovery-mode/), and [JMAP Mail query/get/set semantics](https://www.rfc-editor.org/rfc/rfc8621.html).

## Target and bounded recovery

Accepted transport: Plane API/worker -> `mail.escloud.us:465` -> authenticated Stalwart mailbox `plane@escloud.us`, implicit TLS, normal certificate verification, sender `Plane <plane@escloud.us>`.

Recovery contract was defined before mutation: restore the eight previous effective settings through the native God Mode endpoint; if explicitly rolling back the mailbox, delete only the newly created account after references/data checks. The original mail Compose and Plane env/override/ingress hashes were retained temporarily for equality checks. No shared-account password or service version was changed.

Existing deployed `/usr/local/sbin/edge-state-prepare` already captures `/srv/mail/` as `mail=quiesced_full_tree`, plus Plane's logical PostgreSQL dump, uploads and protected runtime as `plane=quiesced_logical_postgres_dump_plus_uploads_and_runtime`. That normal backup lifecycle protects Stalwart account state and Plane's encrypted runtime settings. No extra Backrest run or persistent ad-hoc recovery copy was introduced. The newly configured state will enter subsequent normal backups; this stage does not claim a new post-change recovery snapshot.

## Native provisioning and effective configuration

Stalwart live Account schema and native queries confirmed domain `b` = `escloud.us`; existing accounts `b` = `admin@escloud.us` and `c` = `es@escloud.us`. `plane@escloud.us` was absent. A new unique 36-random-byte password was generated locally, independently of the operator and former OpenProject credentials.

Upstream Stalwart CLI `1.0.13` was used transiently; its Linux asset SHA256 matched the release digest `1b8509b767edd1a17693e092b518c41610ec4b724f4e62c461bd28cd40c669f7`. Native Account/User creation returned account **`e`**, name `plane`, domain `b`, ordinary `User` role, no aliases. Existing accounts' identity, roles, aliases and credential metadata were equal before/after.

Temporary native `STALWART_RECOVERY_ADMIN` was required because usable stored management credentials were absent from the execution context. It was added through a protected temporary Compose override, without enabling `STALWART_RECOVERY_MODE`. Exactly two Stalwart-only recreations used `--no-deps --pull never --force-recreate --wait`: enable temporary administration, then restore the original environment. Original Compose bytes, image ID, mounts, port bindings and network membership were preserved. Final recovery-env absence and HTTP 401 rejection of the temporary identity both passed.

Native Django/Plane `user_login` and SessionStore provided a short-lived admin session for the existing verified instance administrator. The public God Mode PATCH returned HTTP 200 and exactly eight updated keys. SMTP password remained inside protected local transport/state and the native encrypted DB row.

| Setting | Accepted value |
|---|---|
| `ENABLE_SMTP` | `1` |
| `EMAIL_HOST` | `mail.escloud.us` |
| `EMAIL_PORT` | `465` |
| `EMAIL_HOST_USER` | `plane@escloud.us` |
| `EMAIL_HOST_PASSWORD` | Dedicated secret; encrypted runtime DB; omitted |
| `EMAIL_FROM` | `Plane <plane@escloud.us>` |
| `EMAIL_USE_SSL` | `1` — implicit TLS |
| `EMAIL_USE_TLS` | `0` — STARTTLS disabled |

API and existing worker independently read the effective settings. The password row was marked encrypted, nonempty, and unequal to its decrypted value. `plane.env` was unchanged. No Plane component restarted or recreated; API/worker/beat container IDs and StartedAt values matched the baseline. No TLS verification override was introduced.

Fresh SMTP_SSL preflight and dedicated mailbox authentication passed with TLS 1.3, `CERT_REQUIRED`, hostname checking, EHLO 250 and AUTH 235. Password-compatible AUTH PLAIN/LOGIN was advertised. After removing temporary Stalwart administration, mailbox authentication again returned 235 over validated TLS 1.3; neither auth check sent a message.

## Exactly one native test and delivery evidence

Native `POST /api/instances/email-credentials-check/` with recipient `es@escloud.us` was executed exactly once and returned HTTP 200, `Email successfully sent.` The recipient was the existing real operator mailbox, not a newly created test account.

Send/delivery time: **2026-10-01 23:23:14 UTC / 2026-10-02 02:23:14 +03:00**.

- Fixed native subject: `Email Notification from Plane`.
- From: `Plane <plane@escloud.us>`; To: `es@escloud.us`.
- Message-ID: `179089699442.32.11679012712010050194@279fe06d77b4`.
- Stalwart authenticated account: `plane@escloud.us`, accountId 4, listener `submissions`, localPort 465.
- Queue ID: **`332643947109154816`**; `queue.authenticated-message-queued` confirmed acceptance.
- `message-ingest.ham` confirmed delivery to recipient accountId 2, documentId 23.
- `delivery.dsn-success` returned 250/OK; `delivery.completed` and `delivery.attempt-end` completed successfully. No matching-session relay/auth error occurred.
- Native JMAP filtering by sender, exact subject and send window returned exactly one Email, id **`c2aaaaax`**. Email/get verified the exact headers; Mailbox/get confirmed Inbox (`role=inbox`). Unrelated message bodies were not inspected.

TLS evidence combines the validated SMTP_SSL transport, exact native Django SSL connection settings and the actual authenticated port-465 submission. The INFO log did not expose the test session's negotiated TLS version; TLS 1.3 was directly observed in the separate preflight/auth connections, not invented as a per-message log field.

## Cleanup and non-regression

Native JMAP Email/set destroyed only test Email `c2aaaaax`; Email/get returned that exact ID as notFound. Production mailbox and SMTP settings remain intentionally. Native SessionStore.delete removed the exact temporary Plane session; a matching-session count of zero was verified. The sign-out HTTP response alone was not used as evidence of invalidation.

Temporary source copies, CLI/schema cache, credential/payload/session files, prior-setting/config snapshots, recovery override/env and test artifacts were removed from the task-specific `/tmp` directory. No recovery administrator or new persistent local plaintext credential file remains. No `.bak` or rollback tree was placed beside production. CLI schema/path lookup and redirect-only sign-out verification defects were corrected at their failed points; they were not classified as production failures.

Final read-only verification: all nineteen production containers running, native Docker health checks healthy where defined, Plane public/API/live monitor states OK, worker/beat running, Stalwart healthy, n8n/Mattermost healthy and unchanged container identities/StartedAt. Original mail Compose, Plane env/site override and ingress hashes matched. nginx remained active and native `nginx -t` passed, without reload/configuration change. Fresh Edge Monitor reported `EDGE_STATE=OK`, `OVERALL_STATE=OK`. Plane API token/webhook counts remain zero.

```text
PLANE_SMTP_NATIVE_AVAILABLE=PASS
PLANE_SMTP_MAILBOX_CREATED=PASS
PLANE_SMTP_AUTH=PASS
PLANE_SMTP_TLS=PASS
PLANE_SMTP_CERTIFICATE_VERIFY=PASS
PLANE_SMTP_RUNTIME_CONFIG=PASS
PLANE_SMTP_RESTART_REQUIRED=NO
PLANE_SMTP_TEST_SEND=PASS
STALWART_DELIVERY=PASS
PLANE_SMTP_SENDER=plane@escloud.us
PLANE_SMTP_SECRET_DISCLOSURE=NONE
PLANE=PASS
STALWART=PASS
N8N=PASS
MATTERMOST=PASS
EDGE_STATE=OK
OVERALL_STATE=OK
PLANE_P2_1_SMTP=PASS
```

Canonical persistence is direct to main with remote readback. Historical Part 1 and OpenProject records remain unchanged. Remaining proposed stages: P2-2a internal webhook URL prerequisite; P2-2b current CE webhooks/API v1 bus; P2-3 Mattermost; P2-4 GitHub through n8n; P2-5 Hermes stdio MCP; P2-6 selective Knowledge; P2-7 Nextcloud/calendar and P2-8 intake email only when justified. They were not deployed by this stage.
