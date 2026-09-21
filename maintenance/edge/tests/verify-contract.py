#!/usr/bin/env python3
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
maintenance = json.loads(pathlib.Path(sys.argv[1]).read_text())
actions = json.loads((root / "dashboard/actions.json").read_text())
manifest = json.loads((root / "config/update-units.json").read_text())

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
assert actions["read_only"] is True
assert actions["master_template_id"] is None
assert all(item["template_id"] is None for item in actions["components"].values())
assert all(item["driver_state"] == "acceptance_pending" for item in actions["components"].values())
assert set(actions["components"]) == {u["id"] for u in manifest["units"]}
print("EDGE_MAINTENANCE_CONTRACT=PASS")
