"""Every permanent Plane role contributes to the same service incident."""
import copy
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


class PlaneHealthTest(unittest.TestCase):
    def setUp(self):
        self.monitor = runpy.run_path(str(Path(__file__).with_name('edge-monitor')))
        self.snapshot = {
            'edge': {
                'system_units': {'docker.service': {'state': 'OK'}},
                'docker': {name: {'state': 'OK'} for name in (
                    'plane-web', 'plane-api', 'plane-admin', 'plane-space',
                    'plane-live', 'plane-worker', 'plane-scheduler',
                    'plane-valkey', 'plane-rabbitmq', 'plane-minio')},
            },
            'applications': {probe: {'state': 'OK', 'detail': {'code': 200}}
                             for probe in ('plane', 'plane_api', 'plane_live')},
        }

    def incident(self):
        return self.monitor['build_incidents'](self.snapshot)['plane']

    def test_each_role_and_endpoint_failure_reaches_plane_incident(self):
        self.assertEqual(self.incident()['state'], 'OK')
        baseline = copy.deepcopy(self.snapshot)
        for section in ('docker', 'applications'):
            checks = baseline['edge']['docker'] if section == 'docker' else baseline['applications']
            for name in checks:
                self.snapshot = copy.deepcopy(baseline)
                items = self.snapshot['edge']['docker'] if section == 'docker' else self.snapshot['applications']
                items[name]['state'] = 'FAIL'
                self.assertEqual(self.incident()['state'], 'FAIL', name)

    def test_scheduler_failure_deduplication_and_recovery(self):
        notify = self.monitor['update_notifications']
        sent = []
        with tempfile.TemporaryDirectory(prefix='plane-monitor-test-') as directory:
            with patch.dict(notify.__globals__,
                            post_mattermost=lambda payload: sent.append(payload) or True,
                            STATE_PATH=Path(directory) / 'state.json'):
                durable = {'notification_model': 2, 'incidents': {}}
                for state in ('OK', 'FAIL', 'FAIL', 'OK'):
                    self.snapshot['edge']['docker']['plane-scheduler']['state'] = state
                    notify({'plane': self.incident()}, durable)
        self.assertEqual(len(sent), 2)
        self.assertEqual(durable['incidents']['plane']['state'], 'OK')


if __name__ == '__main__':
    unittest.main()
