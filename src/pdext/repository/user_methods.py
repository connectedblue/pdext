import os

from ..symbols import __default_collection__
from ..extension import Extension
from .staged_install_files import staged_install_files


class user_methods(object):
    """
    All the methods which a user can call to manipulate 
    extensions.

    Specify the directory locations on the local filesystem where installed
    extensions can be found.  

    New repository locations can be added by the user.  The information is
    stored in a yaml file inside the package.

    Extensions can then be installed into the correct location
    so they can be found by the pandas extension class.  Any 
    namespace clashes are resolved using the repository search order
    which can also be specified by the user.
    """
    def install_extension(self, name, extension_location,
                          collection=__default_collection__,
                          repository_name=None):
        """
        Adds extensions into the repository
        Input:
            name -- string name of extension, or a list of extension names
            extension_location -- location of all the files needed
                               for that extension.  There must be a function
                               with the extension name in one of the .py
                               files at that location
                Format options for extension files:
                    <directory name on local file system>
                    <.py file  name on local file system>
                    github:username/repo[@branch/tag][/path/to/directory]
                            where repo is a public repo on github for username
                            latest commit on master is the default unless a
                            specific branch or tag is optionally provided
                            The extension files are assumed to be at the root
                            of the repo unless a path is optionally provided
                            
            collection -- the collection namespace to be used 
            repository_name -- the repository to install the extension into
                               If none specified, then the default is used
        """
        if type(name)==str:
            name = [name]
        if repository_name is None:
            repository_name = self.default_repository
        with staged_install_files(extension_location) as install_dir:
            for ext in name:
                extension_location = os.path.join(self._repository_path(repository_name),
                                                  collection, ext)
                Extension(extension_location).install(install_dir)
        self._build_extension_collections()

    
    def add_repository(self, name, location, beginning = True,
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
        current_search_order = self._search_order
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

    def remove_repository(self, name):
        """
        Remove a new repository from the saved config
        Input:
            name -- string name of repository to remove
        """
        if name not in self._repositories_by_name:
            raise KeyError('No repository with name {}'.format(name))
        if self.default_repository==name:
            raise ValueError('Not allowed to remove default repository {}'\
                                .format(name))
        self.repositories = [r for r in self.repositories \
                                    if r['name']!=name]
        self._write_config_file()

    def new_search_order(self, new_order):
        """
        Specify the order by name
        Input:
            new_order -- list of string names in the desired
                         search order
        """
        if set(new_order) != set(self._search_order):
            raise ValueError('Values of {} not in repository'.format(new_order))
        # iterate through the existing order and create new order
        existing = self._repositories_by_name
        self.repositories = [existing[n] for n in new_order]
        self._write_config_file()

    def set_default_repository(self, value):
        self.default_repository = value    
        self._write_config_file()

    def show_extensions(self):
        # Get the extension names under each collection
        def ext_info(x):
            x.get_extension()
            return (x.name, x.extension_signature)
        extensions = {c:[ext_info(ext[e]) for e in ext] \
                        for c, ext in self.extension_collections.items()}
        num_extensions = sum([len(v) for v in extensions.values()])
        if num_extensions == 0:
            print('No extensions are installed')
            return
        
        if num_extensions==1:
            info = "There is 1 extension installed:\n\n"
        else:
            info = "There are {} extensions installed:\n\n".format(num_extensions)

        if __default_collection__ in extensions:
            for func, sig in extensions[__default_collection__]:
                info += "  {}\n".format(sig)
            extensions.pop(__default_collection__)
        
        for collection in extensions:
            info +='\nCollection: {}\n'.format(collection)
            for func, sig in extensions[collection]:
                info += "  {}\n".format(sig)
        info += "\nFor help on individual extensions, use help(df.ext.<extension name>)"
        print(info)
        return