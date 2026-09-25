# Stage 8 Monitoring Notification Model v2.3.3 — Final Acceptance

Date: 2026-09-25

Status: COMPLETE / ACCEPTED

Acceptance marker: `EDGE_MONITOR_NOTIFICATION_V2_3_3_FINAL_E2E=PASS`

## Accepted production state

- Production runtime: `/usr/local/sbin/edge-monitor`
- Accepted runtime SHA-256: `8bc25a8788bfd60f61c1cc1b62fd61e14f4c551f5ebfc3900f7c837b4dc3b714`
- `edge-monitor.service` active/running with no restart/error regression during final acceptance.
- Live snapshot remained `overall_state=OK`.
- Durable production notification state was unchanged by the final synthetic E2E.
- Durable schema remains `notification_model=2`.

## Accepted Mattermost presentation

- `Monitoring` is an operational incident journal.
- Blocks-only posts; duplicated top-level plain text is removed.
- User-visible classes: INCIDENT, DEGRADED, RECOVERED.
- Large integrated severity heading, e.g. `### 🔴 Mattermost unavailable`.
- Scope/category is a separate small/subtle line.
- Mobile-first vertical metadata; production incident/recovery cards do not use `column_set`.
- Incident metadata: `STARTED` plus optional `CONFIRMED` when meaningful.
- Recovery metadata: `DURATION` plus `RECOVERED`.
- Diagnostics remain collapsed by default.
- Existing service correlation, parent/child suppression, probes, cadences, thresholds, snapshot publication and edge-only architecture remain unchanged.

## Final E2E evidence

The final isolated synthetic E2E exercised the real `update_notifications()`, renderer and Mattermost webhook while stubbing only durable-state persistence.

- initial synthetic FAIL -> one real Mattermost INCIDENT card: PASS;
- repeated identical FAIL -> no second delivery: PASS;
- synthetic OK -> one real RECOVERED card: PASS;
- delivery count exactly 2: PASS;
- incident visual contract: PASS;
- recovery visual contract: PASS;
- final synthetic state returned to OK with `notified_active=False`;
- production durable state SHA before/after was identical;
- production service remained active/running;
- production snapshot remained `overall_state=OK`;
- recent error count: 0.

## Scope preserved

This acceptance does not change Stage 8 collectors, probe cadence, two-failure confirmation semantics, snapshot/state paths, monitoring domains, edge-only monitoring limitation, Stage 7 Maintenance ownership, or the decision not to introduce another monitoring stack or daemon.
