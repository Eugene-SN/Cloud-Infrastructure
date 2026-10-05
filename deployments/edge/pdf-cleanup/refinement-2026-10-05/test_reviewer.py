"""Positive and negative controls for the independent review harness."""
import unittest, tempfile
from pathlib import Path
import pymupdf
from review_pdfium import compare

class ReviewControls(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(dir='/out'); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def pdf(self,name,word='BODY',color=(0,0,0),rotation=0):
        doc=pymupdf.open(); page=doc.new_page(width=400,height=600)
        page.insert_text((60,100),word,fontsize=16,color=color)
        page.set_cropbox(pymupdf.Rect(20,20,380,580)); page.set_rotation(rotation)
        path=self.root/name; doc.save(path); doc.close(); return str(path)
    def test_identical_file_passes(self):
        path=self.pdf('a.pdf'); result=compare(path,path,[[]],[[]]); self.assertEqual(result['status'],'passed')
    def test_removal_mask_does_not_imply_every_source_glyph_was_removed(self):
        path=self.pdf('a.pdf')
        with pymupdf.open(path) as doc:box=list(doc[0].get_text('rawdict')['blocks'][0]['lines'][0]['bbox'])
        result=compare(path,path,[[box]],[[]]);self.assertEqual(result['status'],'passed',result)
    def test_color_damage_is_visible(self):
        result=compare(self.pdf('a.pdf'),self.pdf('b.pdf',color=(1,0,0)),[[]],[[]])
        self.assertGreater(result['pixels_outside_masks'],0)
    def test_text_damage_is_detected(self):
        result=compare(self.pdf('a.pdf'),self.pdf('b.pdf',word='B0DY'),[[]],[[]])
        self.assertEqual(result['status'],'differences'); self.assertTrue(result['failures'][0]['missing_glyphs'])
    def test_metadata_damage_is_detected(self):
        source=self.pdf('a.pdf'); output=self.pdf('b.pdf')
        with pymupdf.open(output) as doc:
            doc.set_metadata({'title':'Changed document title'})
            doc.save(str(self.root/'metadata.pdf'))
        result=compare(source,str(self.root/'metadata.pdf'),[[]],[[]])
        self.assertIn('metadata',result['document_property_changes'])
    def test_exact_removal_masks_with_crop_and_rotation(self):
        for rotation in (0,90,180,270):
            with self.subTest(rotation=rotation):
                path=self.pdf('a.pdf',rotation=rotation)
                with pymupdf.open(path) as doc:
                    boxes=[list(c['bbox']) for b in doc[0].get_text('rawdict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] for c in s['chars']]
                    for box in boxes: doc[0].add_redact_annot(box,fill=False)
                    doc[0].apply_redactions(); cleaned=str(self.root/'b.pdf'); doc.save(cleaned)
                result=compare(path,cleaned,[boxes],[[]]); self.assertEqual(result['status'],'passed',result)

if __name__=='__main__': unittest.main(verbosity=2)
