#!/usr/bin/env python3

from __future__ import annotations

import hmac
import json
import os
import re
import signal
import subprocess
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

LISTEN_HOST = "172.21.0.1"
LISTEN_PORT = 17890

TOKEN_FILE = Path("/etc/codex-runner/token")
TASK_ROOT = Path("/srv/ai-workspace/tasks")

WORKSPACES = {
    "manual": Path("/srv/ai-workspace/workspaces/manual"),
}

MAX_BODY_BYTES = 65536
MAX_PROMPT_CHARS = 12000
MIN_TIMEOUT = 30
MAX_TIMEOUT = 1800

TASK_ID_RE = re.compile(r"^[0-9a-f]{32}$")

active_lock = threading.Lock()
active_task_id: str | None = None


def read_token() -> str:
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()

    if len(token) < 48:
        raise RuntimeError("runner token is missing or too short")

    return token


BEARER_TOKEN = read_token()


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{time.time_ns()}")

    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    os.chmod(temporary, 0o640)
    os.replace(temporary, path)


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def task_status_path(task_dir: Path) -> Path:
    return task_dir / "status.json"


def write_status(
    task_dir: Path,
    *,
    state: str,
    task_id: str,
    **extra: Any,
) -> None:
    data: dict[str, Any] = {
        "task_id": task_id,
        "state": state,
        "updated_at": utc_timestamp(),
    }
    data.update(extra)
    atomic_json(task_status_path(task_dir), data)


