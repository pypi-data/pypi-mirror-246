import importlib

import example.hello
import example2.hello
import pytest
import uologging
from assertpy import assert_that


@pytest.fixture(autouse=True)
def reload_uologging_module_before_each_test_run():
    # uologging module has some module-variables that we need reset between each test run
    importlib.reload(uologging.uologging)
    yield


def test_init_console(caplog):
    # Arrange
    uologging.init_console('example')

    # Act -- do things that cause logging to occur
    example.hello.hello()

    # Assert
    assert_that(caplog.text).contains('WARNING')
    assert_that(caplog.text).does_not_contain('INFO')
    assert_that(caplog.text).does_not_contain('DEBUG')


@pytest.mark.parametrize('verbosity,expected_log_msg', 
                         [
                             (0, 'WARNING'),
                             (1, 'INFO'),
                             (2, 'DEBUG'),
                         ]
                         )
def test_set_verbosity(verbosity, expected_log_msg, caplog):
    # Arrange
    uologging.init_console('example')
    uologging.set_verbosity(verbosity, 'example')

    # Act -- do things that cause logging to occur
    example.hello.hello()

    # Assert
    assert_that(caplog.text).contains(expected_log_msg)


def test_init_console_2_packages(capsys):
    # Arrange
    uologging.init_console('example')
    uologging.set_verbosity(2, 'example')
    uologging.init_console('example2')
    uologging.set_verbosity(2, 'example2')

    # Act -- do things that cause logging to occur
    example.hello.hello()
    example2.hello.hello()

    # Assert
    logs = capsys.readouterr().err
    assert_that(logs).contains('Starting: example.hello:hello')
    assert_that(logs).contains('Starting: example2.hello:hello')


def test_init_console_package_twice(capsys):
    # Arrange
    uologging.init_console('example')
    uologging.set_verbosity(2, 'example')
    uologging.init_console('example')
    uologging.set_verbosity(2, 'example')

    # Act -- do things that cause logging to occur
    example.hello.hello()

    # Assert
    logs = capsys.readouterr()
    logs = logs.err
    assert_that(logs).does_not_match(r'(?m)Starting.*\n*.*Starting')
