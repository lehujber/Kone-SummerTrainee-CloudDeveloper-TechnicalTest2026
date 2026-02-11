from os import getenv
from logging import getLogger

DATABASE_URI = getenv("DATABASE_URI", "sqlite:///./seashells.db")

DEBUG_MODE = getenv("DEBUG_MODE", "false").lower() == "true"

def new_logger(name: str):
    logger = getLogger(name)
    if DEBUG_MODE:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
    return logger