"""Start the persistent PDF Cleanup container; native WebDAV stays in n8n."""
import base64
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys

WORK = Path('/opt/pdf-cleanup/work')
CONTAINER = 'pdf-cleanup'
TIMEOUT = 900
DOCKER = ['/usr/bin/sudo', '-n', '/usr/bin/docker']


def docker(*args, **kwargs):
    return subprocess.run([*DOCKER, *args], capture_output=True, text=True, **kwargs)


def state():
    response = docker('inspect', '--format', '{{json .State}}', CONTAINER, timeout=15)
    if response.returncode:
        raise RuntimeError(response.stderr.strip())
    return json.loads(response.stdout)


def clear_workspace():
    for path in WORK.iterdir():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()


def perform(request):
    execution = str(request['execution_id'])
    if not re.fullmatch(r'[0-9]+', execution):
        raise ValueError('Invalid execution id')
    action = request['action']
    if action not in ('process', 'release'):
        raise ValueError('Use process or release')
    if action == 'process':
        path = request['path']
        if (not isinstance(path, str) or not path.lower().endswith('.pdf')
                or any(part in ('', '.', '..') for part in path.split('/'))
                or re.search(r'[\\\x00-\x1f]', path) or Path(path).name == '.pdf'):
            raise ValueError('Input must be a relative PDF path inside originals')
    if WORK.is_symlink() or not WORK.is_dir() or WORK.stat().st_uid != os.getuid():
        raise ValueError('Workspace ownership/path mismatch')
    marker = WORK/'job.json'
    if action == 'release':
        if marker.exists() and json.loads(marker.read_text())['execution_id'] != execution:
            raise ValueError('Job execution mismatch')
        if state()['Running']:
            raise ValueError('Container is still processing')
        clear_workspace()
        return dict(ok=True, job_removed=True)
    if state()['Running']:
        raise ValueError('PDF Cleanup is already processing')
    with marker.open('x') as stream:
        json.dump(dict(execution_id=execution, path=path), stream)
    try:
        process = subprocess.Popen([*DOCKER, 'start', '--attach', CONTAINER],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            stdout, stderr = process.communicate(timeout=TIMEOUT)
        except BaseException:
            # Stop the container before waiting for its root-owned attached client.
            docker('stop', '--timeout', '5', CONTAINER, timeout=15)
            process.communicate(timeout=15)
            raise
        current = state()
        if current['Running']:
            docker('stop', '--timeout', '5', CONTAINER, timeout=15)
            raise RuntimeError('Container did not finish')
        report = json.loads(stdout)
        response = dict(ok=False, cli_rc=current['ExitCode'], summary=report,
                        stderr=stderr[-16384:])
        output = WORK/'cleaned.pdf'
        if process.returncode or current['ExitCode'] or report.get('status') != 'cleaned':
            response['error'] = report.get('error') or 'PDF cleanup CLI failed'
        elif output.is_symlink() or not output.is_file():
            response['error'] = 'CLI did not publish a regular PDF'
        else:
            response.update(ok=True, status='cleaned', cleaned=True)
        if not response['ok']:
            clear_workspace()
        return response
    except BaseException:
        clear_workspace()
        raise


def container_main():
    from pdf_cleanup.cli import main as cli
    try:
        request = json.loads(Path('/work/job.json').read_text())
        originals = Path('/originals')
        source = (originals/request['path']).resolve()
        if not source.is_relative_to(originals) or not source.is_file():
            raise ValueError('Input must be an existing PDF inside originals')
        sys.argv = ['pdf-cleanup', str(source), '/work/cleaned.pdf']
    except Exception as error:
        print(json.dumps(dict(status='error', error=str(error), exit_code=2)))
        return 2
    return cli()


def main():
    def interrupted(signum, _frame):
        raise InterruptedError(f'Job interrupted by signal {signum}')
    for signum in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(signum, interrupted)
    try:
        request = json.loads(base64.b64decode(sys.argv[1], validate=True))
        result = perform(request)
    except Exception as error:
        result = dict(ok=False, error=f'{type(error).__name__}: {error}')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1:] == ['--container']:
        sys.exit(container_main())
    main()
