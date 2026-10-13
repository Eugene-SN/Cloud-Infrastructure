#!/usr/bin/env python3
"""Exercise every dispatch route with isolated command/filesystem boundaries."""
import contextlib
import io
import json
import pathlib
import runpy
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

root = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((root/'config/update-units.json').read_text())
module = runpy.run_path(root/'scripts/manual-update')['execute'].__globals__
digest = 'sha256:' + 'a'*64
failures = []
for unit in manifest['units']:
    calls = []
    row = {'available_application_version':'35.0.1', 'image_repository':'fixture/image',
           'image_track':'fixture', 'remote_image_digest':digest}
    if unit['id']=='STALWART': row.update(available_application_version='0.16.26', image_track='v0.16')
    services = unit.get('services', [unit.get('service')])
    config = {'services':{s:{'image':'fixture/image:fixture'} for s in services if s}}
    lifecycle = {'capture':lambda *a, **k: None, 'cleanup':lambda *a, **k: None}
    def command(argv, **kwargs):
        calls.append(argv)
        return SimpleNamespace(stdout=json.dumps(config) if 'config' in argv else '1.0.0\n', returncode=0)
    fake_path = MagicMock()
    fake_path.is_file.return_value = False
    with patch.dict(module, run=command, run_as_core=command,
                    subprocess=SimpleNamespace(run=command),
                    pathlib=SimpleNamespace(Path=MagicMock(return_value=fake_path)),
                    shutil=SimpleNamespace(move=MagicMock()),
                    runpy=SimpleNamespace(run_path=lambda p:lifecycle)):
        with contextlib.redirect_stdout(io.StringIO()):module['execute'](unit,row)
    if unit['id']=='NEXTCLOUD':
        expected = [module['sys'].executable, '/opt/edge-maintenance/scripts/update-nextcloud',
                    '--target-version','35.0.1','--target-digest',digest]
        if calls != [expected]:failures.append('NEXTCLOUD missing target version/digest')
    elif unit['id']=='BACKREST':
        if calls != [['/opt/edge-maintenance/scripts/update-github-binary','BACKREST']]:
            failures.append('BACKREST calls absent downloader / old restart branch')
    elif unit['id']=='SEMAPHORE':
        assert len(calls)==1 and calls[0][0]=='systemd-run'
    elif unit['driver']=='compose':
        assert ['docker','pull','fixture/image@'+digest] in calls
        up = next(c for c in calls if 'up' in c)
        assert '--force-recreate' in up and '--no-deps' in up
        assert up[-len(services):]==services
    elif unit['driver']=='maintctl':assert calls == [['/usr/local/bin/maintctl','update',unit['argument']]]
    elif unit['driver']=='self_update':assert calls[0]==[unit['binary'],*unit['arguments']]
    elif unit['id']=='PLANE':assert calls == [[module['sys'].executable,'/opt/edge-maintenance/scripts/update-plane']]
    elif unit['id']=='STALWART':assert '--target-version' in calls[0] and '--target-digest' in calls[0]
    elif unit['id']=='APT_EDGE':assert calls[0]==['apt-get','update'] and any('dist-upgrade' in c for c in calls)
assert not failures, failures
print('ALL_MANUAL_DRIVER_DISPATCH=PASS|TARGETS=18|REAL_UPDATES=NO|SERVICE_RESTARTS=NO')

nextcloud = runpy.run_path(root/'scripts/update-nextcloud')['main'].__globals__
with patch.dict(nextcloud, DIRECTORY=MagicMock(), occ_status=lambda:{'versionstring':'35.0.1'},
                release_map=lambda:{35:'35.0.1'}, verify_runtime=lambda v:None,
                runpy=SimpleNamespace(run_path=lambda p:lifecycle),
                apply_step=lambda *a:None), patch.object(sys, 'argv', ['update-nextcloud','--target-version','35.0.1']):
    # Same-version requests must go through the normal pull/recreate path.
    applied=[]
    with patch.dict(nextcloud, apply_step=lambda *a:applied.append(a)):
        nextcloud['main']()
    assert applied and applied[0][:2]==(35,'35.0.1'), 'same version skipped image refresh'

# Native readiness polling must tolerate entrypoint initialization and reject
# permanent maintenance/DB-upgrade state. No docker exec or sleeping occurs.
probes=iter([(None,'starting'),({'versionstring':'35.0.1','maintenance':False,'needsDbUpgrade':False},'ready')])
with patch.dict(nextcloud, occ_status_probe=lambda:next(probes), time=SimpleNamespace(sleep=lambda t:None)):
    nextcloud['wait_for_runtime']('35.0.1')
with patch.dict(nextcloud, occ_status_probe=lambda:({'versionstring':'35.0.1','maintenance':True,'needsDbUpgrade':True},'busy'),
                RUNTIME_READY_ATTEMPTS=2,time=SimpleNamespace(sleep=lambda t:None)):
    try:nextcloud['wait_for_runtime']('35.0.1')
    except RuntimeError:pass
    else:raise AssertionError('Nextcloud busy runtime accepted')
print('NEXTCLOUD_IMAGE_REFRESH_AND_READINESS=PASS|REAL_DOCKER_CALLS=NO')

# Same-version image refresh must pull the requested digest, recreate both
# consumers without their dependencies, and wait for native runtime readiness.
commands=[]
with patch.dict(nextcloud, effective_nextcloud_image=lambda:'nextcloud:35.0-apache',
                pulled_image_version=lambda ref:'35.0.1',
                compose_run=lambda *a, **k:commands.append(list(a)),
                run=lambda a, **k:commands.append(a),
                wait_for_runtime=lambda v:commands.append(['ready',v])):
    nextcloud['apply_step'](35,'35.0.1',digest)
assert ['docker','pull','nextcloud@'+digest] in commands
assert ['docker','tag','nextcloud@'+digest,'nextcloud:35.0-apache'] in commands
assert ['up','-d','--wait','--force-recreate','--no-deps','app','cron'] in commands
assert commands[-1]==['ready','35.0.1']
assert not any(c and c[0]=='pull' for c in commands), 'moving tag overwrote accepted digest'
for images,accepted in (('new-image\nnew-image\n',True),('new-image\nold-image\n',False)):
    def inspect(argv,**kwargs):
        return SimpleNamespace(stdout='new-image\n' if 'image' in argv else images)
    with patch.dict(nextcloud, run=inspect, compose_run=lambda *a, **k:SimpleNamespace(stdout='app-id\ncron-id\n')):
        try:nextcloud['verify_running_digest'](digest)
        except RuntimeError:assert not accepted
        else:assert accepted
print('NEXTCLOUD_EXACT_IMAGE_AND_BOTH_CONTAINERS=PASS|REAL_DOCKER_CALLS=NO')
