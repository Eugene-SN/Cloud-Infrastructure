#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/vpn-stack"
STATE_DIR="${BASE_DIR}/state"
CONF_DIR="${BASE_DIR}/conf"
XRAY_STATE_DIR="${STATE_DIR}/xray"
HY2_STATE_DIR="${STATE_DIR}/hysteria2"
BACKUP_DIR="/var/backups/vpn-stack/vpnctl"

SERVICES_ENV="${STATE_DIR}/services.env"
XRAY_USERS="${XRAY_STATE_DIR}/users.csv"
HY2_USERS="${HY2_STATE_DIR}/users.csv"
XRAY_PRIMARY_UUID_FILE="${CONF_DIR}/xray_primary_uuid.txt"
HY2_PRIMARY_PASS_FILE="${CONF_DIR}/hysteria2_primary.txt"

XRAY_CONFIG="/etc/xray/config.json"
HY2_CONFIG="/etc/hysteria/config.yaml"
XRAY_SERVICE="xray"
HY2_SERVICE="hysteria-server.service"

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

validate_atom() {
  local value="$1"
  local what="$2"
  [[ "$value" =~ ^[a-z0-9][a-z0-9-]{0,40}$ ]] || die "invalid ${what}: ${value}; use lowercase letters, digits and hyphen"
}

validate_no_csv_break() {
  local value="$1"
  local what="$2"
  [[ "$value" != *","* ]] || die "${what} must not contain comma"
  [[ "$value" != *$'\n'* ]] || die "${what} must not contain newline"
}

confirm_action() {
  local prompt="${1:-Are you sure? [y/N]: }"
  local ans
  read -r -p "$prompt" ans || true
  case "${ans:-}" in
    y|Y|yes|YES) return 0 ;;
    *) return 1 ;;
  esac
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
  : "${XRAY_USER:?missing XRAY_USER in services.env}"
  : "${HY2_USER:?missing HY2_USER in services.env}"
  : "${VLESS_LABEL:?missing VLESS_LABEL in services.env}"
  : "${HY2_LABEL:?missing HY2_LABEL in services.env}"
  export DOMAIN NODE_CODE NODE_DISPLAY XRAY_PORT HY2_PORT XRAY_USER HY2_USER VLESS_LABEL HY2_LABEL XRAY_LABEL VLESS_FLOW
}

ensure_layout() {
  install -d -o root -g root -m 700 "${STATE_DIR}" "${XRAY_STATE_DIR}" "${HY2_STATE_DIR}"
  install -d -o root -g root -m 700 "${CONF_DIR}"
}

new_uuid() {
  if command -v uuidgen >/dev/null 2>&1; then
    uuidgen
  else
    cat /proc/sys/kernel/random/uuid
  fi
}

uri_escape() {
  python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"
}

title_suffix() {
  python3 -c 'import sys; print(sys.argv[1].replace("-", " ").title())' "$1"
}

init_xray_state() {
  load_env
  ensure_layout
  local uuid
  if [ -s "${XRAY_PRIMARY_UUID_FILE}" ]; then
    uuid="$(tr -d '[:space:]' < "${XRAY_PRIMARY_UUID_FILE}")"
  else
    uuid="$(new_uuid)"
  fi

  cat > "${XRAY_USERS}" <<CSV
name,email,uuid,label
primary,${XRAY_USER},${uuid},${VLESS_LABEL}
CSV

  printf '%s\n' "${uuid}" > "${XRAY_PRIMARY_UUID_FILE}"
  chmod 600 "${XRAY_USERS}" "${XRAY_PRIMARY_UUID_FILE}"
  chown root:root "${XRAY_USERS}" "${XRAY_PRIMARY_UUID_FILE}"
}

init_hy2_state() {
  load_env
  ensure_layout
  local pass
  if [ -s "${HY2_PRIMARY_PASS_FILE}" ]; then
    pass="$(tr -d '[:space:]' < "${HY2_PRIMARY_PASS_FILE}")"
  else
    pass="$(openssl rand -hex 16)"
  fi

  cat > "${HY2_USERS}" <<CSV
name,username,password,label
primary,${HY2_USER},${pass},${HY2_LABEL}
CSV

  printf '%s\n' "${pass}" > "${HY2_PRIMARY_PASS_FILE}"
  chmod 600 "${HY2_USERS}" "${HY2_PRIMARY_PASS_FILE}"
  chown root:root "${HY2_USERS}" "${HY2_PRIMARY_PASS_FILE}"
}

