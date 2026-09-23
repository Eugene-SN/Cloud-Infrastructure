# T3 Persistent Remote Workspace — Final Acceptance

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

## Scope

Persistent T3 Code deployment on `edge` as a 24/7 remote workspace, independent of Desktop-managed SSH lifecycle.

## Accepted runtime

- official T3 user service: `t3code.service`;
- service owner: `core` user systemd;
- accepted compatibility pin: `0.0.43-nightly.20260923.2150`;
- service command: `/home/core/.t3/runtime/versions/0.0.43-nightly.20260923.2150/t3 __service-launcher`;
- server runtime: service-managed `t3 serve` on `127.0.0.1:3773`;
- project root: `/home/core/projects`;
- managed relay client: `cloudflared 2026.5.2`;
- T3 Connect state: desired/authenticated/linked;
- `publishAgentActivity=false`;
- public WebUI: `https://code.escloud.us` through existing Xray -> nginx -> Authelia path to `127.0.0.1:3773`;
- Codex ACP and Antigravity ACP remain available through T3;
- standalone `antigravity-cli-daemon.service` remains independent and healthy.

## Compatibility decision

Stable T3 `0.0.42` was rejected for the current persistent deployment because runtime testing exposed two user-visible regressions:

1. persisted/older thread projection decoding failed for existing conversation data;
2. Antigravity provider health reported `Antigravity could not complete its local health check`.

The already-installed nightly `0.0.43-nightly.20260923.2150` restored the existing thread and removed the Antigravity health failure. Exact upstream source for that nightly also changes the Antigravity health path from spawning the large ACP runtime to a lightweight install-resolution probe. The nightly therefore remains a **temporary compatibility pin** until a stable release is verified to contain equivalent behavior.

Do not downgrade to `0.0.42` merely to return to a stable tag. Re-evaluate the pin when a newer stable release is available.

## Client transport

T3 Connect is the accepted client transport for the persistent environment.

Verified clients:

- macOS T3 Desktop through T3 Connect;
- iPad T3 Code through T3 Connect;
- browser WebUI through `code.escloud.us`.

The previous Desktop SSH environment/profile was removed after T3 Connect acceptance. Stale server-side SSH launcher artifacts under `/home/core/.t3/ssh-launch` were deleted, the empty root was removed, and no SSH-managed T3 runtime remains.

Administrative SSH access to `edge` itself is unchanged; only the T3 Desktop SSH transport was retired.

## Reboot acceptance

Controlled reboot acceptance passed:

- boot identity changed;
- `t3code.service` auto-started enabled/active with no service restart loop;
- one service-owned `t3 serve` runtime restored on port `3773`;
- nightly compatibility pin persisted;
- T3 Connect state persisted;
- managed relay reconciled automatically after server startup;
- one `cloudflared tunnel run` process appeared without manual restart or relink;
- four QUIC relay connections registered automatically;
- Mac Desktop and iPad both reconnected through T3 Connect;
- existing conversation data opened successfully after reboot;
- Antigravity remained usable;
- `code.escloud.us` remained functional;
- retired T3 SSH state was not required.

The relay can appear several seconds after `t3 serve` during normal startup reconciliation; acceptance is based on automatic recovery without operator mutation rather than instantaneous process presence at the first post-boot sample.

## Final markers

- `T3_PERSISTENT_SERVICE=PASS`
- `T3_CONNECT=PASS`
- `T3_MAC_DESKTOP_CONNECT=PASS`
- `T3_IPAD_CONNECT=PASS`
- `T3_WEBUI_INGRESS=PASS`
- `T3_OLD_THREAD_COMPATIBILITY=PASS`
- `T3_ANTIGRAVITY_PROVIDER=PASS`
- `T3_SSH_TRANSPORT_RETIREMENT=PASS`
- `T3_STALE_SSH_STATE_CLEANUP=PASS`
- `T3_REBOOT_RELAY_RECOVERY=PASS`
- `T3_REBOOT_ACCEPTANCE=PASS`

