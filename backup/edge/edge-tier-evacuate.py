#!/usr/bin/python3
"""Copy Edge snapshots to PVE, verify identity there, then reclaim only Edge."""
import json
import datetime
import fcntl
import os
from pathlib import Path
import shutil
import subprocess
import sys

SOURCES = {
    'state': ('/srv/backup/backrest/repositories/edge-state-local',
              '/etc/backrest/edge-state-local-password'),
    'knowledge': ('/srv/backup/backrest/repositories/edge-knowledge-local',
                  '/etc/backrest/edge-knowledge-password'),
}
RESTIC = '/usr/local/bin/restic'


def clean_staging(cutoff, current=Path('/var/lib/backrest-staging/edge-state/current'),
                  lock=Path('/run/lock/edge-state-prepare.lock')):
    # A newer or actively prepared generation belongs to the next backup.
    with lock.open('a') as lease:
        try:
            fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        if current.is_symlink():
            raise RuntimeError('Unexpected staging symlink')
        if current.is_dir() and current.stat().st_ctime <= cutoff:
            shutil.rmtree(current)
            print('COPIED_EDGE_STAGING_REMOVED', flush=True)
            return True
    return False


def verified_ids(source, destination):
    copies = {}
    for snapshot in destination:
        copies.setdefault(snapshot.get('original', snapshot['id']), []).append(snapshot)
    fields = ('tree', 'time', 'hostname', 'paths')
    verified = []
    for snapshot in source:
        identity = snapshot.get('original', snapshot['id'])
        if not any(all(copy.get(key) == snapshot.get(key) for key in fields)
                   for copy in copies.get(identity, [])):
            raise RuntimeError('PVE copy not verified: ' + snapshot['id'])
        verified.append(snapshot['id'])
    return verified


def evacuate(kind):
    repository, password = SOURCES[kind]
    if not os.environ.get('RESTIC_REPOSITORY', '').startswith('rest:'):
        raise RuntimeError('Expected the configured remote PVE REST repository')

    def run(arguments, local=False, capture=False):
        env = dict(os.environ)
        if local:
            env.update(RESTIC_REPOSITORY=repository, RESTIC_PASSWORD_FILE=password)
        result = subprocess.run([RESTIC, '--no-cache', '--retry-lock', '10m', *arguments],
                                env=env, check=True, text=True,
                                stdout=subprocess.PIPE if capture else None)
        return json.loads(result.stdout) if capture else None

    source = run(['snapshots', '--json'], local=True, capture=True)
    if source:
        ids = [snapshot['id'] for snapshot in source]
        run(['copy', '--from-repo', repository, '--from-password-file', password, *ids])
        destination = run(['snapshots', '--json'], capture=True)
        ids = verified_ids(source, destination)
        print(f'PVE_COPY_VERIFIED={len(ids)}|SOURCE={kind}', flush=True)
        # Explicit IDs and explicit local repository: never forget on append-only PVE.
        run(['forget', *ids], local=True)
    run(['prune'], local=True)
    if kind == 'state' and not run(['snapshots', '--json'], local=True, capture=True):
        snapshots = source or [s for s in run(['snapshots', '--json'], capture=True)
                               if 'plan:edge-state' in s.get('tags', [])]
        if snapshots:
            cutoff = max(datetime.datetime.fromisoformat(s['time']).timestamp() for s in snapshots)
            clean_staging(cutoff)
    print(f'EDGE_BACKUP_DATA_RECLAIMED={kind}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in SOURCES:
        raise SystemExit('usage: edge-tier-evacuate.py state|knowledge')
    evacuate(sys.argv[1])
