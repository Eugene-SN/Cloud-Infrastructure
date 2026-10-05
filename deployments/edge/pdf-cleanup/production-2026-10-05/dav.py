import base64,json,urllib.request,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cred=json.loads((ROOT/'credential.json').read_text())[0]['data']
base='http://172.30.0.6/remote.php/webdav'
def request(method,path,data=None,content_type=None):
 url=base+'/technical-documentation/lenovo/'+urllib.parse.quote(path,safe='/')
 headers={'Host':'nextcloud.edge.internal','Authorization':'Basic '+base64.b64encode((cred['user']+':'+cred['password']).encode()).decode()}
 if content_type:headers['Content-Type']=content_type
 req=urllib.request.Request(url,data=data,headers=headers,method=method)
 with urllib.request.urlopen(req,timeout=120) as response:return response.status,response.read(),dict(response.headers)
