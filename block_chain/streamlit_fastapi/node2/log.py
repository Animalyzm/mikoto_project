import logging


logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def basic_config(level: str, filename: str = None) -> None:
    format_str = "%(asctime)s - %(levelname)s - %(name)s - \"%(message)s\""
    level_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    if filename:
        logging.basicConfig(filename=filename, format=format_str, level=level_dict[level])
    else:
        logging.basicConfig(format=format_str, level=level_dict[level])
    return None


def log_debug(logger: logging.Logger, message: str) -> None:
    return logger.debug(message)


def log_error(logger: logging.Logger, message: str) -> None:
    return logger.error(message)
