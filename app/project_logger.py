from logging.config import dictConfig
import logging

class UvicornAccessLogFormatter(logging.Formatter):
    """
    uvicorn logger for a separated fields
    """
    def format(self, record: logging.LogRecord) -> str:
        if record.name == "uvicorn.access" and len(record.args) == 5:
            _, method, path, _, status_code = record.args
            record.method = method
            record.path = path
            record.status_code = int(status_code)
        return super().format(record)

class LogConfig:
    """Logging configuration."""
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
            },
            "app_json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            },
            "access_json": {
                "()": "project_logger.UvicornAccessLogFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(method)s %(path)s %(status_code)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            # Handler for application logs
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "app_json", # Use the app json formatter
                "filename": "./logs/app.log",
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 5,
            },
            # NEW: Handler specifically for access logs
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "access_json", # Use the access json formatter
                "filename": "./logs/access.log", # Log to a separate file
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 5,
            },
        },
        "loggers": {
            # Root logger for application code
            "root": {
                "level": "INFO",
                "handlers": ["console", "app_file"],
            },
            # Uvicorn error logger
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "app_file"],
                "propagate": False,
            },
            # UPDATED: Uvicorn access logger
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console", "access_file"],
                "propagate": False,
            },
        },
    }

    @staticmethod
    def setup_logging():
        dictConfig(LogConfig.LOGGING_CONFIG)