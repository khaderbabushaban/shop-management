"""
utils/logger.py
---------------
Application-wide logger.  All modules import `logger` from here so that
log format and level are configured in a single place.
"""

import logging
import sys


def _build_logger() -> logging.Logger:
    log = logging.getLogger("shop_management")
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s  [%(levelname)-8s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log


logger = _build_logger()
