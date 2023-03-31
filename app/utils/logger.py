# clast/app/utils/logger.py

import logging
from logging.handlers import TimedRotatingFileHandler

def generate_logger(logger_name: str, logging_level: int, filename: str) -> logging.Logger:
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(logging_level)

    file_handler = TimedRotatingFileHandler(filename, when="D", interval=1, backupCount=1, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
        '[in %(pathname)s:%(lineno)d]'
        )
    file_handler.setFormatter(formatter)
    new_logger.addHandler(file_handler)

    return new_logger