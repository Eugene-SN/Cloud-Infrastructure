"""Install the verified standalone recipe and atomically select its image."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile


def main():
    record = Path(__file__).resolve().parent
    candidate = json.loads((record.parent/'deployment.json').read_text())
    current = Path('/opt/pdf-cleanup')
    previous = json.loads((current/'deployment.json').read_text())
    assert previous['image_id'] == 'sha256:93ca37d01cdfbb68550cba9d0008aefac52f3b2d6e86ca481e5163fde1ca448e'
    cases = json.loads((record/'regression-results.json').read_text())
    assert len(cases) == 7 and sum(c['pages'] for c in cases) == 947
    assert all(c['all_objects_streams_text_and_72dpi_pixels_equal'] for c in cases)
    assert 'Ran 35 tests' in (record/'unit-tests.log').read_text()
    assert (record/'unit-tests.log').read_text().rstrip().endswith('OK')
    assert json.loads((record/'runtime-before.json').read_text()) == json.loads((record/'runtime-after.json').read_text())
    image = json.loads(subprocess.check_output(['docker', 'image', 'inspect', candidate['image_tag']], text=True))[0]
    assert image['Id'] == candidate['image_id']
    for filename, key in [('core.py', 'installed_core_sha256'), ('native.py', 'installed_native_sha256'), ('lexical.py', 'installed_lexical_sha256')]:
        assert hashlib.sha256((current/'source/src/pdf_cleanup'/filename).read_bytes()).hexdigest() == candidate[key]
    assert hashlib.sha256((current/'job-command.py').read_bytes()).hexdigest() == candidate['job_adapter_sha256']
    connection = sqlite3.connect('file:/srv/n8n/database.sqlite?mode=ro')
    assert not connection.execute("SELECT id FROM execution_entity WHERE workflowId IN ('ENo9jFkwcE4PFOyL','QouVaVNhAqSiYq5D') AND status IN ('running','waiting','new')").fetchall()
    assert not any((path/'job.json').is_file() for path in Path('/tmp').glob('pdf-cleanup-*'))
    changes = []
    # Keep the old selection until the complete build recipe is installed.
    for name in ('Dockerfile', '.dockerignore', 'runtime-requirements.txt', 'deployment.json'):
        payload = (record.parent/name).read_bytes()
        fd, temporary = tempfile.mkstemp(prefix='.standalone-', dir=current)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(payload)
                os.fchmod(stream.fileno(), 0o644)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, current/name)
        finally:
            Path(temporary).unlink(missing_ok=True)
        assert (current/name).read_bytes() == payload
        changes.append(name)
    print(json.dumps(dict(installed=changes, image_id=candidate['image_id']), indent=2))


if __name__ == '__main__':
    main()
