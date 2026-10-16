"""Read back runtime identity, immutable production state and precise cleanup."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    record = Path(__file__).resolve().parent
    baseline = json.loads((record/'production-before.json').read_text())
    state = json.loads(subprocess.check_output(['sudo', '-n', 'python3', str(record/'capture-state.py')], text=True))
    assert state == baseline, 'Production files or documentation workflow definitions changed'
    runtime = Path('/opt/pdf-cleanup')
    for name in ('Dockerfile', '.dockerignore', 'runtime-requirements.txt', 'README.md', 'deployment.json', 'run', 'job-command.py'):
        assert (runtime/name).read_bytes() == (record.parent/name).read_bytes(), name
    manifest = json.loads((runtime/'deployment.json').read_text())
    assert not {'runtime_parent_image', 'runtime_parent_tag'} & manifest.keys()
    images = json.loads(subprocess.check_output(['sudo', '-n', 'docker', 'image', 'inspect', manifest['image_tag'], manifest['base_image']], text=True))
    image, base = images
    assert image['Id'] == manifest['image_id']
    prefix = len(base['RootFS']['Layers'])
    assert image['RootFS']['Layers'][:prefix] == base['RootFS']['Layers']
    retired = json.loads((record/'images-before.json').read_text())[:2]
    for old in retired:
        assert not set(old['RootFS']['Layers'][prefix:]) & set(image['RootFS']['Layers'])
        probe = subprocess.run(['sudo', '-n', 'docker', 'image', 'inspect', old['Id']], capture_output=True, text=True)
        assert probe.returncode != 0 and 'No such image' in probe.stderr, probe.stderr
    listed = [json.loads(line) for line in subprocess.check_output(['sudo', '-n', 'docker', 'image', 'ls', 'edge/pdf-cleanup', '--format', '{{json .}}'], text=True).splitlines()]
    assert len(listed) == 1 and listed[0]['Tag'] == manifest['image_tag'].split(':')[-1]
    containers = [json.loads(line) for line in subprocess.check_output(['sudo', '-n', 'docker', 'ps', '-a', '--format', '{{json .}}'], text=True).splitlines()]
    assert not any('pdf-cleanup' in c['Names'] or 'pdf-cleanup' in c['Image'] for c in containers)
    scratch = Path(json.loads((record/'workspace.json').read_text())['scratch'])
    assert not scratch.exists()
    assert not list(Path('/tmp').glob('pdf-cleanup-*'))
    result = dict(status='PASS', image_id=image['Id'], image_tag=manifest['image_tag'],
                  unchanged_production_files=len(state['files']), unchanged_workflows=len(state['workflows']),
                  retired_images_absent=True, independent_layers=True,
                  runtime_files_match=True, temporary_jobs_and_containers_absent=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
