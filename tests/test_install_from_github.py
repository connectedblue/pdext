import pytest

from pdext.symbols import pd_ext, df_ext
from fixtures.helpers import save_current_installed_extensions, make_test_repos

@pytest.mark.skip_this
def test_install_from_github(temp_module_directory, df_X):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        test_repos = make_test_repos(pdext, temp_module_directory)

        # Check default latest version is downloaded and executes correctly
        assert hasattr(dfext, 'circle_calculations') == False
        # two repos installing into the default
        pdext.install_extension('circle_calculations', 'github:connectedblue/pdext_collection')
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
        pdext.install_extension('circle_calculations', 
                                'github:connectedblue/pdext_collection@pdext_test',
                                collection='demo')
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
        pdext.install_extension('circle_calculations', 
                                'github:connectedblue/pdext_collection@pdext_test_tag',
                                collection='test2')
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