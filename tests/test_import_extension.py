import os, importlib
import pytest

from pdext.symbols import pd_ext, df_ext, __import_file_ext__, __import_file_sep__, __pdext__
from fixtures.helpers import save_current_installed_extensions, make_test_repos

def test_import_extension(temp_module_directory, df_X,testpackage1):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        test_repos = make_test_repos(pdext, temp_module_directory)

        assert hasattr(dfext, 'calculate_circumference_from_radius') == False
        assert hasattr(dfext, 'test') == False
        # two repos installing into the default
        pdext.import_extension(testpackage1+__import_file_sep__+'calculate_circumference_from_radius')
        pdext.import_extension(testpackage1+__import_file_sep__+'test.calculate_circumference_from_diameter')
    
        assert hasattr(dfext, 'calculate_circumference_from_radius') == True
        assert hasattr(dfext, 'test') == True

        assert 'circumference1_from_radius' not in df_X.columns
        assert 'circumference1_from_diameter' not in df_X.columns
        # get the extension to test
        ext = df_ext(df_X)
        ext.calculate_circumference_from_radius('numbers')
        ext.test.calculate_circumference_from_diameter('numbers')
        assert 'circumference1_from_radius' in df_X.columns
        assert 'circumference1_from_diameter' in df_X.columns
        df_X = df_X.drop(columns=['circumference1_from_radius', 'circumference1_from_diameter'])
        ext = df_ext(df_X)

        # Create an import file is the current directory
        import_file_content = """\
# Comment to be ignored
            {package} {sep}  imp.calculate_circumference_from_radius
            {package} {sep}  calculate_circumference_from_diameter
            """.format(package=testpackage1, sep=__import_file_sep__)
        import_file_name = 'import_test' + __import_file_ext__
        with open(import_file_name, 'w') as f:
            f.writelines(import_file_content)
        
        assert hasattr(dfext, 'calculate_circumference_from_diameter') == False
        assert hasattr(dfext, 'imp') == False
        
        # import the packages in the file
        import_test = importlib.import_module('import_test')
        
        # Dummy module loaded in the namespace
        assert 'import_test' in locals()
        assert import_test.__file__ == '<{} import>'.format(__pdext__)

        # clean up before completing tests
        os.remove(import_file_name)

        assert hasattr(dfext, 'calculate_circumference_from_diameter') == True
        assert hasattr(dfext, 'imp') == True

        assert 'circumference1_from_radius' not in df_X.columns
        assert 'circumference1_from_diameter' not in df_X.columns
        # get the extension to test
        ext = df_ext(df_X)
        ext.imp.calculate_circumference_from_radius('numbers')
        ext.calculate_circumference_from_diameter('numbers')
        assert 'circumference1_from_radius' in df_X.columns
        assert 'circumference1_from_diameter' in df_X.columns
        df_X = df_X.drop(columns=['circumference1_from_radius', 'circumference1_from_diameter'])
        ext = df_ext(df_X)
        

def test_extension_dependency_not_installed(temp_module_directory, df_X, 
                                            testpackage1, caplog, capsys):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        dfext = df_ext(df_X)
        make_test_repos(pdext, temp_module_directory)

        assert hasattr(dfext, 'function_uses_external_package_not_installed') == False
        assert len(caplog.records)==0
        # installing into the default - check for warning during install
        pdext.import_extension(testpackage1+__import_file_sep__+'function_uses_external_package_not_installed')
        # function exists but it is a dummy one
        assert hasattr(dfext, 'function_uses_external_package_not_installed') == True
        assert 'EXTENSION CANNOT BE LOADED' in dfext.function_uses_external_package_not_installed.__doc__

        assert len(caplog.records)==1
        record = caplog.records[0]
        assert record.levelname == 'WARNING'
        assert 'extension function_uses_external_package_not_installed requires library pkg_doesnt_exist which is not installed'\
               in record.message

        # catch warning when the function is executed also
        dfext.function_uses_external_package_not_installed()
        assert len(caplog.records)==2
        record = caplog.records[1]
        assert record.levelname == 'WARNING'
        assert record.message == '{} extension function_uses_external_package_not_installed requires library pkg_doesnt_exist which is not installed'\
                                    .format(__pdext__)

        # Check that warning also included in the show_extensions() list
        pdext.show_extensions()
        out, _ = capsys.readouterr()
        function_warning = "function_uses_external_package_not_installed()  - Currently doesn't work because module:  pkg_doesnt_exist  needs to be installed"
        assert function_warning in out
