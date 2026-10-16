#!/usr/bin/python3
"""Project the active gh credential into native clients, then apply changed connections."""
import argparse
import asyncio
import copy
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import tomllib

import yaml

CORE_HOME = Path('/home/core')
STATE = CORE_HOME / '.local/state/github-mcp-token-sync/status.json'
CLIENTS = {
    'codex': (CORE_HOME / '.codex/config.toml', tomllib.loads, 'mcp_servers', 'http_headers'),
    'hermes': (CORE_HOME / '.hermes/config.yaml', yaml.safe_load, 'mcp_servers', 'headers'),
    'antigravity': (CORE_HOME / '.gemini/config/mcp_config.json', json.loads, 'mcpServers', 'headers'),
}
ENDPOINT = 'http://127.0.0.1:18082/'


class SyncError(RuntimeError):
    """Only constant, non-secret error codes may reach status/journal."""


def command(argv, timeout=30):
    return subprocess.run(argv, check=True, capture_output=True, text=True,
                          stdin=subprocess.DEVNULL, timeout=timeout).stdout


def credential():
    # The active stored gh account is authoritative, rather than ambient token overrides.
    environment = dict(os.environ, GH_CONFIG_DIR=str(CORE_HOME / '.config/gh'), GH_PROMPT_DISABLED='1')
    for name in ('GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN'):
        environment.pop(name, None)
    result = subprocess.run(['/usr/bin/gh', 'auth', 'token', '--hostname', 'github.com'],
                            env=environment, capture_output=True, text=True,
                            stdin=subprocess.DEVNULL, timeout=15)
    token = result.stdout.strip()
    if result.returncode or not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise SyncError('GH_CREDENTIAL_UNAVAILABLE')
    return token


def prepare(client, token):
    path, load, section, headers_key = CLIENTS[client]
    if path.is_symlink() or path.stat().st_uid != os.getuid() or path.stat().st_mode & 0o777 != 0o600:
        raise SyncError('CLIENT_FILE_METADATA_DRIFT')
    original = path.read_text()
    before = load(original)
    github = before[section]['github']
    if github.get('url', github.get('serverUrl')) != ENDPOINT or 'command' in github:
        raise SyncError('GITHUB_TRANSPORT_DRIFT')
    if github.get('bearer_token_env_var') or github.get('oauth') or github.get('authProviderType'):
        raise SyncError('GITHUB_AUTH_SOURCE_DRIFT')
    if any(key.lower() == 'authorization' for key in github.get('env_http_headers', {})):
        raise SyncError('GITHUB_AUTH_SOURCE_DRIFT')
    headers = github[headers_key]
    auth = [key for key in headers if key.lower() == 'authorization']
    if len(auth) != 1 or not isinstance(headers[auth[0]], str):
        raise SyncError('AUTH_HEADER_DRIFT')
    key = auth[0]
    value = 'Bearer ' + token
    expected = copy.deepcopy(before)
    expected[section]['github'][headers_key][key] = value
    if headers[key] == value:
        return path, original, original
    if client == 'codex':
        block = re.search(r'(?ms)^\[mcp_servers\.github\]\n.*?(?=^\[|\Z)', original)
        if not block or block.group().count(json.dumps(headers[key])) != 1:
            raise SyncError('CODEX_HEADER_LAYOUT_DRIFT')
        replacement = block.group().replace(json.dumps(headers[key]), json.dumps(value), 1)
        updated = original[:block.start()] + replacement + original[block.end():]
    elif client == 'hermes':
        block = re.search(r'(?ms)^  github:\n.*?(?=^  \S|^\S|\Z)', original)
        if not block:
            raise SyncError('HERMES_HEADER_LAYOUT_DRIFT')
        replacement, count = re.subn(r'(?m)^(      ' + re.escape(key) + r':)[^\n]*$',
                                      lambda m: m[1] + ' ' + json.dumps(value), block.group())
        if count != 1:
            raise SyncError('HERMES_HEADER_LAYOUT_DRIFT')
        updated = original[:block.start()] + replacement + original[block.end():]
    else:
        updated = json.dumps(expected, indent=2) + '\n'
    if load(updated) != expected:
        raise SyncError('UNRELATED_CONFIG_CHANGE')
    return path, original, updated


def atomic_write(path, text):
    fd, name = tempfile.mkstemp(prefix='.github-mcp-token-sync.', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'w') as output:
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def save(status):
    atomic_write(STATE, json.dumps(status, sort_keys=True) + '\n')


