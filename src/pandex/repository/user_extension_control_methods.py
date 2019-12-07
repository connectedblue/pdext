import os

from ..symbols import __default_collection__, __pdext__, __version__, __df_ext__

class user_extension_control_methods_mixin(object):
    """
    All the methods which a user can call to manipulate 
    extensions.

    Extensions can then be installed into the correct location
    so they can be found by the pandas extension class.  Any 
    namespace clashes are resolved using the repository search order
    which can also be specified by the user.
    """    
    def show_extensions(self):
        info = '{} v{}\n'.format(__pdext__, __version__)

        # Get the extension names under each collection
        def ext_info(x):
            x.get_extension()
            if x.imported_ok:
                sig = x.extension_signature
            else:
                sig = "{}  - Currently doesn't work because {}"\
                        .format(x.extension_signature,x.pdext_fix_advice)
            return (x.ext_info.name, sig)
        extensions = {c:[ext_info(ext[e]) for e in ext] \
                        for c, ext in self.extension_collections.items()}
        num_extensions = sum([len(v) for v in extensions.values()])
        if num_extensions == 0:
            print(info+'No extensions are installed')
            return
        
        if num_extensions==1:
            info += "There is 1 extension installed:\n\n"
        else:
            info += "There are {} extensions installed:\n\n".format(num_extensions)

        if __default_collection__ in extensions:
            for _, sig in extensions[__default_collection__]:
                info += "  {}\n".format(sig)
            extensions.pop(__default_collection__)
        
        for collection in extensions:
            info +='\nCollection: {}\n'.format(collection)
            for _ , sig in extensions[collection]:
                info += "  {}\n".format(sig)
        info += "\nFor help on individual extensions, use help(df.{}.<extension name>)"\
                    .format(__df_ext__)
        print(info)
        return

    def disable_extension(self, name, *, _enabled=False):
        """
        Disable an extension
        
        *Input Parameters:*

            **name:**

                string name of extension (including collection if there is one)
        """
        # locate extension to be enabled/disabled
        collection, name=self._parse_extension_name(name)
        ext = self._get_extension_object(name, collection)
        ext.enabled = _enabled
        ext.reload()
    
    def enable_extension(self, name):
        """
        Enable an extension

        *Input Parameters:*

            **name:**
            
                string name of extension (including collection if there is one)
        """
        self.disable_extension(name, _enabled=True)

    def remove_extension(self, name):
        """
        Permanently remove an extension from the repository
        
        *Input Parameters:*

            **name:**
            
                string name of extension (including collection if there is one)
        """
        # locate extension to be removed
        collection, name=self._parse_extension_name(name)
        ext = self._get_extension_object(name, collection)
        ext.remove()
        del(self.extension_collections[collection][name])