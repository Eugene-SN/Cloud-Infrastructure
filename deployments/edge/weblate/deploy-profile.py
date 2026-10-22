#!/usr/bin/env python3
"""Install selected Weblate profile files with the deployment's UID/GID 1000."""
import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

UID = GID = 1000
LOCATIONS = (
    (Path('/opt/weblate/provider'), Path('/opt/weblate')),
    (Path('/srv/weblate/data/python/td_translate'), Path('/srv/weblate/data')),
    (Path('/srv/weblate/data/hermes-skills'), Path('/srv/weblate/data')),
)


def location(destination):
    destination = Path(os.path.abspath(destination))
    for root, anchor in LOCATIONS:
        if destination.is_relative_to(root):
            if not anchor.is_dir() or anchor.resolve() != anchor:
                raise ValueError(f'missing or indirect deployment anchor: {anchor}')
            current = anchor
            for name in destination.relative_to(anchor).parts:
                current = current / name
                if current.is_symlink():
                    raise ValueError(f'symlink in profile destination: {current}')
            return destination, anchor
    raise ValueError(f'not a managed Weblate profile path: {destination}')


def deploy(source, destination):
    if os.geteuid() != 0:
        raise PermissionError('profile installation requires root to assign UID/GID 1000')
    source = Path(source)
    destination, anchor = location(destination)
    if source.is_symlink():
        raise ValueError(f'symlink in profile source: {source}')
    if not source.exists():
        raise ValueError(f'missing profile source: {source}')
    entries = [source, *sorted(source.rglob('*'))] if source.is_dir() else [source]
    directories = set()
    files = []
    # Read/validate the complete selected package before modifying destinations.
    for path in entries:
        mode = path.lstat().st_mode
        target = destination / path.relative_to(source) if source.is_dir() else destination
        target, _ = location(target)
        if stat.S_ISDIR(mode):
            if target.exists() and not target.is_dir():
                raise ValueError(f'profile directory conflicts with a file: {target}')
            directories.add(target)
            parent = target
        elif stat.S_ISREG(mode):
            if target.exists() and not target.is_file():
                raise ValueError(f'profile file conflicts with a directory: {target}')
            files.append((target, path.read_bytes()))
            parent = target.parent
        else:
            raise ValueError(f'not a regular profile file or directory: {path}')
        while parent != anchor:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f'profile parent is not a directory: {parent}')
            directories.add(parent)
            parent = parent.parent

    for directory in sorted(directories, key=lambda p: (len(p.parts), str(p))):
        directory.mkdir(mode=0o755, exist_ok=True)
        # Assign each intermediate directory, not just the final leaf.
        os.chown(directory, UID, GID)

    replaced = 0
    for target, data in files:
        mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o644
        if target.exists() and target.read_bytes() == data:
            os.chown(target, UID, GID)
            continue
        fd, temporary = tempfile.mkstemp(prefix='.profile-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                # The replacement must not inherit an old root-owned target.
                os.fchown(stream.fileno(), UID, GID)
                os.fchmod(stream.fileno(), mode)
                stream.write(data)
            os.replace(temporary, target)
            replaced += 1
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return {'files': len(files), 'replaced': replaced, 'uid': UID, 'gid': GID}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='selected file or directory; no files are deleted')
    parser.add_argument('destination', type=Path, help='exact destination in provider, td_translate or hermes-skills')
    args = parser.parse_args(argv)
    result = deploy(args.source, args.destination)
    subprocess.run([
        'docker', 'exec', 'weblate', '/app/venv/bin/weblate',
        'check', '--deploy', '--fail-level', 'ERROR',
    ], check=True)
    print('WEBLATE_PROFILE_DEPLOY=PASS|' + json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f'WEBLATE_PROFILE_DEPLOY=FAIL|REASON={error}', file=sys.stderr)
        raise SystemExit(1)
