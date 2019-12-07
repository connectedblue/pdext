from .extension_properties import extension_properties_mixin
from .extension_management import extension_management_mixin
from .config_file_management import config_file_management_mixin
from .user_repository_methods import user_repository_methods_mixin
from .user_extension_control_methods import user_extension_control_methods_mixin
from .user_extension_install_methods import user_extension_install_methods_mixin

from ..symbols import __pdext__, __pd_ext__, __import_file_ext__
from ..extensions import ExtensionImporter

class ExtensionRepository(user_repository_methods_mixin,
                          user_extension_install_methods_mixin,
                          user_extension_control_methods_mixin,
                          extension_management_mixin,
                          config_file_management_mixin,
                          extension_properties_mixin):
    """
    This class allows the user to install and manage extensions that
    are be accessible from data frames. 

    Assuming that |``pandex``| is imported as ``pd``, then the
    methods in this class are accessed from the namespace:

    .. parsed-literal::

        |pd.ext|.<method_name>
    
    where ``<method_name>`` is one of:

    """

    def __init__(self):
        self._build_extension_collections()

    @property
    def __version__(self):
        from ..symbols import __version__
        return __version__


# Attach some meta data to the class that allows
# documentation to be auto generated (not needed for actual operation)
setattr(ExtensionRepository, 'ExtensionRepository', ExtensionRepository)
setattr(ExtensionRepository, 'ExtensionImporter', ExtensionImporter)

# Attach some doc string constants to the class
# These are accessed in the conf.py of the docs directory
class doc:
    __pdext__ = __pdext__
    __pd_ext__ = __pd_ext__
    __import_file_ext__ = __import_file_ext__

setattr(ExtensionRepository, 'doc', doc)

