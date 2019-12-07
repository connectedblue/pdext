import sys

from pandex.symbols import df_ext, __df_ext__, __import_file_line_spec__


"""
This set of tests ensures that the import_extension
methods work as a unit test on the ExtensionRepository class

To ensure that extensions can be installed correctly
through the pd.ext user interface, the tests in
test_pdext_install_extension will be run

"""



def test_install(two_test_session_repos, testpackage1):
    repo = two_test_session_repos
    sys_path = sys.path

    def spec(func):
            return __import_file_line_spec__.format(testpackage1, func)
    repo.import_extension(spec('calculate_circumference_from_radius'))
    repo.import_extension(spec('calculate_circumference_from_diameter'))

    # check that the path hasn't been screwed around with
    assert sys.path == sys_path

# First check that the installed functions work correctly as functions
def test_package1func1(two_test_session_repos, df_A):
    repo = two_test_session_repos
    f = repo._get_extension_from_collection('calculate_circumference_from_radius')
    assert 'circumference1_from_radius' not in df_A
    f(df_A, 'numbers')
    assert 'circumference1_from_radius' in df_A

def test_package1func2(two_test_session_repos, df_A):
    repo = two_test_session_repos
    f = repo._get_extension_from_collection('calculate_circumference_from_diameter')
    assert 'circumference1_from_diameter' not in df_A
    f(df_A, 'numbers')
    assert 'circumference1_from_diameter' in df_A

# Now test that they work when called as extensions
def test_dfext_package1func1(df_X):
    assert 'circumference1_from_radius' not in df_X
    # get the extension to test
    ext = df_ext(df_X).calculate_circumference_from_radius
    # and execute it
    ext('numbers')
    assert 'circumference1_from_radius' in df_X
    # Has the docstring pulled through correctly?
    usage = 'USAGE: df.{}.calculate_circumference_from_radius(radius)'.format(__df_ext__) 
    assert usage in ext.__doc__