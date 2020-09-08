============================
Atlassian Python API wrapper
============================
|Build Status| |PyPI version| |PyPI - Downloads| |License| |Codacy Badge| |Docs|

Documentation
-------------

`Documentation`_

.. _Documentation: https://atlassian-python-api.readthedocs.io

Install
-------
.. code-block:: console

   $ pip install atlassian-python-api

Examples
--------
**More examples in ``examples/`` directory.**

Here's a short example of how to create a Confluence page:

.. code-block:: python

    from atlassian import Confluence

    confluence = Confluence(
        url='http://localhost:8090',
        username='admin',
        password='admin')

    status = confluence.create_page(
        space='DEMO',
        title='This is the title',
        body='This is the body. You can use <strong>HTML tags</strong>!')

    print(status)

And here's another example of how to get issues from Jira using JQL Query:

.. code-block:: python

    from atlassian import Jira

    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin')
    JQL = 'project = DEMO AND status IN ("To Do", "In Progress") ORDER BY issuekey'
    data = jira.jql(JQL)
    print(data)

Also, you can use the Bitbucket module e.g. for getting project list

.. code-block:: python

    from atlassian import Bitbucket

    bitbucket = Bitbucket(
            url='http://localhost:7990',
            username='admin',
            password='admin')
    
    data = bitbucket.project_list()
    print(data)

Now you can use the Jira Service Desk module. See docs.
Example to get your requests:

.. code-block:: python

    from atlassian import ServiceDesk

    sd = ServiceDesk(
            url='http://localhost:7990',
            username='admin',
            password='admin')
    
    data = sd.get_my_customer_requests()
    print(data)

Using Xray (Test Management tool for Jira):

.. code-block:: python

    from atlassian import Xray

    xr = Xray(
           url='http://localhost:7990',
            username='admin',
            password='admin')
    
    data = xr.get_tests('TEST-001')
    print(data)

If you want to see the response in pretty print format JSON. Feel free for use construction like:

.. code-block:: python

    from pprint import pprint
    # you code here
    # and then print using pprint(result) instead of print(result)
    pprint(response)

Development and Deployment (For contributors)
---------------------------------------------
First of all, I am happy for any PR requests.
Let's fork and provide your changes :)
See the `Contribution Guidelines for this project`_ for details on how to make changes to this library.

.. _Contribution Guidelines for this project: CONTRIBUTING.rst
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
   :target: https://www.codacy.com/project/gonchik/atlassian-python-api/dashboard
   :alt: Codacy Badge
.. |PyPI - Downloads| image:: https://pepy.tech/badge/atlassian-python-api/month
   :alt: PyPI - Downloads
.. |Docs| image:: https://readthedocs.org/projects/atlassian-python-api/badge/?version=latest
   :target: https://atlassian-python-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Credits
-------
In addition to all the contributors we would like to thank these vendors:

* Atlassian_ for developing such a powerful ecosystem.
* JetBrains_ for providing us with free licenses of PyCharm_
* Travis_ for hosting our continuous integration

.. _Atlassian: https://www.atlassian.com/
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _Travis: https://travis-ci.org/
