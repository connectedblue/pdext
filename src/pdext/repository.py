import os, yaml, shutil, glob, sys

from .symbols import __installed_extensions__, __default_collection__
from .extension import Extension

class extension_repository(object):
    """
    Manages the directory locations on the local filesystem where installed
    extensions can be found.  

    New repository locations can be added by the user.  The information is
    stored in a yaml file inside the package.

    Extensions can then be installed into the correct location
    so they can be found by the pandas extnesion class.  Any 
    namespace clashes are resolved using the repository search order
    managed in this class. 
    """

    def __init__(self):
        self.build_extension_collections()

    def install_extension(self, name, extension_files,
                          collection=__default_collection__,
                          repository_name=None):
        """
        Adds extensions into the repository
        Input:
            name -- string name of extension 
            extension_files -- directory containing all the files needed
                               for that extension.  There must be a function
                               with the extension name in one of the .py
                               files in that directory
            collection -- the collection namespace to be used 
            repository_name -- the repository to install the extension into
                               If none specified, then the default is used
        """
        if repository_name is None:
            repository_name = self.default_repository
        extension_location = os.path.join(self.repository_path(repository_name),
                                          collection, name)
        Extension(extension_location).install(os.path.expanduser(extension_files))
        self.build_extension_collections()
    
    def build_extension_collections(self):
        """
        Create a nested dictionary of function objects of the form
            self.extensions[collection_name][extension_name]=func
        where func is the actual extension function
        """
        self.read_config_file()
        # Get all collection names from all the repositories
        # and initialise
        ext = {}
        for path in self.search_path:
            for collection in next(os.walk(path))[1]:
                ext[collection] = {}
        
        # find the first occurence of each extension on the
        # search path of each collection
        for collection in ext:
            for path in self.search_path:
                extensions = os.path.join(path, collection)
                try:
                    for extension in next(os.walk(extensions))[1]:
                        if extension not in ext[collection]:
                            extension_location = os.path.join(extensions,
                                                              extension)
                            ext[collection][extension] = \
                                Extension(extension_location)
                except StopIteration:
                    # If there are no extensions in the collection,
                    # carry on
                    continue
        self.extension_collections = ext  

    def get_extension(self, name):
        collection, name=self.parse_extension_name(name)
        ext = self.extension_collections[collection][name]
        return ext.get_extension()

    def parse_extension_name(self, name):
        name = name.split('.')
        num_levels = len(name)
        if num_levels>2:
            raise IndexError("Extensions can't be nested {} levels"\
                                .format(num_levels))
        if num_levels==2:
            collection = name[0]
            extension_name = name[1]
        else:
            collection = __default_collection__
            extension_name = name[0]
        return collection, extension_name
    
    def read_config_file(self):
        """
        Read in YAML config file and set up internal
        configuration for the class

        Example structure of YAML file:

            repositories:
            - name: user
            location: ~/.pdext
            - name: shared
            location: /opt/data/.pdext
            default_repository: user

        which parses into the following python object:
            {'repositories': 
                [{'name': 'user', 
                  'location': '~/.pdext'}, 
                 {'name': 'shared', 
                  'location': '/opt/data/.pdext'}], 
             'default_repository': 'user'}
        """
        try:
            no_config_file = False
            with open(__installed_extensions__, 'r') as stream:
                config = yaml.safe_load(stream)        

        except FileNotFoundError:
            # create a default configuration
            config =  {'repositories': 
                        [{'name': 'user', 
                          'location': '~/.pdext'}], 
                       'default_repository': 'user'} 
            no_config_file = True

        self.repositories = config['repositories']
        self.default_repository = config['default_repository']

        # ensure that all the locations exist and create if not
        for directory in self.search_path:
            self.create_directory(directory)
        if no_config_file:
            self.write_config_file()

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def write_config_file(self):
        config = {'repositories': self.repositories,
                  'default_repository': self.default_repository}
        with open(__installed_extensions__, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)
        self.build_extension_collections()
    
    def add_location(self, name, location, beginning = True,
                     default=False):
        """
        Add in a new repository into the saved config
        Input:
            name -- string name of new repository
            location -- path name of new repository
            beginning -- if True, this new location is set to be
                         at the start of the search order
            default -- If True, then this is set to the default
                       repository
        """
        current_search_order = self.search_order
        self.repositories.append({
            'name': name, 
            'location': location
        })
        if beginning:
            new_order = [name] + current_search_order
        else:
            new_order = current_search_order + [name]
        if default:
            self.default_repository = name
        self.new_search_order(new_order)

    def remove_location(self, name):
        """
        Remove a new repository from the saved config
        Input:
            name -- string name of repository to remove
        """
        if name not in self.repositories_by_name:
            raise KeyError('No repository with name {}'.format(name))
        if self.default_repository==name:
            raise ValueError('Not allowed to remove default repository {}'\
                                .format(name))
        self.repositories = [r for r in self.repositories \
                                    if r['name']!=name]
        self.write_config_file()

    @property
    def search_path(self):
        return [self.repository_path(name) \
                    for name in self.search_order]

    @property
    def search_order(self):
        return self._repository_elements('name')
    
    def _repository_elements(self,by):
        return [c[by] for c in self.repositories]

    def new_search_order(self, new_order):
        """
        Specify the order by name
        Input:
            new_order -- list of string names in the desired
                         search order
        """
        if set(new_order) != set(self.search_order):
            raise ValueError('Values of {} not in repository'.format(new_order))
        # iterate through the existing order and create new order
        existing = self.repositories_by_name
        self.repositories = [existing[n] for n in new_order]
        self.write_config_file()

    @property
    def repositories_by_name(self):
        return {n['name']:n for n in self.repositories}

    def repository_path(self, name):
        """
        Returns the path for a particular name
        """
        return os.path.expanduser(self.repositories_by_name[name]['location'])

    @property
    def default_path(self):
        return self.repository_path(self.default_repository)
    

    # Ensure that the default repository exists
    @property
    def default_repository(self):
        return self._default_repository

    @default_repository.setter
    def default_repository(self, value):
        if value not in self.search_order:
            raise KeyError('{} is not a repository name'.format(value))
        self._default_repository = value
        

    def set_default_repository(self, value):
        self.default_repository = value    
        self.write_config_file()

