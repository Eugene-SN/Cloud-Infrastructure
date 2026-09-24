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
manual_update_source = (root / "scripts/manual-update").read_text()
health_source = (root / "scripts/master-health-validate").read_text()

rows = maintenance["rows"]
manual = {u["id"] for u in manifest["units"]}
native = {u["id"] for u in manifest["native_auto"]}
index = {r["component"]: r for r in rows}

assert maintenance["schema"] == 3
assert maintenance["target_model"] == "update_units_v5"
assert manifest["schema"] == 2
assert manifest["ownership_mode"] == "native_first_hybrid"
assert "monitor_only" not in manifest
assert len(manual) == 17
assert native == {"HERMES", "CODEX", "UBUNTU_SECURITY"}
assert set(index) == manual
assert "HERMES" not in index
assert "CODEX" not in index
assert maintenance["summary"]["TOTAL"] == 17
assert maintenance["summary"]["ACTIONABLE_TARGETS"] == 17
assert "MONITOR_ONLY_TARGETS" not in maintenance["summary"]
assert maintenance["summary"]["APT_MANAGED_COMPONENTS"] == 8

for target in manual:
    assert index[target]["actionable"] is True
    assert index[target]["update_owner"] == "maintenance_manual"

docker = [r for r in rows if r["type"] == "DOCKER"]
assert len(docker) == 9
required = {
    "application_version",
    "available_application_version",
    "image_repository",
    "image_track",
    "running_image_digest",
    "remote_image_digest",
    "update_reason",
}
assert all(required <= set(row) for row in docker)
assert next(r for r in docker if r["component"] == "BULWARK")["image_track"] == "latest"
nextcloud = next(r for r in docker if r["component"] == "NEXTCLOUD")
nextcloud_available = nextcloud["available_application_version"]
assert nextcloud_available.count(".") == 2
nextcloud_parts = nextcloud_available.split(".")
assert nextcloud["image_track"] == ".".join(nextcloud_parts[:2]) + "-apache"
assert next(u for u in manifest["units"] if u["id"] == "NEXTCLOUD")["driver"] == "nextcloud_compose"
assert (root / "scripts/update-nextcloud").is_file()

assert templates["schema"] == 2
assert set(templates["components"]) == manual
template_ids = [v["template_id"] for v in templates["components"].values()]
assert len(template_ids) == len(set(template_ids))
assert templates["refresh_template_id"] == 1
assert templates["master_template_id"] == 18

assert enablement["schema"] == 2
assert enablement["master"] is True
assert "CLOUDCLI" not in enablement["enabled"]
assert set(enablement["enabled"]) == manual
assert all(enablement["enabled"].values())

assert 'enablement.get("schema") != 1' not in manual_update_source
assert manual_update_source.count('enablement.get("schema") != 2') == 2
assert 'driver in ("compose", "nextcloud_compose")' in manual_update_source
assert 'elif driver == "nextcloud_compose":' in manual_update_source
assert actions["components"]["NEXTCLOUD"]["managed_by"] == "docker"
assert "--remove-orphans" in manual_update_source
assert '"docker", "rmi"' in manual_update_source
assert '"image", "prune"' in manual_update_source
assert "rotate_backups" in manual_update_source
assert "autoremove" in manual_update_source
assert '"apt-get", "clean"' in manual_update_source
assert ".old" in manual_update_source
assert '"projects-webdav.service"' in health_source
assert 'unit.get("services", [unit["service"]])' in health_source
assert "DOCKER_UNITS=" in health_source
assert "DOCKER_SERVICES=" in health_source

assert actions["schema"] == 10
assert actions["target_model"] == "update_units_v5"
assert actions["execution_mode"] == "manual_only"
assert actions["auto_update"] is False
assert actions["master_template_id"] == 18
assert set(actions["components"]) == manual
assert "HERMES" not in actions["components"]
assert "CODEX" not in actions["components"]

for target in manual:
    assert actions["components"][target]["template_id"] is not None
    assert actions["components"][target]["driver_state"] == "executable"
    assert actions["components"][target]["update_owner"] == "maintenance_manual"

assert not (root / "config/apt-periodic-manual-only.conf").exists()
assert not (root / "playbooks/updates/hermes.yml").exists()
assert not (root / "playbooks/updates/codex.yml").exists()

for path in (
    "rclone.yml",
    "nextcloud.yml",
    "nextcloud-postgresql.yml",
    "nextcloud-redis.yml",
):
    assert (root / "playbooks/updates" / path).is_file()

locked = copy.deepcopy(enablement)
locked["enabled"]["N8N"] = False
locked_actions = renderer["build_actions"](manifest, templates, locked)
assert locked_actions["components"]["N8N"]["template_id"] is None
assert locked_actions["components"]["N8N"]["driver_state"] == "acceptance_pending"

print("EDGE_MAINTENANCE_CONTRACT=PASS")