ensure_state() {
  ensure_layout
  [ -s "${XRAY_USERS}" ] || init_xray_state
  [ -s "${HY2_USERS}" ] || init_hy2_state
}

backup_configs() {
  ensure_layout
  local ts dir
  ts="$(date -u +%Y%m%d-%H%M%S)"
  dir="${BACKUP_DIR}/${ts}"
  install -d -o root -g root -m 700 "${dir}"

  cp -a "${XRAY_CONFIG}" "${dir}/xray.config.json.bak" 2>/dev/null || true
  cp -a "${HY2_CONFIG}" "${dir}/hysteria.config.yaml.bak" 2>/dev/null || true
  cp -a "${XRAY_USERS}" "${dir}/xray.users.csv.bak" 2>/dev/null || true
  cp -a "${HY2_USERS}" "${dir}/hy2.users.csv.bak" 2>/dev/null || true
  cp -a "${XRAY_PRIMARY_UUID_FILE}" "${dir}/xray_primary_uuid.txt.bak" 2>/dev/null || true
  cp -a "${HY2_PRIMARY_PASS_FILE}" "${dir}/hysteria2_primary.txt.bak" 2>/dev/null || true

  echo "backup saved to: ${dir}" >&2
}

user_exists() {
  local file="$1"
  local name="$2"
  awk -F, -v n="$name" 'NR>1 && $1==n {found=1} END{exit found?0:1}' "$file"
}

read_xray_user() {
  ensure_state
  local name="${1:-primary}"
  local row
  row="$(awk -F, -v n="$name" 'NR>1 && $1==n {print $1 "," $2 "," $3 "," $4; exit}' "${XRAY_USERS}")"
  [ -n "$row" ] || die "xray user not found: ${name}"
  IFS=, read -r XRAY_NAME XRAY_EMAIL XRAY_UUID XRAY_LABEL <<< "$row"
}

read_hy2_user() {
  ensure_state
  local name="${1:-primary}"
  local row
  row="$(awk -F, -v n="$name" 'NR>1 && $1==n {print $1 "," $2 "," $3 "," $4; exit}' "${HY2_USERS}")"
  [ -n "$row" ] || die "hysteria2 user not found: ${name}"
  IFS=, read -r HY2_NAME HY2_USERNAME HY2_PASSWORD HY2_LABEL_ROW <<< "$row"
}

write_xray_uuid() {
  local name="$1"
  local uuid="$2"
  ensure_state

  awk -F, -v OFS=, -v n="$name" -v u="$uuid" '
    NR==1 {print; next}
    $1==n {$3=u}
    {print}
  ' "${XRAY_USERS}" > "${XRAY_USERS}.tmp"

  install -m 600 -o root -g root "${XRAY_USERS}.tmp" "${XRAY_USERS}"
  rm -f "${XRAY_USERS}.tmp"

  if [ "$name" = "primary" ]; then
    printf '%s\n' "$uuid" > "${XRAY_PRIMARY_UUID_FILE}"
    chmod 600 "${XRAY_PRIMARY_UUID_FILE}"
    chown root:root "${XRAY_PRIMARY_UUID_FILE}"
  fi
}

write_hy2_password() {
  local name="$1"
  local password="$2"
  ensure_state

  awk -F, -v OFS=, -v n="$name" -v p="$password" '
    NR==1 {print; next}
    $1==n {$3=p}
    {print}
  ' "${HY2_USERS}" > "${HY2_USERS}.tmp"

  install -m 600 -o root -g root "${HY2_USERS}.tmp" "${HY2_USERS}"
  rm -f "${HY2_USERS}.tmp"

  if [ "$name" = "primary" ]; then
    printf '%s\n' "$password" > "${HY2_PRIMARY_PASS_FILE}"
    chmod 600 "${HY2_PRIMARY_PASS_FILE}"
    chown root:root "${HY2_PRIMARY_PASS_FILE}"
  fi
}

