# Core Full Root Sudo Acceptance — 2026-09-18

## Result

`CORE_FULL_ROOT_SUDO=PASS`  
`CORE_NONINTERACTIVE_PRIVILEGE_ESCALATION=PASS`

Recorded: `2026-09-18T20:10:54+03:00`.

## Scope

This corrective operational change supersedes the earlier target-state restriction that shared service/operator account `core` had no sudo access.

The environment is single-operator and `core` is the shared trusted execution identity for host-native Cloud Infrastructure services and agent executors. Continued infrastructure deployment requires non-interactive root-capable execution without switching to a separate root shell.

## Accepted state

- account: `core`;
- UID/GID: `1000:1000`;
- account password remains locked;
- sudo rule: `core ALL=(ALL:ALL) NOPASSWD: ALL`;
- rule path: `/etc/sudoers.d/90-core-root`;
- rule file SHA256: `545bf1fb2ab8c68f09c45e711100bea1db2b14341db1bdec986b315d4f04fc30`;
- `core` is not required to join the `docker` group because root-capable Docker/system operations are available through `sudo -n`;
- critical destructive/system-wide/production/network/credential/data mutations remain governed by the accepted operator-approval policy at the orchestration/instruction layer.

## Verification evidence

The production verification established:

- current sudoers parsed successfully before mutation;
- no pre-existing root sudo permission for `core`;
- new standalone rule passed `visudo -cf`;
- complete sudoers configuration passed `visudo -c` after installation;
- `core -> sudo -n id -u` returned UID `0`;
- `core -> sudo -n id -g` returned GID `0`;
- `core -> sudo -n id -un` returned `root`;
- arbitrary run-as verification succeeded with `sudo -n -u nobody id -u -> 65534`;
- effective policy reports `(ALL : ALL) NOPASSWD: ALL`.

## Operational meaning

Host-native services and trusted specialist agents running as `core` may perform required system administration through `sudo -n` without an interactive password prompt. The Unix identity remains `core`; root capability is explicit per command through sudo rather than by changing UID/GID or running the account as root.

Historical Stage 1/Stage 2 records that describe `core` as having no sudo remain valid historical evidence and are not rewritten retroactively.
