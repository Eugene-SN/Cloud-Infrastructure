import json,hashlib,subprocess,datetime
from pathlib import Path
r=Path('/tmp/pdf-cleanup-refinement-hya_e3w3');m=json.loads((r/'manifest.json').read_text())
rows=[]
for row in m['baseline']:
 p=Path(row['path']);actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 rows.append(dict(row,actual_sha256=actual,unchanged=actual==row['sha256']))
cloud=Path('/srv/cloud/technical-documentation/lenovo')
actual_paths={str(p) for p in cloud.rglob('*') if p.is_file()}
expected={x['path'] for x in m['baseline'] if x['path'].startswith(str(cloud)+'/')}
image=subprocess.check_output(['docker','image','inspect','--format','{{.Id}}','edge/pdf-cleanup:8257cb36be78'],text=True).strip()
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'baseline_files':len(rows),'unchanged_files':sum(x['unchanged'] for x in rows),'cloud_added_paths':sorted(actual_paths-expected),'cloud_removed_paths':sorted(expected-actual_paths),'production_image_id':image,'production_image_unchanged':image=='sha256:3ff39309bab88fca2d28edb606879afbe5ce18fa366d48ade3e9440cbd82c06e','n8n_changes_performed_by_this_workstream':False}
result['status']='passed' if all(x['unchanged'] for x in rows) and actual_paths==expected and result['production_image_unchanged'] else 'differences'
(r/'out/production-final-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'},ensure_ascii=False))
assert result['status']=='passed'
