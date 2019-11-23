from datetime import datetime
import pytest

from pdext.symbols import pd_ext, df_ext, __install_timestamp_fmt__,\
                          __default_collection__, __import_file_line_spec__
from fixtures.helpers import save_current_installed_extensions, make_test_repos


def test_pdext_install_and_remove_extension(temp_module_directory, df_X,
                                   testpackage1, testpackage2, testpackage3):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        time_at_start = datetime.now().strftime(__install_timestamp_fmt__)
        test_repos = make_test_repos(pdext, temp_module_directory)

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False
        # two repos installing into the default
        def spec(func):
            return __import_file_line_spec__.format(testpackage1, func)
        pdext.import_extension(spec('calculate_circumference_from_radius'))
        pdext.import_extension(spec('calculate_circumference_from_diameter'))
        
        assert hasattr(dfext, 'calculate_circumference_from_radius') == True
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True

        # Check recorded install times are correct
        assert pdext.extension_collections[__default_collection__]\
                                          ['calculate_circumference_from_radius']\
                            .ext_info.is_earlier_than(time_at_start) == False

        # can't remove default repo
        with pytest.raises(ValueError):
            pdext.remove_repository('test1')
        
        # change default and remove
        pdext.set_default_repository('test2')
        pdext.remove_repository('test1')

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False

        # should install in test2 by which is now the default
        pdext.import_extension(__import_file_line_spec__.format(testpackage2, 'calculate_circumference_from_radius'))
        pdext.import_extension(__import_file_line_spec__.format(testpackage2, 'calculate_circumference_from_diameter'))
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

def test_multi_extension_install(temp_function_directory, df_X,testpackage1):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        test_repos = make_test_repos(pdext, temp_function_directory)

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False
        # two repos installing into the default
        spec = __import_file_line_spec__.format(testpackage1, 
                                    'calculate_circumference_from_radius') +\
                '\n' +\
               __import_file_line_spec__.format(testpackage1, 
                                    'calculate_circumference_from_diameter')
        pdext.import_extension(spec)
    
        assert hasattr(dfext, 'calculate_circumference_from_radius') == True
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True

        # Test execution of the radius extension
        dfext.calculate_circumference_from_radius('numbers')
        assert 'circumference1_from_radius' in df_X.columns
        dfext.calculate_circumference_from_diameter('numbers')
        assert 'circumference1_from_diameter' in df_X.columns

def test_nested_extension_install(temp_function_directory, df_X,testpackage1):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        test_repos = make_test_repos(pdext, temp_function_directory)

        assert hasattr(dfext, 'calculate_circumference_from_radius_nested') == False
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False
        # two extensions installing into the default
        spec = __import_file_line_spec__.format(testpackage1, 
                                    'calculate_circumference_from_radius_nested') +\
                '\n' +\
               __import_file_line_spec__.format(testpackage1, 
                                    'calculate_circumference_from_diameter')
        pdext.import_extension(spec)

        assert hasattr(dfext, 'calculate_circumference_from_radius_nested') == True
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True
        
        # Test execution of the nested radius extension
        dfext.calculate_circumference_from_radius_nested('numbers')
        assert 'circumference1_from_radius_nested' in df_X.columns
