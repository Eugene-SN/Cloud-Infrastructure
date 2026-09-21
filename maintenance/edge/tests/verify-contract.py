#!/usr/bin/env python3
import copy
import json
import pathlib
import runpy
import sys

root = pathlib.Path(__file__).resolve().parents[1]
maintenance = json.loads(pathlib.Path(sys.argv[1]).read_text())
manifest = json.loads((root / "config/update-units.json").read_text())
templates = json.loads((root / "config/semaphore-templates.json").read_text())
enablement = json.loads((root / "config/manual-driver-enablement.example.json").read_text())
renderer = runpy.run_path(root / "scripts/maintenance-actions-render")
actions = renderer["build_actions"](manifest, templates, enablement)
refresh_source = (root / "scripts/maintenance-refresh").read_text()
semaphore_refresh_source = (root / "playbooks/semaphore-refresh.yml").read_text()
apt_policy = (root / "config/apt-periodic-manual-only.conf").read_text()

rows = maintenance["rows"]
assert maintenance["schema"] == 3
assert maintenance["target_model"] == "update_units_v3"
assert len(rows) == 16
assert maintenance["summary"]["MONITORED_COMPONENTS"] == 23
assert maintenance["summary"]["APT_MANAGED_COMPONENTS"] == 8
assert {row["group"] for row in rows} == {"system", "native", "docker", "cli"}
assert len(manifest["units"]) == 16
assert {u["id"] for u in manifest["units"]} == {r["component"] for r in rows}

apt = next(row for row in rows if row["component"] == "APT_EDGE")
assert len(apt["monitored_components"]) == 8
assert all(not child["actionable"] for child in apt["monitored_components"])
assert all(child["update_target"] == "APT_EDGE" for child in apt["monitored_components"])
assert all(child["component"] not in actions["components"] for child in apt["monitored_components"])

docker = [row for row in rows if row["type"] == "DOCKER"]
assert len(docker) == 6
required = {"application_version", "available_application_version", "image_repository", "image_track", "running_image_digest", "remote_image_digest", "update_reason"}
assert all(required <= set(row) for row in docker)
assert all(row["update_reason"] in {"VERSION_UPDATE", "IMAGE_DIGEST_UPDATE", "CURRENT", "CHECK_FAILED"} for row in docker)
assert next(r for r in docker if r["component"] == "POSTGRESQL")["application_version"] != "18-alpine"
assert next(r for r in docker if r["component"] == "STALWART")["application_version"] != "v0.16"
assert next(r for r in docker if r["component"] == "MATTERMOST")["application_version"] != "latest"

assert actions["schema"] == 8
assert actions["read_only"] is False
assert actions["manual_acceptance_mode"] is True
assert actions["master_template_id"] == 18
assert actions["master_driver_state"] == "executable"
assert actions["stop_on_error"] is True
assert sorted(item["template_id"] for item in actions["components"].values()) == list(range(2, 18))
assert all(item["driver_state"] == "executable" for item in actions["components"].values())
assert set(actions["components"]) == {u["id"] for u in manifest["units"]}
assert not (root / "dashboard/actions.json").exists()
assert "/opt/edge-maintenance/scripts/maintenance-status-render" in refresh_source
assert "/usr/local/bin/maintenance-status-render" not in refresh_source
assert "/opt/edge-maintenance/scripts/maintenance-refresh" in semaphore_refresh_source
assert "/opt/edge-maintenance/scripts/maintenance-status-render" not in semaphore_refresh_source
assert "/opt/edge-maintenance/scripts/maintenance-targets-refresh" not in semaphore_refresh_source
assert "/usr/local/bin/maintenance-status-render" not in semaphore_refresh_source
for apt_key in (
    "Enable",
    "Update-Package-Lists",
    "Download-Upgradeable-Packages",
    "AutocleanInterval",
    "Unattended-Upgrade",
):
    assert f'APT::Periodic::{apt_key} "0";' in apt_policy
assert len(manifest["master_order"]) == 16
assert set(manifest["master_order"]) == {u["id"] for u in manifest["units"]}
assert manifest["master_order"][-1] == "APT_EDGE"
assert next(u for u in manifest["units"] if u["id"] == "SEMAPHORE")["master_policy"] == "individual_only"

locked_enablement = copy.deepcopy(enablement)
locked_enablement["master"] = False
locked_enablement["enabled"]["N8N"] = False
locked_actions = renderer["build_actions"](manifest, templates, locked_enablement)
assert locked_actions["master_template_id"] is None
assert locked_actions["master_driver_state"] == "acceptance_pending"
assert locked_actions["components"]["N8N"]["template_id"] is None
assert locked_actions["components"]["N8N"]["driver_state"] == "acceptance_pending"

broken_enablement = copy.deepcopy(enablement)
del broken_enablement["enabled"]["CODEX"]
try:
    renderer["build_actions"](manifest, templates, broken_enablement)
except RuntimeError:
    pass
else:
    raise AssertionError("actions renderer accepted a missing enablement target")
print("EDGE_MAINTENANCE_CONTRACT=PASS")
