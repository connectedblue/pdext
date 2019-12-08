# pandex - An Extension Framework for pandas

`pandex` is a framework for creating, managing and sharing extensions
for the `pandas` package.

There is a built-in extension system in `pandas` but it is not
straightforward to share these between projects, virtual environments,
other users on the same server or indeed, the wider world.

`pandex` allows extensions to be installed from local files, directories
or directly from public GitHub repositories.  Once installed, they persist 
for a user across multiple virtual environments.

Any existing script can be upgraded to support extensions with a single 
line change. Simply replace:

```
import pandas as pd
```

with:

```
   import pandex as pd
```

and all dataframes created from `pd` will be able to access installed extensions.

An demo extension which calculates the circumference and area of circles from a
column of radius values can be installed:

```
    pd.ext.import_extension('github:connectedblue/pdext_collection -> circle_calculations')
```

Whenever these calculations are required for a dataframe `df` which contains
a column `radius`, the extension can be called:

```
   df.ext.circle_calculations()
```

To see the currently installed extensions:

```
   pd.ext.show_extensions()
```

Full [documentation can be found here](https://pandex.readthedocs.io/en/stable/)
