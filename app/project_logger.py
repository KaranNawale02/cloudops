# project_logger.py

from logging.config import dictConfig
import logging

class UvicornAccessLogFormatter(logging.Formatter):
    """
    Uvicorn logger for separated fields. This class parses the raw
    uvicorn access log record and extracts structured fields like
    method, path, and status_code.
    """
    def format(self, record: logging.LogRecord) -> str:
        # Check if the log record is from uvicorn.access and has the expected format
        if record.name == "uvicorn.access" and len(record.args) == 5:
            # Unpack the arguments from the log record
            _, method, path, _, status_code = record.args
            # Add the extracted fields to the record dictionary
            record.method = method
            record.path = path
            record.status_code = int(status_code)
        return super().format(record)

class LogConfig:
    """Logging configuration to be set for the server."""
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            # Formatter for application logs (JSON format)
            "app_json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            },
            # Formatter for access logs (custom format)
            "access_json": {
                "()": "project_logger.UvicornAccessLogFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(method)s %(path)s %(status_code)d",
            },
        },
        "handlers": {
            # Handler for application logs to stdout
            "app_console": {
                "class": "logging.StreamHandler",
                "formatter": "app_json",
                "stream": "ext://sys.stdout",
            },
            # Handler for access logs to stdout
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access_json",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            # Root logger for application code
            "root": {
                "level": "INFO",
                "handlers": ["app_console"],
            },
            # Uvicorn error logger
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["app_console"],
                "propagate": False,
            },
            # Uvicorn access logger
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": False,
            },
        },
    }

    @staticmethod
    def setup_logging():
        """Load logging configuration."""
        dictConfig(LogConfig.LOGGING_CONFIG)