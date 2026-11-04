#!/usr/bin/env python3
"""Run Stalwart transition/rollback branches with disposable files and fake Docker."""
import contextlib
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
module = runpy.run_path(ROOT / 'scripts/update-stalwart')
globals_ = module['main'].__globals__
OLD = 'sha256:' + 'b' * 64
DIGEST = 'sha256:' + 'a' * 64


def scenario(installed, target, *, preflight=False, failed=False, rollback_failed=False):
    with tempfile.TemporaryDirectory(prefix='stalwart-update-test.') as temporary:
        base = Path(temporary)
        old_reference = 'stalwartlabs/stalwart:v' + '.'.join(installed.split('.')[:2])
        compose_file = base / 'compose.yaml'
        original = 'services:\n  stalwart:\n    image: ' + old_reference + '\n'
        compose_file.write_text(original)
        calls = []
        up_calls = 0
        versions = iter([installed, installed] if failed else [installed, target])
        def compose(*args, **kwargs):
            nonlocal up_calls
            calls.append(list(args))
            if args[0] == 'up':
                up_calls += 1
                if failed and (up_calls == 1 or rollback_failed):
                    raise RuntimeError('fixture unhealthy')
            return SimpleNamespace(stdout='', returncode=0)
        def command(argv, **kwargs):
            calls.append(argv)
            if argv[:2] == ['docker', 'inspect']:
                identity = 'sha256:' + 'c' * 64 if up_calls == 1 and not failed else OLD
                return SimpleNamespace(stdout=identity + '\n', returncode=0)
            if argv[:3] == ['docker', 'image', 'inspect']:
                return SimpleNamespace(stdout='sha256:' + 'c' * 64 + '\n', returncode=0)
            raise AssertionError('unexpected external command: ' + repr(argv))
        lifecycle = {'capture': lambda *a: calls.append(['capture']), 'cleanup': lambda *a: calls.append(['cleanup'])}
        argv = ['update-stalwart', '--target-version', target, '--target-track', 'v' + '.'.join(target.split('.')[:2]), '--target-digest', DIGEST]
        if preflight: argv.append('--preflight')
        output = io.StringIO()
        with patch.dict(globals_, DIRECTORY=base, effective_image=lambda: old_reference,
                        running_version=lambda: next(versions), compose_run=compose,
                        run=lambda a, **kw: calls.append(a), subprocess=SimpleNamespace(run=command),
                        runpy=SimpleNamespace(run_path=lambda p: lifecycle)), patch.object(sys, 'argv', argv), contextlib.redirect_stdout(output):
            error = None
            try: module['main']()
            except RuntimeError as exc: error = str(exc)
        return calls, error, output.getvalue(), compose_file.read_text() == original


for preflight in (True, False):
    calls, error, output, intact = scenario('0.16.27', '1.0.2', preflight=preflight)
    assert error and 'MIGRATION_REQUIRED' in error, 'unsupported store migration was accepted'
    assert not any(c and (c[0] in ['up', 'capture'] or c[:2] == ['docker', 'pull']) for c in calls)
    assert intact

calls, error, output, intact = scenario('0.16.26', '0.16.27')
assert not error and ['cleanup'] in calls and 'STALWART_UPDATE_GATE=PASS' in output

for old, new in [('0.16.26', '0.16.27'), ('1.0.1', '1.0.2'), ('1.0.2', '1.1.0')]:
    calls, error, output, intact = scenario(old, new, failed=True)
    assert error and intact
    assert sum(c and c[0] == 'up' for c in calls) == 2, 'same-track failure skipped image rollback'
    old_ref = 'stalwartlabs/stalwart:v' + '.'.join(old.split('.')[:2])
    assert ['docker', 'tag', OLD, old_ref] in calls, 'rollback did not restore the exact previous image'
    log_index = next(i for i, c in enumerate(calls) if c and c[0] == 'logs')
    restore_index = calls.index(['docker', 'tag', OLD, old_ref])
    assert log_index < restore_index, 'failed-container logs were lost before rollback'
    assert ['cleanup'] not in calls
    assert 'STALWART_IMAGE_ROLLBACK=VERIFIED' in output and 'DATA_RESTORED=NO' in output

calls, error, output, _ = scenario('1.0.1', '1.0.2', failed=True, rollback_failed=True)
assert 'rollback failed' in error.lower() and 'STALWART_IMAGE_ROLLBACK=VERIFIED' not in output
print('STALWART_TRANSITION_AND_ROLLBACK=PASS|REAL_DOCKER_CALLS=NO|REAL_UPDATES=NO')