render_xray_to_file() {
  load_env
  ensure_state
  local out="$1"

  python3 - "$out" "$DOMAIN" "$XRAY_PORT" "$XRAY_USERS" <<'PY'
import csv, json, sys
out, domain, port, users_path = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]

with open(users_path, newline="") as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit("no xray users")

clients = []
for r in rows:
    clients.append({
        "id": r["uuid"],
        "email": r["email"],
        "flow": __import__("os").environ.get("VLESS_FLOW", "xtls-rprx-vision")
    })

data = {
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "tag": "vless-tls-" + __import__("os").environ.get("NODE_CODE", "core"),
      "listen": "0.0.0.0",
      "port": port,
      "protocol": "vless",
      "settings": {
        "clients": clients,
        "decryption": "none",
        "fallbacks": [
          {
            "dest": "127.0.0.1:8080",
            "xver": 1
          }
        ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "tls",
        "tlsSettings": {
          "serverName": domain,
          "alpn": ["http/1.1"],
          "certificates": [
            {
              "certificateFile": "/etc/xray/tls/fullchain.pem",
              "keyFile": "/etc/xray/tls/privkey.pem"
            }
          ]
        }
      },
      "sniffing": {
        "enabled": False
      }
    }
  ],
  "outbounds": [
    {
      "tag": "direct",
      "protocol": "freedom"
    },
    {
      "tag": "blocked",
      "protocol": "blackhole"
    }
  ]
}

with open(out, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
PY
}

render_hy2_to_file() {
  load_env
  ensure_state
  local out="$1"

  python3 - "$out" "$DOMAIN" "$HY2_PORT" "$HY2_USERS" <<'PY'
import csv, sys
out, domain, port, users_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

with open(users_path, newline="") as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit("no hy2 users")

with open(out, "w") as f:
    f.write(f"listen: :{port}\n\n")
    f.write("tls:\n")
    f.write("  cert: /etc/hysteria/tls/fullchain.pem\n")
    f.write("  key: /etc/hysteria/tls/privkey.pem\n")
    f.write("  sniGuard: strict\n\n")
    f.write("auth:\n")
    f.write("  type: userpass\n")
    f.write("  userpass:\n")
    for r in rows:
        f.write(f"    {r['username']}: {r['password']}\n")
    f.write("\n")
    f.write("masquerade:\n")
    f.write("  type: file\n")
    f.write("  file:\n")
    f.write(f"    dir: /var/www/{domain}/public\n")
    f.write("    rewriteLocation: true\n")
PY
}

apply_xray_config() {
  need_cmd python3
  local tmp
  tmp="$(mktemp)"
  render_xray_to_file "$tmp"
  python3 -m json.tool "$tmp" >/dev/null
  install -m 640 -o root -g xray "$tmp" "$XRAY_CONFIG"
  rm -f "$tmp"
  /usr/local/bin/xray run -test -config "$XRAY_CONFIG" >/dev/null
  runuser -u xray -- /usr/local/bin/xray run -test -config "$XRAY_CONFIG" >/dev/null
  systemctl restart "$XRAY_SERVICE"
}

apply_hy2_config() {
  local tmp
  tmp="$(mktemp)"
  render_hy2_to_file "$tmp"
  grep -q 'listen: :443' "$tmp" || die "rendered Hysteria2 config does not listen on :443"
  grep -q 'type: userpass' "$tmp" || die "rendered Hysteria2 config has no userpass auth"
  grep -q 'sniGuard: strict' "$tmp" || die "rendered Hysteria2 config has no strict sniGuard"
  grep -q 'type: file' "$tmp" || die "rendered Hysteria2 config has no file masquerade"
  install -m 640 -o root -g hysteria "$tmp" "$HY2_CONFIG"
  rm -f "$tmp"
  systemctl restart "$HY2_SERVICE"
}

