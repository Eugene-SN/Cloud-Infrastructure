"""Workspace boundary tests; Docker reuse is checked by integration runs."""
import importlib.util
import json
import subprocess
from types import SimpleNamespace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('adapter', Path(__file__).with_name('job-command.py'))
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

class WorkspaceTests(unittest.TestCase):
    def run_fixture(self, root, *, interrupt=False, stop='ok', foreign=False, failed=False):
        running={'Running':False,'ExitCode':0}
        class Process:
            returncode=0
            calls=0
            def communicate(self, timeout):
                self.calls+=1
                if stop=='reap-timeout' and self.calls>1:
                    raise subprocess.TimeoutExpired('fake attach reap',timeout)
                if interrupt and self.calls==1:
                    raise subprocess.TimeoutExpired('fake cleanup',timeout)
                running['Running']=False
                if foreign:
                    (root/'job.json').write_text(json.dumps({'execution_id':'other'}))
                return json.dumps({'status':'error' if failed else 'cleaned'}),''
        def start(*args,**kwargs):
            running['Running']=True
            (root/'cleaned.pdf').write_bytes(b'synthetic output; no PDF processing')
            return Process()
        def stop_container(*args,**kwargs):
            if stop=='throw':raise OSError('fake stop failure')
            if stop=='timeout':raise subprocess.TimeoutExpired('fake stop',15)
            if stop in ('ok','failed-stopped','reap-timeout'):running['Running']=False
            return SimpleNamespace(returncode=1 if stop in ('failed','failed-stopped') else 0)
        with patch.object(adapter,'WORK',root),patch.object(adapter,'state',side_effect=lambda:dict(running)),\
                patch.object(adapter.subprocess,'Popen',side_effect=start),patch.object(adapter,'docker',side_effect=stop_container):
            return adapter.perform(dict(action='process',execution_id='123',path='fixture.pdf'))

    def test_unconfirmed_stop_preserves_owner_and_output(self):
        for failure in ['failed','failed-stopped','throw','timeout','still-running','reap-timeout']:
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                with self.assertRaises(Exception):
                    self.run_fixture(root,interrupt=True,stop=failure)
                self.assertTrue((root/'job.json').exists(), 'Unknown stop lost its owner')
                self.assertTrue((root/'cleaned.pdf').exists(), 'Unknown stop lost its output')
                self.assertEqual(json.loads((root/'job.json').read_text())['execution_id'],'123')
                self.assertEqual((root/'cleaned.pdf').read_bytes(),b'synthetic output; no PDF processing')
                # Current Prepare runs release in finally, even after failed process.
                with patch.object(adapter,'WORK',root),patch.object(adapter,'state',return_value={'Running':False}):
                    with self.assertRaises(ValueError):
                        adapter.perform(dict(action='release',execution_id='123'))
                self.assertTrue((root/'job.json').exists())
                self.assertTrue((root/'cleaned.pdf').exists())

    def test_confirmed_stop_then_reaped_client_can_clear_same_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(subprocess.TimeoutExpired):
                self.run_fixture(root,interrupt=True)
            self.assertEqual(list(root.iterdir()),[])

    def test_process_cleanup_cannot_remove_changed_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):self.run_fixture(root,foreign=True,failed=True)
            self.assertEqual(json.loads((root/'job.json').read_text())['execution_id'],'other')
            self.assertTrue((root/'cleaned.pdf').exists())

    def test_normal_process_and_release_keep_existing_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.assertTrue(self.run_fixture(root)['ok'])
            self.assertTrue((root/'job.json').exists())
            with patch.object(adapter,'WORK',root),patch.object(adapter,'state',return_value={'Running':False}):
                self.assertTrue(adapter.perform(dict(action='release',execution_id='123'))['job_removed'])
                self.assertTrue(adapter.perform(dict(action='release',execution_id='123'))['job_removed'])
            self.assertEqual(list(root.iterdir()),[])

    def test_unowned_nonempty_workspace_is_not_a_release_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'evidence.json').write_text('keep')
            with patch.object(adapter,'WORK',root),patch.object(adapter,'state',return_value={'Running':False}):
                with self.assertRaises(ValueError):adapter.perform(dict(action='release',execution_id='123'))
            self.assertEqual((root/'evidence.json').read_text(),'keep')

    def test_invalid_paths_are_rejected_before_work_is_created(self):
        with tempfile.TemporaryDirectory(prefix='pdf-cleanup-unit-') as directory:
            root = Path(directory)
            with patch.object(adapter, 'WORK', root/'work', create=True):
                for path in ('../a.pdf', '/a.pdf', 'a/../b.pdf', 'a//b.pdf', 'a.txt'):
                    try:
                        adapter.perform(dict(action='process', execution_id='1', path=path))
                    except Exception as error:
                        self.assertIsInstance(error, ValueError)
                    else:
                        self.fail('Invalid path accepted: '+path)
                self.assertEqual(list(root.iterdir()), [])

    def test_release_cannot_remove_another_executions_output(self):
        with tempfile.TemporaryDirectory(prefix='pdf-cleanup-unit-') as directory:
            root = Path(directory)
            (root/'job.json').write_text(json.dumps(dict(execution_id='123', path='a.pdf')))
            output = root/'cleaned.pdf'
            output.write_bytes(b'keep this result')
            with patch.object(adapter, 'WORK', root):
                with self.assertRaises(ValueError):
                    adapter.perform(dict(action='release', execution_id='456'))
            self.assertEqual(output.read_bytes(), b'keep this result')

    def test_unknown_action_creates_no_workspace(self):
        with tempfile.TemporaryDirectory(prefix='pdf-cleanup-unit-') as directory:
            root = Path(directory)
            with patch.object(adapter, 'WORK', root/'work'):
                with self.assertRaises(ValueError):
                    adapter.perform(dict(action='create', execution_id='123'))
            self.assertEqual(list(root.iterdir()), [])

if __name__ == '__main__':
    unittest.main()
