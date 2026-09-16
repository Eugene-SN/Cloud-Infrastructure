#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/vpn-stack"
STATE_DIR="${BASE_DIR}/state"
SERVICES_ENV="${STATE_DIR}/services.env"

[ -f "${SERVICES_ENV}" ] || {
  echo "ERROR: missing ${SERVICES_ENV}" >&2
  exit 1
}

# shellcheck disable=SC1090
. "${SERVICES_ENV}"

[ -n "${DOMAIN:-}" ] || {
  echo "ERROR: DOMAIN is empty in ${SERVICES_ENV}" >&2
  exit 1
}

LE_DIR="/etc/letsencrypt/live/${DOMAIN}"
[ -f "${LE_DIR}/fullchain.pem" ] || {
  echo "ERROR: missing ${LE_DIR}/fullchain.pem" >&2
  exit 1
}
[ -f "${LE_DIR}/privkey.pem" ] || {
  echo "ERROR: missing ${LE_DIR}/privkey.pem" >&2
  exit 1
}

install -d -o root -g ssl-cert -m 0750 /etc/xray/tls
install -d -o root -g hysteria -m 0750 /etc/hysteria/tls

install -o root -g root     -m 0644 "${LE_DIR}/fullchain.pem" /etc/xray/tls/fullchain.pem
install -o root -g ssl-cert -m 0640 "${LE_DIR}/privkey.pem"   /etc/xray/tls/privkey.pem

install -o root -g hysteria -m 0644 "${LE_DIR}/fullchain.pem" /etc/hysteria/tls/fullchain.pem
install -o root -g hysteria -m 0640 "${LE_DIR}/privkey.pem"   /etc/hysteria/tls/privkey.pem

systemctl try-restart xray >/dev/null 2>&1 || true
systemctl try-restart hysteria-server >/dev/null 2>&1 || true

echo "OK: cert synced for ${DOMAIN} to xray and hysteria2"
