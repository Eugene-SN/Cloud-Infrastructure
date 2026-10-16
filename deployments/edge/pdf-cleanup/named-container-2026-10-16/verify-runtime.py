"""Read-only final verification of the deployed named-container contract."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RUNTIME = Path('/opt/pdf-cleanup')


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((REPO/'deployment.json').read_text())
created = json.loads((HERE/'container-created.json').read_text())[0]
current = json.loads(command('sudo', '-n', 'docker', 'inspect', 'pdf-cleanup'))[0]
assert current['Id'] == created['Id']
assert current['Image'] == manifest['image_id'] == created['Image']
assert current['State']['Status'] == 'exited'
assert current['State']['ExitCode'] == 0
assert not current['State']['OOMKilled']
assert current['Config']['User'] == '1000:1000'
assert current['Config']['Entrypoint'] == ['python', '/app/job-command.py', '--container']
host = current['HostConfig']
assert not host['AutoRemove'] and host['ReadonlyRootfs']
assert host['RestartPolicy']['Name'] == 'no' and host['NetworkMode'] == 'none'
assert host['Tmpfs'] == {'/tmp': 'mode=1777'}
mounts = {m['Destination']: (m['Source'], m['RW']) for m in current['Mounts']}
assert mounts == {
    '/originals': (manifest['originals_dir'], False),
    '/work': ('/opt/pdf-cleanup/work', True),
    '/app/job-command.py': ('/opt/pdf-cleanup/job-command.py', False),
}
assert list((RUNTIME/'work').iterdir()) == []
assert (RUNTIME/'work').stat().st_uid == 1000
assert (RUNTIME/'work').stat().st_mode & 0o777 == 0o700
assert not (RUNTIME/'run').exists() and not (REPO/'run').exists()
names = command('sudo', '-n', 'docker', 'ps', '-a', '--format', '{{.Names}}').splitlines()
assert [n for n in names if n.startswith('pdf-cleanup')] == ['pdf-cleanup']
assert not command('sudo', '-n', 'git', '-C', str(RUNTIME/'source'), 'status', '--porcelain')
assert command('sudo', '-n', 'git', '-C', str(RUNTIME/'source'), 'rev-parse', 'HEAD') == manifest['source_commit']
for name in ('README.md', 'compose.yaml', 'job-command.py', 'deployment.json',
             'Dockerfile', 'runtime-requirements.txt', '.dockerignore'):
    assert (RUNTIME/name).read_bytes() == (REPO/name).read_bytes(), name
assert sha(RUNTIME/'job-command.py') == manifest['job_adapter_sha256']
for name in ('core', 'native', 'lexical'):
    assert sha(RUNTIME/f'source/src/pdf_cleanup/{name}.py') == manifest[f'installed_{name}_sha256']
command('sudo', '-n', 'docker', 'compose', '-f', str(RUNTIME/'compose.yaml'), 'config', '--quiet')
health = json.loads(command('sudo', '-n', 'docker', 'inspect', '--format', '{{json .State}}', 'n8n'))
assert health['Running'] and health['Health']['Status'] == 'healthy'
nextcloud = json.loads(command('sudo', '-n', 'docker', 'exec', '--user', 'www-data',
                             'nextcloud', 'php', 'occ', 'status', '--output=json'))
assert nextcloud['installed'] and not nextcloud['maintenance'] and not nextcloud['needsDbUpgrade']
print(json.dumps({
    'container_id': current['Id'], 'image_id': current['Image'],
    'state': current['State']['Status'], 'exit_code': current['State']['ExitCode'],
    'same_container_as_created': True, 'workspace_empty': True,
    'old_launcher_absent': True, 'single_pdf_container': True,
    'runtime_files_match_repository': True, 'source_and_dependencies_preserved': True,
    'compose_native_validation': 'PASS', 'n8n_healthy': True,
    'nextcloud_installed_no_maintenance_no_upgrade': True,
}, indent=2))
