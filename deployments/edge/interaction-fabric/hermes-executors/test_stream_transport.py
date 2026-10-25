import importlib.machinery,importlib.util,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'edge-ai-exec'
class NativeStreamTests(unittest.TestCase):
 def module(self):
  loader=importlib.machinery.SourceFileLoader('ug_helper',str(P));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m);return m
 def test_one_terminal_success_keeps_model_identity(self):
  m=self.module();native={'status':'SUCCESS','num_turns':1,'structured_output':{'ready':True}}
  wire='\n'.join(json.dumps(e) for e in [{'event':'init','init':{'model':'model-x'},'conversation_id':'c1'},{'event':'result','result':native}])
  result=m.stream_result(wire);self.assertEqual(result['model'],'model-x');self.assertTrue(result['structured_output']['ready'])
 def test_missing_or_multiple_turns_are_not_accepted(self):
  m=self.module()
  for events in [[],[{'event':'result','result':{'status':'SUCCESS'}}],[{'event':'init','init':{'model':'x'}},{'event':'result','result':{'num_turns':2}}],[{'event':'init','init':{'model':'x'}},{'event':'result','result':{'num_turns':1}},{'event':'result','result':{'num_turns':2}}]]:
   with self.subTest(events=events),self.assertRaises(ValueError):m.stream_result('\n'.join(json.dumps(e) for e in events))