async def codex_reload():
    from websockets.asyncio.client import unix_connect
    daemon = json.loads(command([str(CORE_HOME / '.local/bin/codex'), 'app-server', 'daemon', 'version']))
    if daemon['status'] != 'running':
        return 'not_running'
    async with unix_connect(daemon['socketPath'], uri='ws://localhost/',
                            open_timeout=10, max_size=20 * 1024 * 1024) as socket:
        async def rpc(identifier, method, params):
            await socket.send(json.dumps({'id': identifier, 'method': method, 'params': params}))
            async with asyncio.timeout(30):
                async for message in socket:
                    response = json.loads(message)
                    if response.get('id') == identifier:
                        if 'error' in response:
                            raise SyncError('CODEX_RPC_REJECTED')
                        return response['result']
            raise SyncError('CODEX_RPC_DISCONNECTED')
        await rpc(1, 'initialize', {'clientInfo': {'name': 'edge_github_token_sync', 'version': '1'}})
        await socket.send(json.dumps({'method': 'initialized', 'params': {}}))
        await rpc(2, 'config/mcpServer/reload', {})
    return 'mcp_reloaded'


def unit_state(unit):
    raw = command(['systemctl', '--user', 'show', unit, '-p', 'ActiveState', '-p', 'MainPID'])
    values = dict(line.split('=', 1) for line in raw.splitlines() if '=' in line)
    return values['ActiveState'], int(values['MainPID'])


def refresh_unit(unit, graceful=False):
    state, previous = unit_state(unit)
    if state == 'inactive':
        return 'not_running'
    if state not in ('active', 'activating'):
        raise SyncError('CLIENT_UNIT_UNHEALTHY')
    command(['systemctl', '--user', 'reload' if graceful else 'restart', unit], timeout=80)
    deadline = time.monotonic() + (210 if graceful else 45)
    stable = None
    while time.monotonic() < deadline:
        state, pid = unit_state(unit)
        if state == 'active' and pid > 0 and pid != previous:
            if stable == pid:
                return pid
            stable = pid
        else:
            stable = None
        time.sleep(2)
    raise SyncError('CLIENT_REPLACEMENT_TIMEOUT')


def antigravity_connected(pid):
    if pid == 'not_running':
        return
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        for path in sorted((CORE_HOME / '.gemini/antigravity-cli/log').glob('cli-*.log'), reverse=True):
            with path.open(errors='replace') as stream:
                header = stream.read(16384)
                if not re.search(rf'Starting language server process with pid {pid}\b', header):
                    continue
                statuses = re.findall(r'Connection status: (\S+)', header + stream.read())
            if statuses and statuses[-1] == 'Connected':
                return
            break
        time.sleep(2)
    raise SyncError('ANTIGRAVITY_CONNECTION_TIMEOUT')


def apply(client):
    if client == 'codex':
        return asyncio.run(codex_reload())
    if client == 'hermes':
        gateway = refresh_unit('hermes-gateway.service', graceful=True)
        dashboard = refresh_unit('hermes-dashboard.service')
        return {'gateway': gateway, 'dashboard': dashboard}
    pid = refresh_unit('antigravity-cli-daemon.service')
    antigravity_connected(pid)
    return pid


def synchronize(force=False):
    try:
        status = json.loads(STATE.read_text())
    except FileNotFoundError:
        status = {'schema': 1, 'pending_reload': [], 'last_success_at': None}
    pending = set(status['pending_reload'])
    if pending - CLIENTS.keys():
        raise SyncError('STATE_CLIENT_DRIFT')
    status.update(result='RUNNING', started_at=time.time(), changed_clients=[])
    save(status)
    try:
        token = credential()
        plans = {client: prepare(client, token) for client in CLIENTS}
        changed = [client for client, (_, before, after) in plans.items() if before != after or force]
        pending.update(changed)
        status.update(changed_clients=changed, pending_reload=sorted(pending))
        # Persist reload obligations before any config write, including partial failures.
        save(status)
        for client in changed:
            path, before, after = plans[client]
            if path.read_text() != before:
                raise SyncError('CONCURRENT_CONFIG_EDIT')
            atomic_write(path, after)
        for client in CLIENTS:
            if client not in pending:
                continue
            result = apply(client)
            pending.remove(client)
            status.setdefault('applied', {})[client] = {'at': time.time(), 'result': result}
            status['pending_reload'] = sorted(pending)
            save(status)
        status.update(result='PASS', last_success_at=time.time())
        status.pop('error', None)
        save(status)
        print('GITHUB_MCP_TOKEN_SYNC=PASS|CHANGED=' + ','.join(changed))
        return 0
    except Exception as error:
        status.update(result='FAIL', error=str(error) if isinstance(error, SyncError) else type(error).__name__)
        save(status)
        print('GITHUB_MCP_TOKEN_SYNC=FAIL|ERROR=' + status['error'])
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Reapply the current credential and refresh clients')
    arguments = parser.parse_args()
    STATE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (STATE.parent / 'lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return synchronize(arguments.refresh)


if __name__ == '__main__':
    raise SystemExit(main())
