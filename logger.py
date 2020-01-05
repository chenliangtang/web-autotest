# -*- coding: utf-8 -*-

import logging
from logging import handlers


def logger(filename, when, interval, backup_count):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = handlers.TimedRotatingFileHandler(
        filename,
        when=when,
        interval=interval,
        backupCount=backup_count
    )
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.disabled = False
    return logger


logger = logger('log/test.log', 'M', 1, 1000)
