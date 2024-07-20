"""Logger configuration for the package."""

import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
