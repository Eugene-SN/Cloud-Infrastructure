#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/vpn-stack"
STATE_DIR="${BASE_DIR}/state"
SERVICES_ENV="${STATE_DIR}/services.env"
BACKUP_DIR="/var/backups/vpn-stack/maintctl"

XRAY_CONFIG="/etc/xray/config.json"
XRAY_SERVICE_UNIT="/etc/systemd/system/xray.service"
HY2_CONFIG="/etc/hysteria/config.yaml"
HY2_SERVICE_UNIT="/etc/systemd/system/hysteria-server.service"
CERT_HOOK="/etc/letsencrypt/renewal-hooks/deploy/xray-cert-sync.sh"
CERT_SYNC_SCRIPT="/usr/local/bin/xray-cert-sync.sh"
WEB_DOMAINS_FILE="${STATE_DIR}/web-domains.txt"
ACME_WEBROOT="/var/www/letsencrypt"
VPNCTL="/opt/vpn-stack/scripts/vpnctl"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing command: $1"
}

need_file() {
  [ -f "$1" ] || die "missing file: $1"
}

pause() {
  echo
  read -r -p "Press Enter to continue..." _ || true
}

clear_screen() {
  command -v clear >/dev/null 2>&1 && clear || true
}

load_env() {
  need_file "${SERVICES_ENV}"
  # shellcheck disable=SC1090
  source "${SERVICES_ENV}"

  : "${DOMAIN:?missing DOMAIN in services.env}"
  : "${NODE_CODE:?missing NODE_CODE in services.env}"
  : "${NODE_DISPLAY:?missing NODE_DISPLAY in services.env}"
  : "${XRAY_PORT:?missing XRAY_PORT in services.env}"
  : "${HY2_PORT:?missing HY2_PORT in services.env}"

  NGINX_SERVICE="nginx"
  XRAY_SERVICE="xray"
  HY2_SERVICE="hysteria-server.service"
}

ensure_layout() {
  install -d -o root -g root -m 700 "${BACKUP_DIR}"
}

current_public_ip() {
  curl -4fsS --max-time 10 https://api.ipify.org 2>/dev/null || true
}

init_header_context() {
  load_env

  if [ -n "${NODE_DISPLAY:-}" ]; then
    MAINT_NAME="$NODE_DISPLAY"
  else
    MAINT_NAME="$(hostnamectl --static 2>/dev/null || hostname)"
  fi

  MAINT_PUBLIC_IP="$(curl -4fsS --max-time 10 https://api.ipify.org 2>/dev/null || true)"
  MAINT_DOMAIN="UNKNOWN"

  local d a
  if [ -n "${MAINT_PUBLIC_IP:-}" ] && [ -d /etc/letsencrypt/live ]; then
    while IFS= read -r d; do
      [ -n "${d:-}" ] || continue
      [ -f "/etc/letsencrypt/live/${d}/fullchain.pem" ] || continue

      a="$(dig +short A "$d" 2>/dev/null | tail -n1 || true)"
      if [ "${a:-}" = "$MAINT_PUBLIC_IP" ]; then
        MAINT_DOMAIN="$d"
        break
      fi
    done < <(find /etc/letsencrypt/live -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort)
  fi

  if [ "$MAINT_DOMAIN" = "UNKNOWN" ] && [ -n "${DOMAIN:-}" ] && [ -n "${MAINT_PUBLIC_IP:-}" ]; then
    a="$(dig +short A "$DOMAIN" 2>/dev/null | tail -n1 || true)"
    if [ "${a:-}" = "$MAINT_PUBLIC_IP" ]; then
      MAINT_DOMAIN="$DOMAIN"
    fi
  fi
}

display_name() {
  if [ -n "${MAINT_NAME:-}" ]; then
    printf '%s\n' "$MAINT_NAME"
  else
    load_env
    if [ -n "${NODE_DISPLAY:-}" ]; then
      printf '%s\n' "$NODE_DISPLAY"
    else
      hostnamectl --static 2>/dev/null || hostname
    fi
  fi
}

current_public_ip() {
  if [ -n "${MAINT_PUBLIC_IP:-}" ]; then
    printf '%s\n' "$MAINT_PUBLIC_IP"
  else
    curl -4fsS --max-time 10 https://api.ipify.org 2>/dev/null || true
  fi
}

current_domain() {
  if [ -n "${MAINT_DOMAIN:-}" ]; then
    printf '%s\n' "$MAINT_DOMAIN"
  else
    load_env
    local ip a
    ip="$(current_public_ip)"
    if [ -n "${DOMAIN:-}" ] && [ -n "${ip:-}" ]; then
      a="$(dig +short A "$DOMAIN" 2>/dev/null | tail -n1 || true)"
      if [ "${a:-}" = "$ip" ]; then
        printf '%s\n' "$DOMAIN"
        return 0
      fi
    fi
    printf 'UNKNOWN\n'
  fi
}

banner() {
  cat <<EOF_BANNER
============================================================
 Name:    ${MAINT_NAME:-$(display_name)}
 Domain:  ${MAINT_DOMAIN:-$(current_domain)}
============================================================
EOF_BANNER
}

action_start() {
  local title="${1:-Action}"
  clear_screen
  echo "──────────────────────────────────────────────"
  echo "$title"
  echo "──────────────────────────────────────────────"
  echo
}

action_screen() {
  action_start "${1:-Action}"
}

ensure_layout() {
  install -d -o root -g root -m 700 "$BACKUP_DIR"
}

