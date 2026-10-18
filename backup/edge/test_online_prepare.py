"""Exercise the complete hook with fixtures; Docker lifecycle calls are denied."""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('edge-state-prepare')
SERVICES = ['web', 'api', 'admin', 'space', 'live', 'worker', 'beat-worker',
            'plane-redis', 'plane-mq', 'plane-minio']
FAKE = r'''#!/usr/bin/env python3
import fnmatch, json, os, pathlib, shutil, sys
name, args = pathlib.Path(sys.argv[0]).name, sys.argv[1:]
root = pathlib.Path(os.environ['FIXTURE_ROOT'])
with (root / 'commands.jsonl').open('a') as log:
    log.write(json.dumps([name, *args]) + '\n')
if name == 'docker':
    if args[:3] == ['exec', 'postgres', 'pg_dump']:
        if os.environ.get('FAIL_DUMP'): sys.exit(42)
        print('fixture dump')
    elif args[:3] == ['exec', 'postgres', 'pg_dumpall']: print('fixture globals')
    elif args[:4] == ['exec', '-i', 'postgres', 'pg_restore']:
        assert 'fixture dump' in sys.stdin.read()
    elif args[:2] == ['volume', 'inspect']:
        print(root / 'var/lib/docker/volumes/plane_uploads/_data')
    elif args[:4] == ['ps', '-a', '-q', '--filter']: print('fixture-container')
    elif args[:2] == ['image', 'inspect']:
        print(json.dumps([{'Id': 'sha256:fixture', 'RepoDigests': ['fixture@sha256:fixture']}]))
    elif args[0] == 'inspect':
        print(json.dumps([{'Config': {'Labels': {'com.docker.compose.service': s},
            'Image': 'fixture:latest'}, 'Image': 'sha256:fixture'}
            for s in json.loads(os.environ['FIXTURE_SERVICES'])]))
    else: sys.exit('FORBIDDEN docker command: ' + repr(args))
elif name == 'rsync':
    src, dst = map(pathlib.Path, args[-2:])
    excludes = [a.split('=', 1)[1].strip('/') for a in args if a.startswith('--exclude=')]
    for path in src.rglob('*'):
        rel = path.relative_to(src)
        if any(fnmatch.fnmatch(str(rel), p) or str(rel).startswith(p + '/') for p in excludes): continue
        target = dst / rel
        if path.is_dir(): target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    if str(src).endswith('/srv/weblate/data'): sys.exit(int(os.environ.get('RSYNC_RESULT', '0')))
else: sys.exit('FORBIDDEN service command: ' + name)
'''

class OnlinePreparation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='backrest-online-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        dirs = ['srv/n8n', 'srv/authelia/data', 'srv/mattermost/volumes/app/mattermost',
                'srv/mail/stalwart/etc', 'srv/mail/stalwart/lib', 'srv/mail/bulwark',
                'srv/weblate/data', 'opt/weblate', 'opt/plane', 'etc/nginx/sites-available',
                'usr/local/sbin', 'var/lib/docker/volumes/plane_uploads/_data',
                'home/core/.codex', 'run/lock', 'bin']
        for name in dirs: (self.root / name).mkdir(parents=True, exist_ok=True)
        for name in ['srv/n8n/database.sqlite', 'srv/authelia/data/db.sqlite3', 'home/core/.codex/state.sqlite']:
            db = sqlite3.connect(self.root / name)
            db.execute('create table evidence(value)')
            db.execute("insert into evidence values ('retained')")
            db.commit(); db.close()
        for name in ['srv/mail/stalwart/lib/CURRENT', 'srv/mail/stalwart/etc/config.json',
                     'srv/weblate/data/source.html', 'opt/weblate/compose.yaml',
                     'usr/local/sbin/plane-compose', 'etc/nginx/sites-available/projects-escloud-us.conf']:
            (self.root / name).write_text('fixture')
        self.stage = self.root / 'var/lib/backrest-staging/edge-state'
        (self.stage / 'current').mkdir(parents=True)
        (self.stage / 'current/sentinel').write_text('previous generation')
        body = SCRIPT.read_text()
        for prefix in ['/var/lib', '/run/lock', '/srv', '/opt', '/home/core', '/etc', '/usr/local/sbin']:
            body = body.replace(prefix, str(self.root) + prefix)
        self.script = self.root / 'prepare'; self.script.write_text(body)
        for cmd in ['docker', 'rsync', 'systemctl', 'service', 'kill', 'reboot', 'shutdown']:
            path = self.root / 'bin' / cmd; path.write_text(FAKE); path.chmod(0o755)
        self.env = dict(os.environ, FIXTURE_ROOT=str(self.root), FIXTURE_SERVICES=json.dumps(SERVICES),
                        PATH=str(self.root / 'bin') + ':' + os.environ['PATH'])

    def run_hook(self, **env):
        result = subprocess.run(['bash', str(self.script)], env=dict(self.env, **env), capture_output=True, text=True)
        self.assertNotIn('FORBIDDEN', result.stderr)
        self.assertFalse(list(self.stage.glob('next.*')))
        return result

    def test_success_retains_online_state_and_excludes_rocksdb(self):
        result = self.run_hook(); self.assertEqual(result.returncode, 0, result.stderr)
        current = self.stage / 'current'
        self.assertIn('service_lifecycle=untouched', (current / 'MANIFEST.txt').read_text())
        self.assertFalse((current / 'mail/stalwart/lib').exists())
        self.assertTrue((current / 'mail/stalwart/etc/config.json').exists())
        self.assertFalse((current / 'sentinel').exists())
        for name in ['n8n/database.sqlite', 'authelia/data/db.sqlite3',
                     'sqlite-overlay' + str(self.root) + '/home/core/.codex/state.sqlite']:
            db = sqlite3.connect(current / name)
            self.assertEqual(db.execute('pragma integrity_check').fetchone()[0], 'ok')
            self.assertEqual(db.execute('pragma journal_mode').fetchone()[0], 'delete')
            self.assertEqual(db.execute('select value from evidence').fetchone()[0], 'retained'); db.close()
        for app in ['mattermost', 'nextcloud', 'plane', 'weblate']:
            self.assertTrue((current / app / 'postgres' / (app + '.dump')).is_file())

    def test_vanished_file_reports_partial_live_copy(self):
        result = self.run_hook(RSYNC_RESULT='24'); self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('ONLINE_FILES_WARNING=vanished_source', result.stderr)

    def test_copy_error_keeps_previous_generation(self):
        result = self.run_hook(RSYNC_RESULT='23'); self.assertEqual(result.returncode, 23, result.stderr)
        self.assertTrue((self.stage / 'current/sentinel').exists())

    def test_dump_error_keeps_previous_generation(self):
        result = self.run_hook(FAIL_DUMP='1'); self.assertEqual(result.returncode, 42, result.stderr)
        self.assertTrue((self.stage / 'current/sentinel').exists())

if __name__ == '__main__': unittest.main()
