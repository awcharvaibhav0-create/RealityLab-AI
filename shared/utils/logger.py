import logging
import logging.handlers
import json
import sys
from typing import Optional


class JSONFormatter(logging.Formatter):
    """Format logs as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


class RealityLogger:
    """A structured JSON-ready logger factory."""

    @staticmethod
    def get_logger(
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO,
        json_format: bool = False,
    ) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Prevent adding handlers multiple times if get_logger is called again
        if not logger.handlers:
            if json_format:
                formatter = JSONFormatter()
            else:
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # File handler
            if log_file:
                # 10 MB per file, keep 5 backups
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10 * 1024 * 1024, backupCount=5
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        return logger
