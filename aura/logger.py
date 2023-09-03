import logging
import os


def setup_logger(is_verbose=False):
    logger = logging.getLogger("auracli")
    logger.setLevel(logging.DEBUG)

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if is_verbose else logging.CRITICAL)

    # Make sure .aura directory and log file exists
    os.makedirs(os.path.dirname(os.path.expanduser("~/.aura/auracli.log")), exist_ok=True)

    log_file_path = os.path.expanduser("~/.aura/auracli.log")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(verbose=False):
    return logging.getLogger("auracli")
