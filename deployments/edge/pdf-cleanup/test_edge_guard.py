import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pymupdf
from pdf_cleanup.core import CleanupError, cleanup


class EdgeOriginalsGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ['TMPDIR'])
        self.root = Path(self.temp.name)
        self.originals = self.root / 'originals'
        self.originals.mkdir()
        self.input = self.root / 'snapshot.pdf'
        with pymupdf.open() as doc:
            doc.new_page().insert_text((72, 100), 'Useful body')
            doc.save(self.input)

    def tearDown(self):
        self.temp.cleanup()

    def test_external_snapshot_cannot_write_anywhere_inside_originals(self):
        output = self.originals / 'derived.pdf'
        with patch.dict(os.environ, PDF_CLEANUP_ORIGINALS_DIR=str(self.originals)):
            with self.assertRaises(CleanupError) as failure:
                cleanup(self.input, output)
        self.assertEqual(failure.exception.rc, 2)
        self.assertFalse(output.exists())

    def test_symlink_parent_cannot_bypass_originals_protection(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.originals, target_is_directory=True)
        with patch.dict(os.environ, PDF_CLEANUP_ORIGINALS_DIR=str(self.originals)):
            with self.assertRaises(CleanupError) as failure:
                cleanup(self.input, alias / 'derived.pdf')
        self.assertEqual(failure.exception.rc, 2)
        self.assertEqual(list(self.originals.iterdir()), [])

    def test_missing_or_relative_originals_configuration_rejected(self):
        for value in ('', 'originals'):
            with patch.dict(os.environ, PDF_CLEANUP_ORIGINALS_DIR=value):
                with self.assertRaises(CleanupError) as failure:
                    cleanup(self.input, self.root / 'derived.pdf')
            self.assertEqual(failure.exception.rc, 2)
        self.assertFalse((self.root / 'derived.pdf').exists())
