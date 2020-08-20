.. Atlassian Python API documentation master file, created by
   sphinx-quickstart on Thu Sep 13 13:43:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Atlassian Python API's documentation!
================================================
|Build Status| |PyPI version| |PyPI - Downloads| |License| |Codacy Badge| |Docs|

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
        
        
Key/Cert Based authentication
-----------------------------

Add a connection using key/cert based authentication:

.. code-block:: python

    from atlassian import Jira
    from atlassian import Confluence
    from atlassian import Bitbucket
    from atlassian import ServiceDesk

    jira = Jira(
        url='http://localhost:8080',
        key='/path/to/key',
        cert='/path/to/cert')

    confluence = Confluence(
        url='http://localhost:8090',
        key='/path/to/key',
        cert='/path/to/cert')

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        key='/path/to/key',
        cert='/path/to/cert')

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        key='/path/to/key',
        cert='/path/to/cert')

Alternatively OAuth can be used:

.. code-block:: python

    oauth_dict = {
        'access_token': 'access_token',
        'access_token_secret': 'access_token_secret',
        'consumer_key': 'consumer_key',
        'key_cert': 'key_cert'}

    jira = Jira(
        url='http://localhost:8080',
        oauth=oauth_dict)

    confluence = Confluence(
        url='http://localhost:8090',
        oauth=oauth_dict)

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        oauth=oauth_dict)

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        oauth=oauth_dict)

Or Kerberos *(installation with kerberos extra necessary)*:

.. code-block:: python

    kerberos_service = 'HTTP/jira.localhost@YOUR.DOMAIN.COM'

    jira = Jira(
        url='http://localhost:8080',
        kerberos=kerberos_service)

    confluence = Confluence(
        url='http://localhost:8090',
        kerberos=kerberos_service)

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        kerberos=kerberos_service)

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        kerberos=kerberos_service)

Or reuse cookie file:

.. code-block:: python

    from atlassian import utils
    cookie_dict = utils.parse_cookie_file("cookie.txt")

    jira = Jira(
        url='http://localhost:8080',
        cookies=cookie_dict)

    confluence = Confluence(
        url='http://localhost:8090',
        cookies=cookie_dict)

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        cookies=cookie_dict)

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        cookies=cookie_dict)

To authenticate to the Atlassian Cloud APIs:

.. code-block:: python

    # Obtain an API token from: https://id.atlassian.com/manage-profile/security/api-tokens

    jira = Jira(
        url='https://your-domain.atlassian.net',
        username=jira_username,
        password=jira_api_token,
        cloud=True)

    confluence = Confluence(
        url='https://your-domain.atlassian.net',
        username=jira_username,
        password=jira_api_token,
        cloud=True)

    bitbucket = Bitbucket(
        url='https://your-domain.atlassian.net',
        username=jira_username,
        password=jira_api_token,
        cloud=True)

    service_desk = ServiceDesk(
        url='https://your-domain.atlassian.net',
        username=jira_username,
        password=jira_api_token,
        cloud=True)



.. toctree::
   :maxdepth: 2

   jira
   confluence
   bitbucket
   bamboo
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
.. |PyPI - Downloads| image:: https://pepy.tech/badge/atlassian-python-api/month
   :alt: PyPI - Downloads
.. |Docs| image:: https://readthedocs.org/projects/atlassian-python-api/badge/?version=latest
   :target: https://atlassian-python-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
