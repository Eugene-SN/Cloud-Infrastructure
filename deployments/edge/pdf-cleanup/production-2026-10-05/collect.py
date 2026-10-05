"""Preserve nonsecret evidence after all production acceptance checks pass."""
from pathlib import Path
import json,shutil,hashlib,datetime
r=Path(__file__).resolve().parent;repo=Path('/home/core/projects/cloud-infrastructure');audit=json.loads((r/'final-audit.json').read_text());assert audit['status']=='passed'
batch=[json.loads(p.read_text()) for p in sorted((r/'out/batch-records').glob('*.json'))];reviews=[json.loads(p.read_text()) for p in sorted((r/'out/reviews').glob('*.json'))];assert len(batch)==len(reviews)==95 and all(x['status']=='passed' for x in batch+reviews)
target=repo/'deployments/edge/pdf-cleanup/production-2026-10-05';target.mkdir(exist_ok=True)
evidence={'status':'passed','recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All 95 current originals, including duplicate contents in different model folders; actual production adapter/launcher/image, native Nextcloud publication and independent all-page verification','source_commit':audit['runtime']['source_commit'],'image_id':audit['runtime']['image_id'],'source_hashes':json.loads((r/'runtime-verification.json').read_text())['source_hashes'],'models':audit['models'],'originals':95,'unique_contents':49,'pages':audit['all_path_pages'],'body_glyphs':audit['body_glyphs'],'pixels_outside_masks':audit['pixels_outside_masks'],'package_tests':35,'independent_controls':6,'console_controls':2,'cleanup_deletions':json.loads((r/'cleaned-deletions.json').read_text()),'checks':audit['checks'],'runtime':audit['runtime'],'lifecycle':json.loads((r/'lifecycle.json').read_text()),'batch':batch,'reviews':reviews}
(target/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
for name in ('final-audit.json','runtime-verification.json','cleaned-deletions.json','source-commit','image-id','image-tag','Dockerfile','batch.py','dav.py','final_audit.py','collect.py','build-cache-targets.json','audit-worker-resume.json','lifecycle.json','Fonts.Dockerfile','fonts_batch.py','workflow-nonregression.json','production-cleanup.json','new-deployment.json','pre-fonts-deployment.json'):
 shutil.copyfile(r/name,target/name)
for name in ('verify_outputs.py','manifest.json','source-hashes.json','fontscheck.py'):shutil.copyfile(r/'audit'/name,target/name)
logs=target/'logs';logs.mkdir(exist_ok=True)
for name in ('build.log','package-tests.log','review-deps.log','test_reviewer.py.log','cli_smoke.py.log','batch.log','review.log','fonts-build.log','fonttools-before.log','fonttools-check.log','fonts-package-tests.log','fonts-tests-recovery.log','fonts-batch.log','fonts-review.log'):shutil.copyfile(r/name,logs/name)
for name in ('fonttools-before.json','fonttools-fonts.json'):shutil.copyfile(r/'out'/name,target/name)
for sub in ('pre-fonts-batch-records','pre-fonts-reviews'):shutil.copytree(r/'out'/sub,target/sub,dirs_exist_ok=True)
assert not list(target.rglob('*.pdf')) and not list(target.rglob('credential.json'))
print(json.dumps({k:evidence[k] for k in ('status','originals','pages','body_glyphs','pixels_outside_masks')},ensure_ascii=False))