cmd_dashboard() {
  load_env

  banner
  echo
  echo "== services =="
  printf 'nginx:       '; systemctl is-active nginx || true
  printf 'xray:        '; systemctl is-active xray || true
  printf 'hysteria2:   '; systemctl is-active hysteria-server || true
  printf 'certbot:     '; systemctl is-active certbot.timer || true
  printf 'ufw:         '; ufw status 2>/dev/null | sed -n 's/^Status: //p' || true
  echo

  echo "== node =="
  echo "hostname:    $(hostnamectl --static 2>/dev/null || hostname)"
  echo "public-ip:   $(curl -4fsS --max-time 10 https://api.ipify.org 2>/dev/null || echo UNKNOWN)"
  echo "dns-a:       $(dig +short A "${DOMAIN}" 2>/dev/null | tail -n1 || echo UNKNOWN)"
  echo

  echo "== ports =="
  ss -lntup | grep -E '(:22|:80|:443|:8080)[[:space:]]' || true
  echo

  echo "== vpn users =="
  python3 <<'PY'
import csv, pathlib
for proto, path in [
    ("xray", pathlib.Path("/opt/vpn-stack/state/xray/users.csv")),
    ("hy2", pathlib.Path("/opt/vpn-stack/state/hysteria2/users.csv")),
]:
    if not path.exists():
        print(f"{proto}: missing state")
        continue
    rows = list(csv.DictReader(path.open(newline="")))
    print(f"{proto}: {len(rows)} user(s)")
    for r in rows:
        if proto == "xray":
            print(f"  - {r.get('name')} | {r.get('email')} | {r.get('label')}")
        else:
            print(f"  - {r.get('name')} | {r.get('username')} | {r.get('label')}")
PY
  echo

  echo "== failed units =="
  systemctl --failed --no-pager || true
}

show_versions() {
  load_env
  echo '== installed versions =='
  echo

  echo '[os]'
  . /etc/os-release 2>/dev/null || true
  echo "${PRETTY_NAME:-unknown}"
  uname -r
  echo

  echo '[nginx]'
  nginx -v 2>&1 || true
  echo

  echo '[xray]'
  /usr/local/bin/xray version 2>&1 | sed -n '1,8p' || true
  echo

  echo '[hysteria2]'
  /usr/local/bin/hysteria version 2>&1 | sed -n '1,18p' || true
  echo

  echo '[certbot]'
  certbot --version 2>&1 || true
  echo

  echo '[jq]'
  jq --version 2>&1 || true
  echo

  echo '[qrencode]'
  qrencode --version 2>&1 | sed -n '1,2p' || true
}

installed_xray_version() {
  /usr/local/bin/xray version 2>/dev/null | awk '/^Xray /{print $2; exit}'
}

installed_hy2_version() {
  /usr/local/bin/hysteria version 2>/dev/null | awk '/^Version:/{print $2; exit}' | sed 's/^v//'
}

github_latest_xray() {
  curl -fsSL --connect-timeout 10 --max-time 30 https://api.github.com/repos/XTLS/Xray-core/releases/latest \
    | jq -r '.tag_name' \
    | sed 's/^v//'
}

github_latest_hy2() {
  curl -fsSL --connect-timeout 10 --max-time 30 https://api.github.com/repos/apernet/hysteria/releases/latest \
    | jq -r '.tag_name' \
    | sed 's#^app/##; s/^v//'
}

cmd_versions_latest() {
  need_cmd curl
  need_cmd jq

  local x_inst h_inst x_latest h_latest
  x_inst="$(installed_xray_version || true)"
  h_inst="$(installed_hy2_version || true)"
  x_latest="$(github_latest_xray || true)"
  h_latest="$(github_latest_hy2 || true)"

  echo "== xray =="
  echo "installed: ${x_inst:-UNKNOWN}"
  echo "latest:    ${x_latest:-UNKNOWN}"
  if [ -n "${x_inst:-}" ] && [ -n "${x_latest:-}" ] && [ "$x_inst" = "$x_latest" ]; then
    echo "status:    current"
  elif [ -n "${x_inst:-}" ] && [ -n "${x_latest:-}" ]; then
    echo "status:    update_available"
  else
    echo "status:    unknown"
  fi
  echo

  echo "== hysteria2 =="
  echo "installed: ${h_inst:-UNKNOWN}"
  echo "latest:    ${h_latest:-UNKNOWN}"
  if [ -n "${h_inst:-}" ] && [ -n "${h_latest:-}" ] && [ "$h_inst" = "$h_latest" ]; then
    echo "status:    current"
  elif [ -n "${h_inst:-}" ] && [ -n "${h_latest:-}" ]; then
    echo "status:    update_available"
  else
    echo "status:    unknown"
  fi
}

normalize_version() {
  local v="${1:-}"
  v="${v#app/}"
  v="${v#v}"
  printf '%s\n' "$v"
}

cmd_update_xray() {
  need_cmd curl
  need_cmd unzip

  local requested="${1:-latest}"
  local version tag work backup old_version

  if [ "$requested" = "latest" ]; then
    version="$(github_latest_xray)"
  else
    version="$(normalize_version "$requested")"
  fi

  [ -n "$version" ] || die "failed to resolve Xray version"
  tag="v${version}"
  old_version="$(installed_xray_version || true)"

  backup="/var/backups/vpn-stack/update-xray-$(date -u +%Y%m%d-%H%M%S)"
  install -d -o root -g root -m 700 "$backup"
  cp -a /usr/local/bin/xray "$backup/xray.previous" 2>/dev/null || true
  cp -a /etc/xray/config.json "$backup/xray.config.json.bak" 2>/dev/null || true

  work="$(mktemp -d /var/tmp/xray-update.XXXXXX)"
  trap 'rm -rf "$work"' RETURN
  cd "$work"

  echo "Updating Xray: ${old_version:-UNKNOWN} -> ${version}"
  curl -fL --retry 3 --connect-timeout 15 --max-time 180 \
    -o xray.zip \
    "https://github.com/XTLS/Xray-core/releases/download/${tag}/Xray-linux-64.zip"

  unzip -o xray.zip -d xray-dist >/dev/null
  install -o root -g root -m 755 xray-dist/xray /usr/local/bin/xray

  /usr/local/bin/xray version | sed -n '1,8p'
  /usr/local/bin/xray version 2>&1 | grep -qE "Xray ${version}"
  /usr/local/bin/xray run -test -config /etc/xray/config.json >/dev/null
  runuser -u xray -- /usr/local/bin/xray run -test -config /etc/xray/config.json >/dev/null

  systemctl restart xray
  systemctl is-active xray
  echo "backup=$backup"
}

