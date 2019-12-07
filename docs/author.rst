Writing Extensions
==================

The |``pandex``| package allows any function which operates on a dataframe to
be installed as an extension.  Functions may be stored in individual ``.py``
files, local directories or modules or on GitHub.

The only requirement is that the function accept a pandas ``DataFrame`` as
the first argument.

Example extension
-----------------

The following function is a valid |``pandex``| extension::

    from math import pi

    def circle_calculations(df, radius='radius'):
        """
        Calculates the circumference and area of a circle
        given a column of radius and adds the result to the
        dataframe
        Input:
            df -- dataframe
            radius -- column name containing the radius values
        """
        df['circumference'] = 2 * pi * df[radius]
        df['area'] = pi * df[radius] ** 2

.. note:: The first argument to the function need not be named ``df``.

If this file is stored in a file named ``circle_calc.py``, then
the extension may be installed as follows:

.. parsed-literal::

    |pd.ext|.import_extension('/path/to/circle_calc_file -> circle_calculations')

.. note::  ``circle_calc.py`` does not have to be in
           ``/path/to/circle_calc_file`` itself - as long as it's in
           a subdirectory somewhere it will get installed.

Extensions may make use of any installed package (dependencies that are not
installed with be highlighted with a warning during import, and also in
the output of |``pd.ext``| ``.show_extensions()``).

Extension usage
---------------

If the user has created a dataframe named ``df``, then the extension can be
accessed as follows:

.. parsed-literal::

    |df.ext|.circle_calculations()


The docstring defined will be available for the dataframe ``df``:

.. parsed-literal::

    help(|df.ext|.circle_calculations)

Extension dependencies
----------------------

If an extension requires supporting functions, these can be located in the same
file.  So the example above may be rewritten to utilise an
``area()`` function::

    from math import pi

    def circle_calculations(df, radius='radius'):
        """
        Calculates the circumference and area of a circle
        given a column of radius and adds the result to the
        dataframe
        Input:
            df -- dataframe
            radius -- column name containing the radius values
        """
        df['circumference'] = 2 * pi * df[radius]
        df['area'] = area(df[radius])

    def area(radius_col):
        return pi * radius_col ** 2

The installation and usage remains as before.

Dependencies in an external file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the extension depends on functions defined in another file
these must be imported using the relative dot notation as you would
for modules.

So, if the ``area()`` function was defined in a file named
``area.py`` in the same directory as ``circle_calc.py`` then the
extension would be written as follows::

    from math import pi
    from .area import area

    def circle_calculations(df, radius='radius'):
        """
        Calculates the circumference and area of a circle
        given a column of radius and adds the result to the
        dataframe
        Input:
            df -- dataframe
            radius -- column name containing the radius values
        """
        df['circumference'] = 2 * pi * df[radius]
        df['area'] = area(df[radius])


The |``pd.ext``| ``.import_extension`` above remains the same - all the
correct files will be installed.
