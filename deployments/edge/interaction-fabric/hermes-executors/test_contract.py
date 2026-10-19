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

    def test_isolated_validation_preserves_legacy_and_has_native_agent_without_global_home(self):
        home=pathlib.Path(self.tmp.name)/'home';agent=home/'.gemini/antigravity-cli/agents/documentation-validation.md'
        agent.parent.mkdir(parents=True);agent.write_text('---\nname: documentation-validation\ntools: [finish]\n---\nValidate only supplied case.\n')
        with patch.object(self.helper.subprocess,'run',return_value=type('Registry',(),{'returncode':0,'stdout':'documentation-validation\n','stderr':''})()):
            result,call=self.execute('antigravity',{'status':'SUCCESS','structured_output':{'verdict':'pass'}},
                permission_mode='read-only',output_mode='json',schema={'type':'object'},
                context_policy='isolated-home-v1',context_home=str(home),agent='documentation-validation')
        self.assertEqual(call.kwargs['env']['HOME'],str(home))
        self.assertEqual(result['context_policy'],'isolated-home-v1')
        self.assertIn('--disable-slash-commands',call.args[0])
        self.assertEqual(call.args[0][call.args[0].index('--agent')+1],'documentation-validation')
        self.assertEqual(call.kwargs['env']['XDG_CONFIG_HOME'],str(home/'.config'))

    def test_isolation_cannot_silently_fall_back_to_shared_home_or_default_agent(self):
        with self.assertRaisesRegex(ValueError,'context'):
            self.execute('antigravity',{},permission_mode='read-only',context_policy='unknown')
        with self.assertRaisesRegex(ValueError,'context'):
            self.execute('codex',{},context_policy='isolated-home-v1',context_home='/home/core')

    def test_cancel_during_registry_check_never_starts_inference(self):
        home=pathlib.Path(self.tmp.name)/'home';agent=home/'.gemini/antigravity-cli/agents/documentation-validation.md'
        agent.parent.mkdir(parents=True);agent.write_text('fixture')
        handlers={};out=io.StringIO()
        def registry(*args,**kwargs):
            handlers[self.helper.signal.SIGTERM](None,None)
            return type('Registry',(),{'returncode':0,'stdout':'documentation-validation\n'})()
        with patch.object(self.helper.signal,'signal',side_effect=lambda sig,fn:handlers.update({sig:fn})), \
             patch.object(self.helper.subprocess,'run',side_effect=registry), \
             patch.object(self.helper.subprocess,'Popen',side_effect=AssertionError('inference must not start')),contextlib.redirect_stdout(out):
            self.helper.execute({'backend':'antigravity','task':'fixture','cwd':self.tmp.name,
                'permission_mode':'read-only','output_mode':'json','schema':{'type':'object'},
                'context_policy':'isolated-home-v1','context_home':str(home),'agent':'documentation-validation'})
        self.assertEqual(json.loads(out.getvalue())['status'],'canceled')
        self.assertFalse(list(self.helper.STATE.glob('*.json')))

    def test_legacy_n8n_mode_is_preserved(self):
        for backend in ['codex', 'antigravity']:
            r, _ = self.execute(backend, {'status': 'SUCCESS', 'response': 'done'})
            self.assertEqual(r['permission_mode'], 'full-access')


if __name__ == '__main__':
    unittest.main()
