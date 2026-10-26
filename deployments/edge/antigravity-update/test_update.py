"""Offline lifecycle tests; all native commands and /proc access are substituted."""
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class UpdateTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('update', Path(__file__).with_name('update.py'))
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory(prefix='agy-update-test-')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.module.STATE = root / 'state'
        self.module.LOGS = root / 'logs'
        self.module.LOGS.mkdir()
        self.module.BINARY = root / 'agy'
        self.module.BINARY.write_text('1.0')
        self.running = root / 'running'
        os.link(self.module.BINARY, self.running)
        self.pid = 100
        self.next_version = None
        self.fail = False
        self.timeout = False
        self.restarts = 0
        self.status = self.module.STATE / 'status.json'

    def replace_binary(self, version):
        replacement = self.module.BINARY.with_suffix('.new')
        replacement.write_text(version)
        replacement.replace(self.module.BINARY)

    def command(self, argv, **kwargs):
        if argv[-1] == 'update':
            if self.next_version:
                self.replace_binary(self.next_version)
            if self.timeout:
                raise subprocess.TimeoutExpired(argv, 720)
            return subprocess.CompletedProcess(argv, 1 if self.fail else 0)
        self.assertEqual(argv, ['systemctl', '--user', 'restart', self.module.DAEMON])
        self.restarts += 1
        self.pid += 1
        self.running.unlink()
        os.link(self.module.BINARY, self.running)
        return subprocess.CompletedProcess(argv, 0)

    def execute(self, ready=True, running=True):
        real_copy = shutil.copyfile
        def copy(source, target):
            return real_copy(self.running if str(source).startswith('/proc/') else source, target)
        def version(binary):
            return (self.running if str(binary).startswith('/proc/') else binary).read_text()
        def pid():
            if not running:
                raise RuntimeError('native daemon is not running')
            return self.pid
        with patch.object(self.module, 'version', side_effect=version), \
             patch.object(self.module, 'daemon_pid', side_effect=pid), \
             patch.object(self.module, 'applied', side_effect=lambda pid: os.path.samefile(
                 self.running, self.module.BINARY)), \
             patch.object(self.module.shutil, 'copyfile', side_effect=copy), \
             patch.object(self.module.subprocess, 'run', side_effect=self.command), \
             patch.object(self.module, 'wait_ready', **(
                 {'return_value': (self.pid + (1 if self.next_version else 0), 'daemon.log')}
                 if ready else {'side_effect': RuntimeError('Connected timeout')})), \
             patch.object(self.module, 'log'):
            return self.module.run_update()

    def test_real_change_restarts_and_removes_verified_previous(self):
        self.next_version = '2.0'
        self.assertEqual(self.execute(), 0)
        self.assertEqual(self.restarts, 1)
        self.assertFalse((self.module.STATE / 'previous-agy').exists())
        self.assertFalse((self.module.STATE / 'previous.json').exists())
        self.assertEqual(json.loads(self.status.read_text())['after_version'], '2.0')
        self.assertFalse((self.module.STATE / 'candidate-agy').exists())

    def test_no_change_keeps_pid_and_removes_stale_backup(self):
        self.next_version = '2.0'
        self.execute()
        (self.module.STATE / 'previous-agy').write_text('obsolete')
        (self.module.STATE / 'previous.json').write_text('{}')
        self.next_version = None
        self.assertEqual(self.execute(), 0)
        self.assertEqual(self.restarts, 1)
        self.assertFalse((self.module.STATE / 'previous-agy').exists())
        self.assertFalse((self.module.STATE / 'previous.json').exists())

    def test_foreground_update_is_applied_even_with_no_new_release(self):
        self.replace_binary('2.0')
        self.assertEqual(self.execute(), 0)
        self.assertEqual(self.restarts, 1)
        self.assertFalse((self.module.STATE / 'previous-agy').exists())

    def test_failed_readiness_keeps_previous_for_unresolved_update(self):
        self.next_version = '2.0'
        self.assertEqual(self.execute(ready=False), 1)
        self.assertEqual((self.module.STATE / 'previous-agy').read_text(), '1.0')

    def test_update_failure_does_not_restart_or_erase_last_success(self):
        self.execute()
        success = json.loads(self.status.read_text())['last_success_at']
        self.fail = True
        self.next_version = '2.0'
        self.assertEqual(self.execute(), 1)
        self.assertEqual(self.restarts, 0)
        self.assertEqual(json.loads(self.status.read_text())['last_success_at'], success)
        self.assertEqual((self.module.STATE / 'previous-agy').read_text(), '1.0')

    def test_stopped_daemon_and_readiness_timeout_fail(self):
        self.assertEqual(self.execute(running=False), 1)
        self.assertEqual(self.execute(ready=False), 1)
        self.assertIsNone(json.loads(self.status.read_text())['last_success_at'])

    def test_interrupted_install_keeps_running_binary_for_recovery(self):
        self.next_version = '2.0'
        self.timeout = True
        self.assertEqual(self.execute(), 1)
        self.assertEqual(self.restarts, 0)
        self.assertEqual((self.module.STATE / 'previous-agy').read_text(), '1.0')

    def test_connection_must_belong_to_pid_and_version_and_be_latest(self):
        log = self.module.LOGS / 'cli-20261016_010000.log'
        log.write_text('Starting language server process with pid 100\n'
                       'Language server version: 1.0\nConnection status: Connected\n')
        self.assertEqual(self.module.connected_log(100, '1.0'), str(log))
        self.assertIsNone(self.module.connected_log(101, '1.0'))
        self.assertIsNone(self.module.connected_log(100, '2.0'))
        with log.open('a') as stream:
            stream.write('Connection status: Disconnected\n')
        self.assertIsNone(self.module.connected_log(100, '1.0'))

    def test_ready_rejects_flapping_pid_and_wrong_binary(self):
        with patch.object(self.module, 'daemon_pid', side_effect=[100, 101, 102]), \
             patch.object(self.module, 'applied', return_value=True), \
             patch.object(self.module, 'connected_log', return_value='daemon.log'), \
             patch.object(self.module.time, 'monotonic', side_effect=[0, 0, 2, 4, 6]), \
             patch.object(self.module.time, 'sleep'):
            with self.assertRaises(RuntimeError):
                self.module.wait_ready('1.0', timeout=6)
        with patch.object(self.module, 'daemon_pid', return_value=100), \
             patch.object(self.module, 'applied', return_value=False), \
             patch.object(self.module.time, 'monotonic', side_effect=[0, 0, 2]), \
             patch.object(self.module.time, 'sleep'):
            with self.assertRaises(RuntimeError):
                self.module.wait_ready('1.0', timeout=2)

    def test_ready_accepts_stable_connected_process(self):
        with patch.object(self.module, 'daemon_pid', return_value=100), \
             patch.object(self.module, 'applied', return_value=True), \
             patch.object(self.module, 'connected_log', return_value='daemon.log'), \
             patch.object(self.module.time, 'monotonic', side_effect=[0, 0, 2]), \
             patch.object(self.module.time, 'sleep'):
            self.assertEqual(self.module.wait_ready('1.0'), (100, 'daemon.log'))


if __name__ == '__main__':
    unittest.main()
