#!/bin/bash
set -Eeuo pipefail

export HOME=/home/core
export USER=core
export LOGNAME=core
export SHELL=/bin/bash
export PATH=/home/core/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export XDG_RUNTIME_DIR=/run/user/1000
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus

MARKER=/home/core/.hermes/native-update-restart-required

PRE_VERSION="$(
    /home/core/.local/bin/hermes --version |
    sed -n '1p'
)"

printf 'PRE_VERSION=%s\n' "$PRE_VERSION"

/home/core/.local/bin/hermes update \
    --yes \
    --no-backup \
    --no-gateway-restart

POST_VERSION="$(
    /home/core/.local/bin/hermes --version |
    sed -n '1p'
)"

printf 'POST_VERSION=%s\n' "$POST_VERSION"

if [ "$POST_VERSION" != "$PRE_VERSION" ]; then
    : >"$MARKER"
    chmod 0600 "$MARKER"
    printf 'UPDATE_CHANGED=YES\n'
    printf 'RESTART_REQUIRED=YES\n'
else
    printf 'UPDATE_CHANGED=NO\n'
    printf 'RESTART_REQUIRED=NO\n'
fi