def validate_request(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("request body must be a JSON object")

    allowed_keys = {"prompt", "workspace", "sandbox", "timeout"}

    unknown = set(data) - allowed_keys
    if unknown:
        raise ValueError(f"unsupported fields: {sorted(unknown)}")

    prompt = data.get("prompt")
    if not isinstance(prompt, str):
        raise ValueError("prompt must be a string")

    prompt = prompt.strip()
    if not prompt:
        raise ValueError("prompt must not be empty")

    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError(
            f"prompt exceeds maximum length of {MAX_PROMPT_CHARS} characters"
        )

    workspace_name = data.get("workspace", "manual")
    if workspace_name not in WORKSPACES:
        raise ValueError(
            f"workspace must be one of: {sorted(WORKSPACES)}"
        )

    sandbox = data.get("sandbox", "read-only")
    if sandbox not in {"read-only", "workspace-write"}:
        raise ValueError(
            "sandbox must be read-only or workspace-write"
        )

    timeout_value = data.get("timeout", 600)

    if isinstance(timeout_value, bool) or not isinstance(timeout_value, int):
        raise ValueError("timeout must be an integer")

    if not MIN_TIMEOUT <= timeout_value <= MAX_TIMEOUT:
        raise ValueError(
            f"timeout must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds"
        )

    return {
        "prompt": prompt,
        "workspace": workspace_name,
        "sandbox": sandbox,
        "timeout": timeout_value,
    }


def run_task(task_id: str, request: dict[str, Any]) -> None:
    global active_task_id

    task_dir = TASK_ROOT / task_id
    workspace = WORKSPACES[request["workspace"]]

    stdout_path = task_dir / "stdout.log"
    stderr_path = task_dir / "stderr.log"
    result_path = task_dir / "result.txt"

    command = [
        "/home/core/.local/bin/codex",
        "exec",
        "--cd",
        str(workspace),
        "--sandbox",
        request["sandbox"],
        "--ephemeral",
        "--color",
        "never",
        "--output-last-message",
        str(result_path),
        request["prompt"],
    ]

    write_status(
        task_dir,
        state="running",
        task_id=task_id,
        started_at=utc_timestamp(),
        workspace=request["workspace"],
        sandbox=request["sandbox"],
        timeout=request["timeout"],
    )

    environment = {
        "HOME": "/home/core",
        "USER": "core",
        "LOGNAME": "core",
        "PATH": (
            "/home/core/.local/bin:"
            "/usr/local/sbin:/usr/local/bin:"
            "/usr/sbin:/usr/bin:/sbin:/bin"
        ),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }

    started = time.monotonic()

    try:
        with (
            stdout_path.open("w", encoding="utf-8") as stdout_file,
            stderr_path.open("w", encoding="utf-8") as stderr_file,
        ):
            completed = subprocess.run(
                command,
                cwd=workspace,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
                timeout=request["timeout"],
                check=False,
            )

        duration = round(time.monotonic() - started, 3)

        if completed.returncode == 0 and result_path.is_file():
            state = "succeeded"
        else:
            state = "failed"

        write_status(
            task_dir,
            state=state,
            task_id=task_id,
            finished_at=utc_timestamp(),
            exit_code=completed.returncode,
            duration_seconds=duration,
            result_available=result_path.is_file(),
        )

    except subprocess.TimeoutExpired:
        duration = round(time.monotonic() - started, 3)

        write_status(
            task_dir,
            state="timed_out",
            task_id=task_id,
            finished_at=utc_timestamp(),
            exit_code=None,
            duration_seconds=duration,
            result_available=result_path.is_file(),
        )

    except Exception as error:
        duration = round(time.monotonic() - started, 3)

        stderr_path.write_text(
            f"{type(error).__name__}: {error}\n",
            encoding="utf-8",
        )

        write_status(
            task_dir,
            state="failed",
            task_id=task_id,
            finished_at=utc_timestamp(),
            exit_code=None,
            duration_seconds=duration,
            result_available=result_path.is_file(),
            error=type(error).__name__,
        )

    finally:
        with active_lock:
            if active_task_id == task_id:
                active_task_id = None


class RunnerHandler(BaseHTTPRequestHandler):
    server_version = "Codex-Runner/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        print(
            f"{self.client_address[0]} "
            f"[{self.log_date_time_string()}] "
            f"{format % args}",
            flush=True,
        )

    def send_json(
        self,
        status: HTTPStatus,
        data: dict[str, Any],
    ) -> None:
        payload = (
            json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def authorized(self) -> bool:
        value = self.headers.get("Authorization", "")
        prefix = "Bearer "

        if not value.startswith(prefix):
            return False

        supplied = value[len(prefix):]
        return hmac.compare_digest(supplied, BEARER_TOKEN)

    def require_auth(self) -> bool:
        if self.authorized():
            return True

        self.send_json(
            HTTPStatus.UNAUTHORIZED,
            {"error": "unauthorized"},
        )
        return False

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "service": "codex-runner",
                    "active_task": active_task_id,
                },
            )
            return

        match = re.fullmatch(
            r"/v1/tasks/([0-9a-f]{32})",
            self.path,
        )

        if match:
            if not self.require_auth():
                return

            task_id = match.group(1)
            status_path = TASK_ROOT / task_id / "status.json"

            if not status_path.is_file():
                self.send_json(
                    HTTPStatus.NOT_FOUND,
                    {"error": "task_not_found"},
                )
                return

            try:
                data = json.loads(
                    status_path.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError):
                self.send_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": "invalid_task_status"},
                )
                return

            self.send_json(HTTPStatus.OK, data)
            return

        self.send_json(
            HTTPStatus.NOT_FOUND,
            {"error": "not_found"},
        )

    def do_POST(self) -> None:
        global active_task_id

        if self.path != "/v1/tasks":
            self.send_json(
                HTTPStatus.NOT_FOUND,
                {"error": "not_found"},
            )
            return

        if not self.require_auth():
            return

        content_length_value = self.headers.get("Content-Length")

        if content_length_value is None:
            self.send_json(
                HTTPStatus.LENGTH_REQUIRED,
                {"error": "content_length_required"},
            )
            return

        try:
            content_length = int(content_length_value)
        except ValueError:
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "invalid_content_length"},
            )
            return

        if content_length < 1 or content_length > MAX_BODY_BYTES:
            self.send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"error": "request_too_large"},
            )
            return

        try:
            raw_body = self.rfile.read(content_length)
            body = json.loads(raw_body.decode("utf-8"))
            request = validate_request(body)
        except UnicodeDecodeError:
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "body_must_be_utf8"},
            )
            return
        except json.JSONDecodeError:
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "invalid_json"},
            )
            return
        except ValueError as error:
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    "error": "invalid_request",
                    "detail": str(error),
                },
            )
            return

        with active_lock:
            if active_task_id is not None:
                self.send_json(
                    HTTPStatus.CONFLICT,
                    {
                        "error": "runner_busy",
                        "active_task": active_task_id,
                    },
                )
                return

            task_id = uuid.uuid4().hex
            active_task_id = task_id

        task_dir = TASK_ROOT / task_id
        task_dir.mkdir(mode=0o750)

        request_path = task_dir / "request.json"
        request_path.write_text(
            json.dumps(request, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.chmod(request_path, 0o640)

        write_status(
            task_dir,
            state="queued",
            task_id=task_id,
            created_at=utc_timestamp(),
            workspace=request["workspace"],
            sandbox=request["sandbox"],
            timeout=request["timeout"],
        )

        worker = threading.Thread(
            target=run_task,
            args=(task_id, request),
            name=f"codex-task-{task_id}",
            daemon=True,
        )
        worker.start()

        self.send_json(
            HTTPStatus.ACCEPTED,
            {
                "task_id": task_id,
                "state": "queued",
                "status_url": f"/v1/tasks/{task_id}",
            },
        )


def shutdown_handler(
    signum: int,
    frame: Any,
) -> None:
    raise KeyboardInterrupt


def main() -> None:
    TASK_ROOT.mkdir(parents=True, exist_ok=True)
    os.chmod(TASK_ROOT, 0o750)

    signal.signal(signal.SIGTERM, shutdown_handler)

    server = ThreadingHTTPServer(
        (LISTEN_HOST, LISTEN_PORT),
        RunnerHandler,
    )

    server.daemon_threads = True

    print(
        f"Codex Runner listening on "
        f"http://{LISTEN_HOST}:{LISTEN_PORT}",
        flush=True,
    )

    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
