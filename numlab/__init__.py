import logging

import numlab.nlre

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

__all__ = ["nlre"]

__version__ = "0.1.1"
