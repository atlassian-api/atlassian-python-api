Jira module
===========

Get issues from jql search result with all related fields
---------------------------------------------------------

.. code-block:: python

    jql_request = 'project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey'
    issues = jira.jql(jql_request)
    print(issues)

Reindex Jira
------------

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

Manage users
------------

.. code-block:: python

    # Get user
    jira.user(account_id)

    # Remove user
    jira.user_remove(username)

    # Deactivate user. Works from 8.3.0 release
    jira.user_deactivate(username)

    # Get web sudo cookies using normal http request
    jira.user_get_websudo()

    # Fuzzy search using emailAddress or displayName
    jira.user_find_by_user_string(query, start=0, limit=50, include_inactive_users=False)

Manage groups
-------------

.. code-block:: python

    # Create a group
    jira.create_group(name)

    # Delete a group
    # If you delete a group and content is restricted to that group, the content will be hidden from all users
    # To prevent this, use this parameter to specify a different group to transfer the restrictions
    # (comments and worklogs only) to
    jira.remove_group(name, swap_group=None)

    # Get all users from group
    jira.get_all_users_from_group(group, include_inactive_users=False, start=0, limit=50)

    # Add given user to a group
    jira.add_user_to_group(username, group_name)

    # Remove given user from a group
    jira.remove_user_from_group(username, group_name)

Manage projects
---------------

.. code-block:: python

    # Get all projects
    # Returns all projects which are visible for the currently logged in user.
    jira.projects(included_archived=None)

    # Get all project alternative call
    # Returns all projects which are visible for the currently logged in user.
    jira.get_all_projects(included_archived=None)

    # Get project
    jira.project(key)

    # Get project components using project key
    jira.get_project_components(key)

    # Get a full representation of a the specified project's versions
    jira.get_project_versions(key, expand=None)

    # Returns all versions for the specified project. Results are paginated.
    # Results can be ordered by the following fields: sequence, name, startDate, releaseDate.
    # Results can be filtered by the following fields: query, status.
    jira.get_project_versions_paginated(key, start=None, limit=None, order_by=None, expand=None, query=None, status=None)

    # Add missing version to project
    jira.add_version(key, project_id, version, is_archived=False, is_released=False)

    # Get project leaders
    jira.project_leaders()

    # Get last project issuekey
    jira.get_project_issuekey_last(project)

    # Get all project issue keys
    jira.get_project_issuekey_all(project)

    # Get project issues count
    jira.get_project_issues_count(project)

    # Get all project issues
    jira.get_all_project_issues(project, fields='*all', start=100, limit=500)

    # Get all assignable users for project
    jira.get_all_assignable_users_for_project(project_key, start=0, limit=50)

    # Update a project
    jira.update_project(project_key, data, expand='lead,description')

    # Get project permission scheme
    # Use 'expand' to get details (default is None)
    jira.get_project_permission_scheme(project_id_or_key, expand='permissions,user,group,projectRole,field,all')

    # Get the issue security scheme for project.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    # Use only_levels=True for get the only levels entries
    jira.get_project_issue_security_scheme(project_id_or_key, only_levels=False)

    # Resource for associating notification schemes and projects.
    # Gets a notification scheme associated with the project.
    # Follow the documentation of /notificationscheme/{id} resource for all details about returned value.
    # Use 'expand' to get details (default is None)  possible values are notificationSchemeEvents,user,group,projectRole,field,all
    jira.get_priority_scheme_of_project(project_key_or_id, expand=None)

Manage issues
-------------

