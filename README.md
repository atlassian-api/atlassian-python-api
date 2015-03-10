Atlassian Python API wrapper
============================


For users
---------

For everyday normal use, just simply type a

    pip install atlassian-python-api

Here's a short example how to create a Confluence page:

    from atlassian import Confluence

    confluence = Confluence(
        url="http://localhost:8090",
        username="admin",
        password="admin")

    status = confluence.create_page(
        space="DEMO",
        title="This is the title",
        body="This is the body. You can use <strong>HTML tags</strong>!")

    print(status)

And here's another example how to get issues from Jira using JQL Query:

    from atlassian import Jira

    jira = Jira(
        url="http://localhost:8080",
        username="admin",
        password="admin")

    JQL = "project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey"
    data = jira.jql(JQL)
    print(data)

Plasease make sure, you've checked `examples/` directory on how to build scripts using the API.


For Contributors
----------------

The following command builds a package and uploads it to PIP repository.

    python setup.py sdist upload

