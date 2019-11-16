
import pytest
from pdext.symbols import __df_ext__, __install_timestamp_fmt__, __default_collection__

def test_enable_disable_extension(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    # We only want the test1 is repository for these tests
    pd_ext.remove_repository('test2')

    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' not in df_X.columns
    # get the extension to test
    ext = df_ext(df_X)
    ext.calculate_circumference_from_radius('numbers')
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns=['circumference1_from_radius', 'circumference1_from_diameter'])
    ext = df_ext(df_X)

    # disable radius
    pd_ext.disable_extension('calculate_circumference_from_radius')
    ext.calculate_circumference_from_radius('numbers')
    # other extensions in the collection should still be active
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_diameter')
    ext = df_ext(df_X)

    # rebuild and still should be disabled
    pd_ext._build_extension_collections()
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' not in df_X.columns
    # repeat last tests to check
    ext.calculate_circumference_from_radius('numbers')
    # other extensions in the collection should still be active
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_diameter')
    ext = df_ext(df_X)

    # cannot disable an extension that doesn't exist
    with pytest.raises(KeyError):
        pd_ext.disable_extension('XXX')

    # check extensions in collections are disabled correctly
    pd_ext.disable_extension('circle1.calculate_circumference_from_diameter')

    ext.circle1.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_diameter' not in df_X.columns
    # radius extension in circle1 should still be there 
    ext.circle1.calculate_circumference_from_radius('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_radius')
    ext = df_ext(df_X)

    # re-active for next tests
    pd_ext.enable_extension('circle1.calculate_circumference_from_diameter')
    pd_ext.enable_extension('calculate_circumference_from_radius')

def test_reinstall_extension(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages

    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' not in df_X.columns
    # get the extension to test
    ext = df_ext(df_X)
    ext.calculate_circumference_from_radius('numbers')
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns=['circumference1_from_radius', 'circumference1_from_diameter'])
    ext = df_ext(df_X)

    # time of install 
    ext_object = pd_ext.extension_collections[__default_collection__]\
                                             ['calculate_circumference_from_radius']
    first_install_time = ext_object.ext_info.install_time

    # reinstall radius
    pd_ext.reinstall_extension('calculate_circumference_from_radius')

    ext.calculate_circumference_from_radius('numbers')
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_diameter')
    ext = df_ext(df_X)

    assert ext_object.ext_info.is_earlier_than(first_install_time) == False


def test_remove_extension(pdext_with_loaded_testpackages,df_X):
    pd_ext, df_ext = pdext_with_loaded_testpackages
    
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' not in df_X.columns
    # get the extension to test
    ext = df_ext(df_X)
    ext.calculate_circumference_from_radius('numbers')
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns=['circumference1_from_radius', 'circumference1_from_diameter'])
    ext = df_ext(df_X)

    # remove radius
    pd_ext.remove_extension('calculate_circumference_from_radius')
    with pytest.raises(AttributeError):
        ext.calculate_circumference_from_radius('numbers')
    # other extensions in the collection should be there
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_diameter')
    ext = df_ext(df_X)

    # rebuild and still should not be there
    pd_ext._build_extension_collections()
    # repeat last tests to check
    with pytest.raises(AttributeError):
        ext.calculate_circumference_from_radius('numbers')
    # other extensions in the collection should be there
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_radius' not in df_X.columns
    assert 'circumference1_from_diameter' in df_X.columns
    df_X = df_X.drop(columns='circumference1_from_diameter')
    ext = df_ext(df_X)

    # cannot remove an extension that doesn't exist
    with pytest.raises(KeyError):
        pd_ext.remove_extension('XXX')

    # check extensions in collections are removed correctly
    pd_ext.remove_extension('circle1.calculate_circumference_from_diameter')

    with pytest.raises(AttributeError):
        ext.circle1.calculate_circumference_from_diameter('numbers')
    # same extensions in the default collection should still be there
    ext.calculate_circumference_from_diameter('numbers')
    assert 'circumference1_from_diameter' in df_X.columns
    # radius extension in circle1 should still be there 
    ext.circle1.calculate_circumference_from_radius('numbers')
    assert 'circumference1_from_radius' in df_X.columns
    df_X = df_X.drop(columns=['circumference1_from_radius','circumference1_from_diameter'])
    ext = df_ext(df_X)

    # rebuild and still should not be there
    pd_ext._build_extension_collections()
    # repeat last tests to check
    with pytest.raises(AttributeError):
        ext.circle1.calculate_circumference_from_diameter('numbers')
    
    