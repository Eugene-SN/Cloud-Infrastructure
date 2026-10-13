#!/usr/bin/env python3
"""Use isolated SQLite/files and mock service boundaries; never run an update."""
import pathlib
import os
import runpy
import sqlite3
import subprocess
import tempfile
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

root = pathlib.Path(__file__).resolve().parents[1]
driver = runpy.run_path(root / "scripts/manual-update")
calls = []
namespace = driver["execute"].__globals__
with patch.dict(namespace,
                run=lambda argv, **kw: calls.append(argv),
                pathlib=SimpleNamespace(Path=MagicMock()),
                shutil=SimpleNamespace(move=MagicMock()),
                subprocess=SimpleNamespace(run=lambda *a, **kw: SimpleNamespace(stdout="2.19.12"))):
    driver["execute"]({"id": "SEMAPHORE", "driver": "github_binary",
                       "service": "semaphore", "repository": "semaphoreui/semaphore"}, {})
assert len(calls) == 1
assert calls[0][:4] == ["systemd-run", "--unit=edge-semaphore-update", "--collect", "--service-type=exec"]
assert "--scope" not in calls[0] and "--pipe" not in calls[0]
assert calls[0][-3:-1] == ["/opt/edge-maintenance/scripts/update-github-binary", "SEMAPHORE"]
assert len(calls[0][-1]) == 32

module = runpy.run_path(root / "scripts/controller-update-state")
module = module["install_semaphore"].__globals__

with tempfile.TemporaryDirectory(prefix="semaphore-update-test-") as temporary:
    base = pathlib.Path(temporary)
    # Execute the real Bash preparation path with a failing local curl substitute.
    # The helper's state path is redirected into this fixture; no network/services.
    state = base / 'state.json'
    helper = base / 'controller-update-state'
    helper.write_text((root/'scripts/controller-update-state').read_text().replace(
        "STATE = Path('/var/www/maintenance-status/controller-update.json')", f"STATE = Path({str(state)!r})"))
    helper.chmod(0o755)
    fake_bin = base/'bin'
    fake_bin.mkdir()
    curl = fake_bin/'curl'
    curl.write_text('#!/bin/sh\nexit 22\n')
    curl.chmod(0o755)
    bash_driver = base/'driver'
    bash_driver.write_text((root/'scripts/update-github-binary').read_text().replace(
        'state=/opt/edge-maintenance/scripts/controller-update-state', f'state={helper}'))
    result = subprocess.run(['bash', str(bash_driver), 'SEMAPHORE', 'download-failure'],
                            env={**os.environ, 'PATH':f'{fake_bin}:' + os.environ['PATH']}, capture_output=True)
    assert result.returncode == 22
    import json
    assert json.loads(state.read_text())['status'] == 'error'
    assert json.loads(state.read_text())['operation'] == 'download-failure'
    binary = base / "semaphore"
    candidate = base / "candidate"
    database = base / "tasks.sqlite"
    backups = base / "backups"
    backups.mkdir()
    binary.write_text("old executable")
    candidate.write_text("new executable")
    with sqlite3.connect(database) as c:
        c.execute("CREATE TABLE task(id INTEGER, status TEXT, runner_id INTEGER)")
        c.execute("INSERT INTO task VALUES(1, 'running', NULL)")
    try:
        module["wait_idle"](database, timeout=0)
    except RuntimeError:
        pass
    else:
        raise AssertionError("accepted an active launching task")
    for status in ("waiting", "starting", "waiting_confirmation", "confirmed", "rejected", "stopping"):
        with sqlite3.connect(database) as c:
            c.execute("UPDATE task SET status=?", (status,))
        try:
            module["wait_idle"](database, timeout=0)
        except RuntimeError:
            pass
        else:
            raise AssertionError("accepted unfinished task: " + status)
    with sqlite3.connect(database) as c:
        c.execute("UPDATE task SET status='success'")
    module["wait_idle"](database, timeout=0)
    module.update(BINARY=binary)
    backup = backups / "semaphore.old"
    backup_db = backups / "semaphore.sqlite"

    # A migration failure restores both old binary and old SQLite data.
    calls.clear()
    def fail_migration(argv):
        calls.append(argv)
        if argv[0] == "runuser":
            with sqlite3.connect(database) as c:
                c.execute("UPDATE task SET status='error'")
            raise RuntimeError("migration failed")
    with patch.dict(module, run=fail_migration, healthy=lambda version: None, binary_version=lambda path: "9.9.9"):
        try:
            module["install_semaphore"](candidate, "9.9.9", database, backup, backup_db)
        except RuntimeError:
            pass
        else:
            raise AssertionError("migration failure became success")
    assert binary.read_text() == "old executable"
    with sqlite3.connect(database) as c:
        assert c.execute("SELECT status FROM task").fetchone()[0] == "success"
    assert calls[-2:] == [["systemctl", "stop", "semaphore"], ["systemctl", "start", "semaphore"]]

    # Failed stop must not replace anything or issue an unconditional restart.
    calls.clear()
    def fail_stop(argv):
        calls.append(argv)
        raise RuntimeError("stop failed")
    with patch.dict(module, run=fail_stop, healthy=lambda version: None, binary_version=lambda path: "9.9.9"):
        try:
            module["install_semaphore"](candidate, "9.9.9", database, backup, backup_db)
        except RuntimeError:
            pass
        else:
            raise AssertionError("failed stop became success")
    assert calls == [["systemctl", "stop", "semaphore"]]
    assert binary.read_text() == "old executable"

    calls.clear()
    with patch.dict(module, run=lambda argv: calls.append(argv), healthy=lambda version: None, binary_version=lambda path: "9.9.9"):
        module["install_semaphore"](candidate, "9.9.9", database, backup, backup_db)
    assert binary.read_text() == "new executable"
    assert calls[1][:4] == ["runuser", "-u", "semaphore", "--"]
    assert calls[1][-3:] == ["migrate", "--config", "/etc/semaphore/config.json"]
    assert calls[-1] == ["systemctl", "start", "semaphore"]

    assert backup.stat().st_mode & 0o777 == 0o600
    assert backup_db.stat().st_mode & 0o777 == 0o600
    # An unsuccessful rollback must remain a failure.
    calls.clear()
    with patch.dict(module, run=lambda argv: calls.append(argv),
                    healthy=lambda version: (_ for _ in ()).throw(RuntimeError("unhealthy")),
                    binary_version=lambda path: "9.9.9"):
        try:
            module["install_semaphore"](candidate, "9.9.9", database, backup, backup_db)
        except RuntimeError as error:
            assert "rollback failed" in str(error)
        else:
            raise AssertionError("failed rollback became success")
print("SEMAPHORE_UPDATE_CONTRACT=PASS|REAL_UPDATE_EXECUTED=NO|SERVICE_RESTARTS=NO")
