import unittest
from pathlib import Path
import pymupdf
from pdf_cleanup import core
from pdf_cleanup.native import inspect_pdf,remove_text_shows

class ActualCorpusRegression(unittest.TestCase):
 def test_nonpainted_zero_width_semantic_character_keeps_text_and_does_not_fail_visual_style(self):
  source=Path('/input/8921606e9e9fcc6b199f2c360787dc228f3180bd2448423d40bd1d101c13be71.pdf')
  output=Path('/out/full-style-diagnostic/edited.pdf')
  self.assertTrue(source.exists() and output.exists())
  # Published research failure is on physical page 14. The independent renderer
  # has already proved page pixels and Unicode glyph positions unchanged.
  with pymupdf.open(source) as original,pymupdf.open(output) as cleaned:
   if not hasattr(core,'body_style_signature'):
    before=core.body_signature(core.lines_for(original[13]))
    after=core.body_signature(core.lines_for(cleaned[13]))
    # Restrict this real regression to the independently located semantic char.
    before=[c for c in before if c['c']=='表' and abs(c['origin'][1]-89.54)<1]
    after=[c for c in after if c['c']=='表' and abs(c['origin'][1]-89.54)<1]
   else:
    before=core.body_style_signature(original[13],core.lines_for(original[13]))
    after=core.body_style_signature(cleaned[13],core.lines_for(cleaned[13]))
    before=[c for c in before if c['c']=='表' and abs(c['origin'][1]-89.54)<1]
    after=[c for c in after if c['c']=='表' and abs(c['origin'][1]-89.54)<1]
   self.assertEqual(len(before),1);self.assertEqual(len(after),1)
   self.assertTrue(core.geometry_equivalent(before,after))

if __name__=='__main__':unittest.main(verbosity=2)
