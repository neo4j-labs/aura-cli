import logging
import os


def setup_logger(is_verbose, save_logs, log_file_path):
    logger = logging.getLogger("auracli")
    logger.setLevel(logging.DEBUG)

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if is_verbose else logging.CRITICAL)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    if save_logs:
        # Make sure .aura directory and log file exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(verbose=False):
    return logging.getLogger("auracli")
