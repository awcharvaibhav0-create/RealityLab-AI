import json
import logging
from shared.utils.logger import RealityLogger


def test_logger_creation():
    logger = RealityLogger.get_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO


def test_json_logger(tmp_path):
    log_file = tmp_path / "test.log"
    logger = RealityLogger.get_logger(
        "json_test", log_file=str(log_file), json_format=True
    )
    logger.info("Test message")

    with open(log_file, "r") as f:
        log_line = f.readline()
        log_data = json.loads(log_line)
        assert log_data["message"] == "Test message"
        assert log_data["level"] == "INFO"
        assert log_data["logger_name"] == "json_test"