label_for_xray() {
  local name="${1:-primary}"
  local custom="${2:-}"
  read_xray_user "$name"
  if [ -n "$custom" ]; then
    validate_no_csv_break "$custom" "profile label"
    printf '%s\n' "$custom"
  else
    printf '%s\n' "$XRAY_LABEL"
  fi
}

label_for_hy2() {
  local name="${1:-primary}"
  local custom="${2:-}"
  read_hy2_user "$name"
  if [ -n "$custom" ]; then
    validate_no_csv_break "$custom" "profile label"
    printf '%s\n' "$custom"
  else
    printf '%s\n' "$HY2_LABEL_ROW"
  fi
}

build_vless_uri() {
  load_env
  local name="${1:-primary}"
  local custom_label="${2:-}"
  read_xray_user "$name"

  local label encoded_label encoded_sni
  label="$(label_for_xray "$name" "$custom_label")"
  encoded_label="$(uri_escape "$label")"
  encoded_sni="$(uri_escape "$DOMAIN")"

  printf 'vless://%s@%s:%s?encryption=none&security=tls&type=tcp&flow=xtls-rprx-vision&headerType=none&sni=%s#%s\n' \
    "$XRAY_UUID" "$DOMAIN" "$XRAY_PORT" "$encoded_sni" "$encoded_label"
}

build_hy2_uri() {
  load_env
  local name="${1:-primary}"
  local custom_label="${2:-}"
  read_hy2_user "$name"

  local label encoded_label encoded_user encoded_pass encoded_sni
  label="$(label_for_hy2 "$name" "$custom_label")"
  encoded_label="$(uri_escape "$label")"
  encoded_user="$(uri_escape "$HY2_USERNAME")"
  encoded_pass="$(uri_escape "$HY2_PASSWORD")"
  encoded_sni="$(uri_escape "$DOMAIN")"

  printf 'hysteria2://%s:%s@%s:%s?sni=%s&insecure=0#%s\n' \
    "$encoded_user" "$encoded_pass" "$DOMAIN" "$HY2_PORT" "$encoded_sni" "$encoded_label"
}

cmd_help() {
  cat <<'USAGE'
vpnctl

CLI mode:
  vpnctl help
  vpnctl list [xray|hy2|all]
  vpnctl uri [xray|hy2|all] [user-name] [profile-label]
  vpnctl qr [xray|hy2] [user-name] [profile-label]
  vpnctl apply [xray|hy2|all]
  vpnctl add-user [xray|hy2] <suffix> [profile-label]
  vpnctl recreate [xray|hy2|all] [user-name]
  vpnctl delete-user [xray|hy2] <user-name>
  vpnctl service [status|start|stop|restart] [xray|hy2|all]

Naming:
  - primary Xray email: ${XRAY_USER}
  - primary Hysteria2 username: ${HY2_USER}
  - add-user hy2 gateway -> ${HY2_USER}-gateway
  - add-user xray gateway -> ${XRAY_USER}-gateway
  - default client labels: "${VLESS_LABEL}", "${HY2_LABEL}"

Security:
  - list/uri/qr print client secrets. Do not paste their output into chats or tickets.
  - recreate rotates secrets and invalidates old client configs for that user.
USAGE
}

cmd_list() {
  ensure_state
  local target="${1:-all}"

  case "$target" in
    xray)
      echo "protocol: xray/vless"
      column -s, -t "$XRAY_USERS"
      ;;
    hy2|hysteria|hysteria2)
      echo "protocol: hysteria2"
      column -s, -t "$HY2_USERS"
      ;;
    all)
      cmd_list xray
      echo
      cmd_list hy2
      ;;
    *) die "usage: vpnctl list [xray|hy2|all]" ;;
  esac
}

cmd_uri() {
  local target="${1:-all}"
  local name="${2:-primary}"
  local label="${3:-}"

  case "$target" in
    xray) build_vless_uri "$name" "$label" ;;
    hy2|hysteria|hysteria2) build_hy2_uri "$name" "$label" ;;
    all)
      build_vless_uri "$name" "$label"
      build_hy2_uri "$name" "$label"
      ;;
    *) die "usage: vpnctl uri [xray|hy2|all] [user-name] [profile-label]" ;;
  esac
}

