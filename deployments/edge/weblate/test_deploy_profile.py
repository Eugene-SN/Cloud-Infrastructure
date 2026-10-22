"""Real filesystem tests; run with sudo to verify UID/GID 1000 ownership."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('deploy-profile.py')


@unittest.skipUnless(os.geteuid() == 0, 'real ownership tests require root')
class ProfileInstallTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'the canonical profile installer is missing')
        self.module = runpy.run_path(str(SCRIPT))
        self.temporary = tempfile.TemporaryDirectory(prefix='weblate-profile-test.')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.program = self.base / 'opt/weblate'
        self.data = self.base / 'srv/weblate/data'
        self.program.mkdir(parents=True)
        self.data.mkdir(parents=True)
        self.roots = (
            (self.program / 'provider', self.program),
            (self.data / 'python/td_translate', self.data),
            (self.data / 'hermes-skills', self.data),
        )
        self.globals = self.module['deploy'].__globals__
        self.locations = patch.dict(self.globals, LOCATIONS=self.roots)
        self.locations.start()
        self.addCleanup(self.locations.stop)
        self.source = self.base / 'source.py'
        self.source.write_bytes(b'profile contents\n')

    def assert_owner(self, path):
        st = path.stat()
        self.assertEqual((st.st_uid, st.st_gid), (1000, 1000), str(path))

    def test_creates_every_missing_intermediate_directory(self):
        target = self.data / 'hermes-skills/technical-html-translation/references/policy.py'
        self.module['deploy'](self.source, target)
        self.assertEqual(target.read_bytes(), b'profile contents\n')
        for path in [target, *target.parents]:
            if path == self.data:
                break
            self.assert_owner(path)
        self.assertEqual(self.data.stat().st_uid, 0, 'must not chown the mount anchor')

    def test_replacement_repairs_existing_root_owners_and_preserves_modes(self):
        target = self.data / 'python/td_translate/html_contract.py'
        target.parent.mkdir(parents=True)
        target.parent.chmod(0o750)
        target.write_bytes(b'old contents\n')
        target.chmod(0o640)
        old_inode = target.stat().st_ino
        self.module['deploy'](self.source, target)
        self.assertEqual(target.read_bytes(), b'profile contents\n')
        self.assertNotEqual(target.stat().st_ino, old_inode)
        self.assert_owner(target)
        self.assert_owner(target.parent)
        self.assert_owner(target.parent.parent)
        self.assertEqual(target.stat().st_mode & 0o777, 0o640)
        self.assertEqual(target.parent.stat().st_mode & 0o777, 0o750)
        self.assertEqual(list(target.parent.glob('.profile-*')), [])

    def test_tree_deployment_supports_all_three_profile_areas(self):
        source = self.base / 'package'
        (source / 'references/empty').mkdir(parents=True)
        (source / 'SKILL.md').write_bytes(b'skill\n')
        (source / 'references/data.json').write_bytes(b'{}\n')
        for root, anchor in self.roots:
            with self.subTest(root=root):
                self.module['deploy'](source, root)
                for path in [root, *root.rglob('*')]:
                    self.assert_owner(path)
                self.assertEqual((root / 'SKILL.md').read_bytes(), b'skill\n')
                self.assertTrue((root / 'references/empty').is_dir())

    def test_identical_content_repairs_ownership_without_replacing_file(self):
        target = self.program / 'provider/hermes.py'
        target.parent.mkdir()
        target.write_bytes(self.source.read_bytes())
        original = target.stat()
        self.module['deploy'](self.source, target)
        self.assert_owner(target)
        self.assertEqual(target.stat().st_ino, original.st_ino)
        self.assertEqual(target.stat().st_mtime_ns, original.st_mtime_ns)
        self.module['deploy'](target, target)
        self.assertEqual(target.stat().st_ino, original.st_ino)

    def test_other_paths_and_symlinks_are_rejected_without_writes(self):
        outside = self.base / 'outside'
        outside.mkdir()
        sentinel = outside / 'hermes.py'
        sentinel.write_bytes(b'untouched\n')
        for target in [sentinel, self.program / 'cloud.env']:
            with self.assertRaises(ValueError):
                self.module['deploy'](self.source, target)
        (self.program / 'provider').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.module['deploy'](self.source, self.program / 'provider/hermes.py')
        self.assertEqual(sentinel.read_bytes(), b'untouched\n')
        self.assertEqual(outside.stat().st_uid, 0)

    def test_cli_runs_only_native_validation_and_propagates_failure(self):
        target = self.program / 'provider/hermes.py'
        calls = []
        def command(argv, **kwargs):
            calls.append(argv)
            raise subprocess.CalledProcessError(1, argv)
        with patch.object(self.globals['subprocess'], 'run', command), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                self.module['main']([str(self.source), str(target)])
        self.assertEqual(calls, [['docker', 'exec', 'weblate', '/app/venv/bin/weblate',
                                 'check', '--deploy', '--fail-level', 'ERROR']])
        self.assert_owner(target)


if __name__ == '__main__':
    unittest.main()
