"""Exercise the production adapter/launcher on a temporary snapshot; no DAV writes."""
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def call(request):
    encoded = base64.b64encode(json.dumps(request).encode()).decode()
    process = subprocess.run(['/usr/bin/python3', '/opt/pdf-cleanup/job-command.py', encoded],
                             capture_output=True, text=True, timeout=960)
    assert process.returncode == 0, process.stderr
    return json.loads(process.stdout)


def main():
    manifest = json.loads(Path('/opt/pdf-cleanup/deployment.json').read_text())
    assert manifest['image_tag'] == 'edge/pdf-cleanup:9c9bbb375751-standalone'
    source = Path(sys.argv[1])
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    created = call(dict(action='create', execution_id='202610160001'))
    assert created['ok'], created
    request = {key: created[key] for key in ('job_dir', 'execution_id')}
    job = Path(request['job_dir'])
    try:
        shutil.copyfile(source, job/'input/source.pdf')
        result = call(dict(request, action='process', upload_ok=True))
        assert result['ok'], result
        assert result['summary']['validation'] == 'passed'
        assert result['summary']['source_commit'] == manifest['source_commit']
        assert result['summary']['input_sha256'] == digest
        assert result['summary']['output_sha256'] == hashlib.sha256((job/'output/cleaned.pdf').read_bytes()).hexdigest()
        assert not result['stderr'], result
    finally:
        release = call(dict(request, action='release'))
        assert release['ok'] and release['job_removed'] and not job.exists(), release
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
    print(json.dumps(dict(image_id=manifest['image_id'], result=result,
                          release=release, no_publication=True), indent=2))


if __name__ == '__main__':
    main()
