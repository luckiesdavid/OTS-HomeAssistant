"""SG Ready room setpoint increase per heating circuit must be adjustable."""

import importlib.util
from pathlib import Path

import pytest


# User-reported Smart app range; not yet APK-confirmed (docs/agent-notes/sg-ready.md).
INCREASES = {
    "ACONg458AAE=": 31886,  # Heating circuit 1
    "ACONg+1MAAE=": 19693,  # Heating circuit 2
    "ACONg8xcAAE=": 23756,  # Heating circuit 3
    "ACONgyssAAE=": 11307,  # Heating circuit 4
}


@pytest.fixture
def builder():
    path = Path(__file__).resolve().parents[1] / "tools/build_discovery_catalog.py"
    spec = importlib.util.spec_from_file_location("sg_ready_catalog_builder", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_packaged_bindings_match_builder(catalog_mod, builder):
    catalog = catalog_mod.load_catalog()
    for oid, hc_tag in INCREASES.items():
        expected = {
            "platform": "number", "write_id": oid, "write_source": "user_reported",
            "unit": "K", "min": 0.0, "max": 5.0, "step": 0.5,
        }
        point = catalog.points_by_id[oid]
        assert point["hc_tag"] == hc_tag
        rebuilt = {"id": oid, "platform": "sensor"}
        builder.apply_apk_number_binding(rebuilt)
        for key, value in expected.items():
            assert point[key] == value
            assert rebuilt[key] == value


def test_sg_ready_discovery_and_existing_sensor_rescan(catalog_mod, discovery_mod, entities_mod):
    catalog = catalog_mod.load_catalog()
    scan = discovery_mod.DiscoveryScanResult(
        catalog_version=catalog.catalog_version,
        values={oid: 1.0 for oid in INCREASES},
    )
    discovered = entities_mod.build_entities(catalog=catalog, scan=scan)
    assert {e["read_id"] for e in discovered["numbers"]} == set(INCREASES)
    assert discovered["sensors"] == []
    for entity in discovered["numbers"]:
        assert entity["write_id"] == entity["read_id"]
        assert entity["unit"] == "K"
        assert entity["step"] == 0.5

    old_sensors = [{"id": oid, "name": "Existing dashboard sensor"} for oid in INCREASES]
    merged, added = entities_mod.merge_discovered_entities({"sensors": old_sensors}, discovered)
    assert added["numbers"] == 4
    assert merged["sensors"] == old_sensors
