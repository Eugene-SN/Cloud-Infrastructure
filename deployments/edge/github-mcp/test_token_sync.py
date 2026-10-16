"""Credential rotation, native configuration preservation and durable retry."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


class TokenSyncTest(unittest.TestCase):
    def setUp(self):
        self.sync = runpy.run_path(str(Path(__file__).with_name('token-sync.py')))['synchronize']
        self.module = self.sync.__globals__
        self.native_credential = self.module['credential']
        self.temporary = tempfile.TemporaryDirectory(prefix='github-token-sync-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / 'status.json'
        self.clients = {}
        examples = Path(__file__).parent.parent / 'interaction-fabric/clients'
        for client, (source, loader, section, headers) in self.module['CLIENTS'].items():
            name = {'codex': 'codex.toml', 'hermes': 'hermes.yaml', 'antigravity': 'antigravity.json'}[client]
            path = self.root / name
            path.write_text((examples / name).read_text().replace('<EXISTING_GH_OPERATOR_TOKEN>', 'old-test-token'))
            path.chmod(0o600)
            self.clients[client] = (path, loader, section, headers)
        self.applied = []
        self.overrides = patch.dict(self.module, STATE=self.state, CLIENTS=self.clients,
                                    credential=lambda: 'new-test-token',
                                    apply=lambda client: self.applied.append(client) or 'reloaded')
        self.overrides.start()
        self.addCleanup(self.overrides.stop)

    def files(self):
        return {client: item[0].read_bytes() for client, item in self.clients.items()}

    def run_sync(self, force=False):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = self.sync(force)
        return result, output.getvalue()

    def test_rotation_changes_only_github_authorization_in_all_clients(self):
        before = {client: loader(path.read_text()) for client, (path, loader, _, _) in self.clients.items()}
        self.assertEqual(self.run_sync()[0], 0)
        for client, (path, loader, section, headers) in self.clients.items():
            expected = copy.deepcopy(before[client])
            expected[section]['github'][headers]['Authorization'] = 'Bearer new-test-token'
            self.assertEqual(loader(path.read_text()), expected)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.applied, list(self.clients))
        status = json.loads(self.state.read_text())
        self.assertEqual(status['pending_reload'], [])
        self.assertNotIn('new-test-token', self.state.read_text())

    def test_unchanged_token_never_writes_or_restarts_clients(self):
        self.assertEqual(self.run_sync()[0], 0)
        stats = {c: p.stat().st_mtime_ns for c, (p, *_) in self.clients.items()}
        self.applied.clear()
        self.assertEqual(self.run_sync()[0], 0)
        self.assertEqual(self.applied, [])
        self.assertEqual(stats, {c: p.stat().st_mtime_ns for c, (p, *_) in self.clients.items()})

    def test_failed_source_preserves_all_configs_and_redacts_exception(self):
        before = self.files()
        with patch.dict(self.module, credential=lambda: (_ for _ in ()).throw(RuntimeError('secret-token'))):
            code, output = self.run_sync()
        self.assertEqual(code, 1)
        self.assertEqual(before, self.files())
        self.assertEqual(self.applied, [])
        self.assertNotIn('secret-token', output + self.state.read_text())

    def test_transport_drift_stops_before_any_write(self):
        path = self.clients['antigravity'][0]
        path.write_text(path.read_text().replace('127.0.0.1:18082', 'example.invalid:18082'))
        before = self.files()
        self.assertEqual(self.run_sync()[0], 1)
        self.assertEqual(before, self.files())
        self.assertFalse(self.applied)

    def test_competing_auth_source_stops_before_any_write(self):
        path = self.clients['codex'][0]
        path.write_text(path.read_text().replace('[mcp_servers.github]',
                        '[mcp_servers.github]\nbearer_token_env_var = "OVERRIDE_TOKEN"'))
        before = self.files()
        self.assertEqual(self.run_sync()[0], 1)
        self.assertEqual(before, self.files())
        self.assertFalse(self.applied)

    def test_failed_reload_retries_after_configs_already_match(self):
        attempts = []
        def apply(client):
            attempts.append(client)
            if client == 'hermes':
                raise self.module['SyncError']('TEST_RELOAD_FAILURE')
            return 'reloaded'
        with patch.dict(self.module, apply=apply):
            self.assertEqual(self.run_sync()[0], 1)
        self.assertEqual(attempts, ['codex', 'hermes'])
        self.assertEqual(json.loads(self.state.read_text())['pending_reload'], ['antigravity', 'hermes'])
        self.assertEqual(self.run_sync()[0], 0)
        self.assertEqual(self.applied, ['hermes', 'antigravity'])
        self.assertEqual(json.loads(self.state.read_text())['pending_reload'], [])

    def test_force_refresh_and_subsequent_noop(self):
        self.assertEqual(self.run_sync()[0], 0)
        self.applied.clear()
        self.assertEqual(self.run_sync(force=True)[0], 0)
        self.assertEqual(self.applied, list(self.clients))
        self.applied.clear()
        self.assertEqual(self.run_sync()[0], 0)
        self.assertFalse(self.applied)

    def test_concurrent_user_edit_is_preserved(self):
        original = self.module['prepare']
        path = self.clients['codex'][0]
        def prepare(client, token):
            result = original(client, token)
            if client == 'antigravity':
                path.write_text(path.read_text() + '\n# concurrent user edit\n')
            return result
        with patch.dict(self.module, prepare=prepare):
            self.assertEqual(self.run_sync()[0], 1)
        self.assertIn('# concurrent user edit', path.read_text())
        self.assertNotIn('new-test-token', path.read_text())
        self.assertFalse(self.applied)

    def test_gh_reads_the_canonical_store_without_environment_token_override(self):
        captured = {}
        def run(argv, **kwargs):
            captured.update(kwargs)
            return type('Result', (), {'returncode': 0, 'stdout': 'new-test-token\n'})()
        with patch.dict(os.environ, GH_TOKEN='override', GITHUB_TOKEN='override'), \
             patch.object(self.module['subprocess'], 'run', run):
            self.assertEqual(self.native_credential(), 'new-test-token')
        self.assertNotIn('GH_TOKEN', captured['env'])
        self.assertNotIn('GITHUB_TOKEN', captured['env'])
        self.assertEqual(captured['env']['GH_CONFIG_DIR'], '/home/core/.config/gh')


if __name__ == '__main__':
    unittest.main()
