#!/usr/bin/env python3
"""Execute the real Ansible control flow against isolated command fixtures."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for case in ('success', 'driver-error', 'refresh-error', 'preflight-error'):
    with tempfile.TemporaryDirectory(prefix='individual-playbook-test.') as temporary:
        base = Path(temporary)
        trace = base / 'trace'
        def executable(name, text):
            p = base / name; p.write_text(text); p.chmod(0o755); return p
        executable('sudo', '#!/bin/sh\n[ "$1" = -n ] && shift\nexec "$@"\n')
        manual = executable('manual-update', '''#!/bin/sh
if [ "$2" = --preflight ]; then
 echo preflight >> "$TRACE"
 [ "$CASE" = preflight-error ] && exit 91
 exit 0
fi
echo driver >> "$TRACE"
if [ "$CASE" = driver-error ]; then echo 'fixture driver failure' >&2; exit 23; fi
echo UPDATE_RESULT=STALWART:SUCCESS
''')
        refresh = executable('maintenance-refresh', '''#!/bin/sh
echo refresh >> "$TRACE"
if [ "$CASE" = refresh-error ] && [ -f "$TRACE.post" ]; then exit 12; fi
touch "$TRACE.post"
echo READ_ONLY_REFRESH=PASS
''')
        text = (ROOT / 'playbooks/update-unit.yml').read_text()
        text = text.replace('/opt/edge-maintenance/scripts/manual-update', str(manual))
        text = text.replace('/opt/edge-maintenance/scripts/maintenance-refresh', str(refresh))
        playbook = base / 'update.yml'; playbook.write_text(text)
        config = base / 'ansible.cfg'; config.write_text('[defaults]\n')
        env = {**os.environ, 'PATH': str(base) + ':' + os.environ['PATH'], 'TRACE': str(trace), 'CASE': case,
               'ANSIBLE_LOCAL_TEMP': str(base / 'ansible-tmp'), 'ANSIBLE_REMOTE_TEMP': str(base / 'remote-tmp'),
               'ANSIBLE_NOCOLOR': '1', 'ANSIBLE_CONFIG': str(config)}
        result = subprocess.run(['ansible-playbook', '-i', 'localhost,', str(playbook), '-e', 'edge_update_target=STALWART'],
                                env=env, capture_output=True, text=True, timeout=60)
        assert trace.exists(), result.stdout + result.stderr
        calls = trace.read_text().splitlines()
        if case == 'preflight-error':
            assert result.returncode != 0 and calls == ['refresh', 'preflight'], result.stdout + result.stderr
        else:
            assert calls == ['refresh', 'preflight', 'driver', 'refresh'], 'driver failure skipped the final refresh: ' + repr(calls)
            assert (result.returncode == 0) == (case == 'success'), result.stdout + result.stderr
        if case == 'driver-error': assert 'fixture driver failure' in result.stdout + result.stderr
print('INDIVIDUAL_ANSIBLE_FAILURE_ISOLATION=PASS|CASES=4|REAL_UPDATES=NO|SERVICE_CALLS=NO')
