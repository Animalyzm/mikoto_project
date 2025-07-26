import logging


logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)


def get_logger(name):
    return logging.getLogger(name)


def basic_config(level, filename=None):
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


def log_debug(logger, message):
    return logger.debug(message)


def log_error(logger, message):
    return logger.error(message)
