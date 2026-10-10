"""Offline helper contracts, explicitly separate from the real lp2468 pilot."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parent / 'skill/technical-html-translation/scripts/html_workflow.py'
spec = importlib.util.spec_from_file_location('html_workflow', SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def fixture():
    positions = sorted(workflow.POSITIONS)
    return {'translation_id': 10, 'language': 'en', 'component': 'lp2468-wr6220-g5-html',
            'units': [{'id': i + 1, 'position': pos, 'source': [f'产品支持{i + 1}个端口。'],
                       'target': [f'The product supports {i + 1} ports.'], 'state': 20}
                      for i, pos in enumerate(positions)]}


class PlannerTests(unittest.TestCase):
    def test_identical_and_moved_units_reuse_without_model_calls(self):
        old = fixture()
        same = workflow.plan(old, copy.deepcopy(old))
        self.assertEqual((len(same['reuse']), len(same['translate'])), (108, 0))
        moved = copy.deepcopy(old)
        moved['units'][0]['position'], moved['units'][1]['position'] = (
            moved['units'][1]['position'], moved['units'][0]['position'])
        moved['units'].reverse()
        plan = workflow.plan(old, moved)
        self.assertEqual(plan['translation_candidates'], 0)
        self.assertEqual(plan['translation_requests'], 0)
        self.assertEqual({u['id']: u['target'] for u in plan['reuse']},
                         {u['id']: u['target'][0] for u in old['units']})

    def test_confirmed_prose_wraps_reuse_but_table_breaks_do_not(self):
        old = fixture()
        old['units'][0].update(source=['产品支持<br>2000个端口。'], target=['The product supports 2000 ports.'],
                               wrapped_prose=True)
        new = copy.deepcopy(old)
        new['units'][0]['source'] = ['产品支持2000个端口。']
        self.assertEqual(workflow.plan(old, new)['translation_candidates'], 0)
        old['units'][0]['wrapped_prose'] = new['units'][0]['wrapped_prose'] = False
        self.assertEqual(workflow.plan(old, new)['translation_candidates'], 1)

    def test_one_changed_quantity_is_the_only_translation_candidate(self):
        old, new = fixture(), fixture()
        new['units'][0]['source'] = ['产品支持200个端口。']
        plan = workflow.plan(old, new)
        self.assertEqual(len(plan['reuse']), 107)
        self.assertEqual([u['id'] for u in plan['translate']], [1])
        self.assertTrue(workflow.check_blocks(plan, {'1': 'The product supports 200 ports.'})['pass'])
        self.assertFalse(workflow.check_blocks(plan, {'1': 'The product supports 2 ports.'})['pass'])

    def test_conflicting_wording_is_reviewed_and_not_silently_reused(self):
        old = fixture()
        old['units'][1]['source'] = old['units'][0]['source']
        old['units'][1]['target'] = ['A contradictory old translation.']
        result = workflow.plan(old, copy.deepcopy(old))
        self.assertEqual(len(result['review']), 2)
        self.assertEqual(result['translation_candidates'], 0)

    def test_glossary_family_numbers_and_attributes_are_enforced(self):
        plan = {'translate': [{'id': 1, 'source': '<a href="guide">联想问天支持2个端口。</a>'}]}
        self.assertTrue(workflow.check_blocks(plan, {'1': '<a href="guide">Lenovo WenTian supports 2 ports.</a>'})['pass'])
        for target in ['<a href="other">Lenovo WenTian supports 2 ports.</a>',
                       '<a href="guide">ThinkSystem supports 2 ports.</a>',
                       '<a href="guide">Lenovo WenTian supports 3 ports.</a>',
                       '<a href="guide">Lenovo WenTian supports 2个 ports.</a>']:
            self.assertFalse(workflow.check_blocks(plan, {'1': target})['pass'])
        with self.assertRaises(ValueError):
            workflow.check_blocks(plan, {'1': 'x', '2': 'outside scope'})

    def test_wrong_scope_is_rejected(self):
        for field, value in [('language', 'ru'), ('translation_id', 11), ('component', 'other')]:
            data = fixture(); data[field] = value
            with self.assertRaises(ValueError): workflow.plan(data, fixture())
        data = fixture(); data['units'].pop()
        with self.assertRaises(ValueError): workflow.plan(data, fixture())
        data = fixture(); data['units'][1]['position'] = data['units'][0]['position']
        with self.assertRaises(ValueError): workflow.plan(data, fixture())

    def test_structure_css_scripts_and_outside_pages_preservation(self):
        original = '<style>td {color:red}</style><script>const n=1;</script><section data-page-idx="0"><p>中文<br>介绍</p><table><tr><td rowspan="2">2</td></tr></table></section><section data-page-idx="3"><p>保持中文</p></section>'
        english = original.replace('中文<br>介绍', 'English introduction')
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / 'source.html', Path(tmp) / 'target.html'
            source.write_text(original)
            target.write_text(english)
            self.assertTrue(workflow.verify_html(source, target, pilot=False)['pass'])
            for mutated in [english.replace('rowspan="2"', 'rowspan="1"'),
                            english.replace('color:red', 'color:blue'),
                            english.replace('const n=1', 'const n=2'),
                            english.replace('保持中文', 'outside translation')]:
                target.write_text(mutated)
                self.assertFalse(workflow.verify_html(source, target, pilot=False)['pass'])


if __name__ == '__main__':
    unittest.main()
