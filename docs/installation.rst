How to Install
==============

Installing the package
----------------------

The package can be installed from pyPI using pip:

.. parsed-literal::

    pip install |pandex|

The only dependency is ``pandas`` which will be installed
if not already present.

The package is used as follows:

.. parsed-literal::

    import |pandex| as pd

Once this has been imported, ``pd`` now references the
standard ``pandas`` and can be used in the normal way. The
extension functionality resides in the |``pd.ext``| namespace.

Installing Extensions
---------------------

Extensions are simply normal functions that take a ``DataFrame``
as the first parameter, along with any other arguments needed.
So, an example extension might look like::

    import numpy as np

    def my_extension(df, arg1, arg2):
        # do something to df ...
        df['col2'] = df.col1 * arg2
        df['col3'] = np.where(df.col2==arg1, 'foo', 'bar')

No special return value is needed - the dataframe will be modified
in place when the extension is executed, but of course you can return
a value if required.

They can be pre-existing, or written specially.  The function
needs to be located on the local filesystem somewhere or in
a publicly accessible GitHub repository

To install an extension located in a file in a directory ``bar``
you simply import:

.. parsed-literal::

    |pd.ext|.import_extension('path/to/bar -> my_extension')

You can also organise extensions into collection namespaces
to make them easier to manage.  This is done during import:

.. parsed-literal::

    |pd.ext|.import_extension('path/to/bar -> collection1.my_extension')

If an extension was located in a GitHub repository, then it
can be imported as follows:

.. parsed-literal::

    |pd.ext|.import_extension('github:username/repo -> my_extension')


Extensions from GitHub can also be organised into collections if
required.

Note, this could be issued from the python interpreter, or included
in a script.  If an extension is already installed, no action is
taken.

Accessing installed extensions
------------------------------

Once installed, the extension are accessed from the |``ext``| namespace
attached to the dataframe:

.. parsed-literal::

    import |pandex| as pd
    df = pd.DataFrame({'col1': [3,4,5]})

    # call the extension
    |df.ext|.my_extension(10, 2)

    # if the extension was installed in a collection ...
    |df.ext|.ext.collection1.my_extension(10, 2)

