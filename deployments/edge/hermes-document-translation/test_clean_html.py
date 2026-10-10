#!/usr/bin/env python3
"""Offline verifier regressions, not evidence of real translation quality."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parent/'skill/technical-html-translation/scripts/clean_html.py'
spec = importlib.util.spec_from_file_location('clean_html', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

class VerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = Path(self.tmp.name)
        self.source = self.w/'source.html'
        self.source.write_text('<html lang="und"><head><style>p{color:red}</style></head><body><section class="docvortex-page" data-page-idx="0"><p class="docvortex-text"><strong>测试2</strong><br/><span class="docvortex-preserve-whitespace"><strong>一个项目</strong></span></p><table><tbody><tr><td>选项1<br/>条件<br/>项目</td></tr></tbody></table></section></body></html>')
        self.save('manifest.json', {'source_only':True,'prior_targets_provided':False,
                  'translation_memory_provided':False,'pages':[1],
                  'source_html_sha256':helper.digest(self.source.read_bytes())})
        with contextlib.redirect_stdout(io.StringIO()):
            helper.extract(self.source,self.w/'manifest.json',self.w)
        self.pack=helper.load(self.w/'extracted.json')
        self.pack['units'][0]['numeric_source_word_equivalences']=[{'source_quote':'一个项目','number':'1'}]
        self.pack['units'][1].update(remove_br_indices=[0],normalization_reason='Audited clause continuation',
            numeric_word_equivalences=[{'source_quote':'选项1','target_pattern':r'\bone\b','number':'1'}])
        self.save('extracted.json',self.pack)
        self.targets={'page01-block000':'<strong>English 2</strong> <span class="docvortex-preserve-whitespace"><strong>1 entry</strong></span>',
                      'page01-block001':'English one condition<br/>entry'}
        self.output=self.w/'output.html'

    def tearDown(self): self.tmp.cleanup()
    def save(self,name,value): (self.w/name).write_text(json.dumps(value))
    def assemble(self):
        self.save('page-01.en.json',self.targets)
        with contextlib.redirect_stdout(io.StringIO()):
            return helper.assemble(self.w/'extracted.json',self.w,self.output)

    def test_source_relative_success_and_exact_word_quantity(self):
        self.assertEqual(self.assemble(),0)
        checks=helper.load(self.output.with_suffix('.checks.json'))
        self.assertEqual(checks['counts']['br'],1)
        self.assertEqual(checks['counts']['span'],1)
        self.assertEqual(len(checks['verified_numeric_word_equivalences']),2)
        self.assertIn('<style>p{color:red}</style>',self.output.read_text())
        self.assertTrue(self.output.read_text().startswith('<html lang="en">'))
        self.assertTrue(self.source.read_text().startswith('<html lang="und">'))
        self.assertFalse(checks['all_bytes_outside_translated_inner_fragments_preserved'])
        self.assertTrue(checks['all_bytes_outside_translated_inner_fragments_preserved_except_declared_metadata'])
        self.assertEqual(checks['metadata_exceptions'],[{'type':'html-language','source_tag':'<html lang="und">',
                         'target_tag':'<html lang="en">','source_byte_offset':0}])

    def test_missing_block_and_false_review_coverage_rejected(self):
        self.targets.pop('page01-block001')
        with self.assertRaisesRegex(ValueError,'coverage'):self.assemble()
        self.save('review.json',{'checked_pages':[1],'checked_block_ids':['page01-block000'],'claimed_blocks':2})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(helper.check_review(self.w/'extracted.json',self.w/'review.json'),1)

    def test_lost_inline_wrapper_rejected(self):
        self.targets['page01-block000']='<strong>English 2 entry</strong>'
        with self.assertRaisesRegex(ValueError,'markup'):self.assemble()

    def test_undeclared_table_break_removal_rejected(self):
        self.targets['page01-block001']='English one condition entry'
        with self.assertRaisesRegex(ValueError,'markup'):self.assemble()

    def test_wrong_quantity_and_source_hash_rejected(self):
        self.targets['page01-block001']='English two condition<br/>entry'
        self.assertEqual(self.assemble(),1)
        self.assertTrue(helper.load(self.output.with_suffix('.checks.json'))['numeric_review_flags'])
        self.targets['page01-block001']='English one condition<br/>entry'
        self.targets['page01-block000']=self.targets['page01-block000'].replace('1 entry','2 entries')
        self.assertEqual(self.assemble(),1)
        self.pack['units'][0]['numeric_source_word_equivalences'][0]['source_quote']='不存在'
        self.save('extracted.json',self.pack)
        with self.assertRaisesRegex(ValueError,'unique word evidence'):self.assemble()
        self.source.write_text(self.source.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'Source changed'):self.assemble()

if __name__=='__main__':unittest.main()
