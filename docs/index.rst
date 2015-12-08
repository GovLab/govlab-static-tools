.. govlab-static-tools documentation master file, created by
   sphinx-quickstart on Fri Dec 04 16:30:58 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to govlab-static-tools's documentation!
===============================================

govlab-static-tools (or simply govlabstatic) is a collection of tools
that make it slightly easier to build static websites for 
GovLab_.

GovLab static sites make use of staticjinja_ and Jinja2_ for the
generation of HTML content and SASS_ for CSS.

Philosophy
----------

This package is generally intended to be used as glue that exposes
the functionality of existing third-party libraries for core
functionality when possible. It's also intended to provide
testing tools out-of-the-box.

Example
-------

See the code for the `example project`_, which contains the
following ``build.py`` file in its root directory:

.. literalinclude:: ../example/build.py

Running ``python build.py --help`` will output:

.. program-output:: python ../example/build.py --help

For a more detailed example, see the source for the `GovLab website`_.

Developer API
-------------

.. currentmodule:: govlabstatic.cli

.. autoclass:: Manager
   :members: run

   .. autoinstanceattribute:: Manager.parser
      :annotation:

   .. autoinstanceattribute:: Manager.watcher
      :annotation:

.. currentmodule:: govlabstatic.watcher

.. autoclass:: Watcher

   .. autoinstanceattribute:: Watcher.observer
      :annotation:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _example project: https://github.com/GovLab/govlab-static-tools/tree/master/example
.. _GovLab website: https://github.com/GovLab/www.thegovlab.org/
.. _GovLab: http://thegovlab.org/
.. _staticjinja: http://staticjinja.readthedocs.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _SASS: http://sass-lang.com/
