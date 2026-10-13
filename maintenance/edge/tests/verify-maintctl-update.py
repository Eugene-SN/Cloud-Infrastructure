#!/usr/bin/env python3
"""Run actual maintctl update functions against disposable command substitutes."""
import argparse
from pathlib import Path
import subprocess
import tempfile

p=argparse.ArgumentParser();p.add_argument('--source',default='/usr/local/bin/maintctl');args=p.parse_args()
source=Path(args.source).read_text()
functions=source[source.index('cmd_update_xray()'):source.index('show_ports()')]
failures=[]
for target,version in (('hy2','2.13.0'),('xray','26.10.0')):
    for fail_download in (False,True):
        with tempfile.TemporaryDirectory(prefix='maintctl-update-test-') as temporary:
            base=Path(temporary)
            (base/'bin').mkdir();(base/'work').mkdir()
            for name,output in (('hysteria','Version: v2.13.0'),('xray','Xray 26.10.0')):
                binary=base/'bin'/name
                binary.write_text('#!/bin/bash\necho '+repr(output)+'\n');binary.chmod(0o755)
            body=functions.replace('/usr/local/bin/',str(base/'bin')+'/').replace('/var/backups/vpn-stack',str(base/'backups')).replace('/var/tmp/',str(base/'work')+'/')
            body=body.replace('/etc/hysteria/config.yaml',str(base/'absent-config')).replace('/etc/xray/config.json',str(base/'absent-config'))
            script=base/'test.sh'
            header='''#!/bin/bash
set -euo pipefail
need_cmd() { :; }
installed_xray_version() { echo 26.9.1; }
installed_hy2_version() { echo 2.12.3; }
normalize_version() { echo "$1"; }
die() { exit 99; }
curl() { return DOWNLOAD_RC; }
install() { if [ "$1" = -d ]; then mkdir -p "${@: -1}"; fi; }
unzip() { :; }
runuser() { :; }
systemctl() { echo "$*" >> SERVICE_LOG; }
'''.replace('DOWNLOAD_RC','22' if fail_download else '0').replace('SERVICE_LOG',str(base/'services.log'))
            script.write_text(header+body+'\ninitial=$PWD\ncmd_update '+target+' '+version+'\n[ "$PWD" = "$initial" ]\n[ -z "$(trap -p RETURN)" ]\n')
            subprocess.run(['bash','-n',str(script)],check=True)
            result=subprocess.run(['bash',str(script)],cwd=base,capture_output=True,text=True)
            expected=22 if fail_download else 0
            if result.returncode!=expected:failures.append((target,fail_download,result.returncode,result.stderr.strip()))
            if list((base/'work').iterdir()):failures.append((target,'temporary work not cleaned'))
            if fail_download and (base/'services.log').exists():failures.append((target,'preparation failure touched service'))
assert not failures,failures
print('MAINTCTL_UPDATE_CLEANUP=PASS|XRAY_AND_HYSTERIA2|REAL_UPDATES=NO|SERVICE_RESTARTS=NO')
