#!/usr/bin/env python3
"""Run native binary preparation/copy with disposable files and fake service calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source',default=str(root/'scripts/update-github-binary'));p.add_argument('--case');args=p.parse_args()
for failure in ([args.case] if args.case else ('none','download','checksum','version','install','health')):
    with tempfile.TemporaryDirectory(prefix='backrest-update-test-') as temporary:
        base=Path(temporary);(base/'bin').mkdir();(base/'work').mkdir()
        binary=base/'backrest'
        version='0.0.0' if failure=='version' else '1.14.1'
        binary.write_text('#!/bin/bash\n[ "$1" = --version ] || exit 89\necho "backrest version: '+version+'"\n')
        binary.chmod(0o755)
        asset='backrest_Linux_x86_64.tar.gz'
        with tarfile.open(base/asset,'w:gz') as archive:archive.add(binary,arcname='backrest')
        expected='0'*64 if failure=='checksum' else hashlib.sha256((base/asset).read_bytes()).hexdigest()
        (base/'checksums').write_text(expected+'  '+asset+'\n')
        release={'tag_name':'v1.14.1','assets':[
            {'name':asset,'browser_download_url':str(base/asset)},
            {'name':'backrest_1.14.1_checksums.txt','browser_download_url':str(base/'checksums')}]}
        (base/'release.json').write_text(json.dumps(release))
        installed=base/'installed';installed.mkdir();(installed/'backrest').write_text('previous binary')
        body=Path(args.source).read_text()
        body=body.replace('work_root=/var/tmp','work_root='+str(base/'work')).replace('/var/backups/edge-maintenance',str(base/'backups')).replace('/usr/local/bin/$binary',str(installed)+'/$binary')
        header='''
curl() {
  if [[ "$*" == *api.github.com* ]]; then cat RELEASE; return; fi
  if [ FAILURE = download ]; then return 22; fi
  local destination=''
  while [ "$#" -gt 1 ]; do
    if [ "$1" = -o ]; then destination="$2"; shift 2; else shift; fi
  done
  cp -- "$1" "$destination"
}
systemctl() {
  echo "$*" >> SERVICE_LOG
  if [ FAILURE = health ] && [ "$1" = is-active ] && [ ! -e BASE/failed-once ]; then touch BASE/failed-once; return 1; fi
}
install() {
  local destination="${@: -1}"
  [[ "$destination" == BASE/* ]] || return 90
  if [ "$1" = -d ]; then mkdir -p "$destination";
  else
    if [ FAILURE = install ] && [ ! -e BASE/failed-once ]; then touch BASE/failed-once; return 23; fi
    cp -- "${@: -2:1}" "$destination"; chmod 755 "$destination"
  fi
}
'''.replace('RELEASE',str(base/'release.json')).replace('FAILURE',failure).replace('SERVICE_LOG',str(base/'services.log')).replace('BASE',str(base))
        script=base/'driver';script.write_text('#!/bin/bash\n'+header+body)
        subprocess.run(['bash','-n',str(script)],check=True)
        result=subprocess.run(['bash',str(script),'BACKREST'],capture_output=True,text=True)
        if failure=='none':
            assert result.returncode==0,result.stderr
            assert (base/'services.log').read_text().splitlines()==['stop backrest','start backrest','is-active --quiet backrest']
            assert (installed/'backrest').read_bytes()==binary.read_bytes()
        elif failure in ('install','health'):
            assert result.returncode!=0
            assert (installed/'backrest').read_text()=='previous binary'
            assert (base/'services.log').read_text().splitlines()[-2:]==['start backrest','is-active --quiet backrest']
        else:
            assert result.returncode!=0
            assert not (base/'services.log').exists(),'preparation failure touched a service'
            assert (installed/'backrest').read_text()=='previous binary'
        assert not list((base/'work').iterdir()),'temporary files retained'
print('BACKREST_PREPARATION_AND_VERSION=PASS|DOWNLOAD_CHECKSUM_VERSION_FAILURES|REAL_UPDATES=NO|SERVICE_RESTARTS=NO')
