#!/usr/bin/env python3
"""Exercise real release preparation with local archives and no service calls."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for case in ('success', 'missing-archive', 'missing-checksums', 'checksum', 'version'):
    with tempfile.TemporaryDirectory(prefix='native-release-test.') as temporary:
        base = Path(temporary)
        candidate = base / 'semaphore'
        candidate.write_text('#!/bin/sh\necho ' + ('0.0.0' if case == 'version' else '2.19.18-fixture') + '\n')
        candidate.chmod(0o755)
        archive = base / 'semaphore_2.19.18_linux_amd64.tar.gz'
        with tarfile.open(archive, 'w:gz') as handle:
            handle.add(candidate, arcname='semaphore')
        checksum = base / 'semaphore_2.19.18_checksums.txt'
        digest = '0' * 64 if case == 'checksum' else hashlib.sha256(archive.read_bytes()).hexdigest()
        checksum.write_text(digest + '  ' + archive.name + '\n')
        assets = [archive, checksum]
        if case == 'missing-archive': assets.remove(archive)
        if case == 'missing-checksums': assets.remove(checksum)
        release = {'tag_name': 'v2.19.18', 'assets': [
            {'name': p.name, 'browser_download_url': 'https://fixture.invalid/' + p.name} for p in assets]}
        (base / 'release.json').write_text(json.dumps(release))
        state = base / 'state'
        state.write_text('#!/usr/bin/env python3\nimport json,sys\nwith open(' + repr(str(base / 'state.log')) + ',"a") as f:f.write(json.dumps(sys.argv[1:])+"\\n")\n')
        state.chmod(0o755)
        header = '''
curl() {
  if [[ "$*" == *api.github.com* ]]; then cat BASE/release.json; return; fi
  printf '%s\\n' "$*" >> BASE/download.log
  local destination=''
  while [ "$#" -gt 1 ]; do
    if [ "$1" = -o ]; then destination="$2"; shift 2; else shift; fi
  done
  [[ "$1" == https://fixture.invalid/* ]] || return 98
  cp "BASE/${1##*/}" "$destination"
}
install() { [ "$1" = -d ] && mkdir -p "${@: -1}"; }
systemctl() { echo FORBIDDEN_SERVICE_CALL >&2; return 99; }
'''.replace('BASE', str(base))
        source = (ROOT / 'scripts/update-github-binary').read_text()
        source = source.replace('/opt/edge-maintenance/scripts/controller-update-state', str(state))
        source = source.replace('/var/backups/edge-maintenance', str(base / 'backups'))
        source = source.replace('work_root=/tmp', 'work_root=' + str(base / 'work'))
        (base / 'work').mkdir()
        driver = base / 'driver'
        driver.write_text('#!/bin/bash\n' + header + source)
        result = subprocess.run(['bash', str(driver), 'SEMAPHORE', 'fixture-operation'], capture_output=True, text=True)
        states = [json.loads(line) for line in (base / 'state.log').read_text().splitlines()]
        installs = [s for s in states if s[0] == 'install']
        if case == 'success':
            assert result.returncode == 0 and len(installs) == 1, result.stdout + result.stderr
            assert installs[0][2:4] == ['2.19.18', 'fixture-operation']
        else:
            assert result.returncode != 0 and not installs, (case, result.stdout, result.stderr)
            assert states[-1][0] == 'error' and states[-1][3], states
            if case.startswith('missing'):
                assert not (base / 'download.log').exists(), 'missing metadata reached the download step'
                assert 'Missing release asset' in result.stderr
        assert not list((base / 'work').iterdir()), 'preparation left temporary files'
print('NATIVE_RELEASE_PREPARATION=PASS|CASES=5|NETWORK=NO|SERVICE_CALLS=NO')
