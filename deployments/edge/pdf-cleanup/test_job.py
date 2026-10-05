"""Regression tests for the consolidated host adapter, using synthetic jobs."""
import importlib.util
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('job_adapter', Path(__file__).with_name('job-command.py'))
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class JobTests(unittest.TestCase):
    def setUp(self):
        self.source = b'%PDF-synthetic-snapshot'
        self.created = adapter.perform({'action': 'create', 'execution_id': '919191'})
        self.root = Path(self.created['job_dir'])
        (self.root / 'input/source.pdf').write_bytes(self.source)
        self.request = {'action': 'process', 'execution_id': '919191',
            'job_dir': str(self.root), 'upload_ok': True}

    def tearDown(self):
        if self.root.exists():
            shutil.rmtree(self.root)

    def process(self, rc=0, create_output=True):
        launcher = self.root / 'synthetic-cli'
        script = '#!/usr/bin/python3\nimport sys\nfrom pathlib import Path\n'
        if create_output:
            script += "Path(sys.argv[2]).write_bytes(b'%PDF-synthetic-cleaned')\n"
        script += "print('CLI report')\nsys.exit(" + str(rc) + ')\n'
        launcher.write_text(script)
        launcher.chmod(0o700)
        with patch.object(adapter, 'LAUNCHER', launcher):
            return adapter.perform(self.request)

    def test_failed_upload_cannot_invoke_cli(self):
        with self.assertRaisesRegex(ValueError, 'upload failed'):
            adapter.perform({**self.request, 'upload_ok': False})
        self.assertFalse((self.root / 'output/cleaned.pdf').exists())

    def test_nonzero_cli_cannot_publish_even_with_output(self):
        self.assertFalse(self.process(rc=4)['ok'])

    def test_success_without_output_is_rejected(self):
        self.assertFalse(self.process(create_output=False)['ok'])

    def test_success_needs_no_repeated_provenance_validation(self):
        result = self.process()
        self.assertTrue(result['ok'])
        self.assertEqual((self.root / 'input/source.pdf').read_bytes(), self.source)

    def test_wrong_execution_cannot_delete_another_job(self):
        request = {**self.request, 'action': 'release', 'execution_id': 'other'}
        with self.assertRaisesRegex(ValueError, 'execution mismatch'):
            adapter.perform(request)
        self.assertTrue(self.root.exists())
        result = adapter.perform({**request, 'execution_id': '919191'})
        self.assertTrue(result['job_removed'])
        self.assertFalse(self.root.exists())


if __name__ == '__main__':
    unittest.main()
