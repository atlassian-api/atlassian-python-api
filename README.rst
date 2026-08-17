============================
Atlassian Python API wrapper
============================
|Build Status| |PyPI version| |PyPI - Downloads| |License| |Codacy Badge| |Docs| |Discord|

What is it?
___________
The **atlassian-python-api** library provides a **simple** and convenient way to interact with Atlassian products
(such as Jira Service management, Jira Software, Confluence, Bitbucket and apps Insight, X-Ray) using Python.
It is based on the official REST APIs of these products, as well as additional private methods and protocols
(such as xml+rpc and raw HTTP requests).
This library can be used to automate tasks, integrate with other tools and systems,
and build custom applications that interact with Atlassian products.
It supports a wide range of Atlassian products, including Jira, Confluence, Bitbucket, StatusPage and others,
and is compatible with both Atlassian Server and Cloud instances.

Overall, the **atlassian-python-api** is a useful tool for Python developers who want to work with Atlassian products.
It is well-documented and actively maintained, and provides a convenient way to access the full range of
functionality offered by the Atlassian REST APIs and made with love for Atlassian.


Documentation
_____________

`Documentation`_

.. _Documentation: https://atlassian-python-api.readthedocs.io

How to Install?
_______________

From PyPI

.. code-block:: console

   $ pip install atlassian-python-api

From Source

- Git clone repository
- Use :code:`pip install -r requirements.txt` to install the required packages
- or :code:`pipenv install && pipenv install --dev`

Examples
________
More **examples** in :code:`examples/` directory.

Here's a short example of how to create a Confluence page:

.. code-block:: python

    from atlassian import Confluence
    import requests
    # If you want to use a session, you can create it like this:
    session =  requests.Session()
    # and pass it to the Confluence constructor
    confluence = Confluence(
        url='http://localhost:8090',
        username='admin',
        password='admin',
        session=session,)

    status = confluence.create_page(
        space='DEMO',
        title='This is the title',
        body='This is the body. You can use <strong>HTML tags</strong>!')

    print(status)

Authentication: Server/Data Center PAT vs Cloud API token
_________________________________________________________

Use ``token=`` for a Jira or Confluence **Server/Data Center personal access
token**. It is sent as a Bearer token:

.. code-block:: python

    from atlassian import Confluence, Jira

    confluence = Confluence("https://confluence.company.example", token="server-or-dc-pat")
    jira = Jira("https://jira.company.example", token="server-or-dc-pat")

Atlassian **Cloud API tokens** use HTTP Basic authentication: pass the account
email as ``username`` and the API token as ``password``. Do not pass a Cloud
API token to ``token=``. The latter creates a Bearer header and Cloud commonly
responds with ``403 Failed to parse Connect Session Auth Token``. ``requests``
encodes the required ``email:api_token`` Basic credentials automatically; do
not base64-encode them yourself.

.. code-block:: python

    from atlassian import Confluence, Jira

    confluence = Confluence(
        "https://your-domain.atlassian.net",
        username="you@example.com",
        password="cloud-api-token",
        cloud=True,
        timeout=120,  # Optional; useful on slow/VPN connections.
    )
    spaces = confluence.get_all_spaces()

    jira = Jira(
        "https://your-domain.atlassian.net",
        username="you@example.com",
        password="cloud-api-token",
        cloud=True,
        timeout=120,
    )
    epic = jira.enhanced_jql('project = DEMO AND issuetype = Epic', limit=50)

    # Confluence Cloud V2 page read. Use the site URL without a trailing /wiki;
    # the client adds the required API context.
    from atlassian import ConfluenceV2

    confluence_v2 = ConfluenceV2(
        "https://your-domain.atlassian.net",
        username="you@example.com",
        password="cloud-api-token",
    )
    page = confluence_v2.get_page_by_id("123456789", body_format="storage")
    storage_xhtml = page["body"]["storage"]["value"]

    # Alternative Confluence Cloud V2 page read. Use the site URL without a trailing /wiki;
    # the client adds the required API context.
    from atlassian import Confluence

    confluence_v2 = Confluence(
        "https://your-domain.atlassian.net",
        username="you@example.com",
        password="cloud-api-token",
        api_version=2,  # Specify API version 2
        cloud=True
    )
    page = confluence_v2.get_page_by_id("123456789", body_format="storage")
    storage_xhtml = page["body"]["storage"]["value"]

See the detailed `authentication documentation`_ for Cloud gateway/scoped-token
notes and other authentication methods.

.. _authentication documentation: https://atlassian-python-api.readthedocs.io/en/latest/index.html#other-authentication-methods

And here's another example of how to get issues from Jira using JQL Query:

.. code-block:: python

    from atlassian import Jira
    import requests

    session = requests.Session()
    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin',
        session=session)  # Optional: use a session for persistent connections
    JQL = 'project = DEMO AND status IN ("To Do", "In Progress") ORDER BY issuekey'
    data = jira.jql(JQL)
    print(data)

The traditional jql method is deprecated for Jira Cloud users, as Atlassian has transitioned to a nextPageToken-based pagination approach instead of startAt. Use enhanced_jql for improved performance and future compatibility.

