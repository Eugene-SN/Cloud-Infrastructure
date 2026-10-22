#!/usr/bin/env python3
"""Check scoped refresh and cache freshness without network or update commands."""
import copy
import datetime as dt
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

with tempfile.TemporaryDirectory(prefix="maintenance-target-test.") as directory:
    base = Path(directory)
    scripts = base / "scripts"
    scripts.mkdir()
    for name in ("maintenance-refresh", "maintenance-status-render", "maintenance-targets-refresh"):
        shutil.copy2(ROOT / "scripts" / name, scripts / name)
    def executable(name, text):
        path = scripts / name
        path.write_text(text)
        path.chmod(0o755)
    executable("maintenance-versions-collector", "#!/bin/sh\nprintf '%s\\n' 'VERSION|SCOPE=EDGE|COMPONENT=WEBLATE|INSTALLED=2026.10.1|STABLE=2026.10.1|STATUS=CURRENT|SOURCE=FIXTURE|APPLICATION_VERSION=2026.10.1|AVAILABLE_VERSION=2026.10.1|IMAGE_REPOSITORY=weblate/weblate|IMAGE_TAG=latest|RUNNING_DIGEST=sha256:a|REMOTE_DIGEST=sha256:a|UPDATE_REASON=CURRENT'\n")
    executable("maintenance-actions-render", "#!/bin/sh\nexit 0\n")
    executable("apt-get", "#!/bin/sh\necho unexpected-apt >> \"$APT_TRACE\"\nexit 1\n")
    raw = json.loads(Path('/var/www/maintenance-status/status.json').read_text())
    cache = json.loads(Path('/var/www/maintenance-status/maintenance.json').read_text())
    old = "2000-01-01T00:00:00+00:00"
    raw['generated_at'] = cache['generated_at'] = old
    for row in cache['rows']:
        row['checked_at'] = old
    original = copy.deepcopy(cache)
    status = base / 'status.json'
    output = base / 'maintenance.json'
    status.write_text(json.dumps(raw))
    output.write_text(json.dumps(cache))
    trace = base / 'apt-trace'
    env = {**os.environ, 'EDGE_MAINTENANCE_BASE': str(base),
           'EDGE_MAINTENANCE_REFRESH_LOCK': str(base / 'lock'),
           'EDGE_MAINTENANCE_STATUS_FILE': str(status),
           'EDGE_MAINTENANCE_OUTPUT_FILE': str(output),
           'APT_TRACE': str(trace), 'PATH': str(scripts) + ':' + os.environ['PATH']}
    result = subprocess.run([str(scripts / 'maintenance-refresh'), '--target', 'WEBLATE'], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert not trace.exists(), 'a Weblate-only refresh must not invoke APT'
    refreshed = json.loads(output.read_text())
    assert refreshed['generated_at'] == old, 'do not renew the full-scan timestamp'
    for row in refreshed['rows']:
        previous = next(item for item in original['rows'] if item['component'] == row['component'])
        if row['component'] == 'WEBLATE':
            assert row['status'] == 'CURRENT' and row['checked_at'] != old
        else:
            assert row == previous, 'unrelated row changed: ' + row['component']
    module = runpy.run_path(ROOT / 'scripts/manual-update')
    validate = module['require_fresh_update']
    refreshed['rows'][0]['status'] = 'UPDATE_AVAILABLE'
    selected = next(row for row in refreshed['rows'] if row['component'] == 'WEBLATE')
    selected['status'] = 'UPDATE_AVAILABLE'
    output.write_text(json.dumps(refreshed))
    with patch.dict(validate.__globals__, STATUS_CACHE=output):
        assert validate('WEBLATE', 300)['component'] == 'WEBLATE'
        other = next(row for row in refreshed['rows'] if row['component'] != 'WEBLATE')
        try:
            validate(other['component'], 300)
        except RuntimeError as error:
            assert 'stale' in str(error)
        else:
            raise AssertionError('unrelated stale row became fresh')
    before = status.read_bytes()
    failed = subprocess.run([str(scripts / 'maintenance-refresh'), '--target', 'UNKNOWN'], env=env, capture_output=True, text=True)
    assert failed.returncode != 0 and status.read_bytes() == before

    # Full Scan and APT-only refresh must still do the actual APT probe.
    executable('apt-get', '#!/bin/sh\necho apt-probe >> "$APT_TRACE"\nexit 0\n')
    executable('maintenance-versions-collector', '#!/usr/bin/env python3\nimport json,os\nj=json.load(open(os.environ["FIXTURE_RAW"]))\nfor r in j["rows"]:\n print("VERSION|"+"|".join(k+"="+str(v) for k,v in r.items() if k!="CHECKED_AT"))\n')
    fixture_raw = base / 'fixture-raw.json'
    fixture_raw.write_text(json.dumps(raw))
    env['FIXTURE_RAW'] = str(fixture_raw)
    result = subprocess.run([str(scripts / 'maintenance-refresh')], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert trace.exists() and json.loads(output.read_text())['generated_at'] != old
    trace.unlink()
    raw['rows'] = [r for r in raw['rows'] if r['COMPONENT'] in {'NGINX', 'CERTBOT', 'UFW', 'DOCKER_ENGINE', 'DOCKER_COMPOSE', 'CONTAINERD', 'NETBIRD', 'SYNCTHING'}]
    fixture_raw.write_text(json.dumps(raw))
    result = subprocess.run([str(scripts / 'maintenance-refresh'), '--target', 'APT_EDGE'], env=env, capture_output=True, text=True)
    assert result.returncode == 0 and trace.exists(), result.stderr

    # Exercise the real collector with only its Docker boundary replaced.
    executable('docker', '''#!/usr/bin/env python3
import json,os,sys
a=sys.argv[1:]
with open(os.environ['DOCKER_TRACE'],'a') as f:f.write(json.dumps(a)+'\\n')
digest='sha256:'+'a'*64
if a[:2]==['inspect','weblate']:
 print('true' if 'Running' in a[-1] else digest)
elif a[:2]==['image','inspect']:
 print(digest)
elif a[:2]==['exec','weblate']:
 print('2026.10.1')
elif a[:3]==['buildx','imagetools','inspect'] and a[3]=='weblate/weblate:latest':
 print(json.dumps(digest)+' '+json.dumps({'config':{'Labels':{'org.opencontainers.image.version':'2026.10.1'}}}))
else:raise SystemExit('Unexpected Docker operation: '+repr(a))
''')
    executable('curl', '#!/bin/sh\nexit 99\n')
    env['DOCKER_TRACE'] = str(base / 'docker-trace')
    collected = subprocess.run([str(ROOT / 'scripts/maintenance-versions-collector'), '--target', 'WEBLATE'], env=env, capture_output=True, text=True)
    assert collected.returncode == 0, collected.stderr
    version_rows = [line for line in collected.stdout.splitlines() if line.startswith('VERSION|')]
    assert len(version_rows) == 1 and '|COMPONENT=WEBLATE|' in version_rows[0] and '|STATUS=CURRENT|' in version_rows[0]
    assert all('pull' not in json.loads(line) and 'up' not in json.loads(line) for line in Path(env['DOCKER_TRACE']).read_text().splitlines())
    invalid = subprocess.run([str(ROOT / 'scripts/maintenance-versions-collector'), '--target', 'UNKNOWN'], env=env, capture_output=True, text=True)
    assert invalid.returncode != 0
print('TARGET_REFRESH_ISOLATION_AND_FRESHNESS=PASS|NETWORK=NO|REAL_UPDATES=NO')
