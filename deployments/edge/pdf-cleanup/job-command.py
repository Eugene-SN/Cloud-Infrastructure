"""Small host-side snapshot/CLI job adapter; WebDAV stays in n8n."""
import base64
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile

LAUNCHER = Path('/opt/pdf-cleanup/run')


def job_path(request):
    path = Path(request["job_dir"])
    if not re.fullmatch(r"/tmp/pdf-cleanup-[A-Za-z0-9_\-]{8,}", str(path)):
        raise ValueError("Invalid job directory")
    if path.is_symlink() or path.resolve() != path or path.stat().st_uid != os.getuid():
        raise ValueError("Job ownership/path mismatch")
    marker = json.loads((path / "job.json").read_text())
    if marker["execution_id"] != request["execution_id"]:
        raise ValueError("Job execution mismatch")
    return path, marker


def perform(request):
    action = request["action"]
    if action == "create":
        execution_id = str(request["execution_id"])
        if not re.fullmatch(r"[0-9]+", execution_id):
            raise ValueError("Invalid execution id")
        os.umask(0o077)
        path = Path(tempfile.mkdtemp(prefix="pdf-cleanup-", dir="/tmp"))
        try:
            for name in ("input", "output", "tmp"):
                (path / name).mkdir(mode=0o700)
            (path / "job.json").write_text(json.dumps({"execution_id": execution_id}))
        except BaseException:
            shutil.rmtree(path)
            raise
        return {"ok": True, "job_dir": str(path), "execution_id": execution_id}
    path, _ = job_path(request)
    if action == "release":
        shutil.rmtree(path)
        return {"ok": True, "job_removed": not path.exists()}
    if action != "process":
        raise ValueError("Unknown action")
    if request.get("upload_ok") is not True:
        raise ValueError("Snapshot upload failed")
    source = path / "input" / "source.pdf"
    launcher = LAUNCHER
    if not launcher.is_file() or not os.access(launcher, os.X_OK):
        return {"ok": False, "status": "cli_unavailable", "cli_rc": 127,
                "error": "PDF cleanup CLI is not installed: /opt/pdf-cleanup/run"}
    output = path / "output" / "cleaned.pdf"
    env = dict(os.environ, TMPDIR=str(path / "tmp"))
    process = subprocess.Popen([str(launcher), str(source), str(output)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, env=env, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        return {"ok": False, "status": "timeout", "cli_rc": process.returncode,
                "error": "Cleanup exceeded 900 seconds"}
    try:
        summary = json.loads(stdout)
    except (ValueError, TypeError):
        summary = None
    result = {"ok": False, "cli_rc": process.returncode, "summary": summary,
              "stderr": stderr[-16384:]}
    if process.returncode != 0:
        result["error"] = (summary.get("error") if isinstance(summary, dict) else None) or "PDF cleanup CLI failed"
        return result
    if output.is_symlink() or not output.is_file():
        result["error"] = "CLI did not publish a regular PDF"
        return result
    result.update(ok=True, status="cleaned", cleaned=True)
    return result


def main():
    try:
        request = json.loads(base64.b64decode(sys.argv[1], validate=True))
        result = perform(request)
    except Exception as error:
        result = {"ok": False, "error": f"{type(error).__name__}: {error}"}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