cmd_update_hy2() {
  need_cmd curl

  local requested="${1:-latest}"
  local version work backup old_version

  if [ "$requested" = "latest" ]; then
    version="$(github_latest_hy2)"
  else
    version="$(normalize_version "$requested")"
  fi

  [ -n "$version" ] || die "failed to resolve Hysteria2 version"
  old_version="$(installed_hy2_version || true)"

  backup="/var/backups/vpn-stack/update-hy2-$(date -u +%Y%m%d-%H%M%S)"
  install -d -o root -g root -m 700 "$backup"
  cp -a /usr/local/bin/hysteria "$backup/hysteria.previous" 2>/dev/null || true
  cp -a /etc/hysteria/config.yaml "$backup/hysteria.config.yaml.bak" 2>/dev/null || true

  work="$(mktemp -d /var/tmp/hy2-update.XXXXXX)"
  trap 'rm -rf "$work"' RETURN
  cd "$work"

  echo "Updating Hysteria2: ${old_version:-UNKNOWN} -> ${version}"
  curl -fL --retry 3 --connect-timeout 15 --max-time 180 \
    -o hysteria-linux-amd64 \
    "https://github.com/apernet/hysteria/releases/download/app%2Fv${version}/hysteria-linux-amd64"

  install -o root -g root -m 755 hysteria-linux-amd64 /usr/local/bin/hysteria

  /usr/local/bin/hysteria version | sed -n '1,18p'
  /usr/local/bin/hysteria version 2>&1 | grep -qE "Version:[[:space:]]+v${version}"

  systemctl restart hysteria-server
  systemctl is-active hysteria-server
  echo "backup=$backup"
}

cmd_update() {
  local target="${1:-all}"
  local version="${2:-latest}"

  case "$target" in
    xray) cmd_update_xray "$version" ;;
    hy2|hysteria|hysteria2) cmd_update_hy2 "$version" ;;
    all)
      cmd_update_xray "$version"
      cmd_update_hy2 "$version"
      ;;
    *) die "usage: maintctl update [xray|hy2|all] [latest|version]" ;;
  esac
}

show_ports() {
  load_env
  echo '== tcp/udp listeners: 22, 80, 443, 8080 =='
  ss -lntup | grep -E '(:22|:80|:443|:8080)[[:space:]]' || true
  echo
  echo '== udp 443 =='
  ss -lnup | grep -E ':443[[:space:]]' || true
}

cert_file() {
  load_env
  printf '/etc/letsencrypt/live/%s/fullchain.pem\n' "${DOMAIN}"
}

show_cert_info() {
  need_cmd openssl
  local cert
  cert="$(cert_file)"
  need_file "${cert}"

  echo '== certificate metadata =='
  openssl x509 -in "${cert}" -noout -subject -issuer -dates -ext subjectAltName
  echo

  echo '== certificate expiry gates =='
  if openssl x509 -checkend 2592000 -noout -in "${cert}" >/dev/null; then
    echo 'CERT_GATE|OK|valid_more_than_30_days'
  else
    echo 'CERT_GATE|WARN|expires_within_30_days'
  fi

  if openssl x509 -checkend 604800 -noout -in "${cert}" >/dev/null; then
    echo 'CERT_GATE|OK|valid_more_than_7_days'
  else
    echo 'CERT_GATE|FAIL|expires_within_7_days'
  fi
}

cmd_check() {
  load_env

  echo '== services =='
  systemctl is-active nginx || true
  systemctl is-active xray || true
  systemctl is-active hysteria-server || true
  systemctl is-active certbot.timer || true
  systemctl --failed --no-pager || true
  echo

  echo '== nginx test =='
  nginx -t 2>&1 || true
  echo

  echo '== xray test as root =='
  /usr/local/bin/xray run -test -config "${XRAY_CONFIG}" 2>&1 || true
  echo

  echo '== xray test as xray user =='
  runuser -u xray -- /usr/local/bin/xray run -test -config "${XRAY_CONFIG}" 2>&1 || true
  echo

  echo '== listeners =='
  show_ports
  echo

  echo '== public http =='
  curl -sSI --max-time 10 "http://${DOMAIN}/" 2>&1 | sed -n '1,16p' || true
  echo

  echo '== public https fallback =='
  curl -ksSI --http1.1 --max-time 10 "https://${DOMAIN}/" 2>&1 | sed -n '1,20p' || true
  echo

  echo '== cert summary =='
  show_cert_info
}

cmd_vpn_structure() {
  load_env

  echo "== services.env =="
  cat "${SERVICES_ENV}"
  echo

  echo "== xray users =="
  column -s, -t /opt/vpn-stack/state/xray/users.csv 2>/dev/null || cat /opt/vpn-stack/state/xray/users.csv
  echo

  echo "== hysteria2 users =="
  column -s, -t /opt/vpn-stack/state/hysteria2/users.csv 2>/dev/null || cat /opt/vpn-stack/state/hysteria2/users.csv
  echo

  echo "== xray config structure =="
  python3 <<'PY'
import json
p="/etc/xray/config.json"
data=json.load(open(p))
print(f"path={p}")
for ib in data.get("inbounds", []):
    print(f"inbound tag={ib.get('tag')} protocol={ib.get('protocol')} listen={ib.get('listen')} port={ib.get('port')}")
    print(f"  clients={len(ib.get('settings', {}).get('clients', []))}")
    print(f"  fallbacks={ib.get('settings', {}).get('fallbacks', [])}")
    print(f"  stream={ib.get('streamSettings', {})}")
print(f"outbounds={[(o.get('tag'), o.get('protocol')) for o in data.get('outbounds', [])]}")
PY
  echo

  echo "== hysteria2 config =="
  cat /etc/hysteria/config.yaml
}

