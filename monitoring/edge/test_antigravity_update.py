"""Offline update monitoring and existing notification-path tests."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class AntigravityUpdateHealthTest(unittest.TestCase):
    def setUp(self):
        self.monitor = runpy.run_path(str(Path(__file__).with_name('edge-monitor')))
        self.collect = self.monitor['collect_antigravity_update']
        self.temp = tempfile.TemporaryDirectory(prefix='agy-monitor-test-')
        self.addCleanup(self.temp.cleanup)
        self.status_path = Path(self.temp.name) / 'status.json'
        self.now = 1800000000
        self.config = {'antigravity_update': {'status_file': str(self.status_path),
                                            'max_success_age_s': 93600}}
        self.status = {'result': 'PASS', 'last_success_at': self.now - 100}
        self.units = ('Id=antigravity-native-update.timer\nActiveState=active\n'
                      'UnitFileState=enabled\nResult=success\n\n'
                      'Id=antigravity-native-update.service\nActiveState=inactive\n'
                      'UnitFileState=static\nResult=success\n')

    def health(self):
        self.status_path.write_text(json.dumps(self.status))
        with patch.dict(self.collect.__globals__, run_text=lambda *a, **kw: self.units):
            return self.collect(self.config, now=self.now)

    def test_pass_and_short_running_check_are_healthy(self):
        self.assertEqual(self.health()['state'], 'OK')
        self.status.update(result='RUNNING', started_at=self.now - 30)
        self.assertEqual(self.health()['state'], 'OK')

    def test_failed_stale_and_stuck_checks_are_visible(self):
        self.status['result'] = 'FAIL'
        self.assertEqual(self.health()['state'], 'DEGRADED')
        self.status.update(result='PASS', last_success_at=self.now - 93601)
        self.assertEqual(self.health()['state'], 'DEGRADED')
        self.status.update(result='RUNNING', last_success_at=self.now - 100,
                           started_at=self.now - 901)
        self.assertEqual(self.health()['state'], 'DEGRADED')

    def test_disabled_timer_and_service_timeout_are_visible(self):
        self.units = self.units.replace('UnitFileState=enabled', 'UnitFileState=disabled')
        self.assertEqual(self.health()['state'], 'DEGRADED')
        self.units = self.units.replace('disabled', 'enabled').replace(
            'UnitFileState=static\nResult=success', 'UnitFileState=static\nResult=timeout')
        self.assertEqual(self.health()['state'], 'DEGRADED')

    def test_missing_or_invalid_status_is_visible(self):
        with patch.dict(self.collect.__globals__, run_text=lambda *a, **kw: self.units):
            self.assertEqual(self.collect(self.config, now=self.now)['state'], 'DEGRADED')
        self.status['last_success_at'] = None
        self.assertEqual(self.health()['state'], 'DEGRADED')

    def test_incident_and_recovery_use_existing_notifications(self):
        sent = []
        notify = self.monitor['update_notifications']
        with patch.dict(notify.__globals__, post_mattermost=lambda payload: sent.append(payload) or True,
                        STATE_PATH=Path(self.temp.name) / 'notifications.json'):
            state = {'notification_model': 2, 'incidents': {}}
            for result in ('PASS', 'FAIL', 'FAIL', 'PASS'):
                self.status['result'] = result
                incidents = self.monitor['build_incidents'](
                    {'applications': {'antigravity_update': self.health()}})
                notify({'antigravity-update': incidents['antigravity-update']}, state)
        self.assertEqual(len(sent), 2)
        self.assertEqual(state['incidents']['antigravity-update']['state'], 'OK')


if __name__ == '__main__':
    unittest.main()
