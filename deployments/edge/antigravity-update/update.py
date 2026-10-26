#!/usr/bin/python3
"""Schedule the vendor updater and apply its result to the native daemon."""
import json
import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path

HOME = Path.home()
BINARY = HOME / '.local/bin/agy'
STATE = HOME / '.local/state/antigravity-native-update'
LOGS = HOME / '.gemini/antigravity-cli/log'
DAEMON = 'antigravity-cli-daemon.service'
ENV = {**os.environ, 'PATH': f'{HOME}/.local/bin:/usr/local/bin:/usr/bin:/bin',
       'AGY_CLI_HIDE_ACCOUNT_INFO': 'true'}
ENV.pop('AGY_CLI_DISABLE_AUTO_UPDATE', None)


def log(message):
    print(message, flush=True)


def atomic_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, sort_keys=True) + '\n')
    os.replace(temporary, path)


def version(binary):
    return subprocess.check_output(
        [str(binary), '--version'], env={**ENV, 'AGY_CLI_DISABLE_AUTO_UPDATE': 'true'},
        stdin=subprocess.DEVNULL, text=True, timeout=10).strip()


def daemon_pid():
    raw = subprocess.check_output(
        ['systemctl', '--user', 'show', DAEMON, '-p', 'ActiveState', '-p', 'MainPID'],
        text=True, timeout=10)
    properties = dict(line.split('=', 1) for line in raw.splitlines() if '=' in line)
    pid = int(properties.get('MainPID', 0))
    if properties.get('ActiveState') != 'active' or pid <= 0:
        raise RuntimeError('native daemon is not running')
    return pid


def applied(pid):
    try:
        return os.path.samefile(f'/proc/{pid}/exe', BINARY)
    except FileNotFoundError:
        return False


def connected_log(pid, expected):
    for path in sorted(LOGS.glob('cli-*.log'), reverse=True):
        with path.open(errors='replace') as stream:
            header = stream.read(16384)
            if not re.search(rf'Starting language server process with pid {pid}\b', header):
                continue
            text = header + stream.read()
        versions = re.findall(r'Language server version: (\S+)', header)
        statuses = re.findall(r'Connection status: (\S+)', text)
        if versions == [expected] and statuses and statuses[-1] == 'Connected':
            return str(path)
    return None


def wait_ready(expected, timeout=60):
    deadline = time.monotonic() + timeout
    stable_pid = None
    while time.monotonic() < deadline:
        try:
            pid = daemon_pid()
            path = connected_log(pid, expected) if applied(pid) else None
        except (OSError, RuntimeError, subprocess.SubprocessError):
            pid, path = None, None
        if path and pid == stable_pid:
            return pid, path
        stable_pid = pid if path else None
        time.sleep(2)
    raise RuntimeError('daemon did not stay on the installed binary with Connected status within 60s')


def run_update():
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    status_path = STATE / 'status.json'
    try:
        previous = json.loads(status_path.read_text())
    except (OSError, ValueError):
        previous = {}
    status = {'result': 'RUNNING', 'started_at': time.time(),
              'last_success_at': previous.get('last_success_at')}
    candidate = STATE / 'candidate-agy'
    candidate_complete = False
    atomic_json(status_path, status)
    log(f"CHECK_STARTED={status['started_at']}")
    try:
        pid = daemon_pid()
        status['before_version'] = version(BINARY)
        # Preserve the running executable even if an interactive CLI updated the disk first.
        running = Path(f'/proc/{pid}/exe')
        running_version = version(running)
        shutil.copyfile(running, candidate)
        candidate.chmod(0o700)
        candidate_complete = True
        log(f"PRE_VERSION={status['before_version']} PRE_PID={pid}\nNATIVE_UPDATE_BEGIN=YES")
        update = subprocess.run([str(BINARY), 'update'], env=ENV,
                                stdin=subprocess.DEVNULL, timeout=720)
        # Retain the last running version before attempting to apply a changed executable.
        if not applied(pid):
            os.replace(candidate, STATE / 'previous-agy')
            atomic_json(STATE / 'previous.json', {'version': running_version})
        update.check_returncode()
        status['after_version'] = version(BINARY)
        status['restarted'] = not applied(daemon_pid())
        log(f"POST_VERSION={status['after_version']}\n"
            f"UPDATE_CHANGED={'YES' if status['before_version'] != status['after_version'] else 'NO'}\n"
            f"DAEMON_RESTART={'YES' if status['restarted'] else 'NO'}")
        if status['restarted']:
            subprocess.run(['systemctl', '--user', 'restart', DAEMON], check=True, timeout=45)
        status['pid'], status['daemon_log'] = wait_ready(status['after_version'])
        # Recovery material is temporary: the installed daemon is now verified.
        for name in ('previous-agy', 'previous.json'):
            (STATE / name).unlink(missing_ok=True)
        status.update(result='PASS', completed_at=time.time())
        status['last_success_at'] = status['completed_at']
        log(f"DAEMON_APPLIED=YES pid={status['pid']} version={status['after_version']}\n"
            f"DAEMON_CONNECTED=YES log={status['daemon_log']}")
    except Exception as error:
        status.update(result='FAIL', completed_at=time.time(), error=str(error))
        log(f'ERROR={error}')
    finally:
        if candidate_complete and candidate.exists() and not applied(pid):
            os.replace(candidate, STATE / 'previous-agy')
            atomic_json(STATE / 'previous.json', {'version': running_version})
        candidate.unlink(missing_ok=True)
        atomic_json(status_path, status)
    log(f"AGY_NATIVE_UPDATE={status['result']}")
    return 0 if status['result'] == 'PASS' else 1


def interrupted(signum, frame):
    raise RuntimeError(f'update interrupted by signal {signum}')


if __name__ == '__main__':
    os.umask(0o077)
    signal.signal(signal.SIGTERM, interrupted)
    raise SystemExit(run_update())
