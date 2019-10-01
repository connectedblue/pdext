"""
This set of tests checks how new repository locations are
defined and managed.

It works at the functional level rather than through the pd
interface

The fixture no_repo_defined installs a temporary yml file to perform 
the tests in and also is passed in before instantiation.  This 
allows tests to be carried out before instantiation.

Means that each test has to instantiate test_repo before any
of the methods can be tested
"""

import os,shutil
import pytest

from pdext.symbols import __installed_extensions__

def test_create_default(no_repo_defined):
    # no yaml file should exist when tests start
    assert os.path.isfile(__installed_extensions__) == False
    repo, test_dir = no_repo_defined
    repo = repo()
    # and then the yaml should after the repo is instantiated
    assert os.path.isfile(__installed_extensions__) == True
    assert repo.default_repository=='user'

def test_adding_and_changing_default(no_repo_defined):
    repo, test_dir = no_repo_defined
    repo = repo()

    #adding a test location should recreate the directory
    repo.add_location('test', test_dir, beginning=True)
    assert os.path.exists(test_dir)
    
    assert repo.search_order == ['test','user']
    assert repo.default_repository=='user'
    # check it has removed correctly
    repo.remove_location('test')
    assert repo.search_order == ['user']
    repo, test_dir = no_repo_defined
    repo = repo()
    assert len(repo.repositories)==1
    # Add in again, this time make it default
    repo.add_location('test', test_dir, beginning=False,
                      default=True)
    assert repo.search_order == ['user', 'test']
    assert repo.search_path[1] == test_dir
    assert repo.default_repository=='test'

def test_error_cases(no_repo_defined):
    repo, test_dir = no_repo_defined
    repo = repo()
    with pytest.raises(ValueError):
         repo.remove_location('test')
    with pytest.raises(KeyError):
         repo.remove_location('xxx')
    with pytest.raises(KeyError):
         repo.default_repository='xxx'
    with pytest.raises(ValueError):
         repo.new_search_order(['test'])
    with pytest.raises(ValueError):
         repo.new_search_order(['test','user', 'xxx'])
    