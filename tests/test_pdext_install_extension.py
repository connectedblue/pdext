import pytest

from pdext.symbols import pd_ext, df_ext
from fixtures.helpers import save_current_installed_extensions, make_test_repos


def test_pdext_install_and_remove_extension(temp_module_directory, df_X,
                                   testpackage1, testpackage2, testpackage3):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        test_repos = make_test_repos(pdext, temp_module_directory)

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False
        # two repos installing into the default
        pdext.install_extension('calculate_circumference_from_radius', testpackage1, repository_name='test1')
        pdext.install_extension('calculate_circumference_from_diameter', testpackage1, repository_name='test1')
    
        assert hasattr(dfext, 'calculate_circumference_from_radius') == True
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True

        # can't remove default repo
        with pytest.raises(ValueError):
            pdext.remove_repository('test1')
        
        # change default and remove
        pdext.set_default_repository('test2')
        pdext.remove_repository('test1')

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False

        # should install in test2 by which is now the default
        pdext.install_extension('calculate_circumference_from_radius', testpackage2)
        pdext.install_extension('calculate_circumference_from_diameter', testpackage2)
        assert hasattr(dfext, 'calculate_circumference_from_radius') == True
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True

        # add test1 back and make it default
        pdext.add_repository('test1', test_repos['test1'],
                              beginning=True, default=True)

        # Test execution of the radius extension based on search order
        def execute_radius_extension(col, df):
            dfext = df_ext(df)
            assert col not in df
            dfext.calculate_circumference_from_radius('numbers')
            assert col in df
            df = df.drop(columns=col)
            return df
        
        df_X = execute_radius_extension('circumference1_from_radius', df_X)
        pdext.new_search_order(['test2', 'test1'])
        df_X = execute_radius_extension('circumference2_from_radius', df_X)