cmd_backup() {
  ensure_layout
  load_env

  local ts dir
  ts="$(date -u +%Y%m%d-%H%M%S)"
  dir="${BACKUP_DIR}/${ts}"
  install -d -o root -g root -m 700 "${dir}"

  cp -a /etc/nginx              "${dir}/etc-nginx.bak" 2>/dev/null || true
  cp -a "${XRAY_CONFIG}"        "${dir}/xray.config.json.bak" 2>/dev/null || true
  cp -a "${XRAY_SERVICE_UNIT}"  "${dir}/xray.service.bak" 2>/dev/null || true
  cp -a "${HY2_CONFIG}"         "${dir}/hysteria.config.yaml.bak" 2>/dev/null || true
  cp -a "${HY2_SERVICE_UNIT}"   "${dir}/hysteria-server.service.bak" 2>/dev/null || true
  cp -a "${SERVICES_ENV}"       "${dir}/services.env.bak" 2>/dev/null || true
  cp -a "${CERT_HOOK}"          "${dir}/cert-sync.hook.bak" 2>/dev/null || true
  cp -a "${CERT_SYNC_SCRIPT}"   "${dir}/xray-cert-sync.sh.bak" 2>/dev/null || true
  cp -a "${VPNCTL}"             "${dir}/vpnctl.bak" 2>/dev/null || true
  cp -a /opt/vpn-stack/scripts/maintctl "${dir}/maintctl.bak" 2>/dev/null || true

  cp -a /opt/vpn-stack/state/xray/users.csv      "${dir}/xray.users.csv.bak" 2>/dev/null || true
  cp -a /opt/vpn-stack/state/hysteria2/users.csv "${dir}/hy2.users.csv.bak" 2>/dev/null || true
  cp -a /opt/vpn-stack/conf/xray_primary_uuid.txt "${dir}/xray_primary_uuid.txt.bak" 2>/dev/null || true
  cp -a /opt/vpn-stack/conf/hysteria2_primary.txt "${dir}/hysteria2_primary.txt.bak" 2>/dev/null || true
  cp -a /etc/letsencrypt "${dir}/etc-letsencrypt.bak" 2>/dev/null || true
  cp -a /var/www "${dir}/var-www.bak" 2>/dev/null || true

  echo "backup saved to: ${dir}"
  echo
  find "${dir}" -maxdepth 1 -mindepth 1 -printf '%M %u:%g %p\n' | sort
}

web_cert_domain_args() {
  load_env
  local d clean
  local -a args=()

  if [ -s "${WEB_DOMAINS_FILE}" ]; then
    while IFS= read -r d; do
      clean="${d%%#*}"
      clean="${clean//[[:space:]]/}"
      [ -n "${clean}" ] || continue
      args+=("-d" "${clean}")
    done < "${WEB_DOMAINS_FILE}"
  else
    args=(
      "-d" "${DOMAIN}"
      "-d" "auth.${DOMAIN}"
      "-d" "go.${DOMAIN}"
      "-d" "app.${DOMAIN}"
      "-d" "docs.${DOMAIN}"
      "-d" "cloud.${DOMAIN}"
      "-d" "sync.${DOMAIN}"
    )
  fi

  [ "${#args[@]}" -gt 0 ] || die "empty cert domain set"
  printf '%s\n' "${args[@]}"
}

cmd_web_check() {
  load_env
  need_cmd openssl
  need_cmd curl

  local cert="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
  local token body d code got fail=0
  local -a domains=()

  if [ -s "${WEB_DOMAINS_FILE}" ]; then
    while IFS= read -r d; do
      d="${d%%#*}"
      d="${d//[[:space:]]/}"
      [ -n "${d}" ] || continue
      domains+=("${d}")
    done < "${WEB_DOMAINS_FILE}"
  else
    domains=("${DOMAIN}" "auth.${DOMAIN}" "go.${DOMAIN}" "app.${DOMAIN}" "docs.${DOMAIN}" "cloud.${DOMAIN}" "sync.${DOMAIN}")
  fi

  echo "== web domains =="
  printf '%s\n' "${domains[@]}"
  echo

  echo "== letsencrypt SAN coverage =="
  need_file "${cert}"
  for d in "${domains[@]}"; do
    if openssl x509 -in "${cert}" -noout -ext subjectAltName 2>/dev/null | grep -q "DNS:${d}\\b"; then
      echo "SAN|OK|${d}"
    else
      echo "SAN|FAIL|${d}"
      fail=1
    fi
  done
  echo

  echo "== tls copies =="
  for f in \
    /etc/letsencrypt/live/"${DOMAIN}"/fullchain.pem \
    /etc/xray/tls/fullchain.pem \
    /etc/hysteria/tls/fullchain.pem
  do
    if [ -f "${f}" ] && openssl x509 -in "${f}" -noout -ext subjectAltName 2>/dev/null | grep -q 'DNS:sync\.escloud\.us\b'; then
      echo "TLS_COPY|OK|${f}"
    else
      echo "TLS_COPY|FAIL|${f}"
      fail=1
    fi
  done
  echo

  echo "== tls key permissions =="
  stat -c 'TLS_MODE|%U|%G|%a|%n' /etc/xray/tls/privkey.pem /etc/hysteria/tls/privkey.pem 2>/dev/null || true
  echo

  echo "== acme http challenge =="
  install -d -o www-data -g www-data -m 0755 "${ACME_WEBROOT}/.well-known/acme-challenge"
  token="maintctl-$(date -u +%H%M%S)"
  body="ok-${token}"
  printf '%s\n' "${body}" > "${ACME_WEBROOT}/.well-known/acme-challenge/${token}"
  chmod 0644 "${ACME_WEBROOT}/.well-known/acme-challenge/${token}"

  for d in "${domains[@]}"; do
    got="$(mktemp /tmp/maintctl-acme.XXXXXX)"
    code="$(curl -sS -o "${got}" -w '%{http_code}' --max-time 8 "http://${d}/.well-known/acme-challenge/${token}" 2>/dev/null || true)"
    if [ "${code}" = "200" ] && grep -qx "${body}" "${got}" 2>/dev/null; then
      echo "ACME|OK|${d}|code=${code}"
    else
      echo "ACME|FAIL|${d}|code=${code}"
      fail=1
    fi
    rm -f "${got}"
  done

  rm -f "${ACME_WEBROOT}/.well-known/acme-challenge/${token}"
  echo

  echo "== services =="
  echo "nginx=$(systemctl is-active nginx 2>/dev/null || true)"
  echo "xray=$(systemctl is-active xray 2>/dev/null || true)"
  echo "hysteria=$(systemctl is-active hysteria-server 2>/dev/null || true)"
  echo "certbot_timer=$(systemctl is-active certbot.timer 2>/dev/null || true)"
  echo

  if [ "${fail}" -eq 0 ]; then
    echo "WEB_CHECK|OK"
  else
    echo "WEB_CHECK|FAIL"
  fi

  return "${fail}"
}

