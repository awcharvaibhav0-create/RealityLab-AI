from sdk.plugin_registry import plugin_registry
from sdk.plugin_validator import plugin_validator


def test_plugin_registry():
    plugin_registry.register("test_plugin", "instance")
    assert plugin_registry.get_plugin("test_plugin") == "instance"
    assert "test_plugin" in plugin_registry.list_plugins()


def test_plugin_validator():
    valid_manifest = {"name": "test", "version": "1.0", "entry_point": "main.py"}
    invalid_manifest = {"name": "test"}

    assert plugin_validator.validate(valid_manifest) == True
    assert plugin_validator.validate(invalid_manifest) == False
