"""Offline boundary properties; no live executors, credentials or production state."""
import contextlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

HELPER = pathlib.Path(__file__).resolve().parent.parent / 'edge-ai-exec'
sys.dont_write_bytecode = True


class ContractTests(unittest.TestCase):
    def setUp(self):
        loader = importlib.machinery.SourceFileLoader('edge_exec_test', str(HELPER))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        self.helper = importlib.util.module_from_spec(spec)
        loader.exec_module(self.helper)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.helper.STATE = pathlib.Path(self.tmp.name) / 'state'

    def execute(self, backend, envelope, **options):
        class Process:
            pid = 12345
            returncode = 0
            def __init__(self, argv, **kwargs):
                self.argv, self.kwargs = argv, kwargs
            def communicate(self, *args, **kwargs):
                if '-o' in self.argv:
                    pathlib.Path(self.argv[self.argv.index('-o')+1]).write_text('CODEX_FINAL')
                return json.dumps(envelope), ''
            def poll(self):
                return self.returncode
        out = io.StringIO()
        with patch.object(self.helper.subprocess, 'Popen', side_effect=Process) as spawn, \
             patch.object(self.helper.signal, 'signal'), contextlib.redirect_stdout(out):
            self.helper.execute({'backend': backend, 'task': 'test', 'cwd': self.tmp.name, **options})
        self.assertEqual(spawn.call_count, 1)  # No fallback, even on native RC0 failure.
        self.assertFalse(list(self.helper.STATE.glob('*.json')))
        return json.loads(out.getvalue()), spawn.call_args

    def test_native_non_success_and_denial_cannot_be_completed(self):
        for envelope, status in [({'status': 'WAITING', 'response': 'partial'}, 'native_error'),
                                 ({'status': 'SUCCESS', 'denied_actions': ['command(test)']}, 'permission_denied')]:
            with self.subTest(status=status):
                r, _ = self.execute('antigravity', envelope, permission_mode='read-only')
                self.assertFalse(r['ok'])
                self.assertEqual(r['status'], status)

    def test_operator_mode_controls_codex_sandbox(self):
        for mode, sandbox in [('read-only', 'read-only'), ('workspace-write', 'workspace-write'),
                              ('full-access', 'danger-full-access')]:
            with self.subTest(mode=mode):
                r, call = self.execute('codex', {}, permission_mode=mode)
                argv = call.args[0]
                self.assertEqual(argv[argv.index('--sandbox')+1], sandbox)
                self.assertEqual(call.kwargs['env']['HOME'], '/home/core')
                self.assertTrue(r['ok'])

    def test_legacy_n8n_mode_is_preserved(self):
        for backend in ['codex', 'antigravity']:
            r, _ = self.execute(backend, {'status': 'SUCCESS', 'response': 'done'})
            self.assertEqual(r['permission_mode'], 'full-access')


if __name__ == '__main__':
    unittest.main()
