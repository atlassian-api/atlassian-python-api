.. Atlassian Python API documentation master file, created by
   sphinx-quickstart on Thu Sep 13 13:43:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Atlassian Python API's documentation!
================================================
|Build Status| |PyPI version| |License| |Codacy Badge|

Getting started
---------------

Install package using pip:

``pip install atlassian-python-api``

Add a connection:

.. code-block:: python

    from atlassian import Jira
    from atlassian import Confluence
    from atlassian import Bitbucket
    from atlassian import ServiceDesk

    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    confluence = Confluence(
        url='http://localhost:8090',
        username='admin',
        password='admin')

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        username='admin',
        password='admin')

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        username='admin',
        password='admin')

.. toctree::
   :maxdept:2

   jira
   confluence
   bitbucket
   service_desk

.. |Build Status| image:: https://travis-ci.org/atlassian-api/atlassian-python-api.svg?branch=master
   :target: https://pypi.python.org/pypi/atlassian-python-api
   :alt: Build status
.. |PyPI version| image:: https://badge.fury.io/py/atlassian-python-api.svg
   :target: https://badge.fury.io/py/atlassian-python-api
   :alt: PyPI version
.. |License| image:: https://img.shields.io/pypi/l/atlassian-python-api.svg
   :target: https://pypi.python.org/pypi/atlassian-python-api
   :alt: License
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c822908f507544fe98ae37b25518ae3d
   :target: https://www.codacy.com/project/gonchik/atlassian-python-api/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AstroMatt/atlassian-python-api&amp;utm_campaign=Badge_Grade_Dashboard
   :alt: Codacy Badge