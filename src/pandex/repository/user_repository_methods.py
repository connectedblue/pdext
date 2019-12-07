import os

class user_repository_methods_mixin(object):
    """
    All the methods which a user can call to manipulate 
    the repositories where extensions are stored.

    Specify the directory locations on the local filesystem where installed
    extensions can be found.  

    New repository locations can be added by the user.  The information is
    stored in a yaml file inside the package.

    Extensions can then be installed into the correct location
    so they can be found by the pandas extension class.  Any 
    namespace clashes are resolved using the repository search order
    which can also be specified by the user.
    """    
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