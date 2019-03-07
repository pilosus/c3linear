import logging

#
# Logging
#


LOG_LEVEL = logging.DEBUG
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s][%(filename)s:%(lineno)d]'
        '[%(name)s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
MAX_PARALLEL_REPLICAS = 2

#
# Pytest configuration
#


def pytest_addoption(parser):
    """
    Called once at the beginning of a test run
    """
    parser.addoption("--loglevel", action="store", default=LOG_LEVEL,
                     help="Application log level")


def pytest_configure(config):
    """
    Gets called for every conftest file after CLI options have been parsed
    """
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.setLevel(config.getoption('--loglevel'))
    LOG_HANDLER.setFormatter(LOG_FORMATTER)
    root_logger.addHandler(LOG_HANDLER)


def pytest_make_parametrize_id(config, val, argname):
    """
    Return parametrization info when running test with verbose option
    """
    if isinstance(val, dict):
        return '{}({})'.format(
            argname,
            ', '.join('{}={}'.format(k, v) for k, v in val.items())
        )
