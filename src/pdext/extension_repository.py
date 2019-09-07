

class extension_repository(object):
    """
    The Repository where all extension functions are stored
    """

    def __init__(self):
        self.clear()
    
    def add_extension(self, func):
        self._registered_functions[func.__name__] = func

    def is_extension(self, ext):
        return ext in self._registered_functions
    
    def get_extension_function(self, func):
        return self._registered_functions[func]

    def clear(self):
        self._registered_functions = {}