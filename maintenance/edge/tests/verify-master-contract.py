#!/usr/bin/env python3
import copy
import datetime as dt
import json
import pathlib
import runpy
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((root / "config/update-units.json").read_text())
master = runpy.run_path(root / "scripts/master-batch-update")
post = runpy.run_path(root / "scripts/master-post-scan-validate")
now = dt.datetime.now(dt.timezone.utc)


def fixture(status="CURRENT"):
    rows = [
        {"component": unit["id"], "status": status, "actionable": True}
        for unit in manifest["units"]
    ]
    return {
        "schema": 3,
        "target_model": "update_units_v3",
        "generated_at": now.isoformat(),
        "rows": rows,
        "summary": {
            "TOTAL": 16,
            "CURRENT": 16 if status == "CURRENT" else 0,
            "UPDATE_AVAILABLE": 16 if status == "UPDATE_AVAILABLE" else 0,
            "CHECK_FAILED": 0,
            "REBOOT_REQUIRED": 0,
        },
    }


clean = fixture()
order, units, rows, stamp = master["validate_plan"](manifest, clean, now)
assert order == manifest["master_order"]
assert set(units) == set(rows)
assert stamp == clean["generated_at"]
assert post["validate"](manifest, clean, now)[0] is True

help_result = subprocess.run(
    [str(root / "scripts/master-batch-update"), "--help"],
    capture_output=True,
    text=True,
    check=False,
)
assert help_result.returncode == 0
assert "--plan-only" in help_result.stdout

one_update = fixture()
target = "AUTHELIA"
next(row for row in one_update["rows"] if row["component"] == target)["status"] = "UPDATE_AVAILABLE"
one_update["summary"]["CURRENT"] = 15
one_update["summary"]["UPDATE_AVAILABLE"] = 1
assert master["validate_plan"](manifest, one_update, now)[2][target]["status"] == "UPDATE_AVAILABLE"
assert post["validate"](manifest, one_update, now)[0] is False

for mutation in ("UNRESOLVED", "MISSING", "SEMAPHORE", "STALE", "REBOOT"):
    broken = copy.deepcopy(clean)
    if mutation == "UNRESOLVED":
        next(row for row in broken["rows"] if row["component"] == "RESTIC")["status"] = "STABLE_UNRESOLVED"
        broken["summary"]["CURRENT"] = 15
    elif mutation == "MISSING":
        broken["rows"].pop()
    elif mutation == "SEMAPHORE":
        next(row for row in broken["rows"] if row["component"] == "SEMAPHORE")["status"] = "UPDATE_AVAILABLE"
        broken["summary"]["CURRENT"] = 15
        broken["summary"]["UPDATE_AVAILABLE"] = 1
    elif mutation == "STALE":
        broken["generated_at"] = (now - dt.timedelta(seconds=301)).isoformat()
    else:
        broken["summary"]["REBOOT_REQUIRED"] = 1
    try:
        master["validate_plan"](manifest, broken, now)
    except RuntimeError:
        pass
    else:
        raise AssertionError(f"Master precheck accepted invalid fixture: {mutation}")

reboot_pending = copy.deepcopy(clean)
reboot_pending["summary"]["REBOOT_REQUIRED"] = 1
assert post["validate"](manifest, reboot_pending, now) == (False, "REBOOT_REQUIRED:1")

print("EDGE_MASTER_CONTRACT=PASS")
