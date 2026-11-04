#!/usr/bin/env python3
"""Backrest 1.14.1 RPC fixtures; no real backup, repository or service calls."""
import copy
import json
from pathlib import Path
import types
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/update-plane'
SNAPSHOT = 'a' * 64
OTHER = 'b' * 64
BASE = '/var/lib/backrest-staging/edge-state/current/plane'
NOW = 1793766000


class PlaneBackrest(unittest.TestCase):
    def setUp(self):
        self.driver = types.ModuleType('plane_update_test')
        exec(compile(SOURCE.read_text(), str(SOURCE), 'exec'), self.driver.__dict__)
        self.config = {'instance': 'edge', 'plans': [{'id': 'edge-state', 'repo': 'edge-pve', 'paths': ['/etc', '/var/lib']}],
                       'repos': [{'id': 'edge-pve'}]}
        self.snapshots = [{'id': SNAPSHOT, 'unixTimeMs': str((NOW - 60) * 1000),
                           'hostname': 'edge', 'tags': ['plan:edge-state', 'created-by:edge'],
                           'paths': ['/etc', '/var/lib']}]
        self.files = {'postgres': 'plane.dump', 'runtime/plane-app': 'plane.env', 'runtime': 'images.json'}
        self.calls = []
        self.driver.rpc = self.rpc
        self.driver.run = lambda *a, **k: self.fail('unexpected process/service call')
        self.clock = patch.object(self.driver.time, 'time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        # Only the existing monitor threshold may be read locally. Prepared
        # staging has been removed by the successful native finalize hook.
        def read_text(path, *a, **k):
            self.assertEqual(str(path), '/etc/edge-monitor/config.json')
            return json.dumps({'backrest': {'degraded_after_s': 3600}})
        self.reader = patch.object(Path, 'read_text', read_text)
        self.reader.start(); self.addCleanup(self.reader.stop)

    def rpc(self, method, payload, **kwargs):
        self.calls.append((method, payload))
        if method == 'GetConfig':
            return copy.deepcopy(self.config)
        if method == 'ListSnapshots':
            self.assertEqual(payload, {'repoId': 'edge-pve', 'planId': 'edge-state'})
            return {'snapshots': copy.deepcopy(self.snapshots)}
        if method == 'ListSnapshotFiles':
            self.assertEqual(payload['repoId'], 'edge-pve')
            self.assertEqual(payload['snapshotId'], SNAPSHOT)
            directory = payload['path'].removeprefix(BASE + '/')
            filename = self.files.get(directory)
            return {'entries': [{'name': filename, 'type': 'file', 'size': '42'}] if filename else []}
        self.fail('unexpected real operation: ' + method)

    def test_current_repository_and_cleaned_staging(self):
        self.assertEqual(self.driver.recent_backup(), SNAPSHOT)
        self.assertEqual(sum(m == 'ListSnapshotFiles' for m, _ in self.calls), 3)

    def test_repository_is_resolved_from_plan_not_a_new_hardcode(self):
        self.config['plans'][0]['repo'] = 'renamed-repo'
        self.config['repos'][0]['id'] = 'renamed-repo'
        original = self.rpc
        def renamed(method, payload, **kwargs):
            if 'repoId' in payload:
                self.assertEqual(payload['repoId'], 'renamed-repo')
                payload = {**payload, 'repoId': 'edge-pve'}
            return original(method, payload, **kwargs)
        self.driver.rpc = renamed
        self.assertEqual(self.driver.recent_backup(), SNAPSHOT)

    def test_missing_or_ambiguous_plan_or_repository_fails_before_repo_access(self):
        for kind in ('missing-plan', 'duplicate-plan', 'missing-repo'):
            with self.subTest(kind=kind):
                config = copy.deepcopy(self.config)
                if kind == 'missing-plan': config['plans'] = []
                if kind == 'duplicate-plan': config['plans'] *= 2
                if kind == 'missing-repo': config['repos'] = []
                self.driver.rpc = lambda method, payload, **k: config if method == 'GetConfig' else self.fail('repository accessed')
                with self.assertRaises(RuntimeError): self.driver.recent_backup()

    def test_missing_or_stale_snapshot_fails(self):
        for snapshots in ([], [{**self.snapshots[0], 'unixTimeMs': str((NOW - 3601) * 1000)}]):
            self.snapshots = snapshots
            with self.assertRaisesRegex(RuntimeError, 'snapshot'):
                self.driver.recent_backup()

    def test_each_required_archived_file_is_checked(self):
        for directory in list(self.files):
            with self.subTest(directory=directory):
                filename = self.files.pop(directory)
                with self.assertRaisesRegex(RuntimeError, filename): self.driver.recent_backup()
                self.files[directory] = filename

    def test_empty_file_or_directory_cannot_replace_dump(self):
        for entry in ({'name': 'plane.dump', 'type': 'file', 'size': '0'},
                      {'name': 'plane.dump', 'type': 'dir', 'size': '42'}):
            with self.subTest(entry=entry):
                self.driver.rpc = lambda m, p, **k: ({'entries': [entry]}
                    if m == 'ListSnapshotFiles' and p['path'].endswith('/postgres') else self.rpc(m, p, **k))
                with self.assertRaisesRegex(RuntimeError, 'plane.dump'): self.driver.recent_backup()

    def test_pre_update_checks_exact_backup_not_unrelated_newer_snapshot(self):
        self.snapshots.append({**self.snapshots[0], 'id': OTHER, 'unixTimeMs': str(NOW * 1000)})
        self.assertEqual(self.driver.recent_backup(SNAPSHOT), SNAPSHOT)
        self.snapshots = self.snapshots[1:]
        with self.assertRaisesRegex(RuntimeError, 'snapshot'):
            self.driver.recent_backup(SNAPSHOT)

    def test_backup_now_passes_completed_snapshot_identity(self):
        before = [{'id': '12', 'flowId': '12', 'status': 'STATUS_PENDING', 'operationBackup': {}}]
        after = before + [{'id': '13', 'flowId': '13', 'snapshotId': SNAPSHOT,
                           'status': 'STATUS_SUCCESS', 'operationBackup': {}},
                          {'id': '14', 'flowId': '13', 'status': 'STATUS_SUCCESS', 'operationRunHook': {}}]
        self.driver.backup_operations = lambda: before if not self.calls else after
        self.driver.rpc = lambda m, p, **k: self.calls.append((m, p)) or {}
        self.driver.recent_backup = lambda snapshot: snapshot
        self.assertEqual(self.driver.backup_now(), SNAPSHOT)
        self.assertEqual(self.calls, [('Backup', {'value': 'edge-state'})])

    def test_failed_backup_hook_stops_before_recovery_or_update(self):
        self.driver.backup_operations = lambda: ([] if not self.calls else [
            {'id': '13', 'flowId': '13', 'snapshotId': SNAPSHOT, 'status': 'STATUS_SUCCESS', 'operationBackup': {}},
            {'id': '14', 'flowId': '13', 'status': 'STATUS_ERROR', 'operationRunHook': {}}])
        self.driver.rpc = lambda m, p, **k: self.calls.append((m, p)) or {}
        self.driver.recent_backup = lambda *a: self.fail('failed flow accepted')
        with self.assertRaisesRegex(RuntimeError, 'flow failed'): self.driver.backup_now()

    def test_missing_completed_snapshot_identity_fails(self):
        with self.assertRaisesRegex(RuntimeError, 'snapshot ID'):
            self.driver.recent_backup('')

    def test_running_flow_is_waited_for_before_snapshot_verification(self):
        polls = iter([[], [
            {'id': '13', 'flowId': '13', 'snapshotId': SNAPSHOT, 'status': 'STATUS_SUCCESS', 'operationBackup': {}},
            {'id': '14', 'flowId': '13', 'status': 'STATUS_INPROGRESS', 'operationIndexSnapshot': {}}], [
            {'id': '13', 'flowId': '13', 'snapshotId': SNAPSHOT, 'status': 'STATUS_SUCCESS', 'operationBackup': {}},
            {'id': '14', 'flowId': '13', 'status': 'STATUS_SUCCESS', 'operationIndexSnapshot': {}}]])
        self.driver.backup_operations = lambda: next(polls)
        self.driver.rpc = lambda m, p, **k: self.calls.append((m, p)) or {}
        self.driver.recent_backup = lambda snapshot: snapshot
        with patch.object(self.driver.time, 'sleep') as sleep:
            self.assertEqual(self.driver.backup_now(), SNAPSHOT)
            sleep.assert_called_once_with(5)


if __name__ == '__main__':
    unittest.main()
