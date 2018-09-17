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

Jira
----

* Get issues from jql search result with all related fields:

.. code-block:: python

    jql_request = 'project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey'
    issues = jira.jql(jql_request)
    print(issues)

* Reindex Jira

.. code-block:: python

    # Reindexing Jira
    jira.reindex()

    # Reindex status
    jira.reindex_status()

    # Reindex type
    jira.reindex_with_type(indexing_type="BACKGROUND_PREFERRED")
    """
    FOREGROUND - runs a lock/full reindexing
    BACKGROUND - runs a background reindexing.
                 If JIRA fails to finish the background reindexing, respond with 409 Conflict (error message).
    BACKGROUND_PREFERRED  - If possible do a background reindexing.
                            If it's not possible (due to an inconsistent index), do a foreground reindexing.
    """

* Manage users

.. code-block:: python

    # Get user
    jira.user(username)

    # Remove user
    jira.user_remove(username)

    # Deactivate user
    jira.user_deactivate(username)

    # Get web sudo cookies using normal http request
    jira.user_get_websudo()

    # Fuzzy search using username and display name
    jira.user_find_by_user_string(username, start=0, limit=50, include_inactive_users=False)

    # Get all users from group
    jira.get_all_users_from_group(group, include_inactive_users=False, start=0, limit=50)

* Manage projects

.. code-block:: python

    # Get all projects
    jira.projects()

    # Get project
    jira.project(key)

    # Get project components using project key
    jira.get_project_components(key)

    # Get a full representation of a the specified project's versions
    jira.get_project_versions(key, expand=None)

    # Returns all versions for the specified project. Results are paginated.
    # Results can be ordered by the following fields: sequence, name, startDate, releaseDate.
    jira.get_project_versions_paginated(key, start=None, limit=None, order_by=None, expand=None)

    # Get project leaders
    jira.project_leaders()

    # Get last project issuekey
    jira.get_project_issuekey_last(project)

    # Get all project issue keys
    jira.get_project_issuekey_all(project)

    # Get project issues count
    jira.get_project_issues_count(project)

    # Get all project issues
    jira.get_all_project_issues(project, fields='*all')

    # Get all assignable users for project
    jira.get_all_assignable_users_for_project(project_key, start=0, limit=50)

* Manage issues

.. code-block:: python

    # Get issue by key
    jira.issue(key)

    # Get issue field value
    jira.issue_field_value(key, field)

    # Update issue field
    fields = {'summary': 'New summary'}
    jira.update_issue_field(key, fields)

    # Rename sprint
    jira.rename_sprint(sprint_id, name, start_date, end_date)

    # Check issue exists
    jira.issue_exists(issue_key)

    # Check issue deleted
    jira.issue_deleted(issue_key)

    # Update issue
    jira.issue_update(issue_key, fields)

    # Create issue
    jira.issue_create(fields)

    # Issue create or update
    jira.issue_create_or_update(fields)

    # Get issue transitions
    jira.get_issue_transitions(issue_key)

    # Get status ID from name
    jira.get_status_id_from_name(status_name)

    # Get transition id to status name
    jira.get_transition_id_to_status_name(issue_key, status_name)

    # Transition issue
    jira.issue_transition(issue_key, status)

    # Set issue status
    jira.set_issue_status(issue_key, status_name)

    # Get issue status
    jira.get_issue_status(issue_key)

* Manage components

.. code-block:: python

    # Get component
    jira.component(component_id)

    # Create component
    jira.create_component(component)

    # Delete component
    jira.delete_component(component_id)

* Upload Jira plugin

.. code-block:: python

    upload_plugin(plugin_path)


.. |Build Status| image:: https://travis-ci.org/AstroMatt/atlassian-python-api.svg?branch=master
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