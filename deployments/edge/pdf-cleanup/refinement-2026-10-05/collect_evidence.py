import json,hashlib,shutil,datetime
from pathlib import Path
r=Path('/tmp/pdf-cleanup-refinement-hya_e3w3');d=Path('/home/core/projects/cloud-infrastructure/deployments/edge/pdf-cleanup/refinement-2026-10-05')
m=json.loads((r/'manifest.json').read_text());selection=json.loads((r/'out/selection.json').read_text());hashes=json.loads((d/'source-hashes.json').read_text())
source_hashes={name:hashes['src/pdf_cleanup/'+name]['candidate_sha256'] for name in ('core.py','native.py','lexical.py')}
records=[json.loads(p.read_text()) for p in (r/'out/results').glob('*.json')]
assert len(records)==len(m['unique_documents'])==49
assert {x['sha256'] for x in records}=={x['sha256'] for x in m['unique_documents']}
for row in records:
 assert row['status']=='passed' and row['independent']['status']=='passed' and row['result']['validation']=='passed',row['path']
 assert row['independent']['pixels_outside_masks']==0 and not row['independent']['failures'] and not row['independent']['document_property_changes']
 assert row['second_pass']['status']=='no_targets' and not row['second_pass']['targets']
 assert row['source_sha256_after']==row['sha256'] and row['candidate_hashes']==source_hashes
 assert row['independent']['pages']==row['result']['pages']
 assert row['independent']['engine']=='156.0.8076.0' and row['independent']['pypdfium2']=='5.14.0' and row['independent']['dpi']==144
for name,row in hashes.items():assert hashlib.sha256((r/'candidate'/name).read_bytes()).hexdigest()==row['candidate_sha256']
sample=[x for x in records if x['phase']=='sample'];holdout=[x for x in records if x['phase']=='holdout']
assert len(sample)==18 and len(holdout)==31
assert sum(x['result']['pages'] for x in sample)==3132 and sum(x['result']['pages'] for x in holdout)==3266
for log,count in [('package-final-tests.log',35),('independent-final-controls.log',7)]:
 text=(r/log).read_text();assert 'Ran '+str(count)+' tests' in text and '\nOK' in text
cli=json.loads((r/'out/cli-smoke/result.json').read_text());assert len(cli)==2 and [x['exit_code'] for x in cli]==[0,2]
assert cli[0]['report']['input_sha256']==cli[0]['report']['output_sha256']
audit=json.loads((r/'out/production-final-audit.json').read_text());assert audit['status']=='passed' and audit['unchanged_files']==115
result_dir=d/'results';result_dir.mkdir(exist_ok=True)
for path in (r/'out/results').glob('*.json'):shutil.copyfile(path,result_dir/path.name)
for name in ['sample-final-0.log','sample-final-1.log','holdout-final-0.log','holdout-final-1.log']:shutil.copyfile(r/name,d/'logs'/name)
shutil.copyfile(r/'out/production-final-audit.json',d/'production-final-audit.json')
shutil.copyfile(r/'out/cli-smoke/result.json',d/'cli-smoke-results.json')
result={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed','deployment_status':'candidate_not_deployed','catalogue_paths':len(m['documents']),'models':len({x['path'].split('/')[0] for x in m['documents']}),'unique_documents':len(records),'pages':sum(x['result']['pages'] for x in records),'sample':{'documents':18,'pages':3132},'holdout':{'documents':31,'pages':3266},'candidate_hashes':source_hashes,'base_and_candidate_files':hashes,'independent':{'engine':'156.0.8076.0','pypdfium2':'5.14.0','dpi':144,'passed_documents':len(records),'pixels_outside_masks':sum(x['independent']['pixels_outside_masks'] for x in records),'body_glyphs':sum(x['independent']['body_glyphs'] for x in records),'glyph_or_reading_order_failures':0,'document_property_changes':0},'second_detection_targets':0,'changed_source_snapshots':0,'tests':{'package':35,'independent_controls':7,'actual_cli':2,'originals_guard_included_in_package':3},'production_audit':{'status':audit['status'],'unchanged_files':audit['unchanged_files'],'production_image_id':audit['production_image_id'],'cloud_added_paths':audit['cloud_added_paths'],'cloud_removed_paths':audit['cloud_removed_paths']},'temporary_artifact_cleanup':{'status':'pending'},'records':[{k:x[k] for k in ('path','sha256','phase','status','total_seconds')} for x in sorted(records,key=lambda row:row['path'])]}
(d/'evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('records','base_and_candidate_files')},ensure_ascii=False))
