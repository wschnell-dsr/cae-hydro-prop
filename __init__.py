# -*- coding: utf-8 -*-

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": 0,
    "formatters": {"standard": {"format": "%(asctime)s %(module)s %(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s"}},
    "handlers": {"default": {"level": "INFO", "formatter": "standard", "class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO"},
        "matplotlib": {"handlers": ["default"], "level": "INFO"},
        "hydro_prop": {"handlers": ["default"], "level": "DEBUG", "propagate": False}
    },
}
