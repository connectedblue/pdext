# Useful extension to dataframe


from ._extension_factory import load_extensions, create_shortcuts

## Create extension namespaces based on a standard Template and extension
## logic defined in the accessor sub folders

# meta namespace
load_extensions('meta')

# pplab namespace
load_extensions('pplab')

# _pdwrapper namespace
# Note users should not manipulate this workspace - it's an internal
# workspace to intercept and wrap calls to standard panda library functions
load_extensions('_pdwrapper')

## Create shortcuts in the pd namespace to
## certain extension functions

create_shortcuts([
 
])

from .custom_shortcuts import *
