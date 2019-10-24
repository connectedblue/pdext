import pytest
from fixtures import *

def pytest_addoption(parser):
    parser.addoption("--skip_this", action="store_true",
                     help="Skip the tests marked skip_this")

def pytest_runtest_setup(item):
    if 'skip_this' in item.keywords and item.config.getoption("--skip_this"):
        pytest.skip("--skip_this flag present, so test skipped")

def pytest_configure(config):
    config.addinivalue_line("markers", "skip_this: custom marker for skipping tests")