cmd_qr() {
  need_cmd qrencode
  local target="${1:-}"
  local name="${2:-primary}"
  local label="${3:-}"
  local uri

  case "$target" in
    xray) uri="$(build_vless_uri "$name" "$label")" ;;
    hy2|hysteria|hysteria2) uri="$(build_hy2_uri "$name" "$label")" ;;
    *) die "usage: vpnctl qr [xray|hy2] [user-name] [profile-label]" ;;
  esac

  printf '%s\n' "$uri" | qrencode -t ANSIUTF8
}

cmd_apply() {
  local target="${1:-all}"
  backup_configs

  case "$target" in
    xray) apply_xray_config ;;
    hy2|hysteria|hysteria2) apply_hy2_config ;;
    all)
      apply_xray_config
      apply_hy2_config
      ;;
    *) die "usage: vpnctl apply [xray|hy2|all]" ;;
  esac

  echo "apply done: $target"
}

cmd_add_user() {
  load_env
  ensure_state

  local target="${1:-}"
  local suffix="${2:-}"
  local custom_label="${3:-}"

  [ -n "$target" ] || die "usage: vpnctl add-user [xray|hy2] <suffix> [profile-label]"
  [ -n "$suffix" ] || die "usage: vpnctl add-user [xray|hy2] <suffix> [profile-label]"
  validate_atom "$suffix" "user suffix"
  validate_no_csv_break "$custom_label" "profile label"

  local default_suffix_title
  default_suffix_title="$(title_suffix "$suffix")"

  backup_configs

  case "$target" in
    xray)
      if user_exists "$XRAY_USERS" "$suffix"; then
        die "xray user already exists: $suffix"
      fi
      local email uuid label
      email="vless-${NODE_CODE}-${suffix}"
      uuid="$(new_uuid)"
      label="${custom_label:-${NODE_DISPLAY} · VLESS · ${default_suffix_title}}"
      validate_no_csv_break "$label" "profile label"
      printf '%s,%s,%s,%s\n' "$suffix" "$email" "$uuid" "$label" >> "$XRAY_USERS"
      chmod 600 "$XRAY_USERS"
      chown root:root "$XRAY_USERS"
      apply_xray_config
      echo "xray user added: $suffix"
      ;;
    hy2|hysteria|hysteria2)
      if user_exists "$HY2_USERS" "$suffix"; then
        die "hysteria2 user already exists: $suffix"
      fi
      local username password label
      username="hy2-${NODE_CODE}-${suffix}"
      password="$(openssl rand -hex 16)"
      label="${custom_label:-${NODE_DISPLAY} · HY2 · ${default_suffix_title}}"
      validate_no_csv_break "$label" "profile label"
      printf '%s,%s,%s,%s\n' "$suffix" "$username" "$password" "$label" >> "$HY2_USERS"
      chmod 600 "$HY2_USERS"
      chown root:root "$HY2_USERS"
      apply_hy2_config
      echo "hysteria2 user added: $suffix"
      ;;
    *) die "usage: vpnctl add-user [xray|hy2] <suffix> [profile-label]" ;;
  esac
}

count_users_file() {
  local file="$1"
  awk -F, 'NR>1 && $1!="" {c++} END{print c+0}' "$file"
}

