#!/usr/bin/env python3
"""Exercise the collector's real Docker Hub resolver without network or Docker."""
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

source = (Path(__file__).resolve().parents[1] / 'scripts/maintenance-versions-collector').read_text()
block = source.split('docker_hub_snapshot() {', 1)[1].split('\ndocker_remote_snapshot()', 1)[0]
resolver = compile(block.split("-c '\n", 1)[1].rsplit("' \\\n", 1)[0], '<docker_hub_snapshot>', 'exec')
REMOTE = 'sha256:' + 'a' * 64
LOCAL = 'sha256:' + 'b' * 64


def resolve(aliases, installed='9.1.2', local=LOCAL, component='WEBLATE_VALKEY'):
    calls = []

    def urlopen(request, **kwargs):
        calls.append(request.full_url)
        if request.full_url.endswith('/latest'):
            data = {'digest': REMOTE}
        elif '?page_size=100&ordering=last_updated' in request.full_url:
            data = {'results': [{'name': name, 'digest': digest} for name, digest in aliases]}
        else:
            raise AssertionError('unexpected network request: ' + request.full_url)
        return io.BytesIO(json.dumps(data).encode())

    stdout = io.StringIO()
    with patch('urllib.request.urlopen', urlopen), patch.object(sys, 'argv', [
        'resolver', component, 'valkey/valkey', 'latest', local, installed,
    ]), contextlib.redirect_stdout(stdout):
        try:
            exec(resolver, {})
        except SystemExit as exc:
            assert exc.code == 0
    return stdout.getvalue().strip(), calls


class ValkeyDiscovery(unittest.TestCase):
    def test_new_stable_version_matches_floating_manifest(self):
        value, _ = resolve([(n, REMOTE) for n in ('latest', '9', '9.1', '9.1.3', '9.1.3-trixie')]
                           + [('9.9.9', LOCAL), ('10.0.0-rc1', REMOTE)])
        self.assertEqual(value, REMOTE + '|9.1.3')

    def test_same_version_new_image_build(self):
        self.assertEqual(resolve([('9.1.2', REMOTE)])[0], REMOTE + '|9.1.2')

    def test_current_manifest_uses_runtime_without_listing_tags(self):
        value, calls = resolve([], local=REMOTE)
        self.assertEqual(value, REMOTE + '|9.1.2')
        self.assertEqual(len(calls), 1)

    def test_no_matching_stable_alias_stays_unresolved(self):
        self.assertEqual(resolve([('9.1.3-rc1', REMOTE), ('9.1.3', LOCAL)])[0], '')

    def test_numeric_version_order_and_existing_component(self):
        aliases = [('9.1.9', REMOTE), ('9.1.10', REMOTE)]
        self.assertEqual(resolve(aliases)[0], REMOTE + '|9.1.10')
        self.assertEqual(resolve(aliases, component='AUTHELIA')[0], REMOTE + '|9.1.10')


if __name__ == '__main__':
    unittest.main()
