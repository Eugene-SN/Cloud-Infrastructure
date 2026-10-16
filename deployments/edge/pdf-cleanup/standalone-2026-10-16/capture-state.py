import hashlib,json,sqlite3,subprocess
from pathlib import Path
root=Path('/srv/cloud/technical-documentation/lenovo')
paths=[p for sub in ('originals','cleaned','translated') for p in (root/sub).rglob('*') if p.is_file()]
paths += [p for p in root.glob('INDEX*') if p.is_file()]
c=sqlite3.connect('file:/srv/n8n/database.sqlite?mode=ro');c.row_factory=sqlite3.Row;c.execute('PRAGMA query_only=ON')
w=[dict(x) for x in c.execute("SELECT id,name,active,activeVersionId,versionId,nodes,connections,settings FROM workflow_entity WHERE id IN ('ENo9jFkwcE4PFOyL','QouVaVNhAqSiYq5D')")]
for item in w:
 for key in ('nodes','connections','settings'):
  item[key+'_sha256']=hashlib.sha256((item.pop(key) or '').encode()).hexdigest()
print(json.dumps({'files':{str(p.relative_to(root)):hashlib.file_digest(p.open('rb'),'sha256').hexdigest() for p in sorted(paths)},'workflows':w},indent=2))
