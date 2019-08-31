# All extensions are defined in mixin classes contained in files in
# a subdirectory of this registration module

# Name of sub directory is the accessor name and each file should
# begin with the accessor plus _
# The convention is that the mixin class name is the same as the file name
# The extensions() function will then load all the extensions dynamically
# for each accessor

import pandas as pd

def get_extensions(accessor):
    import importlib, os
    this_dir, this_file = os.path.split(__file__)
    # get a list of extension files - they are located
    # as subdirectories above this directory
    this_dir = os.path.join(this_dir, '..', accessor)
    ext = [os.path.splitext(f)[0]\
                        for f in os.listdir(this_dir) \
                            if f.startswith(accessor) ]
    # from_here is the package name that this file is in and the
    # extension classes should be at the level above
    from_here = '.'.join(__name__.split('.')[:-2]) 
    # import each class from the module of the same name
    ext = [getattr(importlib.import_module('.{}.{}'.format(accessor,e), from_here), e) \
                     for e in ext]
    return ext

# All extensions will have this template
class ExtensionClassTemplate(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        # This method is defined in the accessor sub folder
        self._initialise()

def load_extensions(namespace):
    # Compose a class from the template and mix-ins defined
    # in the namespace folder
    # give the class the name namespace
    cls = type(namespace, (ExtensionClassTemplate,*get_extensions(namespace),), {})
    
    # register the composed class with the pandas plugin framework
    registered_class = pd.api.extensions.register_dataframe_accessor(namespace)(cls)
    return(registered_class)
    