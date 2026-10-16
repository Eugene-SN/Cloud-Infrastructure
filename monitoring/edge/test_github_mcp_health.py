"""Shared GitHub MCP liveness, dependency suppression and alert recovery."""
import copy
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class GitHubMCPHealthTest(unittest.TestCase):
    def setUp(self):
        self.monitor = runpy.run_path(str(Path(__file__).with_name('edge-monitor')))
        self.snapshot = {
            'edge': {'system_units': {'docker.service': {'state': 'OK'}},
                     'docker': {'github-mcp': {'state': 'OK'}}},
            'applications': {'github_mcp': {'state': 'OK', 'detail': {'code': 401}}},
        }

    def incident(self):
        return self.monitor['build_incidents'](self.snapshot)['github-mcp']

    def test_http_requires_native_auth_challenge(self):
        class Tracker:
            def observe(self, key, ok, detail):
                return {'state': 'OK' if ok else 'FAIL', 'detail': detail}

        collect = self.monitor['collect_http_probes']
        for code in (401, 200, 403, 500, None):
            with patch.dict(collect.__globals__, http_get=lambda *args: {'ok': True, 'code': code}):
                result = collect({'http_probes': {'github_mcp': 'http://localhost/'}}, Tracker())
            self.assertEqual(result['github_mcp']['state'], 'OK' if code == 401 else 'FAIL')

    def test_http_or_container_failure_reaches_one_incident(self):
        self.assertEqual(self.incident()['state'], 'OK')
        baseline = copy.deepcopy(self.snapshot)
        for item in (self.snapshot['applications']['github_mcp'], self.snapshot['edge']['docker']['github-mcp']):
            item['state'] = 'FAIL'
            self.assertEqual(self.incident()['state'], 'FAIL')
            item['state'] = 'OK'
        self.assertEqual(self.snapshot, baseline)

    def test_docker_parent_suppresses_child_alert(self):
        self.snapshot['edge']['system_units']['docker.service']['state'] = 'FAIL'
        self.snapshot['edge']['docker']['github-mcp']['state'] = 'FAIL'
        self.assertTrue(self.incident()['suppressed'])

    def test_failure_deduplication_and_recovery(self):
        sent = []
        notify = self.monitor['update_notifications']
        with tempfile.TemporaryDirectory(prefix='github-mcp-monitor-test-') as temp:
            with patch.dict(notify.__globals__,
                            post_mattermost=lambda payload: sent.append(payload) or True,
                            STATE_PATH=Path(temp) / 'state.json'):
                durable = {'notification_model': 2, 'incidents': {}}
                for state in ('OK', 'FAIL', 'FAIL', 'OK'):
                    self.snapshot['edge']['docker']['github-mcp']['state'] = state
                    notify({'github-mcp': self.incident()}, durable)
        self.assertEqual(len(sent), 2)
        self.assertEqual(durable['incidents']['github-mcp']['state'], 'OK')


if __name__ == '__main__':
    unittest.main()
