# Edge Remote CLI and Reboot Lifecycle Acceptance — 2026-09-23

Status: **COMPLETE / ACCEPTED**

## Scope

This record captures the bounded reconciliation of Codex and Antigravity Remote Control lifecycle ownership and the independent reboot/SSH latency defect traced to unused multipath runtime.

## Codex

- current CLI/runtime: `0.156.0`;
- native managed Remote Control backend: PID;
- native managed app-server through Unix control socket only;
- native `pid-update-loop` updater enabled;
- repeated `codex remote-control start --json` is idempotent and returns `alreadyRunning` without creating a second owner;
- legacy custom `codex-cli-daemon.service` removed;
- controlled clean reboot without a start hook proved native PID backend alone does not restart Codex;
- enabled user oneshot `codex-remote-control-start.service` now invokes only `/home/core/.local/bin/codex remote-control start --json`;
- final reboot verified exactly one managed app-server, exactly one native updater and the control socket without manual Codex start.

## Antigravity

- current runtime: `1.2.7`;
- native `agy remote-control start` registration retained;
- `antigravity-cli-daemon.service` enabled under the lingering `core` user manager;
- final reboot verified native automatic start and active `agy remote-control serve` process.

## Reboot/SSH latency root cause

The earlier slow reboot was not caused by SSH, networking, Codex or Antigravity. Previous shutdown evidence showed `multipathd.service` entered stop at 05:15:31 and did not complete until its 90-second stop timeout forced SIGKILL at 05:17:01.

Fresh storage audit:
- root source: `/dev/vda1`, ext4;
- no device-mapper devices;
- no multipath maps;
- small QEMU SCSI `sda` is a read-only ISO/config disk;
- `multipathd.service` was enabled only through `sysinit.target`;
- `multipathd.socket` is static/inactive.

Accepted correction:
- keep `multipath-tools` installed;
- disable `multipathd.service`;
- leave static socket/helper inactive;
- do not modify initramfs, GRUB or kernel command line.

## Final combined reboot acceptance

- reboot request: 2026-09-23 05:29:27 MSK;
- reboot target: 05:29:39.188 MSK;
- previous journal stopped: 05:29:39.260 MSK;
- new kernel: 05:29:45.786 MSK;
- network-online: 05:29:52.817 MSK;
- SSH listening: 05:29:53.717 MSK;
- full startup: `18.348s`;
- verification started 37 seconds after reboot request;
- `multipathd.service`: disabled/inactive, no current-boot execution;
- Codex boot trigger: enabled; native managed runtime present;
- Codex managed app-server count: 1;
- Codex native updater count: 1;
- Antigravity native service: enabled/active;
- legacy Codex owner absent;
- failed systemd units: 0.

## Acceptance markers

- `EDGE_COMBINED_REBOOT_ACCEPTANCE=PASS`
- `MULTIPATHD_BOOT_DISABLED=PASS`
- `CODEX_BOOT_PERSISTENCE=PASS`
- `CODEX_SINGLE_NATIVE_LIFECYCLE_OWNER=PASS`
- `CODEX_NATIVE_AUTO_UPDATE_PRESERVED=PASS`
- `ANTIGRAVITY_NATIVE_BOOT_PERSISTENCE=PASS`
