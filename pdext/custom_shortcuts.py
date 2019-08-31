



## These shortcuts are temporary - there is a better way
## to store then all within the instance variables of _pdwrapper
## but that is not implemented yet

# Replace some pandas functions with custom versions
# see _pdwrapper extensions for details
import pandas as pd

pd.DataFrame.copy = pd.DataFrame._pdwrapper.copy
pd.DataFrame.merge = pd.DataFrame._pdwrapper.merge

