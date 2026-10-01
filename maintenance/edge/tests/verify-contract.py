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
assert len(manual) == 15
assert native == {"HERMES", "CODEX", "UBUNTU_SECURITY", "ANTIGRAVITY"}
assert set(index) == manual
assert "HERMES" not in index
assert "CODEX" not in index
assert "ANTIGRAVITY" not in index
assert maintenance["summary"]["TOTAL"] == 15
assert maintenance["summary"]["ACTIONABLE_TARGETS"] == 15
assert maintenance["summary"]["CLI_TARGETS"] == 0
assert "MONITOR_ONLY_TARGETS" not in maintenance["summary"]
assert maintenance["summary"]["APT_MANAGED_COMPONENTS"] == 8

for target in manual:
    assert index[target]["actionable"] is True
    assert index[target]["update_owner"] == "maintenance_manual"

docker = [r for r in rows if r["type"] == "DOCKER"]
assert len(docker) == 8
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

postgresql = next(r for r in docker if r["component"] == "POSTGRESQL")
assert postgresql["image_track"] == "18"
assert postgresql["source"] == "POSTGRES_OFFICIAL_LATEST_STABLE_DOCKER"
assert postgresql["application_version"].startswith("18.")
assert postgresql["available_application_version"].startswith("18.")
assert not postgresql["available_application_version"].startswith("19.")
postgresql_unit = next(u for u in manifest["units"] if u["id"] == "POSTGRESQL")
assert postgresql_unit["major_policy"] == "18"
assert postgresql_unit["image_track"] == "18"
assert postgresql_unit["directory"] == "/opt/postgres"
assert postgresql_unit["files"] == ["compose.yaml"]
assert postgresql_unit["service"] == "postgres"
print("POSTGRESQL_IMAGE_TRACK=18")
print("POSTGRESQL_MAJOR_UPGRADE_DISCOVERY=DISABLED")

assert not (root / "playbooks/updates/nextcloud-postgresql.yml").exists()

stalwart = next(r for r in docker if r["component"] == "STALWART")
stalwart_available = stalwart["available_application_version"]
stalwart_parts = stalwart_available.split(".")
assert len(stalwart_parts) == 3
assert stalwart["image_track"] == "v" + ".".join(stalwart_parts[:2])
assert stalwart["source"] == "STALWART_OFFICIAL_LATEST_STABLE_DOCKER"
stalwart_unit = next(u for u in manifest["units"] if u["id"] == "STALWART")
assert stalwart_unit["driver"] == "stalwart_compose"
assert (root / "scripts/update-stalwart").is_file()

restic_unit = next(u for u in manifest["units"] if u["id"] == "RESTIC")
assert restic_unit["driver"] == "self_update"
assert restic_unit["binary"] == "/usr/local/bin/restic"
assert restic_unit["arguments"] == ["self-update"]

assert templates["schema"] == 2
assert set(templates["components"]) == manual
template_ids = [v["template_id"] for v in templates["components"].values()]
assert len(template_ids) == len(set(template_ids))
assert templates["refresh_template_id"] == 1
assert templates["master_template_id"] == 18

assert enablement["schema"] == 2
assert enablement["master"] is True
assert "CLOUDCLI" not in enablement["enabled"]
assert "ANTIGRAVITY" not in enablement["enabled"]
assert set(enablement["enabled"]) == manual
assert all(enablement["enabled"].values())

assert 'enablement.get("schema") != 1' not in manual_update_source
assert manual_update_source.count('enablement.get("schema") != 2') >= 1
assert 'driver in ("compose", "nextcloud_compose", "stalwart_compose")' in manual_update_source
assert 'elif driver == "nextcloud_compose":' in manual_update_source
assert 'elif driver == "stalwart_compose":' in manual_update_source
assert actions["components"]["NEXTCLOUD"]["managed_by"] == "docker"
assert actions["components"]["STALWART"]["managed_by"] == "docker"
assert "NEXTCLOUD_POSTGRESQL" not in actions["components"]
assert "NEXTCLOUD_POSTGRESQL" not in {u["id"] for u in manifest["units"]}
assert "NEXTCLOUD_POSTGRESQL" not in templates["components"]
assert "NEXTCLOUD_POSTGRESQL" not in enablement["enabled"]
assert "--remove-orphans" not in manual_update_source
assert '"docker", "rmi"' in manual_update_source
assert '"image", "prune"' in manual_update_source
assert "rotate_backups" not in manual_update_source
assert "autoremove" in manual_update_source
assert '"apt-get", "clean"' in manual_update_source
assert ".old" in manual_update_source
assert "pg_dumpall" not in manual_update_source
assert "database_backup" not in json.dumps(manifest)
assert '"projects-webdav.service"' in health_source
assert 'unit.get("health_services")' in health_source
assert '"nextcloud_compose"' in health_source
assert '"stalwart_compose"' in health_source
assert "DOCKER_UNITS=" in health_source
assert "DOCKER_SERVICES=" in health_source

# Master health coverage verification
COMPOSE_DRIVERS = ("compose", "nextcloud_compose", "stalwart_compose")
compose_family_units = [u for u in manifest["units"] if u.get("driver") in COMPOSE_DRIVERS]
assert len(compose_family_units) == 8


nc_manifest = next(u for u in manifest["units"] if u["id"] == "NEXTCLOUD")
assert set(nc_manifest["health_services"]) == {"app", "cron"}

sw_manifest = next(u for u in manifest["units"] if u["id"] == "STALWART")
assert set(sw_manifest["health_services"]) == {"stalwart"}

collector_source = (root / "scripts/maintenance-versions-collector").read_text(encoding="utf-8")

# n8n stable aliases can move beyond the first Docker Hub Tags API page when
# nightly tags are published. Discovery must paginate without a version fallback.
assert "n8n_alias_page_limit = 20" in collector_source
assert "while not any(" in collector_source
assert 'next_url = page.get("next")' in collector_source
assert "page_count >= n8n_alias_page_limit" in collector_source


assert '"--target-version"' in manual_update_source
assert '"--target-track"' in manual_update_source
assert '"--target-digest"' in manual_update_source

import subprocess

assert actions["schema"] == 10
assert actions["target_model"] == "update_units_v5"
assert actions["execution_mode"] == "manual_only"
assert actions["auto_update"] is False
assert actions["master_template_id"] == 18
assert set(actions["components"]) == manual
assert "HERMES" not in actions["components"]
assert "CODEX" not in actions["components"]
assert "ANTIGRAVITY" not in actions["components"]

for target in manual:
    assert actions["components"][target]["template_id"] is not None
    assert actions["components"][target]["driver_state"] == "executable"
    assert actions["components"][target]["update_owner"] == "maintenance_manual"

assert not (root / "config/apt-periodic-manual-only.conf").exists()
assert not (root / "playbooks/updates/hermes.yml").exists()
assert not (root / "playbooks/updates/codex.yml").exists()
assert not (root / "playbooks/updates/antigravity.yml").exists()

for path in (
    "rclone.yml",
    "nextcloud.yml",
    "nextcloud-redis.yml",
):
    assert (root / "playbooks/updates" / path).is_file()

locked = copy.deepcopy(enablement)
locked["enabled"]["N8N"] = False
locked_actions = renderer["build_actions"](manifest, templates, locked)
assert locked_actions["components"]["N8N"]["template_id"] is None
assert locked_actions["components"]["N8N"]["driver_state"] == "acceptance_pending"

print("EDGE_MAINTENANCE_CONTRACT=PASS")
