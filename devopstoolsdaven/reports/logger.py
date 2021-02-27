import logging.config
from logging import Logger


# noinspection StrFormat
def logger_setup(log_cfg: dict) -> None:
    logging.config.dictConfig(log_cfg)


def get_logger(name: str) -> Logger:
    return logging.getLogger(name=name)
