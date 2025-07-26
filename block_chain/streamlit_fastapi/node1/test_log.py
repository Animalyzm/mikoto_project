import logging

import log


def test_get_logger():
    """ test: return, type """
    assert log.get_logger('test') == logging.getLogger('test')
    assert isinstance(log.get_logger('test'), type(logging.getLogger('test')))


def test_basic_config():
    """ test: return=None """
    logger = log.get_logger('test')
    log.basic_config('debug', 'test.log')
    assert not log.log_debug(logger, 'debug')


def test_log_debug():
    """ test: return=None """
    logger = logging.getLogger('test')
    assert not log.log_debug(logger, 'debug')


def test_log_error():
    """ test: return=None """
    logger = logging.getLogger('test')
    assert not log.log_error(logger, 'error')