.. code-block:: python

    from atlassian import Jira
    import requests
    session = requests.Session()
    jira = Jira(
        url='https://your-jira-instance.atlassian.net',
        username='your-email@example.com',
        password='your-api-token',
        cloud=True,  # Ensure this is set to True for Jira Cloud
        session=session  # Optional: use a session for persistent connections
    )
    JQL = 'project = DEMO AND status IN ("To Do", "In Progress") ORDER BY issuekey'
    # Fetch issues using the new enhanced_jql method
    data = jira.enhanced_jql(JQL)
    print(data)

Using Confluence v2 API
_______________________

The library now supports Confluence's v2 API for Cloud instances. The v2 API provides improved performance, new content types, and more consistent endpoint patterns.

.. code-block:: python

    from atlassian import ConfluenceV2

    # ConfluenceV2 is an explicit Cloud V2 client; no cloud=True flag is needed.
    confluence = ConfluenceV2(
        url='https://your-instance.atlassian.net',
        username='your-email@example.com',
        password='your-api-token',
    )

    # Get pages from a space
    pages = confluence.get_pages(space_key='DEMO', limit=10)

    # Create a new page
    new_page = confluence.create_page(
        space_id='DEMO',
        title='New Page with v2 API',
        body='<p>This page was created using the v2 API</p>'
    )

    # Use v2-only features like whiteboards
    whiteboard = confluence.create_whiteboard(
        space_id='DEMO',
        title='My Whiteboard',
        content='{"version":1,"type":"doc","content":[]}'
    )

The library includes a compatibility layer to ease migration from v1 to v2 API. See the migration guide in the documentation for details.

Also, you can use the Bitbucket module e.g. for getting project list

.. code-block:: python

    from atlassian import Bitbucket
    import requests

    session= requests.Session()
    bitbucket = Bitbucket(
            url='http://localhost:7990',
            username='admin',
            password='admin',
            session=session)

    data = bitbucket.project_list()
    print(data)

Now you can use the Jira Service Desk module. See docs.
Example to get your requests:

.. code-block:: python

    from atlassian import ServiceDesk
    import requests
    sd = ServiceDesk(
            url='http://localhost:7990',
            username='admin',
            password='admin',
            session=requests.Session())

    data = sd.get_my_customer_requests()
    print(data)

Using Insight (CMDB Tool for Jira):

.. code-block:: python

    from atlassian import Insight
    import requests

    session = requests.Session()
    insight = Insight(
            url='http://localhost:7990',
            username='admin',
            password='admin',
            session=session)

    data = insight.get_object(88)
    print(data)


Using Xray (Test Management tool for Jira):

.. code-block:: python

    from atlassian import Xray
    import requests

    session = requests.Session()
    xr = Xray(
           url='http://localhost:7990',
            username='admin',
            password='admin',
            session=session)

    data = xr.get_tests('TEST-001')
    print(data)

Using Bamboo:

.. code-block:: python

    from atlassian import Bamboo
    import requests

    session = requests.Session()
    bamboo = Bamboo(
            url='http://localhost:6990/bamboo/',
            token="<TOKEN>",
            session=session)

    data = bamboo.get_elastic_configurations()
    print(data)

If you want to see the response in pretty print format JSON. Feel free for use construction like:

.. code-block:: python

    from pprint import pprint
    # you code here
    # and then print using pprint(result) instead of print(result)
    pprint(response)

How to contribute?
__________________
First of all, I am happy for any PR requests.
Let's fork and provide your changes :)
See the `Contribution Guidelines for this project`_ for details on how to make changes to this library.

.. _Contribution Guidelines for this project: CONTRIBUTING.rst
.. |PyPI version| image:: https://badge.fury.io/py/atlassian-python-api.svg
   :target: https://badge.fury.io/py/atlassian-python-api
   :alt: PyPI version
.. |License| image:: https://img.shields.io/pypi/l/atlassian-python-api.svg
   :target: https://pypi.python.org/pypi/atlassian-python-api
   :alt: License
.. |Codacy Badge| image:: https://app.codacy.com/project/badge/Grade/2cca43995cf041b8b181e2b2ff04cee6
   :target: https://app.codacy.com/gh/atlassian-api/atlassian-python-api/dashboard
   :alt: Codacy Badge
.. |PyPI - Downloads| image:: https://static.pepy.tech/badge/atlassian-python-api/month
   :alt: PyPI - Downloads
.. |Docs| image:: https://readthedocs.org/projects/atlassian-python-api/badge/?version=latest
   :target: https://atlassian-python-api.readthedocs.io/?badge=latest
   :alt: Documentation Status
.. |Discord| image:: https://img.shields.io/discord/756142204761669743.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
   :alt: Discord Chat
   :target: https://discord.gg/FCJsvqh


Credits
_______
In addition to all the contributors we would like to thank these vendors:

* Atlassian_ for developing such a powerful ecosystem.
* JetBrains_ for providing us with free licenses of PyCharm_
* Microsoft_ for providing us with free licenses of VSCode_
* Cursor.com_ for AI assistance in development
* John B Batzel (batzel@upenn.edu) for implementing the Confluence Cloud v2 API support

.. _Atlassian: https://www.atlassian.com/
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _Microsoft: https://www.microsoft.com
.. _VSCode: https://code.visualstudio.com
.. _Cursor.com: https://cursor.com