cmd_cert_dry_run() {
  certbot renew --dry-run
}

cmd_cert_renew_if_due() {
  certbot renew
  cmd_cert_sync
}

cmd_cert_force_renew() {
  load_env
  need_cmd certbot

  install -d -o www-data -g www-data -m 0755 "${ACME_WEBROOT}/.well-known/acme-challenge"

  local -a domain_args=()
  mapfile -t domain_args < <(web_cert_domain_args)

  certbot certonly \
    --webroot \
    -w "${ACME_WEBROOT}" \
    --force-renewal \
    --cert-name "${DOMAIN}" \
    "${domain_args[@]}" \
    --non-interactive \
    --agree-tos \
    --register-unsafely-without-email

  cmd_cert_sync
}

cmd_cert_sync() {
  need_file "${CERT_SYNC_SCRIPT}"
  "${CERT_SYNC_SCRIPT}"
  systemctl is-active xray hysteria-server
}

cmd_logs() {
  load_env
  local target="${1:-all}"
  local n="${2:-120}"

  case "${target}" in
    nginx)
      journalctl -u nginx -n "$n" --no-pager || true
      ;;
    xray)
      journalctl -u xray -n "$n" --no-pager || true
      ;;
    hy2|hysteria|hysteria2)
      journalctl -u hysteria-server -n "$n" --no-pager || true
      ;;
    certbot)
      journalctl -u certbot -n "$n" --no-pager || true
      journalctl -u certbot.timer -n "$n" --no-pager || true
      ;;
    ssh)
      journalctl -u ssh -n "$n" --no-pager || journalctl -u sshd -n "$n" --no-pager || true
      ;;
    all)
      echo '[nginx]'
      journalctl -u nginx -n "$n" --no-pager || true
      echo
      echo '[xray]'
      journalctl -u xray -n "$n" --no-pager || true
      echo
      echo '[hysteria2]'
      journalctl -u hysteria-server -n "$n" --no-pager || true
      echo
      echo '[certbot]'
      journalctl -u certbot -n "$n" --no-pager || true
      journalctl -u certbot.timer -n "$n" --no-pager || true
      ;;
    *)
      die "usage: maintctl logs [nginx|xray|hy2|certbot|ssh|all] [lines]"
      ;;
  esac
}

cmd_service() {
  local action="${1:-}"
  local target="${2:-all}"

  case "${action}" in
    status)
      case "${target}" in
        nginx) systemctl status nginx --no-pager -l || true ;;
        xray)  systemctl status xray --no-pager -l || true ;;
        hy2|hysteria|hysteria2) systemctl status hysteria-server --no-pager -l || true ;;
        certbot) systemctl status certbot.timer --no-pager -l || true ;;
        all)
          systemctl status nginx --no-pager -l || true
          echo
          systemctl status xray --no-pager -l || true
          echo
          systemctl status hysteria-server --no-pager -l || true
          echo
          systemctl status certbot.timer --no-pager -l || true
          ;;
        *) die "usage: maintctl service status [nginx|xray|hy2|certbot|all]" ;;
      esac
      ;;
    start|stop|restart|reload)
      case "${target}" in
        nginx) systemctl "${action}" nginx ;;
        xray)  systemctl "${action}" xray ;;
        hy2|hysteria|hysteria2) systemctl "${action}" hysteria-server ;;
        all)
          systemctl "${action}" nginx
          systemctl "${action}" xray
          systemctl "${action}" hysteria-server
          ;;
        *) die "usage: maintctl service ${action} [nginx|xray|hy2|all]" ;;
      esac
      echo "service ${action} done: ${target}"
      ;;
    *) die "usage: maintctl service [status|start|stop|restart|reload] [nginx|xray|hy2|certbot|all]" ;;
  esac
}

cmd_firewall() {
  local sub="${1:-status}"

  case "${sub}" in
    status)
      echo "== ufw status verbose =="
      ufw status verbose || true
      ;;
    rules)
      echo "== nft ruleset =="
      nft list ruleset 2>/dev/null || true
      ;;
    open)
      ufw allow 22/tcp
      ufw allow 80/tcp
      ufw allow 443/tcp
      ufw allow 443/udp
      ufw --force enable
      ufw status verbose
      ;;
    reload)
      ufw reload
      ufw status verbose
      ;;
    *) die "usage: maintctl firewall [status|rules|open|reload]" ;;
  esac
}

