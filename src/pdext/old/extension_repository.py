import inspect, os, glob, sys

from importlib import import_module

from .symbols import __installed_extensions__

class extension_repository(object):
    """
    The Repository where all extension functions are stored
    """

    def __init__(self):
        self.clear()
        self.load_extensions()

    def install_extension(external_obj, *extension_names):
        """
        Installs an extension from an external object into
        the internal package configuration
        Input:
            external_obj -- can be a function object, python file, system
                            directory, local package, installed package
            extension_names -- list of string names of the extensions which
                               are inside the object
                               (Note: not present is external_obj is a
                                function object)
        Output:
            None -- this package repository is updated with details
        """
        
    
    def add_extension(self, func, save=True):
        self._registered_functions[func.__name__] = func
        if save:
            self.save_extension(func)

    def is_extension(self, ext):
        return ext in self._registered_functions
    
    def get_extension_function(self, func):
        return self._registered_functions[func]

    def clear(self):
        self._registered_functions = {}

    def save_extension(self, func):
        src = inspect.getsource(func)
        with open(self._extension_file_name(func), 'w') as extfile:
            extfile.write(src)

    def load_extensions(self):
        if __installed_extensions__ not in sys.path:
            sys.path.append(__installed_extensions__)
        extensions = [os.path.splitext(os.path.basename(f))[0] \
                        for f in glob.glob(__installed_extensions__+'/*.py')]
        for ext in extensions:
            module = import_module(ext)
            self.add_extension(getattr(module, ext), save=False)



        return extensions
        


    @staticmethod
    def _extension_file_name(ext):
        if callable(ext): ext = ext.__name__
        filename = ext + '.py'
        filepath = os.path.join(__installed_extensions__, filename)

        return filepath
