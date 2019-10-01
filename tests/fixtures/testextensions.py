import os

import pytest

test_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'testpackages')

@pytest.fixture(scope='session')
def testpackage1():
    yield os.path.join(test_package_dir, 'package1')

@pytest.fixture(scope='session')
def testpackage2():
    yield os.path.join(test_package_dir, 'package2')

@pytest.fixture(scope='session')
def testpackage3():
    yield os.path.join(test_package_dir, 'package3.py')
