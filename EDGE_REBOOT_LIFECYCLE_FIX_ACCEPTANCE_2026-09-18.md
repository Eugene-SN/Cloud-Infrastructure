# Edge Reboot Lifecycle Fix Acceptance — 2026-09-18

**Status:** ACCEPTED / PASS  
**Scope:** corrective runtime fix discovered during Stage 3 reboot acceptance

## Result

`EDGE_REBOOT_AFTER_LIVE_RESTORE_FIX_ACCEPTANCE_V1=PASS`

The abnormal ~90-second late-shutdown delay introduced after the clean `edge` rebuild is resolved.

## Root cause

Stage 1 explicitly configured Docker `live-restore: true` in `/etc/docker/daemon.json`. On the current `edge` runtime this left the running containers' `containerd-shim-runc-v2` processes alive after `docker.service` / `containerd.service` stopped. The machine then spent approximately the systemd 90-second stop timeout in late shutdown before reboot.

This configuration was unnecessary for the current `edge` operating model because all production application containers use `restart: unless-stopped` and are expected to stop during a full VM shutdown and restart normally on boot.

The issue is therefore recorded as a Stage 1 configuration error, not as a reason to remove `fwupd`, `mdadm`, alter systemd `KillMode`, or pin/downgrade Docker/containerd.

## Corrective change

Changed only:

```json
{
  "live-restore": false
}
```

in `/etc/docker/daemon.json`.

The change was validated with `dockerd --validate` and applied with a Docker daemon reload. No container restarted during the reload.

Rollback copy retained on `edge`:

`/var/backups/docker-daemon-json-before-live-restore-disable-20260918T044818Z`

## A/B evidence

### Before corrective change

Observed during the prior reboot:

- normal userspace shutdown completed in approximately 3 seconds;
- `containerd.service` stopped while `containerd-shim-runc-v2` processes remained;
- approximately 94 seconds elapsed after the journal stopped before the next kernel boot;
- the overall reboot delay was therefore outside normal guest boot time.

### After corrective change

Verified reboot:

- kernel: `1.135s`;
- initrd: `3.183s`;
- userspace: `9.522s`;
- total boot: `13.842s`;
- previous journal stopped at epoch `1789707039.440156`;
- new kernel boot epoch `1789707043.643`;
- late-shutdown-to-new-kernel gap: `4.203s`;
- `POST_USERSPACE_GAP_GATE=PASS`.

Docker lifecycle after reboot:

- Docker active;
- containerd active;
- `live-restore=false` persisted;
- Authelia, Bulwark, n8n and Stalwart all returned automatically;
- all four retain `restart=unless-stopped`;
- four normal `containerd-shim-runc-v2` processes were present for the four running containers;
- system state `running`;
- failed systemd units: zero.

## Decision impact

The `live-restore: true` property recorded by the Stage 1 Docker/final acceptance documents is historical evidence of the state accepted at that time and is not rewritten retroactively.

Current authoritative runtime is:

- Docker `29.8.1`;
- containerd `2.3.5`;
- Docker `live-restore=false`;
- production containers use `restart=unless-stopped`.

No Docker/containerd downgrade or version pin is justified by this fix.

Stage 3 remains in progress until its connectivity-specific final acceptance is completed.
