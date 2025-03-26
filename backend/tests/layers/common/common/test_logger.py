from importlib import import_module
import logging

module = import_module('common.logger')
Logger = getattr(module, 'Logger')
log = Logger()


def test_init_ok(caplog):
    """
    正常系
    """
    # pylint: disable-next=unnecessary-dunder-call
    Logger.__init__(log, 'test')
    assert ("test", logging.info, "test") not in caplog.record_tuples


def test_debug_ok(caplog):
    """
    正常系
    """
    Logger.debug(log, 'test_debug')
    assert ("test", logging.debug, "test_debug") not in caplog.record_tuples


def test_info_ok(caplog):
    """
    正常系
    """
    Logger.info(log, 'test_info')
    assert ("test", logging.info, "test_info") not in caplog.record_tuples


def test_warning_ok(caplog):
    """
    正常系
    """
    Logger.warning(log, 'test_warning')
    assert ("test", logging.warning, "test_warning") not in caplog.record_tuples


def test_error_ok(caplog):
    """
    正常系
    """
    Logger.error(log, 'test_error')
    assert ("test", logging.error, "test_error") not in caplog.record_tuples
