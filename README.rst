============================
Atlassian Python API wrapper
============================

.. image:: https://img.shields.io/pypi/v/atlassian-python-api.svg
            :target: https://pypi.python.org/pypi/atlassian-python-api/
.. image:: https://travis-ci.org/AstroMatt/atlassian-python-api.svg?branch=master 
            :target: https://pypi.python.org/pypi/atlassian-python-api/
.. image:: https://img.shields.io/pypi/l/atlassian-python-api.svg
            :target: https://pypi.python.org/pypi/atlassian-python-api/


For users
=========

For everyday normal use, just install package using pip::

    pip install atlassian-python-api

Here's a short example how to create a Confluence page:

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

And here's another example how to get issues from Jira using JQL Query:

.. code-block:: python

    from atlassian import Jira

    jira = Jira(
        url='http://localhost:8080',
        username='admin',
        password='admin')

    JQL = 'project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey'
    data = jira.jql(JQL)
    print(data)

Please make sure, you've checked ``examples/`` directory on how to build scripts using the API.
If you want to see response in pretty print format json. Feel free for use construction like:

.. code-block:: python

    from pprint import pprint
    # you code here
    # and then print using pprint(result) instead of print(result)
    pprint(response)

For Contributors
================

The following command builds a package and uploads it to PIP repository::

    python setup.py sdist upload

