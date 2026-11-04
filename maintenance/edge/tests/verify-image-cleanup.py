#!/usr/bin/env python3
"""Run the real service cleanup against a disposable Docker reference model."""
import json
from pathlib import Path
import runpy
import subprocess
import tempfile
from unittest.mock import patch

SOURCE=Path(__file__).resolve().parents[1]/'scripts/docker-service-images'
OLD='sha256:'+'a'*64
NEW='sha256:'+'b'*64
TAG='example/service:old'
DIGEST='example/service@sha256:'+'c'*64


def scenario(*, used=False, declared=False, pending=False, foreign=False, fail=False):
    module=runpy.run_path(str(SOURCE)); namespace=module['cleanup'].__wrapped__.__globals__
    with tempfile.TemporaryDirectory(prefix='service-image-cleanup.') as temporary:
        state=Path(temporary)
        receipt=state/'TEST.json'
        payload={'target':'TEST','phase':'pending','images':[{'id':OLD,'references':[TAG]}]}
        receipt.write_text(json.dumps(payload))
        if pending:(state/'OTHER.json').write_text(json.dumps(payload|{'target':'OTHER'}))
        images={OLD:{'Id':OLD,'RepoTags':[TAG,DIGEST]+(['foreign/service:keep'] if foreign else []),'RepoDigests':[DIGEST]}}
        calls=[]
        def command(argv, **kwargs):
            assert argv[0]=='docker',argv
            calls.append(argv)
            rc=0;out='';err=''
            if argv[1:3]==['ps','-aq']:out='container\n' if used else ''
            elif argv[1:3]==['inspect','container']:out=json.dumps([{'Image':OLD}])
            elif argv[1:3]==['image','ls']:out='\n'.join([NEW,*images])+'\n'
            elif argv[1:3]==['image','inspect']:
                image=images.get(argv[3]);rc=0 if image else 1
                out=json.dumps([image]) if image else '';err='' if image else 'No such image'
            elif argv[1:3]==['image','rm']:
                refs=[v for v in argv[3:] if not v.startswith('--')]
                for ref in refs:
                    image=images.get(OLD)
                    if not image or (ref!=OLD and ref not in image['RepoTags']+image['RepoDigests']):
                        rc=1;err='No such image';continue
                    if fail:rc=1;err='daemon denied deletion';break
                    if foreign:
                        image['RepoTags']=[r for r in image['RepoTags'] if r!=ref]
                        image['RepoDigests']=[r for r in image['RepoDigests'] if r!=ref]
                    else:
                        # Docker removes the last tag together with its digest alias.
                        del images[OLD]
            else:raise AssertionError('unexpected Docker command: '+repr(argv))
            result=subprocess.CompletedProcess(argv,rc,out,err)
            if kwargs.get('check'):result.check_returncode()
            return result
        with patch.dict(namespace,STATE=state,declared_images=lambda:{OLD} if declared else set()), patch.object(subprocess,'run',side_effect=command):
            error=None
            try:module['cleanup'].__wrapped__('TEST')
            except subprocess.CalledProcessError as e:error=e
        removals=[c for c in calls if c[1:3]==['image','rm']]
        if used or declared or pending:
            assert not removals and OLD in images and receipt.exists()
            assert json.loads(receipt.read_text())['phase']=='complete_in_use'
        elif fail:
            assert error and OLD in images and receipt.exists(),'real deletion errors must remain failures'
        else:
            assert error is None, 'deleting the first alias removed the second alias but cleanup reported failure'
            assert not receipt.exists()
            if foreign:assert images[OLD]['RepoTags']==['foreign/service:keep']
            else:assert OLD not in images
            assert all(len([r for r in c[3:] if not r.startswith('--')])==1 for c in removals)
        assert all('--force' not in c and '-f' not in c for c in calls)


scenario()
scenario(used=True)
scenario(declared=True)
scenario(pending=True)
scenario(foreign=True)
scenario(fail=True)
print('SERVICE_IMAGE_CLEANUP=PASS|CASES=6|REAL_DOCKER_CALLS=NO|REAL_UPDATES=NO')
