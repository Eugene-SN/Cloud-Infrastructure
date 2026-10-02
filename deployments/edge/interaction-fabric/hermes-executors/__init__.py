"""Native command-only Hermes extension. No tools, inference, hooks or routing."""
import base64
import json
import subprocess
from tools.environments.local import build_subprocess_env

HELPER = '/usr/local/bin/edge-ai-exec'
DEFAULT_CWD = '/home/core/projects/cloud-infrastructure'
FIELDS = {'task', 'cwd', 'timeout', 'permission_mode', 'model', 'effort',
          'output_mode', 'schema', 'request_id', 'action'}


def invoke(backend, raw_args):
    """The command name fixes backend before input parsing or process creation."""
    try:
        raw = raw_args.strip()
        if not raw or raw == 'help':
            return (f'/{backend} TASK (Codex read-only; AGY native plan)\n'
                    f'/{backend} {{"task":"...","cwd":"{DEFAULT_CWD}",'
                    '"timeout":300,"permission_mode":"full-access"}\n'
                    'Write/full access is an explicit operator choice. '
                    'Codex also supports workspace-write. No fallback.')
        p = json.loads(raw) if raw.startswith('{') else {'task': raw}
        if not isinstance(p, dict) or set(p) - FIELDS:
            raise ValueError('expected a task or JSON object containing only supported fields')
        p['backend'] = backend
        p.setdefault('cwd', DEFAULT_CWD)
        p.setdefault('permission_mode', 'read-only')
        encoded = base64.b64encode(json.dumps(p, ensure_ascii=False).encode()).decode()
        # Only a fixed executable and base64 argument cross the process boundary.
        # The existing helper owns native CLI deadline, cancellation and concurrency.
        proc = subprocess.Popen([HELPER, encoded], stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, cwd=DEFAULT_CWD,
                                env=build_subprocess_env(extra={'HOME': '/home/core'}))
        try:
            stdout, stderr = proc.communicate()
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=12)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
        result = json.loads(stdout)
        if proc.returncode:
            result = {'ok': False, 'status': 'helper_error', 'exit_code': proc.returncode,
                      'error': stderr[-16384:]}
        result['selected_by'] = 'operator'
        result['dispatch'] = 'native_plugin_command'
        result['backend'] = backend
        result['hermes_inference_turns'] = 0
        return json.dumps(result, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({'ok': False, 'status': 'invalid_request', 'backend': backend,
                           'selected_by': 'operator', 'error': str(exc)}, ensure_ascii=False)


def codex(raw_args):
    return invoke('codex', raw_args)


def antigravity(raw_args):
    return invoke('antigravity', raw_args)


def register(ctx):
    ctx.register_command('codex', handler=codex,
                         description='Explicit standalone Codex; no Hermes inference',
                         args_hint='TASK or JSON contract')
    ctx.register_command('antigravity', handler=antigravity,
                         description='Explicit standalone Antigravity; no Hermes inference',
                         args_hint='TASK or JSON contract')