cmd_security() {
  local sub="${1:-summary}"

  case "${sub}" in
    summary)
      echo "== ssh effective settings =="
      sshd -T 2>/dev/null | grep -Ei '^(permitrootlogin|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication|challengeresponseauthentication|usepam) ' || true
      echo
      echo "== root authorized_keys =="
      stat -Lc '%a %U:%G %s %n' /root /root/.ssh /root/.ssh/authorized_keys 2>/dev/null || true
      cat /root/.ssh/authorized_keys 2>/dev/null || true
      echo
      echo "== ufw =="
      ufw status verbose || true
      ;;
    ssh)
      sshd -T 2>/dev/null | grep -Ei '^(permitrootlogin|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication|challengeresponseauthentication|usepam) ' || true
      echo
      grep -RInE 'PermitRootLogin|PasswordAuthentication|KbdInteractiveAuthentication|PubkeyAuthentication|ChallengeResponseAuthentication|UsePAM' /etc/ssh/sshd_config /etc/ssh/sshd_config.d 2>/dev/null || true
      ;;
    keys)
      stat -Lc '%a %U:%G %s %n' /root /root/.ssh /root/.ssh/authorized_keys 2>/dev/null || true
      echo
      cat /root/.ssh/authorized_keys 2>/dev/null || true
      ;;
    *) die "usage: maintctl security [summary|ssh|keys]" ;;
  esac
}

vpn_cmd() {
  local sub="${1:-}"
  local target="${2:-all}"

  [ $# -gt 0 ] && shift || true

  case "$sub" in
    list)
      case "${1:-all}" in
        all|"")
          cmd_vpn_users_full
          ;;
        xray|hy2|hysteria|hysteria2)
          "$VPNCTL" list "${1:-all}"
          ;;
        *)
          "$VPNCTL" list "${1:-all}"
          ;;
      esac
      ;;
    uri)
      "$VPNCTL" uri "${1:-all}" "${2:-primary}" "${3:-}"
      ;;
    qr)
      "$VPNCTL" qr "${1:-}" "${2:-primary}" "${3:-}"
      ;;
    add-user)
      "$VPNCTL" add-user "${1:-}" "${2:-}" "${3:-}"
      ;;
    recreate)
      "$VPNCTL" recreate "${1:-}" "${2:-primary}"
      ;;
    delete-user)
      "$VPNCTL" delete-user "${1:-}" "${2:-}"
      ;;
    apply)
      "$VPNCTL" apply "${1:-all}"
      ;;
    service)
      "$VPNCTL" service "${1:-status}" "${2:-all}"
      ;;
    *)
      cat <<'USAGE'
usage:
  maintctl vpn list [xray|hy2|all]
  maintctl vpn uri [xray|hy2|all] [user-name] [profile-label]
  maintctl vpn qr [xray|hy2] [user-name] [profile-label]
  maintctl vpn add-user [xray|hy2] <suffix> [profile-label]
  maintctl vpn recreate [xray|hy2|all] [user-name]
  maintctl vpn delete-user [xray|hy2] <user-name>
  maintctl vpn apply [xray|hy2|all]
  maintctl vpn service [status|start|stop|restart] [xray|hy2|all]
USAGE
      return 2
      ;;
  esac
}

cmd_help() {
  cat <<'USAGE'
maintctl

Interactive mode:
  maintctl

CLI mode:
  maintctl help
  maintctl dashboard
  maintctl check
  maintctl ports
  maintctl structure

  maintctl vpn list [xray|hy2|all]
  maintctl vpn uri [xray|hy2|all] [user-name] [profile-label]
  maintctl vpn qr [xray|hy2] [user-name] [profile-label]
  maintctl vpn add-user [xray|hy2] <suffix> [profile-label]
  maintctl vpn recreate [xray|hy2|all] [user-name]
  maintctl vpn delete-user [xray|hy2] <user-name>
  maintctl vpn apply [xray|hy2|all]
  maintctl vpn service [status|start|stop|restart] [xray|hy2|all]

  maintctl cert info
  maintctl cert dry-run
  maintctl cert renew
  maintctl cert force-renew
  maintctl cert sync
  maintctl web-check

  maintctl logs [nginx|xray|hy2|certbot|ssh|all] [lines]
  maintctl service [status|start|stop|restart|reload] [nginx|xray|hy2|certbot|all]
  maintctl versions
  maintctl latest
  maintctl update [xray|hy2|all] [latest|version]
  maintctl firewall [status|rules|open|reload]
  maintctl security [summary|ssh|keys]
USAGE
}

cmd_vpn_users_full() {
  local file proto n f2 f3 label uri

  printf "%-12s %-24s %-28s %s\n" "PROTOCOL" "USER" "LABEL" "URI"
  printf "%-12s %-24s %-28s %s\n" "--------" "----" "-----" "---"

  file="/opt/vpn-stack/state/xray/users.csv"
  if [ -f "$file" ]; then
    while IFS=, read -r n f2 f3 label _rest; do
      [ "$n" = "name" ] && continue
      [ -n "${n:-}" ] || continue
      uri="$("$VPNCTL" uri xray "$n" 2>/dev/null | grep -m1 "^vless://")"
      printf "%-12s %-24s %-28s %s\n" "xray" "$n" "${label:-}" "$uri"
    done < "$file"
  fi

  file="/opt/vpn-stack/state/hysteria2/users.csv"
  if [ -f "$file" ]; then
    while IFS=, read -r n f2 f3 label _rest; do
      [ "$n" = "name" ] && continue
      [ -n "${n:-}" ] || continue
      uri="$("$VPNCTL" uri hy2 "$n" 2>/dev/null | grep -m1 "^hysteria2://")"
      printf "%-12s %-24s %-28s %s\n" "hysteria2" "$n" "${label:-}" "$uri"
    done < "$file"
  fi
}

