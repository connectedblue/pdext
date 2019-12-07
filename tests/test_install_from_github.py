import logging
import pytest

from pandex.symbols import pd_ext, df_ext, __import_file_line_spec__
from fixtures.helpers import save_current_installed_extensions, make_test_repos

@pytest.mark.skip_this
def test_install_from_github(temp_module_directory, df_X, caplog):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        make_test_repos(pdext, temp_module_directory)

        # capture the log record when a github archive is downloaded
        caplog.set_level(logging.INFO)

        # Check default latest version is downloaded and executes correctly
        assert hasattr(dfext, 'circle_calculations') == False
        # two repos installing into the default
        spec = __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection', 
                            'circle_calculations')
        pdext.import_extension(spec)
        assert hasattr(dfext, 'circle_calculations') == True
        # Test execution of the extension
        assert 'circumference' not in df_X
        assert 'area' not in df_X
        dfext.circle_calculations('numbers')
        assert 'circumference' in df_X
        assert 'area' in df_X
        # Test correct version of the docstring
        assert 'Calculates the circumference' in dfext.circle_calculations.__doc__
        # Clean up
        df_X = df_X.drop(columns=['circumference', 'area'])
        dfext = df_ext(df_X)

        # Check latest version of a particular branch is downloaded and executes correctly
        assert hasattr(dfext, 'test1') == False
        # two repos installing into the default
        spec = __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection@pdext_test', 
                            'demo.circle_calculations')
        pdext.import_extension(spec)

        assert hasattr(dfext, 'demo') == True
        # Test execution of the extension
        assert 'circumference' not in df_X.columns
        assert 'area' not in df_X.columns
        dfext.demo.circle_calculations('numbers')
        assert 'circumference' in df_X.columns
        assert 'area' in df_X.columns
        # Test correct version of the docstring
        assert 'Calculates the circumference' not in dfext.demo.circle_calculations.__doc__
        assert 'Version: test branch' in dfext.demo.circle_calculations.__doc__
        # Clean up
        df_X = df_X.drop(columns=['circumference', 'area'])
        dfext = df_ext(df_X)

        # Check a particular tag is downloaded and executes correctly
        assert hasattr(dfext, 'test2') == False
        # two repos installing into the default
        spec = __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection@pdext_test_tag', 
                            'test2.circle_calculations')
        pdext.import_extension(spec)
        
        assert hasattr(dfext, 'test2') == True
        # Test execution of the extension
        assert 'circumference' not in df_X.columns
        assert 'area' not in df_X.columns
        dfext.test2.circle_calculations('numbers')
        assert 'circumference' in df_X.columns
        assert 'area' in df_X.columns
        # Test correct version of the docstring
        assert 'Calculates the circumference' not in dfext.test2.circle_calculations.__doc__
        assert 'Version: pdext_test_tag tag' in dfext.test2.circle_calculations.__doc__
        # Clean up
        df_X = df_X.drop(columns=['circumference', 'area'])
        dfext = df_ext(df_X)
        # should be three log records, one for each download
        assert len(caplog.records)==3

@pytest.mark.skip_this
def test_multi_install_from_github(temp_module_directory, df_X, caplog):
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        make_test_repos(pdext, temp_module_directory)

        # capture the log record when a github archive is downloaded
        caplog.set_level(logging.INFO)
        assert hasattr(dfext, 'multi') == False
        # install three functions from one repo (which should only be
        # downloaded once)
        spec = __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection@pdext_test', 
                            'multi.circle_calculations') + '\n'
        spec += __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection@pdext_test', 
                            'multi.circle_calculations2') + '\n'
        spec += __import_file_line_spec__\
                    .format('github:connectedblue/pdext_collection@pdext_test', 
                            'multi.circle_calculations3') + '\n'
        pdext.import_extension(spec)
        assert hasattr(dfext, 'multi') == True

        # Test execution of the extension
        assert 'circumference' not in df_X
        assert 'area' not in df_X
        assert 'circumference2' not in df_X
        assert 'area2' not in df_X
        assert 'circumference3' not in df_X
        assert 'area3' not in df_X
        dfext.multi.circle_calculations('numbers')
        dfext.multi.circle_calculations2('numbers')
        dfext.multi.circle_calculations3('numbers')
        assert 'circumference' in df_X
        assert 'area'  in df_X
        assert 'circumference2' in df_X
        assert 'area2' in df_X
        assert 'circumference3' in df_X
        assert 'area3' in df_X

        # Clean up
        df_X = df_X.drop(columns=['circumference', 'area', 
                                  'circumference2', 'area2',
                                  'circumference3', 'area3',])
        dfext = df_ext(df_X)

        # The github archive should only have been downloaded once
        assert len(caplog.records)==1