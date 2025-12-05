import logging

from src.settings import app_settings

log_level: str = app_settings.log_level


class CustomFormatter(logging.Formatter):
    blue = "\x1b[36;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LogManager:

    _loggers = logging.root.manager.loggerDict
    _disabled_loggers = [
        "uvicorn.access",
        "fastapi",
        "uvicorn",
    ]

    @classmethod
    def _set_default_level(cls):
        # for name in cls._loggers:
        #     logging.getLogger(name).setLevel(logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, app_settings.log_level))

    @classmethod
    def _disable_loggers(cls):
        for name in cls._disabled_loggers:
            logger = logging.getLogger(name)
            logger.disabled = True

    @classmethod
    def log_handler(cls) -> logging.StreamHandler:
        cls._set_default_level()
        cls._disable_loggers()
        log_handler = logging.StreamHandler()
        log_handler.setLevel(app_settings.log_level)
        log_handler.setFormatter(CustomFormatter())
        return log_handler
