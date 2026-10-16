"""Workspace boundary tests; Docker reuse is checked by integration runs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('adapter', Path(__file__).with_name('job-command.py'))
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

class WorkspaceTests(unittest.TestCase):
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