select_user_name() {
  local proto="${1:-}"
  local file=""
  local choice=""
  local selected=""

  case "$proto" in
    xray)
      file="/opt/vpn-stack/state/xray/users.csv"
      ;;
    hy2|hysteria|hysteria2)
      file="/opt/vpn-stack/state/hysteria2/users.csv"
      ;;
    *)
      echo "ERROR: select_user_name: invalid proto: $proto" >&2
      return 2
      ;;
  esac

  if [ ! -f "$file" ]; then
    echo "ERROR: missing users file: $file" >&2
    return 2
  fi

  echo "Available users:" >&2
  awk -F, 'NR>1 && $1!="" {printf "  %d) %s\n", NR-1, $1}' "$file" >&2
  echo >&2

  printf "User number or name: " >&2
  IFS= read -r choice || true

  if [ -z "${choice:-}" ]; then
    echo "ERROR: empty user selection" >&2
    return 2
  fi

  if [[ "$choice" =~ ^[0-9]+$ ]]; then
    selected="$(awk -F, -v n="$choice" 'NR>1 && (NR-1)==n {print $1; exit}' "$file")"
  else
    selected="$(awk -F, -v n="$choice" 'NR>1 && $1==n {print $1; exit}' "$file")"
  fi

  if [ -z "${selected:-}" ]; then
    echo "ERROR: user not found: $choice" >&2
    return 2
  fi

  printf "%s\n" "$selected"
}


vpn_stack_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> VPN stack menu

  1) Health check
  2) VPN users
  3) Active ports
  4) Full config/state structure
  5) Public HTTP/HTTPS fallback test
  6) Apply VPN configs from current state

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1) action_screen 'Health check'; cmd_check; pause ;;
      2) vpn_users_menu ;;
      3) action_screen 'Active ports'; show_ports; pause ;;
      4) action_screen 'Full config/state structure'; cmd_vpn_structure; pause ;;
      5)
        action_screen 'Public HTTP/HTTPS fallback test'
        load_env
        d="$(current_domain)"
        [ "$d" != "UNKNOWN" ] || d="$DOMAIN"
        curl -sSI --max-time 10 "http://${d}/" | sed -n '1,16p' || true
        echo
        curl -ksSI --http1.1 --max-time 10 "https://${d}/" | sed -n '1,20p' || true
        pause
        ;;
      6) action_screen 'Apply VPN configs'; "$VPNCTL" apply all; pause ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

vpn_users_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> VPN users menu

  1) Show all users

  2) Show Xray QR
  3) Show Hysteria2 QR

  4) User configuration

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1)
        action_screen 'All VPN users'
        cmd_vpn_users_full
        pause
        ;;
      2)
        action_screen 'Select Xray user'
        if ! u="$(select_user_name xray)"; then
          pause
          continue
        fi
        action_screen "Xray URI / QR: $u"
        "$VPNCTL" uri xray "$u"
        echo
        "$VPNCTL" qr xray "$u"
        pause
        ;;
      3)
        action_screen 'Select Hysteria2 user'
        if ! u="$(select_user_name hy2)"; then
          pause
          continue
        fi
        action_screen "Hysteria2 URI / QR: $u"
        "$VPNCTL" uri hy2 "$u"
        echo
        "$VPNCTL" qr hy2 "$u"
        pause
        ;;
      4) user_config_menu ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

user_config_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> User configuration

  1) Add Xray user
  2) Add Hysteria2 user

  3) Recreate Xray user
  4) Recreate Hysteria2 user

  5) Delete Xray user
  6) Delete Hysteria2 user

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1)
        read -r -p "Suffix, e.g. gateway: " suffix || true
        read -r -p "Profile label [auto]: " label || true
        action_screen 'Add Xray user'
        if [ -n "${label:-}" ]; then
          "$VPNCTL" add-user xray "$suffix" "$label"
        else
          "$VPNCTL" add-user xray "$suffix"
        fi
        echo
        "$VPNCTL" uri xray "$suffix"
        pause
        ;;
      2)
        read -r -p "Suffix, e.g. gateway: " suffix || true
        read -r -p "Profile label [auto]: " label || true
        action_screen 'Add Hysteria2 user'
        if [ -n "${label:-}" ]; then
          "$VPNCTL" add-user hy2 "$suffix" "$label"
        else
          "$VPNCTL" add-user hy2 "$suffix"
        fi
        echo
        "$VPNCTL" uri hy2 "$suffix"
        pause
        ;;
      3)
        action_screen 'Select Xray user'
        if ! u="$(select_user_name xray)"; then
          pause
          continue
        fi
        action_screen "Recreate Xray user: $u"
        "$VPNCTL" recreate xray "$u"
        echo
        "$VPNCTL" uri xray "$u"
        pause
        ;;
      4)
        action_screen 'Select Hysteria2 user'
        if ! u="$(select_user_name hy2)"; then
          pause
          continue
        fi
        action_screen "Recreate Hysteria2 user: $u"
        "$VPNCTL" recreate hy2 "$u"
        echo
        "$VPNCTL" uri hy2 "$u"
        pause
        ;;
      5)
        action_screen 'Select Xray user'
        if ! u="$(select_user_name xray)"; then
          pause
          continue
        fi
        action_screen "Delete Xray user: $u"
        "$VPNCTL" delete-user xray "$u"
        pause
        ;;
      6)
        action_screen 'Select Hysteria2 user'
        if ! u="$(select_user_name hy2)"; then
          pause
          continue
        fi
        action_screen "Delete Hysteria2 user: $u"
        "$VPNCTL" delete-user hy2 "$u"
        pause
        ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

cert_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> Certificates menu

  1) Show certificate info
  2) Dry-run renewal
  3) Renew if due
  4) Force renew now
  5) Sync cert copies to xray/hysteria

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1) action_screen 'Certificate info'; show_cert_info; pause ;;
      2) action_screen 'Certificate dry-run renewal'; cmd_cert_dry_run; pause ;;
      3) action_screen 'Certificate renew if due'; cmd_cert_renew_if_due; pause ;;
      4) action_screen 'Certificate force renew'; cmd_cert_force_renew; pause ;;
      5) action_screen 'Certificate sync'; cmd_cert_sync; pause ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

