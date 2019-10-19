"""
FIXTURE FUNCTIONS USED IN TESTS
"""
import os, shutil, tempfile
import pytest

from pdext import pd
from pdext.repository import ExtensionRepository
from pdext.symbols import df_ext, repository

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
        pd_ext = repository()
        make_test_repos(pd_ext, temp_session_directory)
        # two repos installing into the default
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage1, repository_name='test1')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage1, repository_name='test1')
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage2, repository_name='test2')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage2, repository_name='test2')
        
        # each repo has its own namespace
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage1, repository_name='test1', collection='circle1')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage1, repository_name='test1',  collection='circle1')
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage2, repository_name='test2', collection='circle2')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage2, repository_name='test2', collection='circle2')

        # both functions in the same namespace but different repos
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage1, repository_name='test1', collection='circle3')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage1, repository_name='test2',  collection='circle3')

        # each function in the same namespace, but a clash with a name in a different repo
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage1, repository_name='test1', collection='circle4')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage1, repository_name='test2',  collection='circle4')
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage2, repository_name='test2', collection='circle4')

        # install extensions from a single file into a separate collection
        pd_ext.install_extension('calculate_circumference_from_radius', testpackage3, repository_name='test1', collection='singlepy')
        pd_ext.install_extension('calculate_circumference_from_diameter', testpackage3, repository_name='test1',  collection='singlepy')

        yield pd_ext, df_ext

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

