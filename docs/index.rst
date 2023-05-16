.. Atlassian Python API documentation is linked to HEAD commit,



You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to Atlassian Python API's documentation!
================================================
|Build Status| |PyPI version| |PyPI Downloads| |License| |Codacy Badge| |Docs|

Getting started
---------------

Install package using pip:

``pip install atlassian-python-api``

Add a connection:

.. code-block:: python

    from atlassian import Jira
    from atlassian import Confluence
    from atlassian import Crowd
    from atlassian import Bitbucket
    from atlassian import ServiceDesk
    from atlassian import Xray

    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    confluence = Confluence(
        url='http://localhost:8090',
        username='admin',
        password='admin')

    crowd = Crowd(
        url='http://localhost:4990',
        username='app-name',
        password='app-password'
    )

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        username='admin',
        password='admin')

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    xray = Xray(
        url='http://localhost:8080',
        username='admin',
        password='admin')

Other authentication methods
----------------------------

Further authentication methods are available. For example OAuth can be used:

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

    xray = Xray(
        url='http://localhost:8080',
        oauth=oauth_dict)

OAuth 2.0 is also supported:

.. code-block:: python

    from atlassian.bitbucket import Cloud

    # token is a dictionary and must at least contain "access_token"
    # and "token_type".
    oauth2_dict = {
        "client_id": client_id,
        "token": token}

    bitbucket_cloud = Cloud(
        oauth2=oauth2_dict)

    # For a detailed example see bitbucket_oauth2.py in
    # examples/bitbucket


Or Kerberos *(installation with kerberos extra necessary)*:

.. code-block:: python

    jira = Jira(
        url='http://localhost:8080',
        kerberos={})

    confluence = Confluence(
        url='http://localhost:8090',
        kerberos={})

    bitbucket = Bitbucket(
        url='http://localhost:7990',
        kerberos={})

    service_desk = ServiceDesk(
        url='http://localhost:8080',
        kerberos={})

    xray = Xray(
        url='http://localhost:8080',
        kerberos={})

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

    xray = Xray(
        url='http://localhost:8080',
        cookies=cookie_dict)

Or using Personal Access Token
Note: this method is valid for Jira Data center / server editions only! For Jira cloud, see below.

First, create your access token (check https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html for details)
Then, just provide the token to the constructor:

.. code-block:: python

   jira = Jira(
       url='https://your-jira-instance.company.com',
       token=jira_access_token
   )

To authenticate to the Atlassian Cloud APIs Jira, Confluence, ServiceDesk:

.. code-block:: python

    # Obtain an API token from: https://id.atlassian.com/manage-profile/security/api-tokens
    # You cannot log-in with your regular password to these services.

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

    service_desk = ServiceDesk(
        url='https://your-domain.atlassian.net',
        username=jira_username,
        password=jira_api_token,
        cloud=True)

And to Bitbucket Cloud:

.. code-block:: python

    # Log-in with E-Mail / Username and regular password
    # or with Username and App password.
    # Get App password from https://bitbucket.org/account/settings/app-passwords/.
    # Log-in with E-Mail and App password not possible.
    # Username can be found here: https://bitbucket.org/account/settings/

    from atlassian.bitbucket import Cloud

    bitbucket = Cloud(
        username=bitbucket_email,
        password=bitbucket_password,
        cloud=True)

    bitbucket_app_pw = Cloud(
        username=bitbucket_username,
        password=bitbucket_app_password,
        cloud=True)

Getting started with Cloud Admin module
---------------------------------------

Add a connection:

.. code-block:: python

    from atlassian import CloudAdminOrgs, CloudAdminUsers

    cloud_admin_orgs = CloudAdminOrgs(
        admin-api-key=admin-api-key)

    cloud_admin_users = CloudAdminUsers(
        admin-api-key=admin-api-key)

.. toctree::
   :maxdepth: 2

   jira
   confluence
   crowd
   bitbucket
   bamboo
   service_desk
   xray
   cloud_admin

.. |Build Status| image:: https://github.com/atlassian-api/atlassian-python-api/workflows/Test/badge.svg?branch=master
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
.. |PyPI Downloads| image:: https://pepy.tech/badge/atlassian-python-api/month
   :alt: PyPI Downloads
.. |Docs| image:: https://readthedocs.org/projects/atlassian-python-api/badge/?version=latest
   :target: https://atlassian-python-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