cmd_delete_user() {
  local target="${1:-}"
  local name="${2:-}"

  [ -n "$target" ] || die "usage: vpnctl delete-user [xray|hy2] <user-name>"
  [ -n "$name" ] || die "usage: vpnctl delete-user [xray|hy2] <user-name>"

  backup_configs

  case "$target" in
    xray)
      ensure_state
      user_exists "$XRAY_USERS" "$name" || die "xray user not found: $name"

      local count
      count="$(count_users_file "$XRAY_USERS")"
      [ "$count" -gt 1 ] || die "cannot delete the last xray user; use recreate to rotate credentials or add another user first"

      awk -F, -v OFS=, -v n="$name" 'NR==1 || $1!=n {print}' "$XRAY_USERS" > "${XRAY_USERS}.tmp"
      install -m 600 -o root -g root "${XRAY_USERS}.tmp" "$XRAY_USERS"
      rm -f "${XRAY_USERS}.tmp"

      if [ "$name" = "primary" ]; then
        rm -f "$XRAY_PRIMARY_UUID_FILE"
      fi

      apply_xray_config
      echo "xray user deleted: $name"
      ;;
    hy2|hysteria|hysteria2)
      ensure_state
      user_exists "$HY2_USERS" "$name" || die "hysteria2 user not found: $name"

      local count
      count="$(count_users_file "$HY2_USERS")"
      [ "$count" -gt 1 ] || die "cannot delete the last hysteria2 user; use recreate to rotate credentials or add another user first"

      awk -F, -v OFS=, -v n="$name" 'NR==1 || $1!=n {print}' "$HY2_USERS" > "${HY2_USERS}.tmp"
      install -m 600 -o root -g root "${HY2_USERS}.tmp" "$HY2_USERS"
      rm -f "${HY2_USERS}.tmp"

      if [ "$name" = "primary" ]; then
        rm -f "$HY2_PRIMARY_PASS_FILE"
      fi

      apply_hy2_config
      echo "hysteria2 user deleted: $name"
      ;;
    *)
      die "usage: vpnctl delete-user [xray|hy2] <user-name>"
      ;;
  esac
}


cmd_recreate() {
  local target="${1:-}"
  local name="${2:-primary}"

  backup_configs

  case "$target" in
    xray)
      read_xray_user "$name"
      write_xray_uuid "$name" "$(new_uuid)"
      apply_xray_config
      echo "xray user recreated: $name"
      ;;
    hy2|hysteria|hysteria2)
      read_hy2_user "$name"
      write_hy2_password "$name" "$(openssl rand -hex 16)"
      apply_hy2_config
      echo "hysteria2 user recreated: $name"
      ;;
    all)
      [ "$name" = "primary" ] || die "recreate all supports only primary user"
      read_xray_user primary
      read_hy2_user primary
      write_xray_uuid primary "$(new_uuid)"
      write_hy2_password primary "$(openssl rand -hex 16)"
      apply_xray_config
      apply_hy2_config
      echo "xray and hysteria2 primary users recreated"
      ;;
    *) die "usage: vpnctl recreate [xray|hy2|all] [user-name]" ;;
  esac
}

cmd_service() {
  local action="${1:-}"
  local target="${2:-all}"

  case "$action" in
    status)
      case "$target" in
        xray) systemctl status "$XRAY_SERVICE" --no-pager -l || true ;;
        hy2|hysteria|hysteria2) systemctl status "$HY2_SERVICE" --no-pager -l || true ;;
        all)
          systemctl status "$XRAY_SERVICE" --no-pager -l || true
          echo
          systemctl status "$HY2_SERVICE" --no-pager -l || true
          ;;
        *) die "usage: vpnctl service status [xray|hy2|all]" ;;
      esac
      ;;
    start|stop|restart)
      case "$target" in
        xray) systemctl "$action" "$XRAY_SERVICE" ;;
        hy2|hysteria|hysteria2) systemctl "$action" "$HY2_SERVICE" ;;
        all)
          systemctl "$action" "$XRAY_SERVICE"
          systemctl "$action" "$HY2_SERVICE"
          ;;
        *) die "usage: vpnctl service ${action} [xray|hy2|all]" ;;
      esac
      echo "service $action done: $target"
      ;;
    *) die "usage: vpnctl service [status|start|stop|restart] [xray|hy2|all]" ;;
  esac
}

service_menu() {
  while true; do
    clear_screen
    cat <<'MENU'
vpnctl -> Service menu

  1) Status: all
  2) Status: Xray
  3) Status: Hysteria2
  4) Start: all
  5) Start: Xray
  6) Start: Hysteria2
  7) Stop: all
  8) Stop: Xray
  9) Stop: Hysteria2
  10) Restart: all
  11) Restart: Xray
  12) Restart: Hysteria2

  0) Back