logs_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> Logs menu

  1) nginx
  2) xray
  3) hysteria2
  4) certbot
  5) ssh
  6) all

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true
    [ "${choice:-}" = "0" ] && return 0

    read -r -p "Lines [120]: " n || true
    n="${n:-120}"

    case "${choice:-}" in
      1) action_screen; cmd_logs nginx "$n"; pause ;;
      2) action_screen; cmd_logs xray "$n"; pause ;;
      3) action_screen; cmd_logs hy2 "$n"; pause ;;
      4) action_screen; cmd_logs certbot "$n"; pause ;;
      5) action_screen; cmd_logs ssh "$n"; pause ;;
      6) action_screen; cmd_logs all "$n"; pause ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

service_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> Service management menu

  1) Status all
  2) Active ports

  3) Installed versions
  4) Check latest versions
  5) Update Xray
  6) Update Hysteria2
  7) Update both

  8) Status nginx
  9) Status xray
 10) Status hysteria2
 11) Status certbot timer

 12) Restart nginx
 13) Restart xray
 14) Restart hysteria2
 15) Restart all

 16) Stop xray
 17) Stop hysteria2
 18) Start xray
 19) Start hysteria2

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1) action_screen 'Status all'; cmd_service status all; pause ;;
      2) action_screen 'Active ports'; show_ports; pause ;;
      3) action_screen 'Installed versions'; show_versions; pause ;;
      4) action_screen 'Check latest versions'; cmd_versions_latest; pause ;;
      5)
        read -r -p "Version [latest]: " v || true
        action_screen 'Update Xray'
        cmd_update xray "${v:-latest}"
        pause
        ;;
      6)
        read -r -p "Version [latest]: " v || true
        action_screen 'Update Hysteria2'
        cmd_update hy2 "${v:-latest}"
        pause
        ;;
      7)
        action_screen 'Update both'
        cmd_update all latest
        pause
        ;;
      8) action_screen 'Status nginx'; cmd_service status nginx; pause ;;
      9) action_screen 'Status xray'; cmd_service status xray; pause ;;
      10) action_screen 'Status hysteria2'; cmd_service status hy2; pause ;;
      11) action_screen 'Status certbot timer'; cmd_service status certbot; pause ;;
      12) action_screen 'Restart nginx'; cmd_service restart nginx; pause ;;
      13) action_screen 'Restart xray'; cmd_service restart xray; pause ;;
      14) action_screen 'Restart hysteria2'; cmd_service restart hy2; pause ;;
      15) action_screen 'Restart all'; cmd_service restart all; pause ;;
      16) action_screen 'Stop xray'; cmd_service stop xray; pause ;;
      17) action_screen 'Stop hysteria2'; cmd_service stop hy2; pause ;;
      18) action_screen 'Start xray'; cmd_service start xray; pause ;;
      19) action_screen 'Start hysteria2'; cmd_service start hy2; pause ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

security_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> Security / firewall menu

  1) Security summary
  2) SSH effective config
  3) Root authorized_keys
  4) UFW status
  5) Full nft ruleset
  6) Open standard VPN ports in UFW
  7) Reload UFW

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1) action_screen 'Security summary'; cmd_security summary; pause ;;
      2) action_screen 'SSH effective config'; cmd_security ssh; pause ;;
      3) action_screen 'Root authorized_keys'; cmd_security keys; pause ;;
      4) action_screen 'UFW status'; cmd_firewall status; pause ;;
      5) action_screen 'Full nft ruleset'; cmd_firewall rules; pause ;;
      6) action_screen 'Open standard VPN ports in UFW'; cmd_firewall open; pause ;;
      7) action_screen 'Reload UFW'; cmd_firewall reload; pause ;;
      0) return 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}

main_menu() {
  while true; do
    clear_screen
    banner
    cat <<'MENU'

maintctl -> Main menu

  1) Dashboard
  2) VPN stack menu
  3) Certificates menu
  4) Logs menu
  5) Service management menu
  6) Security / firewall menu
  7) Help

  0) Exit
MENU
    echo
    read -r -p "Select: " choice || true

    case "${choice:-}" in
      1) action_screen 'Dashboard'; cmd_dashboard; pause ;;
      2) vpn_stack_menu ;;
      3) cert_menu ;;
      4) logs_menu ;;
      5) service_menu ;;
      6) security_menu ;;
      7) action_screen 'Help'; cmd_help; pause ;;
      0) exit 0 ;;
      *) echo; echo 'Invalid selection'; pause ;;
    esac
  done
}


main() {
  load_env
  init_header_context

  if [ $# -eq 0 ]; then
    main_menu
    exit 0
  fi

  local cmd="${1:-help}"
  shift || true

  case "${cmd}" in
    help|-h|--help) cmd_help ;;
    dashboard) cmd_dashboard ;;
    check) cmd_check ;;
    ports) show_ports ;;
    versions) show_versions ;;
    latest) cmd_versions_latest ;;
    update) cmd_update "$@" ;;
    structure) cmd_vpn_structure ;;
    backup) echo "maintctl backup is disabled; use manual/specialized backups before major changes" >&2; return 2 ;;
    vpn) vpn_cmd "$@" ;;
    logs) cmd_logs "$@" ;;
    service) cmd_service "$@" ;;
    cert)
      sub="${1:-}"
      shift || true
      case "${sub}" in
        info) show_cert_info ;;
        dry-run) cmd_cert_dry_run ;;
        renew) cmd_cert_renew_if_due ;;
        force-renew) cmd_cert_force_renew ;;
        sync) cmd_cert_sync ;;
        *) die "usage: maintctl cert [info|dry-run|renew|force-renew|sync]" ;;
      esac
      ;;
    web-check) cmd_web_check ;;
    firewall) cmd_firewall "$@" ;;
    security) cmd_security "$@" ;;
    *)
      die "unknown command: ${cmd}"
      ;;
  esac
}

main "$@"
