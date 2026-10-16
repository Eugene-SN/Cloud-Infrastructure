import sys,importlib.metadata as m,json,hashlib,pathlib
print(json.dumps({"python":sys.version,"packages":dict(sorted((d.metadata["Name"],d.version) for d in m.distributions())),"modules":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pathlib.Path("/usr/local/lib/python3.14/site-packages/pdf_cleanup").glob("*.py")}},indent=2))
