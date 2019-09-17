import os,shutil
import pytest

from pdext.repository import extension_repository
from pdext.symbols import __installed_extensions__

test_dir = '/tmp/test_pdext'

def test_create_default(testrepo):
    # no yaml file should exist when tests start
    assert os.path.isfile(__installed_extensions__) == False
    repo = testrepo()
    # and then the yaml should after the repo is instantiated
    assert os.path.isfile(__installed_extensions__) == True
    assert repo.default_repository=='user'

def test_adding_and_changing_default(testrepo):
    repo = testrepo()
    # remove test extension directory if it exists
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    #adding a test location should recreate the directory
    repo.add_location('test', test_dir, beginning=True)
    assert os.path.exists(test_dir)
    repo = testrepo()
    assert repo.search_order == ['test','user']
    assert repo.default_repository=='user'
    # check it has removed correctly
    repo.remove_location('test')
    assert repo.search_order == ['user']
    repo = testrepo()
    assert len(repo.repositories)==1
    # Add in again, this time make it default
    repo.add_location('test', test_dir, beginning=False,
                      default=True)
    assert repo.search_order == ['user', 'test']
    assert repo.search_path[1] == test_dir
    assert repo.default_repository=='test'

def test_error_cases(testrepo):
    repo = testrepo()
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
    
    # clean up
    shutil.rmtree(test_dir)