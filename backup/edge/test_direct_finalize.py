"""Regression checks for remote proof and staging deletion boundaries."""
import datetime
import fcntl
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


class DirectFinalizeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name('edge-state-finalize')
        if not path.exists():
            raise AssertionError('Direct finalizer is missing: no verified staging cleanup exists')
        loader = importlib.machinery.SourceFileLoader('direct_finalize', str(path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.module = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.module)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.current = self.root / 'current'
        self.current.mkdir()
        (self.current / 'dump').write_text('recoverable database state')
        self.lock = self.root / 'prepare.lock'
        self.sid = 'a' * 64
        self.guid = 'e293ee008a257664a7e568787463a9cbab5d0573daf53c5ebd92477d1960cec7'
        cutoff = self.current.stat().st_ctime + 1
        self.snapshot = {
            'id': self.sid, 'tree': 'b' * 64,
            'time': datetime.datetime.fromtimestamp(cutoff, datetime.timezone.utc).isoformat(),
            'hostname': 'edge', 'paths': ['/etc', '/srv', '/var/lib'],
            'tags': ['plan:edge-state', 'created-by:edge'],
        }
        self.config = self.root / 'config.json'
        self.config.write_text(json.dumps({
            'instance': 'edge', 'repos': [{'id': 'edge-pve', 'guid': self.guid}],
            'plans': [{'id': 'edge-state', 'repo': 'edge-pve', 'paths': ['/etc', '/srv', '/var/lib']}],
        }))
        self.fixture = self.root / 'fixture.json'
        self.fake = self.root / 'restic'
        self.fake.write_text('''#!/usr/bin/python3
import json,os,sys
data=json.load(open(os.environ['FINALIZE_FIXTURE']))
a=sys.argv[1:]
if a[:2]!=['--no-lock','--no-cache']:sys.exit(90)
if a[2:]==['cat','config']:out={'id':data['guid']}
elif a[2:]==['snapshots','--json',data['requested']]:out=data['snapshots']
else:sys.exit(91)  # Any mutation or broadened snapshot query fails closed.
if data.get('fail'):sys.exit(92)
print(json.dumps(out))
''')
        self.fake.chmod(0o700)
        self.env = dict(os.environ, FINALIZE_FIXTURE=str(self.fixture),
                        RESTIC_REPOSITORY='rest:http://192.168.1.14:8000/edge/')

    def run_finalize(self, *, guid=None, snapshots=None, fail=False, sid=None):
        self.fixture.write_text(json.dumps({
            'guid': guid or self.guid, 'requested': self.sid, 'fail': fail,
            'snapshots': [self.snapshot] if snapshots is None else snapshots,
        }))
        with patch.object(self.module, 'RESTIC', str(self.fake)), \
             patch.object(self.module, 'CONFIG', self.config), \
             patch.object(self.module.socket, 'gethostname', return_value='edge'):
            return self.module.finalize(self.sid if sid is None else sid, self.env, self.current, self.lock)

    def test_confirmed_exact_snapshot_removes_only_its_generation_and_is_idempotent(self):
        unrelated = self.root / 'other'; unrelated.mkdir()
        self.assertTrue(self.run_finalize())
        self.assertFalse(self.current.exists())
        self.assertTrue(unrelated.exists())
        self.assertFalse(self.run_finalize())

    def test_missing_or_ambiguous_snapshot_preserves_staging(self):
        for snapshots in [[], [self.snapshot, self.snapshot]]:
            with self.subTest(snapshots=len(snapshots)), self.assertRaises(RuntimeError):
                self.run_finalize(snapshots=snapshots)
            self.assertTrue((self.current / 'dump').exists())

    def test_wrong_repo_or_read_failure_preserves_staging(self):
        for kwargs in [{'guid': 'c'*64}, {'fail': True}]:
            with self.subTest(kwargs=kwargs), self.assertRaises((RuntimeError, subprocess.CalledProcessError)):
                self.run_finalize(**kwargs)
            self.assertTrue((self.current / 'dump').exists())

    def test_unrelated_snapshot_or_missing_time_cannot_authorize_cleanup(self):
        original = dict(self.snapshot)
        for key, value in [('id','d'*64), ('hostname','ai-node'),
                           ('paths',['/home']), ('tags',['plan:edge-state']),
                           ('time','invalid')]:
            self.snapshot = dict(original, **{key:value})
            with self.subTest(field=key), self.assertRaises((RuntimeError, ValueError)):
                self.run_finalize()
            self.assertTrue((self.current / 'dump').exists())

    def test_newer_generation_is_preserved(self):
        self.snapshot['time'] = '2000-01-01T00:00:00+00:00'
        self.assertFalse(self.run_finalize())
        self.assertTrue((self.current / 'dump').exists())

    def test_busy_prepare_lock_preserves_generation(self):
        with self.lock.open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertFalse(self.run_finalize())
        self.assertTrue((self.current / 'dump').exists())

    def test_symlink_cannot_delete_its_target(self):
        target = self.root / 'target'; self.current.rename(target)
        self.current.symlink_to(target, target_is_directory=True)
        with self.assertRaises(RuntimeError): self.run_finalize()
        self.assertTrue((target / 'dump').exists())

    def test_bad_snapshot_id_or_wrong_endpoint_preserves_generation(self):
        with self.assertRaises(ValueError): self.run_finalize(sid='')
        self.env['RESTIC_REPOSITORY'] = '/srv/local'
        with self.assertRaises(RuntimeError): self.run_finalize()
        self.assertTrue((self.current / 'dump').exists())


if __name__ == '__main__':
    unittest.main()
