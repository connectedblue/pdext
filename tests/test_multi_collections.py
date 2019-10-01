
def test_default_no_collection(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    # test1 is the default repository
    pd_ext.new_search_order(['test1', 'test2'])

    assert 'circumference1_from_radius' not in df_X
    # get the extension to test
    ext = df_ext(df_X)
    radius = ext.calculate_circumference_from_radius('numbers')
    diameter = ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X
    assert 'circumference1_from_diameter' in df_X

    # switch default
    pd_ext.new_search_order(['test2', 'test1'])

    radius = ext.calculate_circumference_from_radius('numbers')
    diameter = ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference2_from_radius' in df_X
    assert 'circumference2_from_diameter' in df_X

def test_collection(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    # test1 is the default repository
    pd_ext.new_search_order(['test1', 'test2'])

    assert 'circumference1_from_radius' not in df_X
    # get the extension to test
    ext = df_ext(df_X)

    # Call the collection specific extensions
    radius = ext.circle2.calculate_circumference_from_radius('numbers')
    diameter = ext.circle2.calculate_circumference_from_diameter('numbers')
    assert 'circumference2_from_radius' in df_X
    assert 'circumference2_from_diameter' in df_X

    assert 'circumference1_from_radius' not in df_X
    assert 'circumference1_from_diameter' not in df_X

def test_collection_across_repos(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    # test1 is the default repository
    pd_ext.new_search_order(['test1', 'test2'])

    # get the extension to test
    ext = df_ext(df_X)

    # Call the collection specific extensions
    radius = ext.circle3.calculate_circumference_from_radius('numbers')
    diameter = ext.circle3.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X
    assert 'circumference1_from_diameter' in df_X

    assert 'circumference2_from_radius' not in df_X
    assert 'circumference2_from_diameter' not in df_X


def test_collection_across_repos_extension_clash(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    # test1 is the default repository
    pd_ext.new_search_order(['test1', 'test2'])

    # get the extension to test
    ext = df_ext(df_X)

    # Call the collection specific extensions
    radius = ext.circle4.calculate_circumference_from_radius('numbers')
    diameter = ext.circle4.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X
    assert 'circumference1_from_diameter' in df_X

    assert 'circumference2_from_radius' not in df_X
    assert 'circumference2_from_diameter' not in df_X

    # switch around
    pd_ext.new_search_order(['test2', 'test1'])
    radius = ext.circle4.calculate_circumference_from_radius('numbers')
    diameter = ext.circle4.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X
    assert 'circumference1_from_diameter' in df_X

    assert 'circumference2_from_radius' in df_X
    assert 'circumference2_from_diameter' not in df_X


def test_remove_repo(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    
    pd_ext.new_search_order(['test2', 'test1'])    
    # remove test2 all together
    pd_ext.remove_location('test2')

    # get the extension to test
    ext = df_ext(df_X)
    radius = ext.calculate_circumference_from_radius('numbers')
    diameter = ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference2_from_radius' not in df_X
    assert 'circumference2_from_diameter' not in df_X