.. code-block:: python

    # Get issue by key
    jira.issue(key)

    # Get issue field value
    jira.issue_field_value(key, field)

    # Update issue field
    fields = {'summary': 'New summary'}
    jira.update_issue_field(key, fields)

    # Get existing custom fields or find by filter
    get_custom_fields(self, search=None, start=1, limit=50):

    # Check issue exists
    jira.issue_exists(issue_key)

    # Check issue deleted
    jira.issue_deleted(issue_key)

    # Update issue
    jira.issue_update(issue_key, fields)

    # Assign issue to user
    jira.assign_issue(issue_key, account_id)

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
    jira.set_issue_status(issue_key, status_name, fields=None)

    # Set issue status by transition_id
    jira.set_issue_status_by_transition_id(issue_key, transition_id)

    # Get issue status
    jira.get_issue_status(issue_key)

    # Get Issue Link
    jira.get_issue_link(link_id)

    # Create Issue Link
    data = {
            "type": {"name": "Duplicate" },
            "inwardIssue": { "key": "HSP-1"},
            "outwardIssue": {"key": "MKY-1"},
            "comment": { "body": "Linked related issue!",
                         "visibility": { "type": "group", "value": "jira-software-users" }
            }
    }
    jira.create_issue_link(data)

    # Remove Issue Link
    jira.remove_issue_link(link_id)

    # Create or Update Issue Remote Links
    jira.create_or_update_issue_remote_links(issue_key, link_url, title, global_id=None, relationship=None)

    # Get Issue Remote Link by link ID
    jira.get_issue_remote_link_by_id(issue_key, link_id)

    # Update Issue Remote Link by link ID
    jira.update_issue_remote_link_by_id(issue_key, link_id, url, title, global_id=None, relationship=None)

    # Delete Issue Remote Links
    jira.delete_issue_remote_link_by_id(issue_key, link_id)

    # Export Issues to csv
    jira.csv(jql, all_fields=False)


Manage Boards
-------------

.. code-block:: python

    # Create sprint
    jira.jira.create_sprint(sprint_name, origin_board_id,  start_datetime, end_datetime, goal)

    # Rename sprint
    jira.rename_sprint(sprint_id, name, start_date, end_date)

    # Add/Move Issues to sprint
    jira.add_issues_to_sprint(sprint_id, issues_list)

Attachments actions
-------------------

.. code-block:: python

    # Add attachment to issue
    jira.add_attachment(issue_key, filename)

Manage components
-----------------

.. code-block:: python

    # Get component
    jira.component(component_id)

    # Create component
    jira.create_component(component)

    # Delete component
    jira.delete_component(component_id)

Upload Jira plugin
------------------

.. code-block:: python

    upload_plugin(plugin_path)

Issue link types
----------------
.. code-block:: python

    # Get Issue link types
    jira.get_issue_link_types():

    # Create Issue link types
    jira.create_issue_link_type(data):
    """Create a new issue link type.
        :param data:
                {
                    "name": "Duplicate",
                    "inward": "Duplicated by",
                    "outward": "Duplicates"
                }
    """

    # Get issue link type by id
    jira.get_issue_link_type(issue_link_type_id):

    # Delete issue link type
    jira.delete_issue_link_type(issue_link_type_id):

    # Update issue link type
    jira.update_issue_link_type(issue_link_type_id, data):

Issue security schemes
----------------------
.. code-block:: python

    # Get all security schemes.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    jira.get_issue_security_schemes()

    # Get issue security scheme.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    # Use only_levels=True for get the only levels entries
    jira.get_issue_security_scheme(scheme_id, only_levels=False)

TEMPO
----------------------
.. code-block:: python

    # Find existing worklogs with the search parameters.
    # Look at the tempo docs for additional information:
    # https://www.tempo.io/server-api-documentation/timesheets#operation/searchWorklogs
    # NOTE: check if you are using correct types for the parameters!
    #     :param from: string From Date
    #     :param to: string To Date
    #     :param worker: Array of strings
    #     :param taskId: Array of integers
    #     :param taskKey: Array of strings
    #     :param projectId: Array of integers
    #     :param projectKey: Array of strings
    #     :param teamId: Array of integers
    #     :param roleId: Array of integers
    #     :param accountId: Array of integers
    #     :param accountKey: Array of strings
    #     :param filterId: Array of integers
    #     :param customerId: Array of integers
    #     :param categoryId: Array of integers
    #     :param categoryTypeId: Array of integers
    #     :param epicKey: Array of strings
    #     :param updatedFrom: string
    #     :param includeSubtasks: boolean
    #     :param pageNo: integer
    #     :param maxResults: integer
    #     :param offset: integer
    jira.tempo_4_timesheets_find_worklogs(**params)

    # :PRIVATE:
    # Get Tempo timesheet worklog by issue key or id.
    jira.tempo_timesheets_get_worklogs_by_issue(issue)
