from pdext.symbols import pd_ext, df_ext, __import_file_line_spec__, __df_ext__
from fixtures.helpers import save_current_installed_extensions, make_test_repos


def test_show_extension(temp_module_directory, testpackage1, capsys):
    # Create a test repo for the whole duration of tests
    with save_current_installed_extensions():
        # make two test repos to install extensions into
        pdext = pd_ext()
        make_test_repos(pdext, temp_module_directory)

        pdext.show_extensions()
        out, _ = capsys.readouterr()
        assert 'No extensions are installed' in out
        assert 'For help on individual extensions, use help(df.ext.<extension name>)' not in out
        def spec(func):
            return __import_file_line_spec__.format(testpackage1, func)
        pdext.import_extension(spec('calculate_circumference_from_radius'))
        pdext.show_extensions()
        out, _ = capsys.readouterr()
        assert 'There is 1 extension installed' in out
        assert 'df.{}.calculate_circumference_from_radius(radius)'\
                .format(__df_ext__) in out
        assert 'For help on individual extensions, use help(df.{}.<extension name>)'\
                .format(__df_ext__) in out
        
        pdext.import_extension(spec('calculate_circumference_from_diameter'))
        pdext.show_extensions()
        out, _ = capsys.readouterr()
        assert 'There are 2 extensions installed' in out
        assert 'df.{}.calculate_circumference_from_radius(radius)'\
                .format(__df_ext__) in out
        assert 'df.{}.calculate_circumference_from_diameter(diameter)'\
                .format(__df_ext__) in out
        assert 'For help on individual extensions, use help(df.{}.<extension name>)'\
                .format(__df_ext__) in out
        
        pdext.import_extension(spec('test.calculate_circumference_from_radius'))
        pdext.show_extensions()
        out, _ = capsys.readouterr()
        assert 'There are 3 extensions installed' in out
        assert 'df.{}.calculate_circumference_from_radius(radius)'\
                .format(__df_ext__) in out
        assert 'df.{}.calculate_circumference_from_diameter(diameter)'\
                .format(__df_ext__) in out
        assert 'Collection: test' in out
        assert 'df.{}.test.calculate_circumference_from_radius(radius)'\
                .format(__df_ext__) in out
        assert 'For help on individual extensions, use help(df.{}.<extension name>)'\
                .format(__df_ext__) in out