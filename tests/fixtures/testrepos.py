"""
FIXTURE FUNCTIONS USED IN TESTS
"""
import os, shutil, tempfile
import pytest

import pdext as pd
from _pdext.repository import ExtensionRepository
from _pdext.symbols import df_ext, repository, __import_file_line_spec__

from .helpers import save_current_installed_extensions, make_test_repos, \
                     temp_session_directory, temp_module_directory

@pytest.fixture(scope='module')
def pdext_with_loaded_testpackages(temp_session_directory, 
                                   testpackage1, testpackage2, testpackage3):
    """
    This fixture provides an imported pdext module pre configured
    with all the test packages, divided into various collections

    Any existing yaml file is preserved and replaced after the 
    test module completes

    Two items passed to the test function:
        pd_ext - the pandas module configured with the extensions
                 already intalled
        df_ext - a function to obtain the extension namespace from a dataframe

    Don't use this fixture in the same module as the other similar fixtures
    """
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        pdext = repository()
        make_test_repos(pdext, temp_session_directory)

        def spec(test_package,func):
            return __import_file_line_spec__.format(test_package, func)
        
        # two repos installing into the default
        pdext.set_default_repository('test1')
        pdext.import_extension(spec(testpackage1,'calculate_circumference_from_radius'))
        pdext.import_extension(spec(testpackage1,'calculate_circumference_from_diameter'))
        pdext.set_default_repository('test2')
        pdext.import_extension(spec(testpackage2,'calculate_circumference_from_radius'))
        pdext.import_extension(spec(testpackage2,'calculate_circumference_from_diameter'))
        
        # each repo has its own namespace
        pdext.set_default_repository('test1')
        pdext.import_extension(spec(testpackage1,'circle1.calculate_circumference_from_radius'))
        pdext.import_extension(spec(testpackage1,'circle1.calculate_circumference_from_diameter'))
        pdext.set_default_repository('test2')
        pdext.import_extension(spec(testpackage2,'circle2.calculate_circumference_from_radius'))
        pdext.import_extension(spec(testpackage2,'circle2.calculate_circumference_from_diameter'))

        # both functions in the same namespace but different repos
        pdext.set_default_repository('test1')
        pdext.import_extension(spec(testpackage1,'circle3.calculate_circumference_from_radius'))
        pdext.set_default_repository('test2')
        pdext.import_extension(spec(testpackage1,'circle3.calculate_circumference_from_diameter'))

        # each function in the same namespace, but a clash with a name in a different repo
        pdext.set_default_repository('test1')
        pdext.import_extension(spec(testpackage1,'circle4.calculate_circumference_from_radius'))
        pdext.set_default_repository('test2')
        pdext.import_extension(spec(testpackage1,'circle4.calculate_circumference_from_diameter'))
        pdext.import_extension(spec(testpackage2,'circle4.calculate_circumference_from_radius'))

        # install extensions from a single file into a separate collection
        pdext.set_default_repository('test1')
        pdext.import_extension(spec(testpackage3,'singlepy.calculate_circumference_from_radius'))
        pdext.import_extension(spec(testpackage3,'singlepy.calculate_circumference_from_diameter'))

        yield pdext, df_ext

@pytest.fixture(scope='module')
def two_test_session_repos(temp_module_directory):
    """
    This fixture provides an instantiated ExtensionRepository
    class object to allow a test to define any repository location
    required.

    Any existing yaml file is preserved and replaced after the 
    test module completes

    One item passed to the test function:
        test_repo - two different locations named test1 and test2
                    where extensions can be installed
    """
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        test_repo = ExtensionRepository()
        make_test_repos(test_repo, temp_module_directory)
        yield test_repo


@pytest.fixture(scope='module')
def no_repo_defined(temp_module_directory):
    """
    This fixture provides an uninstantiated ExtensionRepository
    class object to allow a test to define any repository location
    required.

    Any existing yaml file is preserved and replaced after the 
    test module completes

    Two items passed to the test function:
        extension_repository - class
        temp_module_directory 
    """
    with save_current_installed_extensions():
        yield ExtensionRepository, temp_module_directory


