import logging
import os


def setup_logger(is_verbose, save_logs, log_file_path):
    logger = logging.getLogger("auracli")
    logger.setLevel(logging.DEBUG)

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if is_verbose else logging.CRITICAL)

    # Read environment variables for log convigurations
    collect_logs = os.environ.get("AURA_CLI_SAVE_LOGS", "").lower() in {"yes", "y", "true", "1"}
    logfile_path = os.environ.get("AURA_CLI_LOGS_PATH") or os.path.expanduser("~/.aura/auracli.log")

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    if collect_logs:
        # Make sure .aura directory and log file exists
        os.makedirs(os.path.dirname(logfile_path), exist_ok=True)
        file_handler = logging.FileHandler(logfile_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(verbose=False):
    return logging.getLogger("auracli")
