# CloudCLI Final Runtime Retirement Acceptance — 2026-09-23

**Status:** COMPLETE / ACCEPTED

CloudCLI was fully retired from edge after the operator rejected it for the current persistent remote-workspace requirement.

Accepted final runtime state:

- `cloudcli.service` absent;
- CloudCLI process absent;
- listener `127.0.0.1:18140` absent;
- npm package/binary absent;
- `/home/core/.cloudcli` absent;
- `/srv/ai-workspace` absent;
- CloudCLI removed from edge backup SQLite-overlay staging;
- Semaphore template ID 15 and environment reference absent;
- Semaphore checkout cache cleaned;
- CloudCLI removed from Maintenance source/generated state and Cloud Portal;
- Maintenance current model: 17 actionable manual targets, 24 monitored components;
- nginx, Backrest, Semaphore and edge-monitor non-regression PASS; zero failed systemd units;
- `code.escloud.us` DNS/TLS/Authelia identity preserved and reserved for T3; current backend is an authenticated HTTP 503 placeholder until T3 deployment.

Historical Stage acceptance records and historical journal/backup records are intentionally preserved.

Acceptance marker: `CLOUDCLI_RETIREMENT_FINAL_ACCEPTANCE=PASS`.
