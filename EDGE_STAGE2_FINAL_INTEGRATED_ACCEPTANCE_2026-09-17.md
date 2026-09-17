# Edge Stage 2 Final Integrated Acceptance — 2026-09-17

## Result

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Stage 2 — Edge Core Applications is COMPLETE / ACCEPTED.

## Accepted Stage 2 production set

- Authelia `4.39.27`;
- n8n `2.39.7`;
- CloudCLI `1.37.3`;
- Codex CLI `0.154.0` official standalone runtime;
- Antigravity CLI `1.2.5` with persistent Remote Control instance `edge`;
- Stalwart `0.16.22`;
- Bulwark `1.9.2`.

Backrest, Semaphore, maintenance page and the full private `app.escloud.us` portal are not Stage 2 blockers. They are explicitly deferred to late-stage Operations & Lifecycle work after the functional service inventory stabilizes.

## Final verification evidence

The final acceptance sequence established:

- host foundation services active;
- Authelia, n8n, Stalwart and Bulwark containers running with zero restarts;
- Authelia/n8n container health healthy;
- CloudCLI active with zero restarts;
- `core` lingering user manager active;
- Antigravity daemon active/enabled with zero restarts;
- WebUI backend bindings exactly loopback-only: `127.0.0.1:19091`, `15678`, `18140`, `18083`, `18084`;
- no public binding on 587, 995, 4190 or the loopback application ports;
- intended public TCP 22/80/443/25/465/993 and UDP 443 present;
- UFW rules consistent with the accepted listener contract;
- public HTTPS routes for `auth`, `n8n`, `code`, `mail` functional;
- local readiness/health endpoints functional;
- SMTP/25 banner and SMTPS certificate identity correct;
- mail DNS identity correct: MX, A, no AAAA, PTR, current DKIM selectors and retired legacy selector;
- accepted configuration hashes unchanged;
- temporary Vandelay capture absent;
- migration-preservation archive retained with expected SHA256;
- final runtime non-regression PASS;
- production configuration mutation during final acceptance: NO.

## Recovery notes

V1 stopped at Antigravity user-service verification because root did not have the `core` user systemd bus context. V2 corrected the user-bus context but then produced a false public-listener failure because its regex matched the suffix of `127.0.0.1:15678`. Neither failure changed production state. V3 used exact wildcard/public binding checks and completed the acceptance with RC=0.

## Current retained migration archive

`/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`

SHA256:

`0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`

Retain until later functional stages no longer require legacy configuration/reference material. Do not restore legacy application credentials from it.
