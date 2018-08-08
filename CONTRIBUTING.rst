How to contribute
=================

You’re very welcome to make bug fixes or enhancements to this library.
This document lays out the guidelines for how to get those changes into
the main package repository.

Getting Started
---------------

1. Fork the repository on GitHub:
   https://github.com/AstroMatt/atlassian-python-api
2. Make changes
3. Send pull request

Using your changes before they’re live
--------------------------------------

You may want to use the changes you’ve made to this library before the
merging/review process has been completed. To do this you can install it
into the global python environment by running this command from the top
level directory.

::

   pip install . --upgrade

The following command builds a package and uploads it to PIP repository.

::

   python setup.py sdist upload
