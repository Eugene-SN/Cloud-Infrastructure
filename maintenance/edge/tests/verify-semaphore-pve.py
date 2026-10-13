#!/usr/bin/env python3
"""Validate PVE patch delivery in a disposable fixture, without pct/systemd calls."""
import ast
import hashlib
import os
from pathlib import Path
import runpy
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
outer = runpy.run_path(root / 'semaphore-pve-fix.py')
ast.parse(outer['CHILD'])
child = {'__name__': 'fixture'}
exec(compile(outer['CHILD'], 'PVE child', 'exec'), child)
assert child['CORE'] == (root / 'scripts/controller-update-state').read_text()
with tempfile.TemporaryDirectory(prefix='semaphore-pve-test-') as temporary:
    base = Path(temporary)
    repo = base / 'repo'
    web = base / 'web'
    for p in (repo/'scripts', repo/'playbooks', repo/'dashboard', web):
        p.mkdir(parents=True)
    manual = repo / 'scripts/manual-update'
    original = '''#!/bin/bash
case "$TARGET" in
    SEMAPHORE_CONTROLLER)
        echo "SEMAPHORE_CONTROLLER_UPDATE_PHASE=PRECHECK"
        NEW="$OLD"
        ;;
esac
'''
    manual.write_text(original)
    manual.chmod(0o755)
    helper = repo / 'scripts/controller-update-state'
    helper.write_text('#!/usr/bin/env python3\n')
    helper.chmod(0o755)
    (repo/'playbooks/manual-update.yml').write_text('''---
- hosts: localhost
  tasks:
    - name: Подтвердить отсутствие recovery действий
      ansible.builtin.debug:
        msg:
          - "ROLLBACK_EXECUTED=NO"
''')
    page = '<script>\n    async function waitControllerUpdate(taskId) {}\n    async function pollTask() {}\n</script>\n'
    for p in (web/'index.html', repo/'dashboard/index.html'):
        p.write_text(page)
    digest = hashlib.sha256(manual.read_bytes()).hexdigest()
    try:
        child['prepare'](repo, web)
    except RuntimeError as e:
        assert 'differs from audited' in str(e)
    else:
        raise AssertionError('source guard accepted unrecognized manual-update')
    assert manual.read_text() == original
    changes = child['prepare'](repo, web, expected=digest)
    # Native Ansible parser verifies the exact modified playbook, without execution.
    checked_playbook = base/'manual-update.yml'
    checked_playbook.write_text(changes[repo/'playbooks/manual-update.yml'])
    subprocess.run(['ansible-playbook', '--syntax-check', '-i', 'localhost,', str(checked_playbook)],
                   env={**os.environ, 'ANSIBLE_LOCAL_TEMP':str(base/'ansible-tmp')}, check=True)
    js = base/'wait.js'
    js.write_text(child['WAIT'] + '''
const assert = require('assert');
let attempts = 0;
global.setTimeout = cb => cb();
global.showToast = () => {};
global.fetch = async url => ({ok:true, json:async () => {
  if (url.endsWith('/output')) return [{output:'SEMAPHORE_UPDATE_ID=new-operation'}];
  return attempts++ === 0 ? {status:'success',operation:'old-operation'} : {status:'success',operation:'new-operation'};
}});
waitControllerUpdate(1).then(() => {assert.equal(attempts,2);}).catch(e => {console.error(e);process.exit(1);});
''')
    subprocess.run(['node', str(js)], check=True)
    recovery = base/'recovery'
    child['install'](changes, recovery, backup_files=[])
    for path, data in changes.items():
        assert path.read_text() == data
    assert (recovery/'0').read_text() == original
    assert (recovery/'manifest.json').stat().st_mode & 0o777 == 0o600
    assert manual.stat().st_mode & 0o777 == 0o755
    assert helper.stat().st_mode & 0o777 == 0o755
print('PVE_HANDLER_INSTALLER=PASS|REAL_PCT_CALLS=NO|SERVICE_RESTARTS=NO')
