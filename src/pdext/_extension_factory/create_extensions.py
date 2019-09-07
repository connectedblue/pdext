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
       
    def __getattr__(self, func):
        if pd.ext.is_extension(func):
            func = pd.ext.get_extension_function(func)
            if hasattr(func, '__call__'):
                @wraps(func)
                def newfunc(*args, **kwargs):
                    result = func(self._obj, *args, **kwargs)
                    return result
                self._update_func_doc(newfunc)
                return newfunc
        else:
            return self.__getattribute__(func)
    
    @staticmethod
    def _update_func_doc(func):
        func_name = func.__name__
        sig = inspect.signature(func)
        doc = func.__doc__
        params = list(sig.parameters)
        first_arg = params[0]
        other_args = ', '.join(params[1:])
        args = first_arg + other_args
        doc += '\nUSAGE: {first_arg}.ext.{func_name}({other_args})'\
                .format(first_arg=first_arg,
                        func_name=func_name,
                        other_args=other_args)
        func.__doc__ = doc

def load_extensions(namespace):
    # Compose a class from the template and mix-ins defined
    # in the namespace folder
    # give the class the name namespace
    cls = type(namespace, (ExtensionClassTemplate,*get_extensions(namespace),), {})
    
    # register the composed class with the pandas plugin framework
    registered_class = pd.api.extensions.register_dataframe_accessor(namespace)(cls)
    return(registered_class)
    