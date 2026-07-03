import pytest
from shared.config.config_manager import ConfigurationManager
from shared.config.validator import ConfigurationError


def test_config_manager_singleton():
    manager1 = ConfigurationManager.get_instance()
    manager2 = ConfigurationManager.get_instance()
    assert manager1 is manager2


def test_config_loading(monkeypatch):
    monkeypatch.setenv("REALITYLAB_ENV", "testing")
    monkeypatch.setenv("DATABASE_PATH", "test.db")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    manager = ConfigurationManager()
    manager.initialize()

    config = manager.get()
    assert config.environment == "testing"
    assert config.database.path == "test.db"
    assert config.logging.level == "DEBUG"


def test_config_validation_missing_env(monkeypatch):
    monkeypatch.delenv("REALITYLAB_ENV", raising=False)

    manager = ConfigurationManager()

    # We provide a default environment "development" so it won't fail here usually
    # But let's mock the loader to return an invalid dict
    from shared.config.loader import ConfigurationLoader

    class BadLoader(ConfigurationLoader):
        def load(self):
            self.validator.validate({})
            return None

    manager.loader = BadLoader()
    with pytest.raises(
        ConfigurationError, match="Missing required config: environment"
    ):
        manager.initialize()


def test_config_validation_missing_db(monkeypatch):
    manager = ConfigurationManager()
    from shared.config.loader import ConfigurationLoader

    class BadLoader(ConfigurationLoader):
        def load(self):
            self.validator.validate({"environment": "test"})
            return None

    manager.loader = BadLoader()
    with pytest.raises(
        ConfigurationError, match="Missing required config: database.path"
    ):
        manager.initialize()
