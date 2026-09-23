#!/usr/bin/env python3
import copy
import datetime as dt
import json
import pathlib
import runpy
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((root / "config/update-units.json").read_text())
enablement = json.loads((root / "config/manual-driver-enablement.example.json").read_text())
sudoers = (root / "config/semaphore-sudoers").read_text()
master = runpy.run_path(root / "scripts/master-batch-update")
post = runpy.run_path(root / "scripts/master-post-scan-validate")
now = dt.datetime.now(dt.timezone.utc)
manual = [u["id"] for u in manifest["units"]]

assert manifest["schema"] == 2
assert enablement["schema"] == 2
assert enablement["master"] is True
assert len(manual) == 17
assert set(manual) == set(manifest["master_order"])
assert set(enablement["enabled"]) == set(manual)
assert manifest["master_order"][-1] == "APT_EDGE"
assert next(u for u in manifest["units"] if u["id"] == "SEMAPHORE")["master_policy"] == "individual_only"
assert "/opt/edge-maintenance/scripts/master-post-scan-validate" in sudoers
assert "/opt/edge-maintenance/scripts/master-health-validate" in sudoers


def fixture(status="CURRENT"):
    rows = [
        {
            "component": target,
            "status": status,
            "actionable": True,
            "update_owner": "maintenance_manual",
        }
        for target in manual
    ]
    return {
        "schema": 3,
        "target_model": "update_units_v5",
        "generated_at": now.isoformat(),
        "rows": rows,
        "summary": {
            "TOTAL": 17,
            "ACTIONABLE_TARGETS": 17,
            "CURRENT": 17 if status == "CURRENT" else 0,
            "UPDATE_AVAILABLE": 0 if status == "CURRENT" else 17,
            "CHECK_FAILED": 0,
            "REBOOT_REQUIRED": 0,
        },
    }


clean = fixture()
order, units, rows, stamp = master["validate_plan"](manifest, clean, now)
assert order == manifest["master_order"]
assert set(units) == set(manual)
assert set(rows) == set(manual)
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
next(r for r in one_update["rows"] if r["component"] == target)["status"] = "UPDATE_AVAILABLE"
one_update["summary"]["CURRENT"] = 16
one_update["summary"]["UPDATE_AVAILABLE"] = 1
assert master["validate_plan"](manifest, one_update, now)[2][target]["status"] == "UPDATE_AVAILABLE"
assert post["validate"](manifest, one_update, now)[0] is False

for mutation in ("UNRESOLVED", "MISSING", "SEMAPHORE", "STALE", "REBOOT", "NONACTIONABLE"):
    broken = copy.deepcopy(clean)
    if mutation == "UNRESOLVED":
        next(r for r in broken["rows"] if r["component"] == "RESTIC")["status"] = "STABLE_UNRESOLVED"
    elif mutation == "MISSING":
        broken["rows"] = [r for r in broken["rows"] if r["component"] != "RESTIC"]
    elif mutation == "SEMAPHORE":
        next(r for r in broken["rows"] if r["component"] == "SEMAPHORE")["status"] = "UPDATE_AVAILABLE"
    elif mutation == "STALE":
        broken["generated_at"] = (now - dt.timedelta(seconds=301)).isoformat()
    elif mutation == "REBOOT":
        broken["summary"]["REBOOT_REQUIRED"] = 1
    else:
        next(r for r in broken["rows"] if r["component"] == "N8N")["actionable"] = False

    try:
        master["validate_plan"](manifest, broken, now)
    except RuntimeError:
        pass
    else:
        raise AssertionError(f"Master precheck accepted invalid fixture: {mutation}")

print("EDGE_MASTER_CONTRACT=PASS")
