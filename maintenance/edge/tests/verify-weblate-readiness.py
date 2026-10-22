#!/usr/bin/env python3
"""Exercise Weblate readiness through update drivers without Docker mutations."""
import contextlib
import copy
import io
import json
import pathlib
import runpy
import subprocess
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
module = runpy.run_path(ROOT / 'scripts/manual-update')
manifest = json.loads((ROOT / 'config/update-units.json').read_text())
units = {unit['id']: unit for unit in manifest['units']}
globals_ = module['execute'].__globals__
row = {'image_repository': 'fixture/image', 'image_track': 'stable',
       'remote_image_digest': 'sha256:' + 'a' * 64}
native_check = ['docker', 'exec', 'weblate', '/app/venv/bin/weblate',
                'check', '--deploy', '--fail-level', 'ERROR']


def exercise(target, states, *, check_error=False, preflight=False):
    calls = []
    samples = iter(states)
    unit = copy.deepcopy(units[target])
    with tempfile.TemporaryDirectory(prefix='weblate-readiness-test.') as directory:
        unit['directory'] = directory
        for name in unit.get('files', []):
            pathlib.Path(directory, name).touch()
        config = {'services': {unit.get('service'): {'image': 'fixture/image:stable'}}}

        def command(argv, **kwargs):
            calls.append(argv)
            if argv[:2] == ['apt-get', 'update'] or argv[0] == 'apt-get':
                return SimpleNamespace(stdout='', returncode=0)
            if argv[:2] == ['docker', 'inspect']:
                state = next(samples)
                return SimpleNamespace(stdout=json.dumps(state), returncode=0)
            if argv == native_check:
                if check_error:
                    raise subprocess.CalledProcessError(1, argv, stderr='weblate.E027')
                return SimpleNamespace(stdout='', returncode=0)
            if argv[:2] in (['docker', 'pull'], ['docker', 'tag']):
                return SimpleNamespace(stdout='', returncode=0)
            if argv[:2] == ['docker', 'compose']:
                return SimpleNamespace(stdout=json.dumps(config), returncode=0)
            raise AssertionError('Unexpected command: ' + repr(argv))

        lifecycle = {'capture': lambda *a: calls.append(['capture']),
                     'cleanup': lambda *a: calls.append(['cleanup'])}
        with patch.dict(globals_, subprocess=SimpleNamespace(run=command),
                        runpy=SimpleNamespace(run_path=lambda p: lifecycle),
                        time=SimpleNamespace(sleep=lambda s: None)), contextlib.redirect_stdout(io.StringIO()):
            try:
                if preflight:
                    module['preflight'](unit)
                module['execute'](unit, row)
            except (RuntimeError, subprocess.CalledProcessError) as error:
                return calls, error
    return calls, None


starting = {'Status': 'running', 'Running': True, 'Health': {'Status': 'starting'}}
healthy = {'Status': 'running', 'Running': True, 'Health': {'Status': 'healthy'}}

# APT can restart Docker. Its success must wait for the application, including
# a startup longer than the former six-minute browser limit.
calls, error = exercise('APT_EDGE', [starting] * 200 + [healthy])
assert error is None, error
assert calls[-1] == native_check, 'APT returned before verifying Weblate readiness'
assert sum(c[:2] == ['docker', 'inspect'] for c in calls) == 201

for target in ['POSTGRESQL', 'WEBLATE_VALKEY', 'WEBLATE']:
    calls, error = exercise(target, [starting, healthy])
    assert error is None, error
    assert native_check in calls, target + ' skipped Weblate validation'
    assert calls.index(native_check) < calls.index(['cleanup']), 'discarded recovery before acceptance'

for state in [
    {'Status': 'exited', 'Running': False, 'ExitCode': 1},
    {'Status': 'running', 'Running': True, 'Health': {'Status': 'unhealthy'}},
]:
    calls, error = exercise('WEBLATE', [state])
    assert error is not None, 'a stopped/unhealthy Weblate was accepted'
    assert ['cleanup'] not in calls, 'recovery was discarded after failed readiness'

calls, error = exercise('WEBLATE', [healthy], check_error=True, preflight=True)
assert error is not None, 'invalid profile ownership was accepted by preflight'
assert not any(c[:2] == ['docker', 'pull'] for c in calls), 'pulled an image despite failed preflight'

calls, error = exercise('WEBLATE', [healthy], check_error=True)
assert error is not None and ['cleanup'] not in calls, 'post-update native check failure was ignored'
print('WEBLATE_READINESS_AND_PROFILE_CHECKS=PASS|REAL_UPDATES=NO|RESTARTS=NO')
