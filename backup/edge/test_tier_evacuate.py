import importlib.util
import os
from pathlib import Path
import subprocess
import unittest
import tempfile
import time
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('evacuate', Path(__file__).with_name('edge-tier-evacuate.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EvacuationTests(unittest.TestCase):
    source = {'id': 'a' * 64, 'tree': 'tree', 'time': 'time',
              'hostname': 'edge', 'paths': ['/srv']}

    def test_identity_requires_contents_and_paths(self):
        copy = dict(self.source, id='b' * 64, original=self.source['id'])
        self.assertEqual(module.verified_ids([self.source], [copy]), [self.source['id']])
        for key in ('tree', 'time', 'hostname', 'paths'):
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                module.verified_ids([self.source], [dict(copy, **{key: 'wrong'})])

    def test_staging_keeps_newer_generation_and_removes_copied_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / 'current'
            current.mkdir()
            (current / 'dump').write_text('database')
            lock = Path(tmp) / 'prepare.lock'
            self.assertFalse(module.clean_staging(0, current, lock))
            self.assertTrue((current / 'dump').exists())
            self.assertTrue(module.clean_staging(time.time() + 1, current, lock))
            self.assertFalse(current.exists())

    def execute(self, copy_fails=False, destination_present=True):
        import json
        calls = []
        def command(argv, **kwargs):
            calls.append((argv, kwargs['env']['RESTIC_REPOSITORY']))
            if 'copy' in argv and copy_fails:
                raise subprocess.CalledProcessError(1, argv)
            if 'snapshots' in argv:
                local = kwargs['env']['RESTIC_REPOSITORY'].startswith('/srv/')
                records = [self.source] if local else ([dict(self.source, id='b' * 64,
                           original=self.source['id'])] if destination_present else [])
                return subprocess.CompletedProcess(argv, 0, json.dumps(records))
            return subprocess.CompletedProcess(argv, 0)
        with patch.dict(os.environ, {'RESTIC_REPOSITORY': 'rest:http://pve/edge/'}), \
             patch.object(module.subprocess, 'run', side_effect=command):
            try:
                module.evacuate('state')
            except (RuntimeError, subprocess.CalledProcessError):
                return calls, False
        return calls, True

    def test_copy_failure_preserves_local_snapshots(self):
        calls, success = self.execute(copy_fails=True)
        self.assertFalse(success)
        self.assertFalse(any('forget' in args or 'prune' in args for args, _ in calls))

    def test_missing_destination_proof_preserves_local_snapshots(self):
        calls, success = self.execute(destination_present=False)
        self.assertFalse(success)
        self.assertFalse(any('forget' in args or 'prune' in args for args, _ in calls))

    def test_success_reclaims_only_local_repository_and_explicit_ids(self):
        calls, success = self.execute()
        self.assertTrue(success)
        destructive = [(args, repo) for args, repo in calls if 'forget' in args or 'prune' in args]
        self.assertEqual(len(destructive), 2)
        self.assertTrue(all(repo == module.SOURCES['state'][0] for _, repo in destructive))
        self.assertIn(self.source['id'], destructive[0][0])


if __name__ == '__main__':
    unittest.main()
