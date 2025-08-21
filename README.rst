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

Please, note Confluence Cloud need to be used via token parameter.
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
.. |Build Status| image:: https://github.com/atlassian-api/atlassian-python-api/workflows/Test/badge.svg?branch=master
   :target: https://github.com/atlassian-api/atlassian-python-api/actions?query=workflow%3ATest+branch%3Amaster
   :alt: Build status
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
* GitHub_ for hosting our repository and continuous integration

.. _Atlassian: https://www.atlassian.com/
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _GitHub: https://github.com/
.. _Microsoft: https://github.com/Microsoft/vscode/
.. _VSCode: https://code.visualstudio.com/