MENU
    echo
    read -r -p "Select: " choice || true
    case "${choice:-}" in
      1) cmd_service status all; pause ;;
      2) cmd_service status xray; pause ;;
      3) cmd_service status hy2; pause ;;
      4) cmd_service start all; pause ;;
      5) cmd_service start xray; pause ;;
      6) cmd_service start hy2; pause ;;
      7)
        if confirm_action 'Stop Xray and Hysteria2? [y/N]: '; then cmd_service stop all; fi
        pause
        ;;
      8)
        if confirm_action 'Stop Xray? [y/N]: '; then cmd_service stop xray; fi
        pause
        ;;
      9)
        if confirm_action 'Stop Hysteria2? [y/N]: '; then cmd_service stop hy2; fi
        pause
        ;;
      10) cmd_service restart all; pause ;;
      11) cmd_service restart xray; pause ;;
      12) cmd_service restart hy2; pause ;;
      0) return 0 ;;
      *) echo 'Invalid selection'; pause ;;
    esac
  done
}

main_menu() {
  while true; do
    clear_screen
    cat <<'MENU'
vpnctl -> Main menu

  1) Show all users
  2) Show Xray users
  3) Show Hysteria2 users
  4) Show all primary URIs
  5) Show Xray URI
  6) Show Hysteria2 URI
  7) Show Xray QR
  8) Show Hysteria2 QR
  9) Apply configs from current state
  10) Add Xray user
  11) Add Hysteria2 user
  12) Recreate Xray user
  13) Recreate Hysteria2 user
  14) Recreate both primary users
  15) Service management menu
  16) Help

  0) Exit
MENU
    echo
    read -r -p "Select: " choice || true
    case "${choice:-}" in
      1) cmd_list all; pause ;;
      2) cmd_list xray; pause ;;
      3) cmd_list hy2; pause ;;
      4) cmd_uri all; pause ;;
      5)
        read -r -p "User name [primary]: " n || true
        cmd_uri xray "${n:-primary}"
        pause
        ;;
      6)
        read -r -p "User name [primary]: " n || true
        cmd_uri hy2 "${n:-primary}"
        pause
        ;;
      7)
        read -r -p "User name [primary]: " n || true
        cmd_qr xray "${n:-primary}"
        pause
        ;;
      8)
        read -r -p "User name [primary]: " n || true
        cmd_qr hy2 "${n:-primary}"
        pause
        ;;
      9) cmd_apply all; pause ;;
      10)
        read -r -p "Suffix, e.g. gateway: " suffix || true
        [ -n "${suffix:-}" ] && cmd_add_user xray "$suffix"
        pause
        ;;
      11)
        read -r -p "Suffix, e.g. gateway: " suffix || true
        [ -n "${suffix:-}" ] && cmd_add_user hy2 "$suffix"
        pause
        ;;
      12)
        read -r -p "User name [primary]: " n || true
        if confirm_action "Recreate Xray user ${n:-primary}? Old client config will stop working. [y/N]: "; then cmd_recreate xray "${n:-primary}"; fi
        pause
        ;;
      13)
        read -r -p "User name [primary]: " n || true
        if confirm_action "Recreate Hysteria2 user ${n:-primary}? Old client config will stop working. [y/N]: "; then cmd_recreate hy2 "${n:-primary}"; fi
        pause
        ;;
      14)
        if confirm_action 'Recreate both primary users? Old primary client configs will stop working. [y/N]: '; then cmd_recreate all; fi
        pause
        ;;
      15) service_menu ;;
      16) cmd_help; pause ;;
      0) exit 0 ;;
      *) echo 'Invalid selection'; pause ;;
    esac
  done
}

main() {
  load_env
  ensure_state

  if [ $# -eq 0 ]; then
    exec /usr/local/bin/maintctl
  fi

  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    help|-h|--help) cmd_help ;;
    list) cmd_list "${1:-all}" ;;
    uri) cmd_uri "${1:-all}" "${2:-primary}" "${3:-}" ;;
    qr) cmd_qr "${1:-}" "${2:-primary}" "${3:-}" ;;
    apply) cmd_apply "${1:-all}" ;;
    add-user) cmd_add_user "$@" ;;
    recreate) cmd_recreate "${1:-}" "${2:-primary}" ;;
    delete-user) cmd_delete_user "$@" ;;
    service) cmd_service "$@" ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"
