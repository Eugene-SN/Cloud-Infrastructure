"""Weblate dependency failures and notification recovery, without live alerts."""
import copy
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class WeblateHealthTest(unittest.TestCase):
    def setUp(self):
        self.monitor = runpy.run_path(str(Path(__file__).with_name('edge-monitor')))
        self.snapshot = {
            'edge': {'system_units': {'docker.service': {'state': 'OK'}},
                     'docker': {name: {'state': 'OK'} for name in (
                         'weblate-edge-weblate-1', 'weblate-edge-cache-1', 'postgres')}},
            'applications': {'weblate': {'state': 'OK', 'detail': {'code': 200}}},
        }

    def incident(self):
        return self.monitor['build_incidents'](self.snapshot)['weblate']

    def test_each_dependency_and_http_failure_reaches_one_incident(self):
        self.assertEqual(self.incident()['state'], 'OK')
        baseline = copy.deepcopy(self.snapshot)
        for name in baseline['edge']['docker']:
            self.snapshot = copy.deepcopy(baseline)
            self.snapshot['edge']['docker'][name]['state'] = 'FAIL'
            self.assertEqual(self.incident()['state'], 'FAIL', name)
        self.snapshot = copy.deepcopy(baseline)
        self.snapshot['applications']['weblate']['state'] = 'FAIL'
        self.assertEqual(self.incident()['state'], 'FAIL')

    def test_docker_parent_suppresses_child_alert(self):
        self.snapshot['edge']['system_units']['docker.service']['state'] = 'FAIL'
        self.snapshot['edge']['docker']['weblate-edge-cache-1']['state'] = 'FAIL'
        self.assertTrue(self.incident()['suppressed'])

    def test_failure_deduplication_and_recovery(self):
        sent = []
        notify = self.monitor['update_notifications']
        with tempfile.TemporaryDirectory(prefix='weblate-monitor-test-') as temp:
            with patch.dict(notify.__globals__,
                            post_mattermost=lambda payload: sent.append(payload) or True,
                            STATE_PATH=Path(temp) / 'state.json'):
                durable = {'notification_model': 2, 'incidents': {}}
                for state in ('OK', 'FAIL', 'FAIL', 'OK'):
                    self.snapshot['edge']['docker']['weblate-edge-cache-1']['state'] = state
                    notify({'weblate': self.incident()}, durable)
        self.assertEqual(len(sent), 2)
        self.assertEqual(durable['incidents']['weblate']['state'], 'OK')


if __name__ == '__main__':
    unittest.main()
